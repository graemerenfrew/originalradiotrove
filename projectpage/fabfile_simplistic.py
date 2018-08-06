from __future__ import with_statement
import posixpath

from fabric.api import run, local, abort, env, put, task, settings
from fabric.contrib.files import exists
from fabric.context_managers import cd, lcd, settings, hide
import psutil

from fabric.contrib.console import confirm

# CHANGEME:
prod_server = 'grenfrew@web381.webfactional.com'
USER = 'grenfrew'
HOST = 'web381.webfaction.com'
APP_NAME = 'projectpage'
APP_PORT = 30123
#GUNICORN_WORKERS = 1

# Host and login username:
env.hosts = ['%s@%s' % (USER, HOST)]

# Directory where everything to do with this app will be stored on the server.
DJANGO_APP_ROOT = '/home/%s/webapps/radiostream/projectpage/%s' % (USER, APP_NAME)

# Directory where static sources should be collected.  This must equal the value
# of STATIC_ROOT in the settings.py that is used on the server.
STATIC_ROOT = '/home/%s/webapps/radiostream/projectpage/%s/static/' % (USER, APP_NAME)

def prepare_deploy():
#    local("python2.7 manage.py test creativework")
#    local("hg add -p && hg commit")
#    local("hg push")

    with settings(warn_only=True):
        result = local("python2.7 manage.py test creativework", capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
    message = raw_input("Enter a git commit message:  ")
    local("hg commit -m \"%s\"" % message)
    local("hg push")
    local("hg sum")

def prod():
    env.hosts = [prod_server]
    env.remote_app_dir = DJANGO_APP_ROOT
    env.remote_apache_dir = '/home/grenfrew/webapps/radiostream/apache2'


def commit():
    message = raw_input("Enter a git commit message:  ")
#    local("hg add -A && hg commit -m \"%s\"" % message)
#    local("hg push origin master")
    print "Changes have been pushed to remote repository..."


def collectstatic():
    require('hosts', provided_by=[prod])
    run("cd %s; python2.7 manage.py collectstatic --noinput" % env.remote_app_dir)


def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    require('remote_apache_dir', provided_by=[prod])

    run("%s/bin/restart;" % (env.remote_apache_dir))


def deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])

    # First lets commit changes to bitbucket
    commit()
    # Now lets pull the changes to the server
    run("cd %s; git pull" % env.remote_app_dir)
    # And lastly update static media files
    collectstatic()
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import auth
from django.core.context_processors import csrf


from forms import MyRegistrationForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
 
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

import logging

logr = logging.getLogger(__name__)



def login(request):
    c = {}
    import pdb; pdb.set_trace()
    c.update(csrf(request))
    if request.user.is_authenticated():
        return HttpResponseRedirect('/creativework/') 
    else:    
        return render_to_response('allauth/templates/account/login.html', c)
#===============================================================================
#    
#def auth_view(request):
#    username = request.POST.get('username', '')
#    password = request.POST.get('password', '')
#    user = auth.authenticate(username=username, password=password)
#    
#    if user is not None:
#        auth.login(request, user)
#        return HttpResponseRedirect('/accounts/loggedin')
#    else:
#        return HttpResponseRedirect('/accounts/invalid')
#    
# def loggedin(request):
#    return render_to_response('loggedin.html', 
#                              {'full_name': request.user.username}, context_instance=RequestContext(request))
# 
# def invalid_login(request):
#    return render_to_response('invalid_login.html')
# 
# def logout(request):
#    auth.logout(request)
#    c = {}
#    c.update(csrf(request))    
#    return render_to_response('logout.html', c)
# 
# def register_user(request):
#    if request.method == 'POST':
#        form = MyRegistrationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/accounts/register_success')
#        
#    else:
#        form = MyRegistrationForm()
#    args = {}
#    args.update(csrf(request))
#    #import pdb; pdb.set_trace()
#    args['form'] = form
#    return render_to_response('register.html', args)
# 
# def register_success(request):
#    return render_to_response('register_success.html')
#===============================================================================
 

 

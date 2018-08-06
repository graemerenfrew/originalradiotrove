from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test
from django.conf.urls.static import static
from filebrowser.sites import site
from django.contrib.sitemaps.views import sitemap
from creativework.sitemaps import EpisodeBaseSitemap, SeriesSitemap
from django.http import HttpResponse

sitemaps = {
    'episode':EpisodeBaseSitemap,
    'series':SeriesSitemap
}


login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
 
urlpatterns = patterns('',
#    url(r'^$', TemplateView.as_view(template_name='creativeworkindex.html')),

    url(r'^$',                              'creativework.views.index'),
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
    url(r'^admin/filebrowser/',             include(site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^accounts/',                      include('allauth.urls')),   
    url(r'^review/',                        include('review.urls')),
    url(r'^grappelli/',                     include('grappelli.urls')), # grappelli URLS
    url(r'^admin/',                         include(admin.site.urls)),
    url(r'^pages/',                         include('django.contrib.flatpages.urls')),
    url(r'^creativework/$',                 'creativework.views.index'),   
    url(r'^creativework/',                  include('creativework.urls')),
    url(r'^search/',                        include('haystack.urls')),
    url(r'^accounts/profile/',              'userprofile.views.user_profile'),
    url("^audio",                           include("audiotracks.urls")),
    # Some URLs require a Django username
    url("^(?P<username>[\w\._-]+)/audio",   include("audiotracks.urls")),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^googled9a0fc80c6c78918\.html$', lambda r: HttpResponse("google-site-verification: googled9a0fc80c6c78918.html", mimetype="text/plain")),
     
)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS,
        }),
   )
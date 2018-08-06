from django.conf.urls import patterns, url, include
from django.contrib import admin
from views import ShowListView, GatherAudioWizardView, SeriesCreateView, AddSeasonView, start, import_uploader
from forms import SeasonGatherAudioForm1, SeasonGatherAudioForm2, SeasonGatherAudioForm3

admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^$', 'creativework.views.index', { 'template_name':'index.html'}, name='creativework_home'),
                       url(r'start$',       start, name="start"),
                       url(r'ajax-upload$', import_uploader, name="my_ajax_upload"),
                       
                       
                       url(r'^$', ShowListView.as_view() ),
                       url(r'^showlist/(\w+)/$', ShowListView.as_view() ),  #TODO This can be used to pass in sorting variables
                       #https://docs.djangoproject.com/en/1.4/topics/class-based-views/#performing-extra-work
                       
                       url(r'^search/$', 'creativework.views.search_series'),
                       url(r'^import/$', SeriesCreateView.as_view()),
                       
                       url(r'^addseason/$', AddSeasonView.as_view(), {'template_name':'create_season.html'}),
                       #url(r'^import/$', GatherAudioWizardView.as_view([SeasonGatherAudioForm1,SeasonGatherAudioForm2,SeasonGatherAudioForm3])),
                       #ParentGenre level URLs
                       url(r'^parentgenre/$', 'creativework.views.parentgenres',                                                                        name='show_all_parentgenre_default'),
                       url(r'^parentgenre/all/$', 'creativework.views.parentgenres',                                                                    name='show_all_parentgenre'),
                       url(r'^parentgenre/(?P<parentgenre_slug>[-\w]+)/$','creativework.views.show_parentgenre', {'template_name':'parentgenre.html'},  name='show_parentgenre_byslug') ,
                   

                       #Genre level URLs
                       url(r'^genre/$',                         'creativework.views.genres',                                      name='show_all_genre_default'),
                       url(r'^genre/all/$',                     'creativework.views.genres',                                      name='show_all_genre'),
                       url(r'^genre/get/(?P<genre_id>\d+)/$',   'creativework.views.genre',                                       name='show_genre_byid'),
                       url(r'^genre/(?P<genre_slug>[-\w]+)/$',  'creativework.views.show_genre', {'template_name':'genre.html'},  name='show_genre_byslug') ,
                    
                       #Series level URLs
                       url(r'^series/like/(?P<series_id>\d+)/$','creativework.views.like_series',                                  name='like_series_byid'),
                       url(r'^series/all/$',                    'creativework.views.genres',                                       name='show_all_series_bygenre'),
                       url(r'^series/get/(?P<series_id>\d+)/$', 'creativework.views.series',                                       name='show_series_byid'),
                       url(r'^series/(?P<series_slug>[-\w]+)/$','creativework.views.show_series', {'template_name':'series.html'}, name='show_series_byslug') ,
                        
                       #Season level URLs
                       #Working
#                       url(r'^season/(?P<season_slug>[-\w]+)/$','creativework.views.show_season', {'template_name':'season.html'},  name='show_season_byslug') ,                      
                       url(r'^series/(?P<season_partOfSeries_slug>[-\w]+)/season/(?P<season_slug>[-\w]+)/$','creativework.views.show_season', {'template_name':'season.html' },  name='show_season_byslug') ,

                       #Episode level urls
                       url(r'^getbyid/(?P<episode_id>\d+)/$',        'creativework.views.episode',                                          name='show_episode_byid'),
                       url(r'^getbyslug/(?P<episode_slug>[-\w]+)/$', 'creativework.views.show_episode', {'template_name':'episode.html'},   name='show_episode_byslug'),
                       url(r'^all/$', 'creativework.views.episodes',                                                                        name='show_all_episodes'),
                            
                       url(r'^createreview/(?P<series_id>\d+)/$',   'creativework.views.create_review', {'series_id':'2'}, name='create_review_byseriesid'),
                       #show_review_byslug  not yet implemented TODO
                       
                       )
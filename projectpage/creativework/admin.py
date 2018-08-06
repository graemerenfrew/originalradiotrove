from django.contrib import admin
from models import Genre, Season, Series, EpisodeBase, ParentGenre, ContentSource
from django import forms
from forms import EpisodeAdminForm
from django.conf import settings
from django.template.defaultfilters import slugify
import pdb
import sys, traceback
from audiotracks.models import AbstractTrack, slugify_uniquely
from django.core.files.uploadhandler import TemporaryFileUploadHandler

try:
    import mutagen
except ImportError:
    import mutagenx as mutagen  # Py3

import logging
logger = logging.getLogger(__name__)

class ContentSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified', )
    list_display_links = ('name',)
    ordering = ['name']

class GenreAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created', 'modified',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description'] 
    prepopulated_fields = {'slug' : ('name',)}
    
class ParentGenreAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists parent genres
    list_display = ('name', 'created', 'modified',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description'] 
    prepopulated_fields = {'slug' : ('name',)}


def slugify_uniquely(value, obj, slugfield="slug"):
    suffix = 1
    potential = base = slugify(value)
    filter_params = {}
    filter_params['user'] = obj.user
    while True:
        if suffix > 1:
            potential = "-".join([base, str(suffix)])
        filter_params[slugfield] = potential
        obj_count = obj.__class__.objects.filter(**filter_params).count()
        if not obj_count:
            return potential[:50]
        # we hit a conflicting slug, so bump the suffix & try again
        suffix += 1 

def gather_audio_get_tag_info( audiofile ):
    ''' function to intially extract info from the tags '''
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    
    import unicodedata

    title           = ''
    broadcastDate   = ''
    episodeNumber   = 0
    length          = 60
    
    try:
        id3 = EasyID3(audiofile)
        mp3 = MP3(audiofile)
    
        print 'This is id3: %s ' % id3
        logger.info('ID3: %s' % id3)
        length        = mp3.info.length
        broadcastDate = unicodedata.normalize('NFKD', id3['comment'][0] ).encode('ascii','ignore')
        title         = unicodedata.normalize('NFKD', id3['title'][0] ).encode('ascii','ignore')
        episodeNumber = unicodedata.normalize('NFKD', id3['tracknumber'][0] ).encode('ascii','ignore')
        logger.info('title: %s date: %s track: %s lenght: %s' % ( title, broadcastDate, episodeNumber, length))
        
    except:
        print 'died'
    
    return title, broadcastDate, episodeNumber, length
    
def set_temporary_file_upload_handler(request):
    # Disable in memory upload before accessing POST
    # because we need a file from which to read metadata
    request.upload_handlers = [TemporaryFileUploadHandler()]


METADATA_FIELDS = ('title', 'artist', 'genre', 'description', 'date')

def gather_audio2(modeladmin, request, queryset):
    ''' another attempt '''
    import os
    import traceback
    
    try:
        for s in queryset:
            print 'The season is : %s\n ' % s
            print 'The folder is %s\n ' % (settings.MEDIA_URL + s.audioFolder ) 
            myfiles = settings.MEDIA_URL + s.audioFolder 
            os.chdir(myfiles)  
             
            for audiofile in os.listdir("."):  
                if audiofile != '.DS_Store': #Ignore this file if it's in the directory 
                    print  'Audiofile just read: = %s\n' % audiofile
                    #If audiofile is mp3 try and upload it, then if successful, create episode
                    #set_temporary_file_upload_handler(request)
                    if request.method == "POST":
                        audio_file = audiofile
                        audio_file_path = str(myfiles) + str(audiofile)
                        metadata = mutagen.File(audio_file, easy=True)
                        track = AbstractTrack()
                        print 'here'
                        print type(track)
                        track = track.save(commit=False)
                        print 'here2'
                        track.user = request.user
                        for field in METADATA_FIELDS:
                            if metadata and metadata.get(field):
                                setattr(track, field, metadata.get(field)[0])
                        track.save()
                
                        #return HttpResponseRedirect(urlresolvers.reverse('edit_track', args=[track.id]))
                    
                    else:
                        print 'oh dear'
                    
                    
    except Exception:
        print 'exception %s' % traceback.format_exc()                
                
                
                  
    
def gather_audio(modeladmin, request, queryset):
    import os
    newEpisode = None
    
    newEpisodes = []
    import pdb; 

    for s in queryset:
        print "Audio Folder = %s " % (settings.MEDIA_URL + s.audioFolder ) 
        myfileslocation = settings.MEDIA_URL + s.audioFolder     
        myfiles = myfileslocation
        os.chdir(myfiles)  
        for audiofile in os.listdir("."):  
            if audiofile != '.DS_Store': #Ignore this file if it's in the directory        
                logger.info( 'Audiofile just read: = %s' % audiofile )
         
                #A preprocess, which takes the file and
                #extracts the tags from it
                title, broadcastDate, episodeNumber, length = gather_audio_get_tag_info(audiofile)
                
                #A check on the tags
                
                #A check on the slug  
                slug = slugify(audiofile)   
                
                #Populate some holding fields
                description      = 'this is desc'
                hackUrl          = 'http://www.google.com'
                image            = 'NA'  
                is_active        = True
                meta_keywords    = meta_description = 'meta stuff'
                season           = s
                likes            = 0   
                
                name = audiofile
                audioFileLocation = str(myfiles) + str(audiofile)

                file          = ''
                logger.info(slug)
                pdb.set_trace()   
                  
                newEpisode = EpisodeBase.create(  name, 
                                                  description, 
                                                  hackUrl, 
                                                  slug, 
                                                  image, 
                                                  is_active, 
                                                  meta_keywords, 
                                                  meta_description, 
                                                  season, 
                                                  audioFileLocation, 
                                                  length,
                                                  broadcastDate, 
                                                  title,
                                                  episodeNumber,
                                                  likes)

                newEpisode.save()
    
      
gather_audio.short_description = "Gather the audio for this season and create episodes"

gather_audio2.short_description = "try and upload too"
    
class SeasonAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created', 'modified','audioFolder')
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description'] 
    prepopulated_fields = {'slug' : ('name',)}
    actions = [gather_audio, gather_audio2]
    

  
#trying to get admin to allow related creation
from django.contrib import admin   
class SeasonInline(admin.TabularInline):
    model = Season
    fk_name = 'partOfSeries'
      
class SeriesAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created', 'modified',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description'] 
    prepopulated_fields = {'slug' : ('name',)}
#    inlines = [
#        SeasonInline,
#    ]
    
    # sets up slug to be generated from category name prepopulated_fields = {'slug' : ('name',)}
class EpisodeAdmin(admin.ModelAdmin): 
    form = EpisodeAdminForm
    # sets values for how the admin site lists your products
    list_display = ('name', 'episode_series','get_episode_season', 'created', 'modified') 
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created']

    search_fields = ['name', 'description', 'meta_keywords', 'meta_description'] 
    #    exclude = ('created', 'modified',)
    # sets up slug to be generated from product name 
    prepopulated_fields = {'slug' : ('name',)}
    

    # registers your product model with the admin site admin.site.register(Product, ProductAdmin)
admin.site.register(EpisodeBase,    EpisodeAdmin)
admin.site.register(Series,         SeriesAdmin)
admin.site.register(Season,         SeasonAdmin)
admin.site.register(Genre,          GenreAdmin)
admin.site.register(ParentGenre,    ParentGenreAdmin)
admin.site.register(ContentSource,  ContentSourceAdmin)



 
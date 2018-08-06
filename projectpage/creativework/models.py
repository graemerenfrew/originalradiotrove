from django.db import models
from django.core.urlresolvers import reverse 
from django.utils.translation import ugettext as _
from django.db.models import permalink
from django.conf import settings 

from django.template.defaultfilters import slugify
from mutagen.easyid3 import EasyID3
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.dispatch import receiver

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.signals import file_uploaded

import logging
logger = logging.getLogger(__name__)
 
def gather_audio_get_tag_info( audiofile ):
    ''' function to intially extract info from the tags '''
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    import time
    import datetime
    from datetime import datetime

    
    import unicodedata
    import sys, traceback
    
    title           = ''
    broadcastDate   = ''
    episodeNumber   = 0
    length          = 60
     
    try:
        id3 = EasyID3(audiofile)
        mp3 = MP3(audiofile)
 
        length        = mp3.info.length
        broadcastDate = unicodedata.normalize('NFKD', mp3["COMM::'XXX'"].text[0]  ).encode('ascii','ignore') 
        
        if broadcastDate[2] == '-':
            broadcastDate = '19' + broadcastDate

        title         = unicodedata.normalize('NFKD', id3['title'][0] ).encode('ascii','ignore')
        episodeNumber = unicodedata.normalize('NFKD', id3['tracknumber'][0] ).encode('ascii','ignore')
        logger.info('title: %s date: %s track: %s lenght: %s' % ( title, broadcastDate, episodeNumber, length))

    except:
        traceback.print_exc(file=sys.stdout)
        print 'died in gather_audio_get_tag_info'
    
    return title, broadcastDate, episodeNumber, length

@receiver(file_uploaded, sender=AjaxFileUploader)
def create_on_upload(sender, backend, request, **kwargs):
    #MyModel.objects.create(user=request.user, document=backend.path)
    import pdb;  
    logger.debug('in create_on_upload')
    logger.info('info create_on_upload')
    try:
        import mutagen
    except ImportError:
        import mutagenx as mutagen  # Py3
    #So I can get the upload here, but do I actually have the file, so I can get the tags out it?
    #'QUERY_STRING': 'season_id=28&subdir=shows&qqfile=Nightwatch+54-06-25+(10)+Big+Search.mp3',
    #season_subdir
    metadata = mutagen.File(backend.path, easy=True)            
    import pdb;   
    fullpath      = backend.path
    uploaddir     = getattr(settings, "UPLOAD_DIR", "uploads")
    season_subdir = request.GET.get('season_subdir')
    filename      = request.GET.get('qqfile')
    #Replace any spaces in the filename with -
    filename = filename.replace (" ", "-")
    
    pathToFile = str(uploaddir) + str('/') + str(season_subdir) + str(filename)
    logger.info( 'Audiofile just read: = %s' % filename )
    
    #A preprocess, which takes the file and
    #extracts the tags from it
    title, broadcastDate, episodeNumber, length = gather_audio_get_tag_info(fullpath)
     
    #Populate some holding fields
    description      = 'this is desc'
    hackUrl          = 'http://www.google.com'
    image            = 'NA'  
    is_active        = True
    meta_keywords    = meta_description = 'meta stuff'
    seasonID         = request.GET.get('season_id')
    season           = Season.objects.get(id=seasonID)
    likes            = 0   
    
    name = title
 
    #A check on the slug  
    slug = slugify(str(season_subdir) + str('-') + str(filename))  
    if slug.endswith('mp3'):
        slug = slug[:-3]  #take the trailing mp3 off the slug
        
    logger.debug('slug!!')
    
    logger.debug('Name = %s' % name)
    logger.debug('description = %s' % description)
    logger.debug('hackUrl = %s' % hackUrl)
    logger.debug('slug = %s' % slug)
    logger.debug('image = %s' % image)
    logger.debug('is_active = %s' % is_active)
    logger.debug('meta_keywords = %s' % meta_keywords)
    logger.debug('meta_description = %s' % meta_description)
    logger.debug('season = %s' % season)
    logger.debug('pathToFile = %s' % pathToFile)
    logger.debug('length = %s' % length)
    logger.debug('broadcastDate = %s' % broadcastDate)
    logger.debug('title = %s' % title)
    logger.debug('episodeNumber = %s' % episodeNumber)
    logger.debug('likes = %s' % likes)
 
    newEpisode = EpisodeBase.create(  name, 
                                      description, 
                                      # hackUrl, 
                                      slug, 
                                      #image, 
                                      is_active, 
                                      meta_keywords, 
                                      meta_description, 
                                      season, 
                                      pathToFile, 
                                      length,
                                      broadcastDate, 
                                      title,
                                      episodeNumber,
                                      likes)
    
    newEpisode.save()


# Create your models here.
class TimeStampedModel( models.Model ):
    """
    An abstract base class model that provides self-updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        
class ResourceURL( TimeStampedModel):
    ''' seperate class for storing URLs '''
    url = models.CharField(max_length=200)
    
class Thing( TimeStampedModel):
    ''' Superclass '''    
    additionalType  = ResourceURL()
    description     = models.CharField(max_length=500, unique=False) 
    image           = ResourceURL()
    name            = models.CharField(max_length=200, unique=False)
    url             = ResourceURL()
    #hackUrl         = models.CharField(max_length=200, unique=False)
    
class ContentSource( Thing ):
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords for Genre')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta for Genre')    
    
    def __unicode__(self):
        return self.name
    
class ParentGenre( Thing ):
    slug                = models.SlugField(max_length=255, unique=True, help_text='Unique value for this parent genre')
    is_active           = models.BooleanField(default = False)
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords for Genre')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta for Genre')
    
    class Meta:
        db_table = 'parentgenre'
        ordering = ['-created']
        verbose_name_plural = 'ParentGenre'
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse( "show_parentgenre_byslug", kwargs={'parentgenre_slug':self.slug})

class Genre( Thing ):
    slug                = models.SlugField(max_length=255, unique=True, help_text='Unique value for this genre')
    is_active           = models.BooleanField(default = False)
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords for Genre')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta for Genre')
    partOfParentGenres  = models.ManyToManyField(ParentGenre)
    
    class Meta:
        db_table = 'genre'
        ordering = ['-created']
        verbose_name_plural = 'Genre'
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse( "show_genre_byslug", kwargs={'genre_slug':self.slug})
    
class Series( Thing ):
    is_active           = models.BooleanField(default = False)
    slug                = models.SlugField(max_length=255, unique=True, help_text='Unique value for Series, create from Series name')
    partOfGenres        = models.ManyToManyField(Genre)
    partOfParentGenres  = models.ManyToManyField(ParentGenre)
    numberOfSeasons     = models.IntegerField(default = 1)
    #startDate           = models.DateField()
    #endDate             = models.DateField()
    '''  simple counter of likes '''
    likes               = models.IntegerField(default = 0)
    viewcount           = models.IntegerField(default = 0)
    
    narrative           = models.TextField(max_length=2000, default='')
   
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta')
    
    thumbnail           = models.ImageField(upload_to=getattr(settings, "MEDIA_URL", None), blank=True, null=True)
    #mainimg             = models.ImageField(upload_to=getattr(settings, "MEDIA_URL", None), blank=True, null=True)
  
  
    class Meta:
        db_table = 'series'
        ordering = ['-created']
        verbose_name_plural = 'Series'
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse( "creativework.views.show_series", kwargs={'series_slug':self.slug})

class Season( Thing):
    is_active           = models.BooleanField(default = False)
    slug                = models.SlugField(max_length=255, unique=True, help_text='Unique value for season, created from Series and seasonNumber')
    numberOfEpisodes    = models.IntegerField(default=1)
    #startDate           = models.DateField()
    #endDate             = models.DateField()
    seasonNumber        = models.IntegerField(default=1)
    partOfSeries        = models.ForeignKey(Series)  
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta')
    audioFolder         = models.CharField(max_length=1000, default = '/Not Required')
    #fileLocation        = models.FilePathField()
    
    class Meta:
        db_table = 'seasons'
        ordering = ['-created']
        verbose_name_plural = 'Seasons'
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse( "show_season_byslug", kwargs={'season_slug':self.slug, 'season_partOfSeries_slug': self.partOfSeries.slug })


class EpisodeBase( Thing ):
    ''' base episode class '''
    slug                = models.SlugField(max_length=255, unique=True, help_text='Unique value for episode, created from Series and Season')
    ##image               = models.CharField(max_length=50, default='')  # TODO make the images a collection
    is_active           = models.BooleanField(default = False)
    meta_keywords       = models.CharField(max_length=255, help_text='Comma delimited SEO keywords')
    meta_description    = models.CharField(max_length=255, help_text='Comment for desc meta')
    season              = models.ForeignKey(Season)
    length              = models.IntegerField(default = 0)
    title               = models.CharField(max_length=255,default='', help_text='Title for this episode')
    audioFileLocation   = models.CharField(max_length=255,default='', help_text='Path to the audio for this episode')
    broadcastDate       = models.DateField(_("Date"), default='1970-01-01')
    episodeNumber       = models.IntegerField(default = 0)
    
    '''  simple counter of likes '''
    likes               = models.IntegerField()

    def get_episode_length(self):
        ''' return the length value in min:sec '''
        import datetime
        return str(datetime.timedelta(seconds=self.length))
    
    def get_episode_season(self):
        return self.season.name
    
    def episode_series(self):
        return self.season.partOfSeries.name
     
    class Meta:
        db_table = 'episodes' 
        ordering = ['-created']
        verbose_name_plural = 'Episodes'
        
    def __unicode__(self): return self.name

    def get_absolute_url(self):
        return reverse( "creativework.views.show_episode", kwargs={'episode_slug':self.slug})
    

    @classmethod
    def create(cls, 
                name, 
                description,
                #hackUrl,              
                slug,
                #image,
                is_active,
                meta_keywords,
                meta_description,
                season,
                audioFileLocation,
                length, 
                broadcastDate, 
                title,
                episodeNumber,
                likes = 0):
 
        episode = cls(name = name, 
                description = description,
                #hackUrl = hackUrl,
                slug = slug,
                #image = image,
                is_active = is_active,
                meta_keywords = meta_keywords,
                meta_description = meta_description,
                season = season,
                audioFileLocation = audioFileLocation,
                length = length,
                broadcastDate = broadcastDate, 
                title = title,
                episodeNumber = episodeNumber,
                likes = 0)
        
        # do something with the episode
        return episode
    
    
class Review( Thing ):
    is_active           = models.BooleanField(default = False)
    is_flagged          = models.BooleanField(default = False)
    slug                = models.SlugField(max_length=255, unique=True, help_text='Probably not going to be used')
    series              = models.OneToOneField(Series)
    meta_keywords       = models.CharField(max_length=255, help_text='Probably not going to be used')
    meta_description    = models.CharField(max_length=255, help_text='Probably not going to be used')
    reviewtext          = models.CharField(max_length=500, unique=False) 
    rating              = models.IntegerField(default = 0)
    
    '''  simple counter of likes '''
    helpful               = models.IntegerField(default = 0)
    unelpful              = models.IntegerField(default = 0)

    class Meta:
        db_table = 'review'
        ordering = ['-created']
        verbose_name_plural = 'Reviews'
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse( "show_review_byslug", kwargs={'review_slug':self.slug})
    

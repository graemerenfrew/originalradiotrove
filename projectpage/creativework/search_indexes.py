import datetime
from haystack import indexes
from models import Series, EpisodeBase
 

class SeriesIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
 
    content_auto = indexes.EdgeNgramField(model_attr = 'name')

    def get_model(self):
        return Series
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all() #TODO only return active?
    
class EpisodeIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    
    content_auto = indexes.EdgeNgramField(model_attr = 'name')

    def get_model(self):
        return EpisodeBase
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all() #TODO only return active?

from django.contrib.sitemaps import Sitemap
from models import Series, Season, EpisodeBase

class SeriesSitemap(Sitemap):
    changefreq = 'Monthly'
    priority = 0.5
    
    def items(self):
        return Series.objects.all()
    
    def lastmod(self, obj):
        return obj.modified
    
class EpisodeBaseSitemap(Sitemap):
    changefreq = 'Monthly'
    priority = 0.5
    
    def items(self):
        return EpisodeBase.objects.all()
    
    def lastmod(self, obj):
        return obj.modified
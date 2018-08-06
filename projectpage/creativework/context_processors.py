from models import Season, EpisodeBase, Genre, Series, ParentGenre
from review.models import Review

def creativeworkprocessor(request): 
    return {
            'recent_reviews':       Review.objects.order_by('-creation_date')[:5],
           # 'recent_reviews':       Review.objects.all(),
         
            'active_seasons':       Season.objects.filter(is_active=True), 
            'active_episodes':      EpisodeBase.objects.filter(is_active=True),
            'active_genres':        Genre.objects.filter(is_active=True), 
            'active_parentgenres':  ParentGenre.objects.filter(is_active=True),
            'active_series':        Series.objects.filter(is_active=True), 
            'site_name':            'radioTrove',    
            'meta_keywords':        'meta',
            'meta_description':     'meta',
            'request':              request }
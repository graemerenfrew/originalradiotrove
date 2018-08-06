from django import template
from creativework.models import ParentGenre, Genre

register = template.Library()

def nav_parentgenrelist():
        parentgenres = ParentGenre.objects.filter(is_active=1)
        return {'parentgenres': parentgenres}
    
register.inclusion_tag('parentgenre_list.html')(nav_parentgenrelist)
 

def nav_genrelist():
        genres = Genre.objects.filter(is_active=1)
        return {'genres': genres}
    
register.inclusion_tag('genre_list.html')(nav_genrelist)
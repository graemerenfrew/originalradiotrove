from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from creativework.models import Season, Series, EpisodeBase, Genre, ParentGenre
from django.shortcuts import render_to_response 

def listing(request):
    import pdb; pdb.set_trace()
    show_list = Series.objects.all()
    paginator = Paginator(show_list, 12) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        shows = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        shows = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        shows = paginator.page(paginator.num_pages)

    return render_to_response('_series_list.html', {"shows": shows})
        

from django.shortcuts import get_object_or_404, render_to_response 
from models import Season, Series, EpisodeBase, Genre, ParentGenre
from django.template import RequestContext
from forms import ReviewForm 
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.formtools.wizard.views  import SessionWizardView
from django.core.mail import send_mail
from django.views.generic import CreateView
from models import Series
from forms import SeriesForm, SeasonFormSet, SeasonForm, EpisodeFormSet

    
import logging
logger = logging.getLogger(__name__)

from django.views.generic import CreateView
from django.shortcuts import redirect

from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader

def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()


class AddSeasonView(CreateView):
    template_name = 'create_season.html'
    form_class = SeasonForm

    def get_context_data(self, **kwargs):
        context = super(AddSeasonView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = EpisodeFormSet(self.request.POST)
        else:
            context['formset'] = EpisodeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SeriesCreateView(CreateView):
    ''' form to allow me to get all episodes associated with a series season '''
    template_name = "gather_audio.html"
    model         = Series
    form_class    = SeriesForm
    success_url   = 'creativework/success/'
    
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object  = None
        form_class   = self.get_form_class()
        form         = self.get_form(form_class)
        season_form  = SeasonFormSet()
        episode_form = EpisodeFormSet()
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  season_form=season_form,
                                  episode_form=episode_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object  = None
        form_class   = self.get_form_class()
        form         = self.get_form(form_class)
        season_form  = SeasonFormSet(self.request.POST)
        episode_form = EpisodeFormSet(self.request.POST)
        
        if (form.is_valid() and season_form.is_valid() and
            episode_form.is_valid()):
            return self.form_valid(form, season_form, episode_form)
        else:
            return self.form_invalid(form, season_form, episode_form)

    def form_valid(self, form, season_form, episode_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object          = form.save()
        season_form.instance = self.object
        season_form.save()
        
        episode_form.instance = self.object
        episode_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, season_form, episode_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  season_form=season_form,
                                  episode_form=episode_form))
        

#url(r'^import/$', GatherAudioWizardView.as_view([SeasonGatherAudioForm1,SeasonGatherAudioForm2,SeasonGatherAudioForm3])),
                    
class GatherAudioWizardView(SessionWizardView):
    ''' view to do all the stuff to get audio together '''
    template_name = "gather_audio_wizard.html"
    
    def get_form_kwargs(self, step=None):
        kwargs = {}
         
        if step == '1':
            partOfSeries = self.get_cleaned_data_for_step('0')['partOfSeries']
            kwargs.update({'partOfSeries': partOfSeries, })
        if step == '2':
            season = self.get_cleaned_data_for_step('1')['season']
            kwargs.update({'season': season })
            
        return kwargs
     
    def done(self, form_list, **kwargs):
        form_data = process_audio_form_data(form_list)
        
        return render_to_response('gather_done.html')

def process_audio_form_data(form_list):
    ''' should save to database in the correct objects '''
    form_data = [form.cleaned_data for form in form_list]
    
    logger.debug(form_data[0]['subject'])
    logger.debug(form_data[1]['subject'])
    logger.debug(form_data[2]['subject'])
    
    ''' send a quick confirm email '''
    send_mail(form_data[0]['subject'],
              ['graemerenfrew@gmail.com'],
              fail_silently=False)
    
    return form_data
 

class ShowListView( ListView ):
    ''' sorted list view '''
    template_name = "creativeworkindex.html"
    model = Series
    
    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)
        orderedBy = self.args[0]
        
        if orderedBy:
            if orderedBy == 'oldest':
                context['shows'] = Series.objects.filter(is_active = True).order_by( 'modified' )
            elif orderedBy == 'newest':
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
            else:
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
        else:
            context['shows'] = Series.objects.all().filter(is_active = True)
        
        return context
        
class ShowListViewOld( ListView ):
    ''' Main View for all the shows on the front page '''   
    template_name = "creativeworkindex.html"
    
    def get_context_data(self, **kwargs):
        import pdb; 
         
        orderedBy = ''
        context = super(ShowListView, self).get_context_data(**kwargs)
        pdb.set_trace()
        orderedBy = self.args[0]
        
        if orderedBy:
            if orderedBy == 'oldest':
                context['shows'] = Series.objects.filter(is_active = True).order_by( 'modified' )
            elif orderedBy == 'newest':
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
            elif orderedBy == 'highest':    
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
            elif orderedBy == 'lowest':    
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
            else:
                context['shows'] = Series.objects.filter(is_active = True).order_by( '-modified' )
        else:
            context['shows'] = Series.objects.all()
        
        return context

class ShowListViewFiltered( ListView ):
    ''' Main View for all the shows on the front page but with filter applied '''   

    context_object_name = "series_list"
    template_name = "creativeworkindex.html"
    
    def get_queryset(self):
        queryset = Series.objects.all().order_by('-modified')
        #publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return queryset
    
    #def get_context_data(self, **kwargs):
    #    filteredBy = ''
    #    context = super(ShowListViewFiltered, self).get_context_data(**kwargs)
    #    
    #    filteredBy = self.args[0]
    #    if filteredBy:
    #        logger.debug('***filter = %s' % filteredBy )
    #        context['shows'] = Series.objects.filter(is_active = True)
    #    else:
    #        context['shows'] = Series.objects.all()
        
    #    return context

 
def myfunction():
    logger.debug("this is a debug message!")
 
def myotherfunction():
    logger.error("this is an error message!!")

def episodes(request, template_name="listofepisodes.html"):
    return render_to_response(template_name, {'episodes': EpisodeBase.objects.all()}, context_instance=RequestContext(request))

def episode(request, template_name="episode.html", episode_id=1):
    return render_to_response(template_name, {'episode': EpisodeBase.objects.get(id = episode_id) }, context_instance=RequestContext(request))

def index(request, template_name="creativeworkindex.html"):

    #choiceForm = SortDropDownForm()
    #return render_to_response(template_name, {'shows': Series.objects.all(), 'SortDropDownForm': SortDropDownForm}, context_instance=RequestContext(request))
    return render_to_response(template_name, {'shows': Series.objects.all()}, context_instance=RequestContext(request))

def genres(request, template_name="genres.html"):
    return render_to_response(template_name, {'genres': Genre.objects.all()}, context_instance=RequestContext(request))

def genre(request, template_name="genre.html", genre_id=1):
    return render_to_response(template_name, {'episode': Genre.objects.get(id = genre_id)}, context_instance=RequestContext(request))
   
def parentgenres(request, template_name="parentgenres.html"):
    return render_to_response(template_name, {'parentgenres': ParentGenre.objects.all()}, context_instance=RequestContext(request))

def series(request, template_name="series.html", series_id=1):
    series = get_object_or_404(Series, id=series_id)
 
    seasons = series.season_set.all()
    page_title = series.name
    meta_keywords = series.meta_keywords 
    meta_description = series.meta_description 

 
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
           
def show_parentgenre(request, parentgenre_slug, template_name="parentgenre.html"): 
    parentgenre = get_object_or_404(ParentGenre, slug=parentgenre_slug)
    series = parentgenre.series_set.all()
    subgenres = parentgenre.genre_set.all()
    page_title = parentgenre.name
    meta_keywords = parentgenre.meta_keywords 
    meta_description = parentgenre.meta_description 
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
   
def show_genre(request, genre_slug, template_name="genre.html"): 
    genre = get_object_or_404(Genre, slug=genre_slug)
    series = genre.series_set.all()
    page_title = genre.name
    meta_keywords = genre.meta_keywords 
    meta_description = genre.meta_description 
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
   
def show_series(request, series_slug, template_name="listofseries.html"): 
    series = get_object_or_404(Series, slug=series_slug)
    series.viewcount += 1
    series.save() 
    seasons = series.season_set.all()
    page_title = series.name
    meta_keywords = series.meta_keywords 
    meta_description = series.meta_description 

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def like_series(request, series_id ): 
    if series_id:
        s = Series.objects.get( id = series_id )
        count = s.likes
        count += 1
        s.likes = count
        s.save()
               
    return HttpResponseRedirect('/creativework/series/get/%s' % series_id)


def show_season(request, season_slug, season_partOfSeries_slug, template_name="season.html"): 
     
    season = get_object_or_404(Season, slug=season_slug)
    episodes = season.episodebase_set.all().order_by('episodeNumber')

    series_slug = season.partOfSeries.slug
    series = get_object_or_404(Series, slug=series_slug)
     
    page_title = season.name
    meta_keywords = season.meta_keywords 
    meta_description = season.meta_description 

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_episode(request, episode_slug, template_name="episode.html"): 
    episode = get_object_or_404(EpisodeBase, slug=episode_slug)
    #seasons = a.seasons.filter(is_active=True)
    page_title = episode.title
    meta_keywords = episode.meta_keywords
    meta_description = episode.meta_description
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def create_review(request, series_id):
    if request.POST:
        form = ReviewForm(request.POST, series_id)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/genre/all/') #stuck this here, trying to get past it
    else:
        form = ReviewForm()
        
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    args['series_id'] = series_id
        
    return render_to_response('create_review.html', args)
              
def search_series(request):
    series = SearchQuerySet().filter(content = request.POST.get('search_text','term'))
    args = {}
    args.update(csrf(request))
    args['series'] = series

    return render_to_response('ajax_search.html', args, context_instance=RequestContext(request) )


def index_old(request, format):
    series_list = Series.objects.filter(is_active = True).order_by('-modified')

    return ListView(request, template_name = '_series_list.html', queryset = series_list, paginate_by = 25)
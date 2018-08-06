from django import forms
from models import EpisodeBase, Review, Series, Season
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
 
class SeriesForm(ModelForm):
    ''' build a show '''
    class Meta:
        model = Series
        
class SeasonForm(ModelForm):
    ''' build a show '''
    class Meta:
        model = Season
        
SeasonFormSet  = inlineformset_factory(Series, Season, fk_name="partOfSeries", extra=1)
EpisodeFormSet = inlineformset_factory(Season, EpisodeBase, fk_name="season",  extra=5)
    
class EpisodeAdminForm(forms.ModelForm): 
    class Meta:
        model = EpisodeBase 
         
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.') 
        return self.cleaned_data['price']
    
class SeasonGatherAudioForm1(forms.Form):
    ''' Special Form to allow me to gather all episodes in a season at the same time '''    
    class Meta:
        model = Series
        
    #Select the season we want to get the audio information in to
    #Get the folder where the audio has been uploaded to (manually)
    partOfSeries = forms.ModelChoiceField(queryset=Series.objects.all())
    
class SeasonGatherAudioForm2(forms.Form):
    
    class Meta:
        model = Season
        fields = ('series',)
        
    #Select the season we want to get the audio information in to
    #Get the folder where the audio has been uploaded to (manually)
    #series = forms.CharField(label=u' Series :', max_length=30) 
         
    def __init__(self,  *args, **kwargs):
        #Need to pop the data out of kwargs before super'ing 
        self.partOfSeries = kwargs.pop('partOfSeries', None)       
        super(SeasonGatherAudioForm2, self).__init__( *args, **kwargs)
        self.fields['series']  = self.partOfSeries.id

    season = forms.ModelChoiceField(queryset=Season.objects.filter(partOfSeries =  29)) 
    
class SeasonGatherAudioForm3(forms.Form):
    ''' comment ''' 
    #Loop over the folder 
    #    get all fileness
    #    extract tag information
    #    
    # 
    def __init__(self, *args, **kwargs):
        self.season = kwargs.pop('season')

        super(SeasonGatherAudioForm2, self).__init__(*args, **kwargs)
        
        #Where is the audio stored for this series' season?
        audioFolder = self.season.audioFolder 
        print 'the audio is here %s ' % audioFolder
        
class ReviewForm(forms.ModelForm ):
    
    class Meta:
        model = Review
        fields = ('reviewtext',)
        
        

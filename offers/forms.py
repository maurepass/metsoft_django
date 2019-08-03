from django import forms

from .models import (AtestType, Detail, HeatTreatment, Notice, Offer,
                     OfferPatternStatus, PatternTaper)


class OfferDetailsForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ['notices', 'status']
        widgets = {
          'notices': forms.Textarea(attrs={'rows': 15, 'cols': 100}),
        }


class OfferCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ['offer_no', 'client', 'user_mark', 'user_tech', 'date_tech_in']
        widgets = {'date_tech_in': forms.DateInput(attrs={'id': 'datepicker1'}, format='%Y-%m-%d')}


class DetailCreateForm(forms.ModelForm):

    pattern = forms.ChoiceField(
        choices=[(choice.status, choice.status) for choice in OfferPatternStatus.objects.all()],
        label="Model"
    )
    heat_treat = forms.ChoiceField(
        choices=[(choice.term, choice.term) for choice in HeatTreatment.objects.all()],
        label='Obróbka cieplna'
    )
    tapers = forms.ChoiceField(
        choices=[(choice.taper, choice.taper) for choice in PatternTaper.objects.all()],
        label='Pochylenia'
    )
    atest = forms.ChoiceField(
        choices=[(choice.atest, choice.atest) for choice in AtestType.objects.all()],
        label='Atest'
    )
    boxes = forms.CharField(label='Skrzynki formierskie',
                            widget=forms.TextInput(attrs={'placeholder': '1,0 x 2,0 x 3,0'})
                            )

    class Meta:
        model = Detail
        fields = ('cast_name', 'drawing_no', 'mat', 'draw_weight', 'cast_weight', 'pieces_amount',
                  'yeld', 'difficulty', 'pattern', 'heat_treat', 'machining', 'tolerances', 'tapers',
                  'atest', 'required', 'quality_class', 'boxes', 'others', 'fr_chromite')


class DetailUpdateForm(forms.ModelForm):

    class Meta:
        model = Detail
        exclude = ('offer', 'fr_mold_work', 'fr_mold_mat', 'fr_fettling', 'fr_welding', 'fr_heating', 'fr_scrap')


class OfferNoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'cols': 100}),
        }


class DetailSeachingForm(forms.Form):

    drawing_no = forms.CharField(label='Wpisz nr rysunku:', required=False)
    cast_name = forms.CharField(label='Wpisz nazwę odlewu:', required=False)
    offer_no = forms.CharField(label='Wpisz nr oferyt:', required=False)

    class Meta:
        fields = ['drawing_no', 'cast_name', 'offer_no']

from django import forms

from .models import Order


class OrderUpdateForm(forms.ModelForm):
    numer_met = forms.CharField(disabled=True, label='Nr zlecenia')
    company = forms.CharField(disabled=True, label='Klient')
    cast_name = forms.CharField(disabled=True, label='Nazwa odlewu')
    pict_number = forms.CharField(disabled=True, label='Nr rysunku')
    cast_pcs = forms.CharField(disabled=True, label='Il. sztuk')
    cust_material = forms.CharField(disabled=True, label='Materiał')
    model = forms.CharField(disabled=True, required=False, label='Model')
    rawcast = forms.CharField(disabled=True, required=False, label='Odlew')
    painting = forms.CharField(disabled=True, required=False, label='Malowanie')
    mechrough = forms.CharField(disabled=True, required=False, label='Obr. zgrubna')
    mechfine = forms.CharField(disabled=True, required=False, label='Obr. na gotowo')
    marketing = forms.CharField(disabled=True, label='Marketing')
    ord_in = forms.DateField(disabled=True, label='Data otrzymania')

    class Meta:
        model = Order
        fields = ('numer_met', 'company', 'cast_name', 'pict_number', 'cast_pcs', 'cust_material', 'model', 'rawcast',
                  'painting', 'mechrough', 'mechfine', 'marketing', 'ord_in', 'tech_memb', 'uwagi', 'status')


class OfferStatsForm(forms.Form):
    date_stats_from = forms.DateField(label="Data początkowa",
                                      widget=forms.DateInput(
                                            attrs={'id': 'datepicker1', 'width': '275px'},
                                            format='%Y-%m-%d',
                                            )
                                      )
    date_stats_to = forms.DateField(label="Data końcowa",
                                    widget=forms.DateInput(
                                        attrs={'id': 'datepicker2', 'width': '275px'},
                                        format='%Y-%m-%d',
                                        )
                                    )

    class Meta:
        fields = ['date_stats_from', 'date_stats_to']

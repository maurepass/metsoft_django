from django import forms

from .models import Order


class OrderUpdateForm(forms.ModelForm):
    numer_met = forms.CharField(disabled=True, required=False, label="Nr zlecenia")
    company = forms.CharField(disabled=True, required=False, label="Klient")
    cast_name = forms.CharField(disabled=True, required=False, label="Nazwa odlewu")
    pict_number = forms.CharField(disabled=True, required=False, label="Nr rysunku")
    cast_pcs = forms.IntegerField(disabled=True, required=False, label="Il. sztuk")
    cust_material = forms.CharField(disabled=True, required=False, label="Materiał")
    marketing = forms.CharField(disabled=True, required=False, label="Marketing")
    ord_in = forms.DateField(disabled=True, required=False, label="Data otrzymania")

    class Meta:
        model = Order
        fields = (
            "numer_met",
            "company",
            "cast_name",
            "pict_number",
            "cast_pcs",
            "cust_material",
            "marketing",
            "ord_in",
            "tech_memb",
            "uwagi",
            "status",
        )


class OfferStatsForm(forms.Form):
    date_stats_from = forms.DateField(
        label="Data początkowa",
        widget=forms.DateInput(
            attrs={"id": "datepicker1", "width": "275px"}, format="%Y-%m-%d",
        ),
    )
    date_stats_to = forms.DateField(
        label="Data końcowa",
        widget=forms.DateInput(
            attrs={"id": "datepicker2", "width": "275px"}, format="%Y-%m-%d",
        ),
    )

    class Meta:
        fields = ["date_stats_from", "date_stats_to"]

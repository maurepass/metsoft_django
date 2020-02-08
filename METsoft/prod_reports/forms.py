from django import forms


class ExecutionTimeForm(forms.Form):
    met_number = forms.CharField(label='Nr MET', required=False)
    company = forms.CharField(label='Klient', required=False)
    cast_name = forms.CharField(label='Nazwa odlewu', required=False)
    picture_number = forms.CharField(label='Numer rysunku', required=False)

    class Meta:
        fields = "__all__"

from django import forms

from .models import Pattern


class PatternReportForm(forms.Form):

    customer1 = forms.CharField(
        max_length=50,
        required=True,
        label="Nazwa firmy nr 1",
        widget=forms.TextInput(attrs={"placeholder": "pole wymagane"}),
    )
    # customer2 = forms.CharField(max_length=50, required=False, label='Nazwa firmy nr 2')
    # customer3 = forms.CharField(max_length=50, required=False, label='Nazwa firmy nr 3')
    # not_using_time = forms.IntegerField(required=False,
    #                                     label='Czas nieużywania modelu',
    #                                     widget=forms.TextInput(attrs={'placeholder': 'ilość miesięcy'})
    #                                     )

    class Meta:
        # fields = ('customer1', 'customer2', 'customer3', 'not_using_time')
        fields = "customer1"


class PatternCreateForm(forms.ModelForm):

    material = forms.ChoiceField(
        choices=[
            ("", ""),
            ("staliwo", "staliwo"),
            ("żeliwo", "żeliwo"),
            ("kolorki", "kolorki"),
        ]
    )

    class Meta:
        model = Pattern
        fields = "__all__"
        widgets = {
            "verification": forms.Textarea(attrs={"rows": 1, "cols": 50}),
            "verification_date": forms.DateInput(
                attrs={"id": "datepicker2", "width": "230px"}, format="%Y-%m-%d"
            ),
            "remarks": forms.Textarea(attrs={"rows": 1, "cols": 50}),
            "move_in": forms.DateInput(
                attrs={"id": "datepicker1", "width": "230px"}, format="%Y-%m-%d"
            ),
            "last_order": forms.DateInput(
                attrs={"id": "datepicker3", "width": "230px"}, format="%Y-%m-%d"
            ),
        }


class PatternUpdateForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = "__all__"
        widgets = {
            "verification": forms.Textarea(attrs={"rows": 1, "cols": 50}),
            "remarks": forms.Textarea(attrs={"rows": 1, "cols": 50}),
            "move_in": forms.DateInput(
                attrs={"id": "datepicker1", "width": "230px"}, format="%Y-%m-%d"
            ),
            "last_order": forms.DateInput(
                attrs={"id": "datepicker3", "width": "230px"}, format="%Y-%m-%d"
            ),
        }

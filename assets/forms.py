from django import forms


class AssetCreateUpdateForm(forms.Form):
    amount = forms.FloatField()

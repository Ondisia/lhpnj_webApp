from django import forms

class PencarianForm(forms.Form):
    query = forms.CharField(label="Cari", max_length=255)
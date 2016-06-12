from django import forms


class FileAddForm(forms.Form):
    name = forms.CharField()
    file = forms.FileField()

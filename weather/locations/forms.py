from django import forms


class SearchLocations(forms.Form):
    city = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control me-1', 'placeholder': 'Поиск локации', 'type': "search"}))

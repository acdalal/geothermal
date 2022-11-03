from django import forms

class TempVsTimeForm(forms.Form):
    channelNumber = forms.ChoiceField(label='Display data from channel number ', choices=[(1, 1), (2, 2), (3, 3)])
    startDate = forms.CharField(label = "from ", widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    endDate = forms.CharField(label = "to ", widget=forms.TextInput(attrs={'autocomplete': 'off'}))
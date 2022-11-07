from django import forms


class TempVsTimeForm(forms.Form):
    channelNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3)],
    )
    startDate = forms.CharField(
        label="from ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )
    endDate = forms.CharField(
        label="to ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

    depth = forms.DecimalField(label="at depth:", decimal_places=2)


class TempVsDepthForm(forms.Form):
    channelNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3)],
    )
    timestamp = forms.CharField(
        label="at time ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

from django import forms


class TempVsTimeForm(forms.Form):
    boreholeNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    startDate = forms.CharField(
        label="from ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )
    endDate = forms.CharField(
        label="to ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

    depth = forms.DecimalField(label="at depth:", decimal_places=2)


class TempVsDepthForm(forms.Form):
    boreholeNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    timestamp = forms.CharField(
        label="at time ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

from django import forms
from .constants import DATA_START_DATE, DATA_END_DATE


class TempVsTimeForm(forms.Form):
    boreholeNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    dateRange = forms.CharField(
        label="during ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

    depth = forms.IntegerField(
        label="at depth:",
        widget=forms.NumberInput(attrs={"type": "number", "min": "0", "step": "1"}),
    )


class TempVsTimeDownloadForm(forms.Form):
    boreholeNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    dateRange = forms.CharField(
        label="during ", widget=forms.TextInput(attrs={"autocomplete": "off"})
    )

    depth = forms.IntegerField(
        label="at depth:",
        widget=forms.NumberInput(attrs={"type": "number", "min": "0", "step": "1"}),
    )


class TempVsDepthForm(forms.Form):
    boreholeNumber = forms.ChoiceField(
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    )
    timestamp = forms.CharField(
        label="at time ",
        widget=forms.TextInput(attrs={"autocomplete": "off", "value": DATA_START_DATE}),
    )


class QuerySelectionForm(forms.Form):
    queryType = forms.ChoiceField(
        choices=[
            ("tempvstime", "Temperature vs. Time"),
            ("tempvsdepth", "Temperature vs. Depth"),
        ],
    )

from django import forms
from .helper.constants import (
    DATA_START_DATE,
    DATA_END_DATE,
    MONTH_BEFORE_END,
    STARTING_DEPTH,
)


class TempVsTimeForm(forms.Form):
    """
    A class used to represent a temperature vs. time form.

    Attributes
    ----------
    boreholeNumber : django.forms.ChoiceField
        the borehole options a user may select to query
    dateRange : django.forms.CharField
        the date range that is queried for
    depth : django.forms.IntegerField
        the integer depth a user may select to query
    """

    boreholeNumber = forms.ChoiceField(
        label="Borehole",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    tempVsTimeDateRange = forms.CharField(
        label="Date range",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{MONTH_BEFORE_END} - {DATA_END_DATE}",
                "class": "form-control",
            }
        ),
    )

    tempVsTimeDepth = forms.IntegerField(
        label="Depth",
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "min": "0",
                "step": "1",
                "class": "form-control",
                "value": f"{STARTING_DEPTH}",
            }
        ),
    )

    tempVsTimeUnits = forms.ChoiceField(
        label="Units",
        choices=[(0, "Metric"), (1, "Imperial")],
        initial=(0, "Metric"),
        widget=forms.RadioSelect(
            attrs={
                "class": "form-control form-check-inline",
                "value": "Metric",
            }
        ),
    )


class TempVsDepthForm(forms.Form):
    """
    A class used to represent a temperature vs. depth form.

    Attributes
    ----------
    boreholeNumber : django.forms.ChoiceField
        the borehole options a user may select to query
    dateRange : django.forms.CharField
        the date range that is queried for
    """

    boreholeNumber = forms.ChoiceField(
        label="Borehole",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    tempVsDepthTimestamp = forms.CharField(
        label="Time",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": DATA_END_DATE,
                "class": "form-control",
            }
        ),
    )

    tempVsDepthUnits = forms.ChoiceField(
        label="Units",
        choices=[(0, "Metric"), (1, "Imperial")],
        initial=(0, "Metric"),
        widget=forms.RadioSelect(
            attrs={
                "class": "form-control form-check-inline",
                "value": "Metric",
            }
        ),
    )


class TemperatureProfileForm(forms.Form):
    """
    A class used to represent a form for a temperature profile plot.

    Attributes
    ----------
    boreholeNumber : django.forms.ChoiceField
        the borehole options a user may select to query
    timestamp : django.forms.CharField
        the time stamp to query data at, with a minimum at the data start date
    """

    boreholeNumber = forms.ChoiceField(
        label="Borehole",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    temperatureProfileDateRange = forms.CharField(
        label="Date range",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{MONTH_BEFORE_END} - {DATA_END_DATE}",
                "class": "form-control",
            }
        ),
    )

    temperatureProfileTimeSelector = forms.CharField(
        label="Time",
        widget=forms.TextInput(attrs={"class": "form-control", "value": "12:00 AM"}),
    )

    tempProfileUnits = forms.ChoiceField(
        label="Units",
        choices=[(0, "Metric"), (1, "Imperial")],
        initial=(0, "Metric"),
        widget=forms.RadioSelect(
            attrs={
                "class": "form-control form-check-inline",
                "value": "Metric",
            }
        ),
    )


class RawQueryForm(forms.Form):
    rawQuery = forms.CharField(widget=forms.Textarea)

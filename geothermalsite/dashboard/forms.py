from django import forms
from .helper.constants import DATA_START_DATE, DATA_END_DATE


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
        label="Display temperature from borehole number",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    dateRange = forms.CharField(
        label="during",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{DATA_START_DATE} - {DATA_END_DATE}",
                "class": "form-control",
            }
        ),
    )

    depth = forms.IntegerField(
        label="at depth:",
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "min": "0",
                "step": "1",
                "class": "form-control",
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
        label="Display temperature from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    dateRange = forms.CharField(
        label="at time ",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": DATA_START_DATE,
                "class": "form-control",
            }
        ),
    )


class StratigraphyForm(forms.Form):
    """
    A class used to represent a form for a stratigraphy plot.

    Attributes
    ----------
    boreholeNumber : django.forms.ChoiceField
        the borehole options a user may select to query
    timestamp : django.forms.CharField
        the time stamp to query data at, with a minimum at the data start date
    """

    boreholeNumber = forms.ChoiceField(
        label="Display temperature vs depth data from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    dateRange = forms.CharField(
        label="during ",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{DATA_START_DATE} - {DATA_END_DATE}",
                "class": "form-control",
            }
        ),
    )
    timeSelector = forms.CharField(
        label="at time ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class QuerySelectionForm(forms.Form):
    """
    A class used to represent a query selection form.

    Attributes
    ----------
    queryType : django.forms.ChoiceField
        the type of query to be executed
    """

    # BOREHOLE_NUMBERS = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]

    # queryType = forms.ChoiceField(
    #     label="Select a type of query ",
    #     choices=[
    #         ("tempvstime", "Temperature vs. Time"),
    #         ("tempvsdepth", "Temperature vs. Depth"),
    #     ],
    #     widget=forms.Select(attrs={"class": "form-control"}),
    # )
    # boreholeNumbers = forms.MultipleChoiceField(
    #     label="Select borehole(s) to be displayed ",
    #     required=True,
    #     choices=BOREHOLE_NUMBERS,
    #     widget=forms.CheckboxSelectMultiple(
    #         attrs={"class": "form-control form-check-inline"}
    #     ),
    # )
    # measurementTimePoint = forms.ChoiceField(
    #     label="Select measurement time point ",
    #     choices=[
    #         ("midnight", "at midnight"),
    #         ("noon", "at noon"),
    #         ("daily_average", "daily average"),
    #     ],
    #     widget=forms.Select(attrs={"class": "form-control"}),
    # )
    # dateRange = forms.CharField(
    #     label="Selecte a date range",
    #     widget=forms.TextInput(
    #         attrs={
    #             "autocomplete": "off",
    #             "value": f"{DATA_START_DATE} - {DATA_END_DATE}",
    #             "class": "form-control",
    #         }
    #     ),
    # )

    boreholeNumber = forms.ChoiceField(
        label="Display temperature vs depth data from borehole number ",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    dateRange = forms.CharField(
        label="during ",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{DATA_START_DATE} - {DATA_END_DATE}",
                "class": "form-control",
            }
        ),
    )
    timeSelector = forms.CharField(
        label="at time ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

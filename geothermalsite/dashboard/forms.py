from django import forms
from datetime import datetime, timedelta
from .helper.constants import (
    DATA_START_DATE,
    DATA_END_DATE,
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

    # if the end date is dynamic, then we need to update the DATA_END_DATE
    # to yesterday. In either case, we need to define MONTH_BEFORE_END as
    # well.
    global DATA_END_DATE
    if DATA_END_DATE == "yesterday":
        DATA_END_DATE = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")

    MONTH_BEFORE_END = (
        datetime.strptime(DATA_END_DATE, "%m/%d/%Y") - timedelta(days=30)
    ).strftime("%m/%d/%Y")

    tempVsTimeBoreholeNumber = forms.ChoiceField(
        label="Borehole",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )

    tempVsTimeDateRange = forms.CharField(
        label="Date range",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{MONTH_BEFORE_END} - {DATA_END_DATE}",
                "class": "form-control",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
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
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )

    tempVsTimeUnits = forms.ChoiceField(
        label="Display units",
        choices=[(0, "Metric"), (1, "Imperial")],
        initial=(0, "Metric"),
        widget=forms.RadioSelect(
            attrs={
                "class": "form-control custom-radio-form",
                "value": "Metric",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )


# class TempVsDepthForm(forms.Form):
#     """
#     A class used to represent a temperature vs. depth form.

#     Attributes
#     ----------
#     boreholeNumber : django.forms.ChoiceField
#         the borehole options a user may select to query
#     dateRange : django.forms.CharField
#         the date range that is queried for
#     """

#     tempVsDepthBoreholeNumber = forms.ChoiceField(
#         label="Borehole",
#         choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
#         widget=forms.Select(
#             attrs={
#                 "class": "form-control",
#                 "oninput": "cacheInput(this.attributes['name'].value, this.value)",
#             }
#         ),
#     )

#     tempVsDepthTimestamp = forms.CharField(
#         label="Date",
#         widget=forms.TextInput(
#             attrs={
#                 "autocomplete": "off",
#                 "value": DATA_END_DATE,
#                 "class": "form-control",
#                 "oninput": "cacheInput(this.attributes['name'].value, this.value)",
#             }
#         ),
#     )

#     tempVsDepthUnits = forms.ChoiceField(
#         label="Display units",
#         choices=[(0, "Metric"), (1, "Imperial")],
#         initial=(0, "Metric"),
#         widget=forms.RadioSelect(
#             attrs={
#                 "class": "form-control custom-radio-form",
#                 "value": "Metric",
#                 "oninput": "cacheInput(this.attributes['name'].value, this.value)",
#             }
#         ),
#     )


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

    # if the end date is dynamic, then we need to update the DATA_END_DATE
    # to yesterday. In either case, we need to define MONTH_BEFORE_END as
    # well.
    global DATA_END_DATE
    if DATA_END_DATE == "yesterday":
        DATA_END_DATE = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")

    MONTH_BEFORE_END = (
        datetime.strptime(DATA_END_DATE, "%m/%d/%Y") - timedelta(days=30)
    ).strftime("%m/%d/%Y")

    tempProfileBoreholeNumber = forms.ChoiceField(
        label="Borehole",
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )

    temperatureProfileDateRange = forms.CharField(
        label="Date range",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "value": f"{MONTH_BEFORE_END} - {DATA_END_DATE}",
                "class": "form-control",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )

    temperatureProfileTimeSelector = forms.CharField(
        label="Time",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "value": "12:00 AM",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )

    tempProfileUnits = forms.ChoiceField(
        label="Display units",
        choices=[(0, "Metric"), (1, "Imperial")],
        initial=(0, "Metric"),
        widget=forms.RadioSelect(
            attrs={
                "class": "form-control custom-radio-form",
                "value": "Metric",
                "oninput": "cacheInput(this.attributes['name'].value, this.value)",
            }
        ),
    )


class RawQueryForm(forms.Form):
    rawQuery = forms.CharField(widget=forms.Textarea)

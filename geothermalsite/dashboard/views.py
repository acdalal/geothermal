from django.shortcuts import render
import dateparser
import re

from .forms import TempVsTimeForm, TempVsDepthForm
from .api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages


def index(request):
    return render(request, "dashboard/index.html")


def _getTempVsTimeFormData(cleanedData: dict) -> dict:
    boreholeNumber = cleanedData["boreholeNumber"]
    depth = cleanedData["depth"]

    dateRange = cleanedData["dateRange"]
    dateList = re.findall(r"../../....", dateRange)
    startDate, endDate = dateList

    startDateUtc = dateparser.parse(startDate).__str__()
    endDateUtc = dateparser.parse(endDate).__str__()

    return {
        "boreholeNumber": boreholeNumber,
        "depth": depth,
        "startDateUtc": startDateUtc,
        "endDateUtc": endDateUtc,
    }


def tempVsTime(request):
    if request.method == "POST":
        userForm = TempVsTimeForm(request.POST)
        if userForm.is_valid():
            formData = _getTempVsTimeFormData(userForm.cleaned_data)
            queryResults = getTempVsTimeResults(
                formData["boreholeNumber"],
                formData["depth"],
                formData["startDateUtc"],
                formData["endDateUtc"],
            )

            print(queryResults)
            return render(
                request,
                "dashboard/tempvstime.html",
                context={"queryData": queryResults},
            )
        else:
            print(userForm.errors)
            return render(request, "dashboard/tempvstime.html", {"queryData": "error"})

    else:
        return render(
            request, "dashboard/tempvstime.html", context={"form": TempVsTimeForm()}
        )


def _getTempVsDepthFormData(cleanedData: dict) -> dict:
    boreholeNumber = cleanedData["boreholeNumber"]

    timestamp = cleanedData["timestamp"]
    timestampUtc = dateparser.parse(timestamp).__str__()

    return {"timestampUtc": timestampUtc, "boreholeNumber": boreholeNumber}


def tempVsDepth(request):
    if request.method == "POST":
        userForm = TempVsDepthForm(request.POST)
        if userForm.is_valid():
            formData = _getTempVsDepthFormData(userForm.cleaned_data)

            queryResults = getTempVsDepthResults(
                formData["boreholeNumber"], formData["timestampUtc"]
            )
            return render(
                request, "dashboard/tempvsdepth.html", {"queryData": queryResults}
            )
        else:
            print(userForm.errors)
            return render(
                request,
                "dashboard/tempvsdepth.html",
                {"queryData": "error", "form": TempVsDepthForm()},
            )

    else:
        return render(
            request, "dashboard/tempvsdepth.html", {"form": TempVsDepthForm()}
        )

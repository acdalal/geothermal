from django.shortcuts import render
import dateparser

from .forms import TempVsTimeForm, TempVsDepthForm
from .api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages


def index(request):
    return render(request, "dashboard/index.html")


def tempVsTime(request):
    if request.method == "POST":

        userForm = TempVsTimeForm(request.POST)
        if userForm.is_valid():
            boreholeNumber = userForm.cleaned_data["boreholeNumber"]
            startDate = userForm.cleaned_data["startDate"]
            endDate = userForm.cleaned_data["endDate"]
            depth = userForm.cleaned_data["depth"]

            startDateUtc = dateparser.parse(startDate).__str__()
            endDateUtc = dateparser.parse(endDate).__str__()

            queryResults = getTempVsTimeResults(
                int(boreholeNumber), depth, startDateUtc, endDateUtc
            )

            print(queryResults)
            return render(
                request,
                "dashboard/tempvstime.html",
                context={"queryData": queryResults, "test": "test"},
            )
        else:
            print(userForm.errors)
            return render(request, "dashboard/tempvstime.html", {"queryData": "error"})

    else:
        return render(
            request, "dashboard/tempvstime.html", context={"form": TempVsTimeForm()}
        )


def tempVsDepth(request):
    if request.method == "POST":

        userForm = TempVsDepthForm(request.POST)
        if userForm.is_valid():
            boreholeNumber = userForm.cleaned_data["boreholeNumber"]
            timestamp = userForm.cleaned_data["timestamp"]

            timestampUtc = dateparser.parse(timestamp).__str__()

            queryResults = getTempVsDepthResults(int(boreholeNumber), timestampUtc)
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

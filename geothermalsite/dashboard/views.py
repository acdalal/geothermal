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
            channelNumber = userForm.cleaned_data["channelNumber"]
            startDate = userForm.cleaned_data["startDate"]
            endDate = userForm.cleaned_data["endDate"]

            startDateUtc = dateparser.parse(startDate).__str__()
            endDateUtc = dateparser.parse(endDate).__str__()

            queryResults = getTempVsDepthResults(channelNumber, startDateUtc)
            return render(
                request, "dashboard/tempvstime.html", {"queryData": queryResults}
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
            channelNumber = userForm.cleaned_data["channelNumber"]
            timestamp = userForm.cleaned_data["timestamp"]

            queryResults = getTempVsDepthResults(channelNumber, timestamp)
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

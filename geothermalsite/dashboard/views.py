from django.shortcuts import render
import dateparser

from .forms import TempVsTimeForm
from .api import getTempVsDepthResults, getTempVsTimeResults, getDataOutages


def index(request):
    if request.method == "POST":

        userForm = TempVsTimeForm(request.POST)
        if userForm.is_valid():
            channelNumber = userForm.cleaned_data["channelNumber"]
            startDate = userForm.cleaned_data["startDate"]
            endDate = userForm.cleaned_data["endDate"]

            startDateUtc = dateparser.parse(startDate).__str__()
            endDateUtc = dateparser.parse(endDate).__str__()

            queryResults = getTempVsDepthResults(channelNumber, startDate)
            return render(request, "dashboard/index.html", {"queryData": queryResults})
        else:
            print(userForm.errors)
    form = TempVsTimeForm()
    return render(request, "dashboard/index.html", {"form": form})

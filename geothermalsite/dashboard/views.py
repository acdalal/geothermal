from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from datetime import datetime, timedelta
import dateparser
from .forms import TempVsTimeForm


def index(request):
    if request.method == "POST":
        userForm = TempVsTimeForm(request.POST)
        # check whether it's valid:
        if userForm.is_valid():
            channelNumber = userForm.cleaned_data["channelNumber"]
            startDate = userForm.cleaned_data["startDate"]
            endDate = userForm.cleaned_data["endDate"]

            startDateUtc = dateparser.parse(startDate).__str__()

            endDateUtc = dateparser.parse(endDate).__str__()
            print(channelNumber, startDateUtc, endDateUtc)
        else:
            print(userForm.errors)
    form = TempVsTimeForm()
    return render(request, "dashboard/index.html", {"form": form})


def countMeasurement(request):
    # proof of concept query

    query = "select COUNT(*) from measurement"
    with connections["geothermal"].cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return HttpResponse(results)


def getTempVsDepthResults(request):
    """
    Returns a list of all data points across all measurements associated with
    the channel during that hour.

    Parameters
    ----------
    channel (int:1 or 3)
    startHour (string datetime format: '%Y-%m-%d %H:%M:%S')

    Returns
    ----------
    An HttpResponse holding a dictionary with form (column label:data point)

    Example
    ----------
    URL: /dashboard/tempvsdepth?channel=1&startHour=2022-05-17 00:00:00
    Result: all data points from channel 1 on 2022-05-17 from 00:00:00 to
                                                              01:00:00
    """

    query = """SELECT channel_id, measurement_id, datetime_utc, dts_data.id,
            dts_data.temperature_c, dts_data.depth_m
            FROM measurement, dts_data
            WHERE measurement.channel_id IN (SELECT id FROM channel WHERE
                                             channel_name=%s)
            AND measurement.datetime_utc between %s AND %s
            AND measurement.id = dts_data.measurement_id;
            """
    results = []

    channel = request.GET.get("channel")
    channelName = "channel " + channel
    startHour = request.GET.get("startHour")
    startHourDatetime = datetime.strptime(startHour, f"%Y-%m-%d %H:%M:%S")
    endHourDatetime = startHourDatetime + timedelta(hours=1)
    endHour = endHourDatetime.strftime(f"%Y-%m-%d %H:%M:%S")

    with connections["geothermal"].cursor() as cursor:
        cursor.execute(
            query,
            (
                channelName,
                startHour,
                endHour,
            ),
        )
        for row in cursor.fetchall():
            datapoint = {
                "channel_id": row[0],
                "measurement_id": row[1],
                "datatime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
                "data_id": row[3],
                "temperature_c": row[4],
                "depth_m": row[5],
            }
            results.append(datapoint)

    return HttpResponse(results)

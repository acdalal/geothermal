from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from datetime import datetime, timedelta


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def countMeasurement(request):
    # proof of concept query

    query = 'select COUNT(*) from measurement'
    with connections['geothermal'].cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return HttpResponse(results)
    

def getTempVsDepthResults(request):
    # TODO: clean this function up

    """Given a channel (1 or 3) and a startHour (in string datetime
    format: '%Y-%m-%d %H:%M:%S'), returns a list of all data points
    across all measurements associated with a the channel during that hour
    in JSON format.
    """

    query = """SELECT measurement_id, datetime_utc, dts_data.id, dts_data.temperature_c, dts_data.depth_m
                FROM measurement, dts_data
                WHERE measurement.channel_id = 15
                AND measurement.datetime_utc between %s AND %s
                AND measurement.id = dts_data.measurement_id
            """
    results = []
    #2022-05-17 00:00:00', '2022-05-17 01:00:00'
    # startHourDatetime = datetime.strptime(startHour, f"%Y-%m-%d %H:%M:%S")
    # endHourDatetime = startHourDatetime + timedelta(hours=1)
    # endHour = endHourDatetime.strftime(f"%Y-%m-%d %H:%M:%S")
    startHour = request.GET.get('startHour')
    endHour = request.GET.get('endHour')
    with connections['geothermal'].cursor() as cursor:
        print("established connection")
        cursor.execute(
            query, (startHour, endHour,),
            # (
            #     channel,
            # ),
        )
        print("query executed")
        rowCount = 0
        for row in cursor.fetchall():
            results.append(row)
            # datapoint = {
            #     "chanel_id": row[0],
            #     "measurement_id": row[1],
            #     "datatime_utc": row[2].strftime(f"%Y-%m-%d %H:%M:%S"),
            #     "data_id": row[3],
            #     "temperature_c": row[4],
            #     "depth_m": row[5],
            # }
            # results.append(datapoint)
            # rowCount += 1
            # print(rowCount)

    return HttpResponse(results)

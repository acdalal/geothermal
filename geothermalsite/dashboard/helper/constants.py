from datetime import datetime, timedelta


DATA_START_DATE = "02/27/2019"

# When set to "today", the most current data will be available.
# This can be changed to a date in the same format as DATA_START_DATE
# if you would like to hard-code the last day that data will be available.
# NOTE: we set this to "yesterday" rather than "today" since we don't want users
# to be able to query data from the current day when there might not be any
# data at certain times.
DATA_END_DATE = "yesterday"

STARTING_DEPTH = 10

METRIC = 0
IMPERIAL = 1

HOURS = 0  # each line is a measurement
DAYS = 1  # each color is a day
WEEKS = 2  # each color is a week
MONTHS = 4  # each color is a month
YEARS = 5  # each color is a year
GROUPS = [HOURS, DAYS, WEEKS, MONTHS, YEARS]

MONTH_SHORTHAND = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


DEPTH_LOW_THRESHOLD_M = 2
DEPTH_HI_THRESHOLD_M = 158
DEPTH_LOW_THRESHOLD_FT = 5
DEPTH_HI_THRESHOLD_FT = 520

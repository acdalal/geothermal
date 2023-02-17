from datetime import datetime, timedelta


DATA_START_DATE = "02/27/2019"
DATA_END_DATE = "09/04/2022"
MONTH_BEFORE_END = (
    datetime.strptime(DATA_END_DATE, "%m/%d/%Y") - timedelta(days=30)
).strftime("%m/%d/%Y")

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

import datetime
import lib.user
import lib.polarflow

# START_DATE = "2019-10-18"
START_DATE = "2022-10-18"
access_token = lib.user.get_access_token()


def get_missing_dates(data):
  missing_dates = []
  if len(data) == 0:
    date_str = START_DATE
  else:
    date_str = data[-1]["date"]
  date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
  date += datetime.timedelta(days=1)
  while date < datetime.datetime.now():
    missing_dates.append(date)
    date += datetime.timedelta(days=1)
  return missing_dates


def get_date_data(date, data_group, get_row_data):
  date_str = date.strftime("%Y-%m-%d")
  endpoint = f'/users/{data_group}/{date_str}'
  result = lib.polarflow.get(endpoint, access_token["access_token"])
  return get_row_data(result)

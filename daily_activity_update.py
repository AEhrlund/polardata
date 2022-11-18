CSV_FILE = "data/daily_activity.csv"
DATA_GROUP = "activity-transactions"


def get_empty_row(date):
  return {
    "date": date.strftime("%Y-%m-%d"),
  }


def get_row_data(row):
  return {
    "date": row["date"],
  }


import lib.update
import lib.database

data = lib.database.read(CSV_FILE, get_row_data)
missing_dates = lib.update.get_missing_dates(data)
for date in missing_dates:
  data_row = None
  try:
    data_row = lib.update.get_date_data(date, DATA_GROUP, get_row_data)
  except Exception as ex:
    data_row = get_empty_row(date)
  data.append(data_row)
# lib.database.save(CSV_FILE, data)

import lib.update
import lib.database
import lib.nightly_recharge

data = lib.database.read(lib.nightly_recharge.CSV_FILE, lib.nightly_recharge.get_row_data)
missing_dates = lib.update.get_missing_dates(data)
for date in missing_dates:
  data_row = None
  try:
    data_row = lib.update.get_date_data(date, lib.nightly_recharge.DATA_GROUP, lib.nightly_recharge.get_row_data)
  except Exception as ex:
    data_row = lib.nightly_recharge.get_empty_row(date)
  data.append(data_row)
lib.database.save(lib.nightly_recharge.CSV_FILE, data)

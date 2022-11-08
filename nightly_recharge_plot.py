import pandas
import matplotlib.pyplot as plt
import lib.database
import lib.nightly_recharge

data = lib.database.read(lib.nightly_recharge.CSV_FILE, lib.nightly_recharge.get_row_data)

y_axis = []
dates = []
value_name = "heart_rate_avg"
min_value = -1
max_value = 62

for date_value in data:
  if date_value[value_name] > min_value and date_value[value_name] < max_value:
    y_axis.append(date_value[value_name])
    dates.append(date_value["date"])


def plot_data(dates, y_axis):
  plt.plot(dates, y_axis)
  plt.show()


def get_moving_average(data, windows_size):
  series = pandas.Series(data)
  ma_data = [window.mean() for window in series.rolling(windows_size) if len(window) == windows_size]
  return ma_data


ma_data = get_moving_average(y_axis, 100)
dates = dates[len(dates) - len(ma_data):]
plot_data(dates, ma_data)

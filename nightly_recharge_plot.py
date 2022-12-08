import pandas
import argparse
import matplotlib.pyplot as plt
import lib.database
import lib.nightly_recharge


def plot_data(dates, y_axis):
  plt.plot(dates, y_axis)
  plt.show()


def get_moving_average(data, windows_size):
  series = pandas.Series(data)
  ma_data = [window.mean() for window in series.rolling(windows_size) if len(window) == windows_size]
  return ma_data


if __name__ == '__main__':
  value_name = "heart_rate_avg"
  min_value = -1
  max_value = 65

  argparser = argparse.ArgumentParser()
  argparser.add_argument("value_name", choices=["hr", "hrv"])
  args = argparser.parse_args()
  if args.value_name == "hrv":
      value_name = "heart_rate_variability_avg"

  y_axis = []
  dates = []
  data = lib.database.read(lib.nightly_recharge.CSV_FILE, lib.nightly_recharge.get_row_data)
  for date_value in data:
    if date_value[value_name] > min_value and date_value[value_name] < max_value:
        y_axis.append(date_value[value_name])
        dates.append(date_value["date"])

  ma_data = get_moving_average(y_axis, 100)
  dates = dates[len(dates) - len(ma_data):]
  plot_data(dates, ma_data)

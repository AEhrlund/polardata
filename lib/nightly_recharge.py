CSV_FILE = "data/nightly_recharge.csv"
DATA_GROUP = "nightly-recharge"


def get_empty_row(date):
  return {
    "date": date.strftime("%Y-%m-%d"),
    "heart_rate_avg": -1,
    "beat_to_beat_avg": -1,
    "heart_rate_variability_avg": -1,
    "breathing_rate_avg": -1.0
  }


def get_row_data(row):
  return {
    "date": row["date"],
    "heart_rate_avg": int(row["heart_rate_avg"]),
    "beat_to_beat_avg": int(row['beat_to_beat_avg']),
    "heart_rate_variability_avg": int(row["heart_rate_variability_avg"]),
    "breathing_rate_avg": float(row["breathing_rate_avg"])
  }

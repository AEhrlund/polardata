import os
import csv


def read(file, get_row_data):
  data = []
  if not os.path.isfile(file):
    return data
  with open(file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      data.append(get_row_data(row))
  return data


def save(file, data):
  with open(file, 'w', newline='') as csvfile:
    writer = None
    for date_value in data:
      if writer is None:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
      writer.writerow(date_value)

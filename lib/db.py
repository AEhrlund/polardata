import json


class DB:
    def __init__(self, storage):
        self.storage = storage
        self.data = storage.get()

    def __del__(self):
        self.storage.set(self.data)

    def addDate(self, date, heart_rate_avg, beat_to_beat_avg, heart_rate_variability_avg, breathing_rate_avg):
        self.data.append({'date': date, 'heart_rate_avg': heart_rate_avg,
                          'beat_to_beat_avg': beat_to_beat_avg,
                          'heart_rate_variability_avg': heart_rate_variability_avg,
                          'breathing_rate_avg': breathing_rate_avg})

    def getLastDate(self):
        size = len(self.data)
        if size > 0:
            return self.data[size - 1]['date']

    def exportCVS(self, type, filter):
        filename = f'{type}.csv'
        with open(filename, 'w') as file:
            for data_point in self.data:
                if filter(data_point[type]):
                    file.write(f'{data_point["date"]};{data_point[type]}\n')


class DBStorage:
    def __init__(self):
        self.file = 'data/db.json'

    def get(self):
        with open(self.file, 'r') as file:
            return json.load(file)

    def set(self, data):
        # print(data)
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=True)


if __name__ == '__main__':
    storage = DBStorage()
    db = DB(storage)
    # db.addDate('12-12-12', 1, 2, 3, 4)
    print(db.getLastDate())
    del db

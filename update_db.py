import lib.db as db
import datetime
import lib.polar_get_data as polar_get_data


def get_from_date(date):
    while date <= date.today():
        data = polar_get_data.get_nightly_recharge(date)
        if data:
            print(date.strftime("%Y-%m-%d"))
            db.addDate(date.strftime("%Y-%m-%d"), data['heart_rate_avg'], data['beat_to_beat_avg'],
                       data['heart_rate_variability_avg'], data['breathing_rate_avg'])
        else:
            print(f'{date.strftime("%Y-%m-%d")} - no data')
        date += datetime.timedelta(days=1)


def get_next_date(db):
    last_date = db.getLastDate()
    if not last_date:
        last_date = '2019-01-01'
    next_date = datetime.datetime.strptime(last_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    return next_date


if __name__ == '__main__':
    db = db.DB(db.DBStorage())
    get_from_date(get_next_date(db))
    del db

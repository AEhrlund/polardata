import lib.db as db


def filter(hr):
    return hr < 65


if __name__ == '__main__':
    db = db.DB(db.DBStorage())
    db.exportCVS('heart_rate_avg', filter)
    del db

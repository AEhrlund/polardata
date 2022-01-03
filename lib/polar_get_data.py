import requests
import lib.polar_open_accesslink_api as polar_open_accesslink_api


def get_nightly_recharge(date):
    try:
        data = polar_open_accesslink_api.get(f'/users/nightly-recharge/{date.strftime("%Y-%m-%d")}',
                                             polar_open_accesslink_api.userId['access_token'])
    except requests.exceptions.HTTPError as ex:
        print(ex)
        data = None
    return data


if __name__ == '__main__':
    data = get_nightly_recharge('2020-01-01')
    print(data)

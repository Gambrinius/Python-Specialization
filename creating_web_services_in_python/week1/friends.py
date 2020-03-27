import requests
from datetime import date

API_BASE_URL = 'https://api.vk.com/method'
API_VERSION = 5.71
# test token
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def get_user_id(uid):
    params_user = {
        'v': API_VERSION,
        'access_token': [ACCESS_TOKEN],
        'user_ids': [uid]
    }
    response_data = requests.get(url=f'{API_BASE_URL}/users.get',
                                 params=params_user).json()
    user_id = response_data['response'][0]['id']

    return user_id


def get_friends_list(user_id):
    params_friends = {
        'v': API_VERSION,
        'access_token': [ACCESS_TOKEN],
        'user_id': [user_id],
        'fields': 'bdate'
    }
    response_data = requests.get(url=f'{API_BASE_URL}/friends.get',
                                 params=params_friends).json()
    friends_list = response_data['response']['items']

    return friends_list


def calc_age(uid):
    user_id = get_user_id(uid)
    friends_list = get_friends_list(user_id)

    result_dict = {}
    current_year = date.today().year
    for friend_data in friends_list:
        if 'bdate' not in friend_data:
            continue

        friend_bdate = friend_data['bdate'].split('.')
        if len(friend_bdate) != 3:
            continue

        day, month, year = friend_bdate
        current_age = current_year - int(year)
        if current_age in result_dict:
            result_dict[current_age] += 1
        else:
            result_dict[current_age] = 1

    return sorted(result_dict.items(), key=lambda i: (-i[1], i[0]))


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

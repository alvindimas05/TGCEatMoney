import requests
import uuid
import random
import string

def random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


# with open('PickUpWaxid.json', 'r') as f:
#     data = json.load(f)
#     # data = list(filter(lambda x: 'levelId' in x and x['levelId'] == 1649439303, data))
#     data = map(lambda x: x['waxIds'], data)
#     waxIds = [waxId for sublist in data for waxId in sublist]

baseUrl = 'https://live.radiance.thatgamecompany.com'

class User:
    userId = '00000000-0000-0000-0000-000000000000'
    deviceId = '00000000-0000-0000-0000-000000000000'
    key = '0000000000000000000000000000000000000000000000000000000000000000'
    sessionId = str(uuid.uuid4())
    deviceName = ''
    userAgent = 'Sky-Live-com.tgc.sky.android/0.31.0.350504 (Iphone 14 Pro Max; iOS 26.0.0; en)'
    traceId = random_string(7)
    sessionToken = None
    authHeaders = {
        'User-Agent': userAgent,
        'Content-Type': 'application/json',
        'X-Session-ID': sessionId,
        'trace-id': traceId,
        'x-retry': '1',
        'x-sky-build-access-key': '1743442606-1ea0df430687c53e7b4c615b1f09eebbfd72c1f83fd6d0fc482a38ad68f79a16',
        'x-sky-level-id': '1509719447',
    }

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'session': self.sessionToken,
            'user': self.userId,
            'User-Agent': self.userAgent,
            'user-id': self.userId,
        }

    def auth(self):
        response = requests.post(baseUrl + '/account/auth/login', headers=self.authHeaders,
            json={
                'type': 'Google',
                'external_credentials': {
                    'external_account_type': 'Google',
                    'player_id': '109818588317229384265',
                    'signature': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImZiOWY5MzcxZDU3NTVmM2UzODNhNDBhYjNhMTcyY2Q4YmFjYTUxN2YiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MjUwNjc4ODU0OTYtMzNuOXVwODJvczE2YWFzNTliMmMyNHVzcWJlZTNicHUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MjUwNjc4ODU0OTYtMzNuOXVwODJvczE2YWFzNTliMmMyNHVzcWJlZTNicHUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDk4MTg1ODgzMTcyMjkzODQyNjUiLCJlbWFpbCI6ImxlbW9uMTEwNzIwMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJISGFjdVU3bnU5aDJ2ZzJfN2Z0cGVRIiwiaWF0IjoxNzYxMDI4MDA1LCJleHAiOjE3NjEwMzE2MDV9.mXVuSTVTuKsZ5Ucq0962ziGmlnjGH77LgeXz1-HN1kzVAD_-tqcKLDumaNTKXk_tIZZ-WlKdit7x82s1SvubB8tI5YvP_KtyomcAXwJBkfe55C8Xbqq4IZw1mWpHl4S05cEi9rKnt845mpe9d3Q0sXXZUWWPQHpLBfbeA1jRLCm15hPN6AiSVzawtt6LlSxGP5LzKnh-kuDybOK5xP7ScSdk0dNh2tLK2Icq18TGcyzqTav5IFtmt71ei6NZju4M5l_qzvmwuLDzLEnmlm-n8bjhDsMNHH0BIatzvUaQHQgiSmnpr8wE5idtfuy_Viw77VQ4oq9AqjTC0oC7v0zKRA',
                },
                'user': self.userId,
                'device': self.deviceId,
                'key': self.key,
                'device_name': self.deviceName,
                'device_token': '',
                'production': False,
                'tos_version': 4,
                'device_key': 'A2mzX28z6vSLcclRp0+17vrw4FF2lDopcwnA+b/+QXkr',
                'sig_ts': 1761017732,
                'sig': 'MEYCIQDpCNcWrD4FH1HlWexv0gPJG8LyfG4k6pihfNN+JUT94AIhAPwUKM7FUCb0dD1SjmG40q0EjPac32tKRnpZo3BHvYOf',
                'hashes': [
                    297493752,
                    1913095961,
                    3267480264,
                    221463403,
                    3643541163,
                    2989952136,
                    1731370194,
                    2265070178,
                    1173390722,
                    2568820904,
                    1663246119,
                    3836951006,
                    3390444872,
                    3850074570,
                    2245054157,
                    1118191907,
                    857670903,
                    3174660782,
                    2312856752,
                    3851695576,
                    2644524417,
                    1908769478,
                    796727208,
                    1923038502,
                    1452596462,
                    2119069447,
                    2476579611,
                    3013312771,
                    913207759,
                    1755094869,
                    4133182092,
                    756995841,
                    1963479903,
                    2548934399,
                    2738197704
                ],
                'integrity': True,
            })

        self.sessionToken = response.json().get('session')
        self.userId = response.json().get('authinfo').get('user')

    def get_friends_info(self):
        friendStatuesResponse = requests.post(baseUrl + '/account/get_friend_statues', headers=self.get_headers(), json={
            'max': 150,
            'session': self.sessionId,
            'sort_ver': 1,
            'user': self.userId,
            'user_id': self.userId
        })

        onlineFriendsResponse = requests.post(baseUrl + '/account/get_online_friends', headers=self.get_headers(), json={
            'user': self.userId,
            'user_id': self.userId,
            'session': self.sessionToken,
        })

        blockedFriendsResponse = requests.post(baseUrl + '/account/get_blocked_friends', headers=self.get_headers(), json={
            'user': self.userId,
            'user_id': self.userId,
            'session': self.sessionToken,
            'page_max': 100,
            'page_offset': 0,
        })

        friendStatues = friendStatuesResponse.json().get('set_friend_statues')

        friendsResponse = requests.post(baseUrl + '/account/get_friends', headers=self.get_headers(), json={
            'user': self.userId,
            'user_id': self.userId,
            'session': self.sessionToken,
            'players': list(map(lambda friend: friend['friend_id'], friendStatues)),
        })

        friends = friendsResponse.json().get('set_friends')
        blockedFriendsData = blockedFriendsResponse.json().get('set_blocked_friends')['friends']
        onlineFriends = onlineFriendsResponse.json().get('online_friends')

        # Get deleted friends data
        deletedFriendsData = list(filter(
            lambda f: f.get('local_soft_deleted'),
            friendStatuesResponse.json().get('set_friend_statues')
        ))

        # Mark and merge blocked + deleted friends
        for bf in blockedFriendsData:
            bf['is_blocked'] = True
            friends.append(bf)

        for df in deletedFriendsData:
            df['is_deleted'] = True
            friends.append(df)

        # Remove duplicates by friend_id (keep first occurrence)
        unique_friends = {f['friend_id']: f for f in friends}.values()

        # Sort: online first, then A–Z
        friends_sorted = sorted(
            unique_friends,
            key=lambda f: (
                f['friend_id'] not in onlineFriends,
                f.get('nickname', '').lower()
            )
        )

        print('Friends:')
        for i, friend in enumerate(friends_sorted):
            id = friend['friend_id']
            nickname = friend.get('nickname', 'No Name')

            # Determine status
            if friend.get('is_blocked'):
                status = 'Blocked'
            elif friend.get('is_deleted'):
                status = 'Deleted'
            elif friend.get('local_blocked'):
                status = 'Blocked You'
            elif id in onlineFriends:
                status = 'Online'
            else:
                status = None

            print(f"{i + 1}. {nickname}{' (' + status + ')' if status else ''}")


user = User()
user.auth()
user.get_friends_info()

# collectResponse = requests.post(
#     'https://live.radiance.thatgamecompany.com/account/collect_pickup_batch',
#     headers={
#         'User-Agent': userAgent,
#         'Content-Type': 'application/json',
#         'X-Session-ID': sessionId,
#         'trace-id': traceId,
#         'user-id': userId,
#         'session': sessionToken,
#         'x-user-id': userId,
#         'x-session-token': sessionToken,
#         'x-level-id': '3526133726',
#     },
#     json={
#         'user': userId,
#         'user_id': userId,
#         'session': sessionToken,
#         'level_id': 3526133726,
#         'pickup_ids':  [
#             2060386489,
#             2060386486,
#             2060386488,
#             2060386388
#         ],
#         'global_pickup_ids': [],
#         'emitters': []
#     })
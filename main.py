from typing import Tuple

import requests


def get_authentication_cookie(email: str, password: str) -> str:
    url = "https://hochschulsport.uni-heidelberg.de/oa_oeff/login.php"
    payload = {
        "email": email,
        "passw": password,
        "submit1": "Anmelden",
        "do": "check"
    }
    response = requests.post(url, payload, allow_redirects=False)
    if "Set-Cookie" not in response.headers.keys():
        return ""  # TODO: Exception
    return response.headers["Set-Cookie"].split(";")[0]


def get_course_specific_payload(course: str, cookie: str) -> dict:
    url = "https://hochschulsport.uni-heidelberg.de/oa_oeff/qr_rubriken.php"
    response = requests.get(url, headers={"Cookie": cookie}).text

    if course not in response:
        return {}  # TODO: Exception

    k1 = response.split(course)[0].split("<INPUT TYPE=\"submit\" NAME=\"")[-1].split("\"")[0]
    v1 = "Ticket erstellen"

    k2 = response.split(course)[1].split("<INPUT TYPE=\"hidden\" NAME=\"")[1].split("\"")[0]
    v2 = response.split(course)[1].split("<INPUT TYPE=\"hidden\" NAME=\"" + k2 + "\" VALUE=\"")[1].split("\"")[0]

    return {
        k1: v1,
        k2: v2
    }


def book(username: str, password: str, course_name: str = "Volleyball - 50:50") -> bool:
    cookie = get_authentication_cookie(username, password)
    if cookie == "":
        print("Could not authenticate user.")
        return False

    payload = get_course_specific_payload(course_name, cookie)
    if payload == {}:
        print("Could not find course.")
        return False

    url = "https://hochschulsport.uni-heidelberg.de/oa_oeff/qr_info.php"
    res = requests.post(url, payload, headers={"Cookie": cookie}).text
    if "Für diesen Kurs sind leider keine Tickets mehr verfügbar!" in res:
        print("Course already fully booked.")
        return False
    return True


def load_credentials(path: str = "credentials.txt"):
    return tuple(map(lambda x: x.strip(), open(path, "r").readlines()[:2]))


print(book(*load_credentials()))
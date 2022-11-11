import requests
from typing import Tuple


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


def get_submit_form_payload(course_form_data: dict, cookie: str) -> dict:
    url = "https://hochschulsport.uni-heidelberg.de/oa_oeff/qr_info.php"
    response = requests.post(url, course_form_data, headers={"Cookie": cookie}).text
    if "Für diesen Kurs sind leider keine Tickets mehr verfügbar!" in response:
        return {}

    k1 = response.split('<FORM METHOD="POST" ACTION="qr_info.php" name="LoginForm">')[1].split('<INPUT TYPE="hidden" NAME="')[1].split("\"")[0]
    v1 = response.split('<FORM METHOD="POST" ACTION="qr_info.php" name="LoginForm">')[1].split('<INPUT TYPE="hidden" NAME="' + k1 + '" VALUE="')[1].split("\"")[0]

    k2 = "do"
    v2 = "do"

    k3 = "buchen"
    v3 = "Ein für heute gültiges Ticket erstellen"

    return {
        k1: v1,
        k2: v2,
        k3: v3
    }


def submit(submit_form_data: dict, cookie: str) -> str:
    url = "https://hochschulsport.uni-heidelberg.de/oa_oeff/qr_info.php"
    return requests.post(url, submit_form_data, headers={"Cookie": cookie}).text


def book(username: str, password: str, course_name: str) -> Tuple[bool, str]:
    cookie = get_authentication_cookie(username, password)
    if cookie == "":
        print("Could not authenticate user.")
        return False, ""

    course_form_data = get_course_specific_payload(course_name, cookie)
    if course_form_data == {}:
        print("Could not find course.")
        return False, ""

    submit_form_data = get_submit_form_payload(course_form_data, cookie)
    if submit_form_data == {}:
        print("Course already fully booked.")
        return False, ""

    res = submit(submit_form_data, cookie)

    return True, res

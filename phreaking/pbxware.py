import requests

def session(url,username,password):
    s = requests.Session()
    login_data = {
        "email": username,
        "password": password,
        "sm_int_login": "Login"
    }

    # Log in
    s.post(url, data=login_data, headers=HEADERS)
    return s
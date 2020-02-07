def session(username,password):
    s = requests.Session()

    login_page = "https://portal.orbtalk.co.uk/index.php/auth/signin"
    login_data = {
        "LoginForm[email]": username,
        "LoginForm[password]": password,
        "LoginForm[signin]": "existing-user",
        "yt0": "Sign in"
    }

    # Log in
    s.post(login_page, data=login_data)
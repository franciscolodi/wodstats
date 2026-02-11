import streamlit_authenticator as stauth


def login():

    credentials = {
        "usernames": {
            "admin": {
                "name": "Admin",
                "password": stauth.Hasher(["1234"]).generate()[0]
            }
        }
    }

    authenticator = stauth.Authenticate(
        credentials,
        "wodstats_cookie",
        "abcdef",
        cookie_expiry_days=1
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    return name, authentication_status, username, authenticator

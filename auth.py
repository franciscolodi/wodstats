import streamlit_authenticator as stauth

# Crear hash SOLO una vez
hashed_passwords = stauth.Hasher(['1234']).generate()


def login():

    names = ["Admin"]
    usernames = ["admin"]

    authenticator = stauth.Authenticate(
        names,
        usernames,
        hashed_passwords,
        "wodstats_cookie",
        "abcdef",
        cookie_expiry_days=1
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    return name, authentication_status, username, authenticator

import streamlit as st
import requests
import os
import msal


def get_auth_url(app: msal.ConfidentialClientApplication)->str:
    auth_url = app.get_authorization_request_url(
        ["User.ReadBasic.All"],
        redirect_uri=os.environ['REDIRECT_URI']
    )
    return auth_url


def get_token_from_code(app: msal.ConfidentialClientApplication, auth_code: str)->str:
    result = app.acquire_token_by_authorization_code(
        auth_code,
        scopes=["User.ReadBasic.All"],
        redirect_uri=os.environ['REDIRECT_URI']
    )
    return result['access_token']


def get_user_info(access_token: str)->dict:
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me/memberOf',
        headers=headers
    )
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers=headers
    )

    return response.json()


def handle_redirect(app: msal.ConfidentialClientApplication)->None:
    if not st.session_state.get('access_token'):
        code = st.experimental_get_query_params().get('code')
        if code:
            access_token = get_token_from_code(app, code)
            st.session_state['access_token'] = access_token
            st.experimental_set_query_params()


def login_step()->msal.ConfidentialClientApplication:
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    TENANT_ID = os.environ['TENANT_ID']

    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    if st.experimental_get_query_params().get('code'):
        handle_redirect(app)

    access_token = st.session_state.get('access_token')

    if access_token:
        user_info = get_user_info(access_token)
        st.session_state['user_info'] = user_info
        return app
    else:
        auth_url = get_auth_url(app)
        if st.button('Login'):
            st.markdown(
                f"<meta http-equiv='refresh' content='0;url={auth_url}'>",
                unsafe_allow_html=True
            )
        st.stop()

def logout_flow(app: msal.ConfidentialClientApplication):
    home_accounts = app.get_accounts(st.session_state['user_info']['userPrincipalName'])
    for home_account in home_accounts:
        app.remove_account(home_account)
    del st.session_state['access_token']

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
        'https://graph.microsoft.com/v1.0/me/appRoleAssignments', headers=headers)
    return response.json()


def handle_redirect(app: msal.ConfidentialClientApplication)->None:
    if not st.session_state.get('access_token'):
        code = st.experimental_get_query_params().get('code')
        if code:
            access_token = get_token_from_code(app, code)
            st.session_state['access_token'] = access_token
            st.experimental_set_query_params()


def login_step():
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
        return True
    else:
        st.write("Please sign-in to use this app.")
        auth_url = get_auth_url(app)
        st.markdown(
            f"<a href='{auth_url}' target='_self'>Sign In</a>", unsafe_allow_html=True)
        st.stop()

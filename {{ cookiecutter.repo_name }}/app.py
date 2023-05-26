from src.security import login_step, logout_flow
from src.utils import dotenv_loader
import streamlit as st

if __name__ == '__main__':
    dotenv_loader()
    msal_app = login_step()
    st.write('This is the app')
    st.button('Logout', on_click=logout_flow, args=(msal_app,))

from src.security import login_step
from src.utils import dotenv_loader
import streamlit as st

if __name__ == '__main__':
    dotenv_loader()
    login_step()
    st.write('This is the app')

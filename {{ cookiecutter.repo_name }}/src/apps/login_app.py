import time
from typing import Dict
import streamlit as st
from hydralit import HydraHeadApp
import os


class LoginApp(HydraHeadApp):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def run(self) -> None:
        st.markdown(
            "<h1 style='text-align: center;'>Login</h1>",
            unsafe_allow_html=True
        )
        _, c2, _, = st.columns([2, 2, 2])
        form_data = self._create_login_form(c2)

        pretty_btn = """
        <style>
        div[class="row-widget stButton"] > button {
            width: 100%;
        }
        </style>
        <br><br>
        """
        c2.markdown(pretty_btn, unsafe_allow_html=True)
        if form_data['submitted']:
            self._do_login(form_data, c2)

    def _create_login_form(self, parent_container) -> Dict:

        login_form = parent_container.form(key="login_form")

        form_state = {}
        form_state['username'] = login_form.text_input('Username')
        form_state['password'] = login_form \
            .text_input('Password', type="password")
        form_state['submitted'] = login_form.form_submit_button('Login')

        return form_state

    def _do_login(self, form_data, msg_container) -> None:

        # access_level=0 Access denied!
        access_level = self._check_login(form_data)

        if access_level > 0:
            msg_container.success("✔️ Login success")
            with st.spinner("🤓 now redirecting to application...."):
                time.sleep(1)

                # access control uses an int value to allow for levels of
                # permission that can be set for each user, this can then
                # be checked within each app seperately.
                self.set_access(access_level)

                # Do the kick to the home page
                self.do_redirect()
        else:
            self.session_state.allow_access = 0

            msg_container.error(
                '''❌ Login unsuccessful, 😕 please check your
                username and password and try again.'''
            )

    def _check_login(self, login_data) -> int:
        # this method returns a value indicating the success of verifying the
        # login details provided and the permission level, 1 for default
        # access, 0 no access etc.
        self.check_environ()
        if login_data['username'] == os.environ['EXAMPLE_1_USER']:
            if login_data['password'] == os.environ['EXAMPLE_1_PASSWORD']:
                return 1
        if login_data['username'] == os.environ['EXAMPLE_2_USER']:
            if login_data['password'] == os.environ['EXAMPLE_2_PASSWORD']:
                return 2
        if login_data['username'] == os.environ['EXAMPLE_3_USER']:
            if login_data['password'] == os.environ['EXAMPLE_3_PASSWORD']:
                return 3
        return 0

    def check_environ(self):
        if 'EXAMPLE_1_PASSWORD' not in os.environ:
            from dotenv import find_dotenv, load_dotenv
            dotenv_path = find_dotenv()
            load_dotenv(dotenv_path)

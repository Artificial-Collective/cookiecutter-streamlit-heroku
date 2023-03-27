from hydralit import HydraHeadApp
import streamlit as st

class ExampleApp(HydraHeadApp):

    def __init__(self, config, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.config = config

    def run(self):
        st.write('Hello!')

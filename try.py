import streamlit as st
import PyPDF2
import g4f

available_models = dir(g4f.models)
st.write("Available models:", available_models)
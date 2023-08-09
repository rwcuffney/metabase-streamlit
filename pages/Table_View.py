import streamlit as st
from lexisnexisapi import metabase as mb



st.session_state.query = st.session_state.query
myData = st.session_state.myData

st.header("View the articles")
df = myData.articles_dataframe()
st.dataframe(df)
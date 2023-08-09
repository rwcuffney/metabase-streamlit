import streamlit as st
import datetime
from lexisnexisapi import metabase as mb
from lexisnexisapi import credentials as cred

st.set_page_config(layout="wide")
st.header("Metabase Search")
st.write("This is my Streamlit app")

#from lexisnexisapi import credentials as cred
#mbkey = cred.get_Key('Metabase_Search_Key')
mbkey = cred.get_Key("Metabase_Search_Key")
#st.write(f"hide this in production: {mbkey}")

with st.form("mbkey_form"):
    #mbkey = cred.get_Key('Metabase_Search_Key')
    if mbkey =='':
        st.write("you ain't got no key yo")
    else:
        st.write(f"looks like we've already got your key ending in {mbkey[-4:]}")
    input_label = 'metabase key'
    key_input = st.text_input('metabase key',mbkey[-4:])
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(key_input)
        mb.set_mb_search_key(key_input)

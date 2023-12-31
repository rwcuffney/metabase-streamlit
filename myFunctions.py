import streamlit as st

def set_session_state_variables():

	#SET SESSION STATE VARIABLES:
	session_state_variables = [
		{"field_name":"query",
		"default_value":""},
		
		{"field_name":"myData",
		"default_value":None},
		
		{"field_name":"limit",
		"default_value":200},
		
		{"field_name":"recent",
		"default_value":"false",
		"type":"parameter",
		"setup_code":"st.session_state.recent  = st.radio('recent',('true', 'false'),key='recent_parameter')"},
		
		{"field_name":"sequence_id",
		"default_value":None},
		
		{"field_name":"sort",
		"default_value":"desc"},
		
		{"field_name":"relevance_percent",
		"default_value":0},
		
		{"field_name":"sort_by_relevance",
		"default_value":"true"},
		
		{"field_name":"show_relevance_score",
		"default_value":"true"},
		
		{"field_name":"show_matching_keywords",
		"default_value":"true"},
        
        {"field_name":"query_history",
		"default_value":[]}
		]

	for i, var in enumerate(session_state_variables):
		if var['field_name'] not in st.session_state:
			st.session_state[var['field_name']] = var['default_value']
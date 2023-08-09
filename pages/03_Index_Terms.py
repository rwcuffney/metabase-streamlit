import streamlit as st
from lexisnexisapi import metabase as mb
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Page Two")

#if st.session_state.myData == None:
#    st.write('you have not run the API query yet')
#    st.stop()

indx_df = mb.indexTerms(st.session_state.myData)
max_value=len(indx_df)
slider_value = st.slider("Slider",key="slider", min_value=1, max_value=max_value,value=10)

options=set(indx_df.domains.explode())
options = st.multiselect('Please select search fields:',options = ['SUB','IND','GEO','PEO']) 

if options:
    indx_df["INCLUDE"] = indx_df["domains"].apply(lambda v: len(list(set(v).intersection(options)) )!=0 )
    indx_df =  indx_df[indx_df['INCLUDE']].reset_index(drop=True)
    del indx_df['INCLUDE']
df = indx_df.head(slider_value)
sns.set(font_scale=1)
sns.set_style('whitegrid')
ax=sns.catplot(data=df, 
    x='name', 
    y='count', 
    hue='count', 
    kind='bar', 
    palette='Blues', 
    aspect=2)

plt.xlabel('Clusters')
plt.ylabel('Scores')
plt.xticks(rotation = 45)
fig = ax.figure




cols =st.columns([1,3])
i = 0
with cols[i]:
    #st.write(indx_df[indx_df['count']>slider_value])
    
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df)
i+=1
with cols[i]:
    st.pyplot(fig)


#st.write(st.session_state.myData.articles[0])




st.session_state.query = st.session_state.query

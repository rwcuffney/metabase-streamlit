import streamlit as st
from lexisnexisapi import metabase as mb
from datetime import datetime




st.session_state.query = st.session_state.query
myData = st.session_state.myData

st.header("View the articles")
df = myData.articles_dataframe('title','url')
#options box:
options = set(df['title'].to_list())
selectbox = st.selectbox(label = 'selectbox',options=options,key='selectbox')
max_value=len(myData.articles)

slider_value = st.slider("Slider",key="slider", min_value=1, max_value=max_value,value=1)


#url = df['url'].loc[df['title'] == selectbox].head(1).item()

#st.write(df)

url = myData.articles[slider_value]["url"]
#url =df['url']


    
cols = st.columns(2)
i=0
with cols[i]:
    st.write(myData.articles[slider_value]['title'])
i+=1
with cols[i]:
    article = myData.articles[slider_value]
    title = article['title']
    pubDate = datetime.strptime(article.get('publishedDate'),'%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y')
    sourceName = article['source'].get('name','')
   
    st.write(f"[{title}]({url})")
    st.write(f"{sourceName} | {pubDate}")
    st.write(
            f'<iframe src="{url}" height="250" width="400"</iframe>',
            unsafe_allow_html=True,
            height="10000",
        )
    
    #st.write(pubDate)
    #st.write(pubDate.strftime('%m/%d/%Y'))
    #st.write(article.get('publishedDate')[:10])
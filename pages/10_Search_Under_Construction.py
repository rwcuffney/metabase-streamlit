import streamlit as st
import datetime
from lexisnexisapi import metabase as mb
from uuid import uuid4
import inspect
import myFunctions

st.set_page_config(layout="wide")
st.title("Metabase Search")

#st.session_state.query_history = []


    
def add_to_query(s):
    q = f"{st.session_state.query} {s}"
    st.session_state.query = q
    st.session_state.query_history.append(q)
    
    
def updateQueryString():
    st.session_state.query = query
    




#CREATE PARAMETERS DICTIONARY FOR API CALL:
def parameters_dict():

    #Basic parameters:
    parameters = {
    "format":"json",
    "query":st.session_state.query
    }
    
    #default parameters that need adjusting
    if st.session_state.limit != 'true':
        parameters["limit"]: st.session_state.limit
    if st.session_state.recent != 'true':
        parameters["recent"]:st.session_state.recent
    if st.session_state.sort != 'asc':
        parameters["sort"]:st.session_state.sort
    if  st.session_state.show_matching_keywords != 'false':
        parameters["show_matching_keywords"]:st.session_state.show_matching_keywords
    if st.session_state.show_relevance_score != 'false':
        parameters["show_relevance_score"]:st.session_state.show_relevance_score
    if st.session_state.sequence_id != "None":
        parameters["sequence_id"]=st.session_state.sequence_id
    if st.session_state.relevance_percent != 0:
        parameters["relevance_percent"]=st.session_state.relevance_percent
    return parameters

def and_or(k):
    return st.radio("And/or",('AND', 'OR'),key=k)  
     

myFunctions.set_session_state_variables()
    
st.header("Parameters:")

#BUILD THE PARAMETERS (SET TO DEFAULT):
cols = st.columns(3)
i=0
with cols[i]:
    st.session_state.recent = st.radio(label='recent',label_visibility='visible',options=('true', 'false'),key='recent_parameter_')
    st.session_state.sort=st.radio(label = 'sort',label_visibility='visible',options =('desc', 'asc'),key='sort_parameter_')
    st.session_state.sort_by_relevance  = st.radio(label = 'sort_by_relevance',label_visibility='visible',options =('true', 'false'),key='sort_by_relevance_parameter_')
i+=1
with cols[i]:
    st.session_state.show_relevance_score = st.radio(label = 'show_relevance_score',label_visibility='visible',options=('true', 'false'),key='show_relevance_score_parameter_')
    st.session_state.show_matching_keywords= st.radio(label='show_matching_keywords',label_visibility='visible',options=('true', 'false'),key='show_matching_keywords_parameter_')
i+=1
with cols[i]:
    st.session_state.limit =  st.number_input(label = 'limit',label_visibility='visible', min_value=0, max_value=500,value=200,key='limit_parameter_')#,on_change= test_function)
    st.session_state.sequence_id = st.text_input('sequence_id ',  value= st.session_state.sequence_id , key = 'sequence_id_parameter_')
    st.session_state.relevance_percent = st.number_input('relevance_percent', min_value=0, max_value=100, value= 0,key='relevance_percent_parameter_')

#SELECT DATE FIELDS:
st.markdown("""---""")
st.header("Date Fields:")


DATE_FIELDS = set(['pubDate','harvestDate'])

#columns for adjusting date fields:
cols = st.columns(4)
i=0
with cols[i]: 
    date_field_and_or = and_or(k='date_field_and_or')  
    date_field = st.selectbox("Select data field:",options=DATE_FIELDS,key='select_date_feild')
i+=1
with cols[i]:
    start_date = st.date_input('From',datetime.date(2020, 1, 1,),key='start_date')
    start_time = st.time_input('Start Time', datetime.time(0, 00),key='start_time')
i+=1
with cols[i]:
    end_date = st.date_input("to:",datetime.date.today(),key='end_date')
    end_time = st.time_input('End Time', datetime.time(11, 59),key='end_time')
#add to query button:    
i+=1
with cols[i]:
    if st.button(label= 'Add to query',key='add_date_field_to_query'):
        query_string= f"{date_field_and_or} {date_field}:[ {start_date}T{start_time}:00Z TO {end_date}T{end_time}:00Z]"
        add_to_query(query_string)

#SELECT TERMS:
st.markdown("""---""")
st.header("Search Terms:")

SEARCH_TERMS = ['keyword','industry','subject','language','sourceRank']
options = st.multiselect('Please select search fields:',options = SEARCH_TERMS) 
   
#CREATE TERMS INPUT:
if 'keyword' in options:
    cols = st.columns([4,2])
    i=0
    with cols[i]:
        keyword_input = st.text_input(label='keyword(s)',key='keyword_input') 
    i+=1
    with cols[i]:
        if st.button(label= 'Add keyword(s) to query',key=f'add_keywords_to_query',use_container_width =True):
            add_to_query(keyword_input)


if 'industry' in options:
    k = 'industry'
    cols = st.columns([1,3,2])
    i=0
    with cols[i]:
        industry_term_and_or= and_or(k=f'{k}_term_field_and_or')  
    i+=1
    with cols[i]:
        industry_term = st.text_input(label=k,key=f'{k}_input')   
    i+=1
    with cols[i]:
        if st.button(label= f'Add {k} to query',key=f'add_{k}_term_to_query',use_container_width =True):
            query_string = f"{industry_term_and_or} industry:({industry_term})"
            add_to_query(query_string)



if 'subject' in options:
    cols = st.columns([1,3,2])
    i=0
    with cols[i]: 
        subject_term_and_or= and_or(k='subject_term_field_and_or')  
    i+=1
    with cols[i]:
        subject_term = st.text_input(label='subject',key="subject_input")   
    i+=1
    with cols[i]:
        if st.button(label= 'Add subject to query',key='add_subject_term_to_query',use_container_width =True):
            query_string = f"{subject_term_and_or} subject:({subject_term})"
            add_to_query(query_string)   

            
            
if 'language' in options:
    cols = st.columns([1,3,2])
    i=0
    with cols[i]: 
        industry_term_and_or= and_or(k='language_term_field_and_or')  
    i+=1
    with cols[i]:
        industry_term = st.text_input(label='language',key="language_input")   
    i+=1
    with cols[i]:
        if st.button(label= 'Add language to query',key='add_language_term_to_query',use_container_width =True):
            query_string=f"{industry_term_and_or} language:({industry_term})"
            add_to_query(query_string)

if 'sourceRank' in options: 
    cols = st.columns([1,3,2])
    i=0
    with cols[i]: 
        sourceRank_and_or= and_or(k='sourceRank_field_and_or')  
    i+=1
    with cols[i]:
        sourceRank_options = st.multiselect('Source Rank:',options = [1,2,3,4,5,6,7,8,9,10])    
    i+=1
    with cols[i]:
        if st.button(label= 'Add Source Rank to query',key='add_sourceRank_term_to_query',use_container_width =True):
            options_string = ""
            for o in sourceRank_options:
                st.write(o)
                options_string = f"{options_string} {str(o)}"
               
            query_string = f"{sourceRank_and_or} sourceRank:({options_string[1:]})"
            add_to_query(query_string)


#QUERY STRING:
st.markdown("""---""")
st.header("Query String:")
cols = st.columns([4,1])
i=0
with cols[i]: 
    st.session_state.query=st.text_area(label='Search Query',label_visibility='hidden', key = 'query_',value=st.session_state.query)#,on_change = updateQueryString)
i+=1
with cols[i]:
    if st.button(label= 'clear query',key='clear_query'):
         st.session_state.query = ""
         st.experimental_rerun()
    #Use query_history to undo unwanted changes
    if st.button(label= 'Undo',key='undo_query'):
         if len(st.session_state.query_history)==0:
            st.session_state.query = ""
            st.experimental_rerun()
         elif len(st.session_state.query_history)==1:
            st.session_state.query = ""
            st.session_state.query_history.pop()
            st.experimental_rerun()
         else:
            st.session_state.query = st.session_state.query_history[-2]
            st.session_state.query_history.pop()
            st.experimental_rerun()

if st.button('Call API',key='call_api_button'):
    #updateQueryString()
    p = parameters_dict()
    st.write(dict(p))
    #st.session_state.request_history.append(p)
    st.session_state.myData = mb.Search(**p)

#else:
if st.session_state.myData == None:
    st.stop()
st.write(**parameters_dict())
st.write(f"link to the url [link]({st.session_state.myData.url})")
st.write(f"Total Results: {st.session_state.myData.totalResults}")
max_value=len(st.session_state.myData.articles)
if max_value > 0:
    slider_value = st.slider("Slider",key="slider", min_value=1, max_value=max_value,value=1)
    st.write(st.session_state.myData.articles[slider_value-1])    
else:
    st.write('Your search did not yield any results')
    
    
    
st.stop()    
'''
limit: The maximum number of articles to return. This can be between 1 and 200. The default is 1.
format: The format of the response. Can be 'xml', 'json', 'rss', or 'atom'. The default is 'xml'.
recent=true: Use this if you only need results from within the last three days. This will make your query run faster.
sequence_id: This is used for paging through the results, which can be useful if you want to retrieve more than 200 articles for a query. For example, if the last <sequenceId> tag in a response is <sequenceId>215555160724</sequenceId>, then you can get the next page of results with this request: http://metabase.moreover.com/api/v10/searchArticles?key=(your_API_key)&query=(your_query)&sequence_id=215555160724
filter_duplicates=true: Used to filter out duplicate articles. An article is considered a duplicate of another article if the articles have the same title or very similar content. Articles which are considered duplicates will have the same <duplicateGroupId> value. filter_duplicates=true will remove duplicate articles from the response, only showing the originally harvested article, i.e. the earliest <harvestDate>. When using this, the <totalResults> tag may show a count higher than the actual number of results.
duplicate_order=latest: Instead of showing the article with the earliest <harvestDate> (the 'oldest' article in the system), duplicate_order=latest will show the most recent article of a group of duplicate articles.
sort: Whether to sort the articles in ascending or descending order (ordered by the value in the <sequenceId> tag). Use sort=asc to sort in ascending order; use sort=desc to sort in descending order. The default is 'desc'. This works as expected with the sequence_id parameter: if you use limit=200&sequence_id=215555160724&sort=desc, you will get back the next 200 articles with a sequenceId less than 215555160724; if you use limit=200&sequence_id=215555160724&sort=asc, you will get back the next 200 articles with a sequenceId greater than 215555160724.
relevance_percent: Filter out less relevant articles using a whole number percentage between 1 and 100. A higher relevancy percentage will limit your results to more relevant articles. By default all matching articles are included in the results.
sort_by_relevance=true: Sort by relevanceScore instead of by sequenceId. Paging is not supported when using this parameter. The relevance of an article is based on a number of factors, including how many of the search keywords appear in the article, the number of occurrences of each keyword, how common or uncommon a keyword is (i.e., an uncommon word that appears in few documents will score higher than a common word that appears in many documents), and the total number of terms in the article text.
show_relevance_score=true: Adds a <relevanceScore> tag to each article which contains a number indicating how relevant the article is to the query. This score has no maximum value and does not have the same range of values as the 'relevancy percentage' mentioned above. This score should only be used to compare articles within a single set of results.
show_matching_keywords=true: Adds a <matchingKeywords> tag to each article which contains which keywords from the query matched the article. Matching keywords will not be shown if the query contains wildcards.
Rate Limits
'''




'''
class anotherField():
    (c1,c2,c3,c4,c5,c6,c7) = st.columns(7)
    with c1:
        connector = st.radio('And/or_',('AND', 'OR'))
    with c2:
        selected_field = st.selectbox(label = 'selected_field',options=fields)
        st.write('Published Date:')
    with c3:
        startdate = st.date_input('From',datetime.date(2010, 1, 1,),key='yo')
    with c4:
        starttime = st.time_input('Start Time', datetime.time(0, 00),key='yo_')
    with c5:
        enddate = st.date_input('to',datetime.date.today(),key='next')
    with c6:
        endtime = st.time_input('End Time', datetime.time(12, 59),key='new key')
    with c7:
        if st.button('Add to Query',key='Add_to_Query_again'):
            st.session_state.query = st.session_state.query+' '+connector+' '+ selected_field+':[ '+str(startdate)+'T00:00:00Z TO '+str(enddate)+'T00:00:00Z]'
'''
           
#mytest2 = anotherField()

'''
column_formatting = [radio_and_or,
                    select_field_input,
                    select_startdate,
                    select_starttime,
                    select_enddate,
                    select_endtime,
                    create_string]

cols = st.columns(len(column_formatting))
for i, x in enumerate(cols):
    with x:
        st.write(column_formatting[i]())

'''
'''
(c1,c2,c3,c4,c5,c6,c7) = st.columns(7)
with c1:
    connector_2 = st.radio('And/or_2',('AND', 'OR'))
with c2:
    datefield_2 = st.selectbox(label = 'datefield_2',options=fields,key='datefield_2')
    st.write('Published Date:')
with c3:
    startdate = st.date_input('From',datetime.date(2010, 1, 1,))
with c4:
    starttime = st.time_input('Start Time', datetime.time(0, 00))
with c5:
    enddate = st.date_input('to',datetime.date.today())
with c6:
    endtime = st.time_input('End Time', datetime.time(12, 59))
with c7:
    if st.button('Add to Query',key='Add_to_Query'):
        st.session_state.query = st.session_state.query+' '+connector+' '+ selected_field+':[ '+str(startdate)+'T00:00:00Z TO '+str(enddate)+'T00:00:00Z]'
'''
 

    
#if st.button('edit query',key='edit_query_button'):
#    st.write('adding this to query')
#    st.session_state.query = newQuery
#else:
#    st.write('click here')
    
    
'''
st.code(st.session_state.query)
if st.button('Call API',key='call_api_button'):
    st.session_state.myData = mb.Search(query=st.session_state.query)
    myDict = st.session_state.myData.parameters
    myDict['key']=f'***{myDict['key'][-4:]}'
    st.write(myDict)
    st.write(st.session_state.query)
    st.write(st.session_state.myData.totalResults)
    st.write(st.session_state.myData.articles[0])
else:
    st.stop()
    
'''

'''
c1,c2 = st.columns(2)
with c1:
    connector = st.radio('And/or',('AND', 'OR'))
with c2:
    selected_field = st.selectbox(label = 'Searchfield',options=fields,key='selected_field',on_change=on_change_expression)
    st.write('Search Field:')

'''
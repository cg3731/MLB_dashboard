from operator import index
from matplotlib import markers
#from regex import I
import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
from pprint import pprint

# code for elastic search, code from search_es.py
load_dotenv()
es_cloud_id = os.getenv("ES_CLOUD_ID")
es_api_id = os.getenv("ES_API_ID")
es_api_key = os.getenv("ES_API_KEY")

es = Elasticsearch(
    cloud_id=es_cloud_id,
    api_key=(es_api_id, es_api_key),  # API key ID and secret
)


plt.rc('font', family='Malgun Gothic')

BASE_PATH = '.'

st.set_page_config(
    page_title="Find An Expert",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Find An AI Expert')
st.markdown('---')


with st.sidebar:
    a = st.selectbox(
        'MENU', 
        (   
            'User guide',
            'Search Expert'
            
        )
    )
    
    st.markdown('---')

    st.markdown(
        '''
            <style>
                .css-1adrfps.e1fqkh3o2 {
                    width: 500px;
                }
                .css-1wf22gv.e1fqkh3o2 {
                    width: 500px;
                    margin-left: -500px;
                }
            </style>
        ''',
        unsafe_allow_html=True
    )

filter_options = st.sidebar.empty()



if a == 'User guide':
    st.markdown('''
        ## Info
        Scholary API와 Mongo DB 이용하여 서울대학교 전기 정보공학부 교수님들의 저자 정보와 출판물 정보를 수집하고 elastic search를 기반으로 검색을 지원 하는 페이지 
        
        ## How to use
        1) 조건 설정
            -  연도, 저널, 인용 수 등 검색 조건 설정

        2) 검색어 입력
            - 찾고자 하는 전문가와 관련된 기술 키워드 입력
        
        3) 결과 확인
            - DB에서 검색된 전문가 목록과 상세정보 출력
    ''')
    
if a== 'Search Expert':

    range_row = filter_options.slider(
        "연도 선택",
        2018, 2023, (2018, 2023)
    )
    st.markdown('''
                ### Please input your query for searching
                ''')
    search_query = st.text_input('input yor query', 'Autonomus driving')

    submit = st.sidebar.button('Search')

    if submit:
        keyword = search_query
        query = {    
            'query': {        
                'match': {            
                    'abstract': keyword
                }    
            }
        }
        column_list = ['title','name','pub_year','num_citations','abstract']
        df = pd.DataFrame(columns=column_list)
        # search for documents
        result = es.search(index='publications', body=query)
        for i in result["hits"]["hits"]:
            data = i['_source']
            new_row_data = {
                'title': data['title'],
                'name': data['name'],
                'pub_year':data['pub_year'],
                'num_citations':data['num_citations'],
                'abstract':data['abstract']
            }
            df.loc[len(df)]=new_row_data
        st.dataframe(df)


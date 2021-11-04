import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def remove_duplicates(df):

    df_clean = df.T.drop_duplicates().T
    df_clean = df_clean.dropna(axis=1, how='all')

    return df_clean
    
def tab3():
    st.title("Forecast triggers \n") 
    st.markdown('#')

    # Keys
    keys = ['a3','b3','c3','d3']

    df1 = pd.read_csv("Data/Metrics/Metrics_1_dcast.csv") 
    df1['Year'] = [str(round(i)) for i in df1.Year]
    df1[df1.columns[8:]] = df1[df1.columns[8:]].astype(pd.Int64Dtype())

    df2 = pd.read_csv("Data/Metrics/long.csv") 

    col1, col2 = st.columns([1,1]) 

    # Widgets
    windex = col1.multiselect("SPI Index", list(set(df1.Index)), [], key = keys[0])
    if not windex:
        windex = list(set(df1.Index))

    month = col1.multiselect("Month of forecast issue", list(set(df1.Month_of_issue)), [], key = keys[1])
    if not month:
        month = list(set(df1.Month_of_issue)) 



    district = col2.multiselect("District", list(set(df1.District)), [], key = keys[2])
    if not district:
        district = list(set(df1.District))

    category = col2.multiselect("Category", list(set(df1.Category)), [], key = keys[3])
    if not category:
        category = list(set(df1.Category))


    # Filter data
    df_filt1 = df1[df1['Index'].isin(windex)]
    df_filt1 = df_filt1[df_filt1['Month_of_issue'].isin(month)]
    df_filt1 = df_filt1[df_filt1['District'].isin(district)]
    df_filt1 = df_filt1[df_filt1['Category'].isin(category)]
    data1 = df_filt1.drop(['Index', 'Month_of_issue', 'District', 'Category'], axis = 1)
    data1 = remove_duplicates(data1)

    # Filter data
    df_filt2 = df2[df2['Index'].isin(windex)]
    df_filt2 = df_filt2[df_filt2['Month_of_issue'].isin(month)]
    df_filt2 = df_filt2[df_filt2['District'].isin(district)]
    df_filt2 = df_filt2[df_filt2['Category'].isin(category)]
    data2 = df_filt2.drop(['Index', 'Month_of_issue', 'District', 'Category', 'Years', 'Actual',  'Probability', 'Actual_Drought'], axis = 1)
    data2 = remove_duplicates(data2)

    # Display dataframes
    st.markdown('##')
    st.dataframe(data1)
    st.markdown('##')
    st.dataframe(data2)


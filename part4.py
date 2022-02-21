import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def tab4():
    st.title("SPI Outlook \n") 
    st.markdown('#')

    df2 = pd.read_csv("Data/Probabilities/SPI_probabilities.csv") 

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df2.District))
    pb_dist = []
    checkg2 = col1.checkbox(all_districts[0], True)
    checkh2 = col1.checkbox(all_districts[1], True)
    checki2 = col1.checkbox(all_districts[2], True)
    checkj2 = col1.checkbox(all_districts[3], True)
    checkl2 = col1.checkbox(all_districts[4], True)
    pb_districts = [all_districts[i] for i,d in enumerate([checkg2, checkh2, checki2, checkj2,checkl2]) if d]
    if len(pb_districts) == 0:
        pb_districts = all_districts
    pb_year = col1.multiselect("Year_of_issue", list(set(df2.Year_of_issue)), [])
    if not pb_year:
        pb_year = list(set(df2.Year_of_issue))
    pb_cate = col1.multiselect("Category", list(set(df2.Category)), [])
    if not pb_cate:
        pb_cate = list(set(df2.Category))
    pb_cate = sorted(pb_cate)
    pb_month = col1.multiselect("Month of forecast issue", list(set(df2.Month_of_issue)), [])
    if not pb_month:
        pb_month = list(set(df2.Month_of_issue))    

    # Filtering data
    data = df2[np.logical_and(df2['Year_of_issue'].isin(pb_year), df2['District'].isin(pb_districts))]
    data = data[np.logical_and(data['Category'].isin(pb_cate), data['Month_of_issue'].isin(pb_month))]
     
    # Displaying data  
    colors_dict = {'Leve':'yellow', 'Moderado':'orange', 'Severo':'red'}
    colors = [colors_dict[cate] for cate in pb_cate] 
    c = alt.Chart(data).mark_point(size = 150, filled = True).encode(
        alt.X('Index', title = '', scale=alt.Scale(zero=False), sort = ['SPI ON', 'SPI ND', 'SPI DJ', 'SPI JF', 'SPI FM','SPI MA', 'SPI OND', 'SPI NDJ', 'SPI DJF', 'SPI JFM','SPI FMA']),
        alt.Y('Probability',  title = 'Probability Values'),
        shape = 'District',
        color = alt.Color('Category', scale=alt.Scale(range=colors)),
        tooltip=['Index', 'District', 'Year_of_issue', 'Probability', 'Category', 'Month_of_issue']).properties(height=550)
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure(background='#F5F5F5').configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)

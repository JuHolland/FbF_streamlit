
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def tab2():

    st.title("Drought occurrence \n") 
    st.markdown('#')

    # Keys
    keys = ['a2','b2','c2','d2','e2','f2','g2','h2','i2','j2','k2','l2','m2','n2']
    

    # TABLE 1

    st.markdown('### Observations')
    df1 = pd.read_csv("Data/Observations/SPI_observations.csv") 

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df1.District))
    checka2 = col1.checkbox(all_districts[0], True, key=keys[0])
    checkb2 = col1.checkbox(all_districts[1], True, key=keys[1])
    checkc2 = col1.checkbox(all_districts[2], True, key=keys[2])
    checkd2 = col1.checkbox(all_districts[3], True, key=keys[3])
    ob_districts = [all_districts[i] for i,d in enumerate([checka2, checkb2, checkc2, checkd2]) if d]
    if len(ob_districts) == 0:
        ob_districts = all_districts
    ob_index = col1.multiselect("Index", list(set(df1.Index)), [], key = keys[4])
    if not ob_index:
        ob_index = list(set(df1.Index))
    ob_ylim = col1.slider('Value limits',float(df1.Value.min()), float(df1.Value.max()),
     (float(df1.Value.min()), float(df1.Value.max())), key = keys[5])

    # Filtering data
    data = df1[np.logical_and(df1['Index'].isin(ob_index), df1['District'].isin(ob_districts))]
    data = data[np.logical_and(data['Value'] > ob_ylim[0], data['Value'] < ob_ylim[1])]
     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Years', scale=alt.Scale(zero=False)),
        alt.Y('Value',  title = 'SPI Values', scale=alt.Scale(domain=ob_ylim)),
        color = 'District',
        tooltip=['Index', 'District', 'Years', 'Value'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)





    st.markdown('#')
    # TABLE 2

    st.markdown('### Forecasts')
    df2 = pd.read_csv("Data/Probabilities/SPI_probabilities.csv") 

    col1, col, col2 = st.columns([10, 1, 30]) 
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

    # Widgets
    col1.write('District')
    all_districts = list(set(df2.District))
    pb_dist = []
    checkg2 = col1.checkbox(all_districts[0], True, key=keys[6])
    checkh2 = col1.checkbox(all_districts[1], True, key=keys[7])
    checki2 = col1.checkbox(all_districts[2], True, key=keys[8])
    checkj2 = col1.checkbox(all_districts[3], True, key=keys[9])
    pb_districts = [all_districts[i] for i,d in enumerate([checkg2, checkh2, checki2, checkj2]) if d]
    if len(pb_districts) == 0:
        pb_districts = all_districts
    pb_index = subcol1.multiselect("Index", list(set(df2.Index)), [], key = keys[10])
    if not pb_index:
        pb_index = list(set(df2.Index))
    pb_cate = subcol2.multiselect("Category", list(set(df2.Category)), [], key = keys[11])
    if not pb_cate:
        pb_cate = list(set(df2.Category))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df2.Month_of_issue)), [], key = keys[12])
    if not pb_month:
        pb_month = list(set(df2.Month_of_issue))    
    pb_ylim = col1.slider('Value limits',float(df2.Probability.min()), float(df2.Probability.max()),
        (float(df2.Probability.min()), float(df2.Probability.max())), key = keys[13])

    # Filtering data
    data = df2[np.logical_and(df2['Index'].isin(pb_index), df2['District'].isin(pb_districts))]
    data = data[np.logical_and(data['Category'].isin(pb_cate), data['Month_of_issue'].isin(pb_month))]
    data = data[np.logical_and(data['Probability'] > pb_ylim[0], data['Probability'] < pb_ylim[1])]
     
    # Displaying data   
    c = alt.Chart(data).mark_circle(line = True).encode(
        alt.X('Year_of_issue', title = 'Years', scale=alt.Scale(zero=False)),
        alt.Y('Probability',  title = 'Probability Values', scale=alt.Scale(domain=pb_ylim)),
        color = 'District',
        tooltip=['Index', 'District', 'Year_of_issue', 'Probability', 'Category', 'Month_of_issue'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)

    



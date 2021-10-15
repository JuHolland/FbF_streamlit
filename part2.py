
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def main():

    st.title("Drought occurrence \n") 
    st.markdown('#')

    # TABLE 1
    df = pd.read_csv("Data/Observations/SPI_observations.csv") 

    st.markdown('### Observations')

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    ob_dist = []
    for i,d in enumerate(all_districts):
        a = col1.checkbox(d, True, key=i)
        ob_dist.append(a)
    districts = [all_districts[i] for i,d in enumerate(ob_dist) if d]
    if len(districts) == 0:
        districts = all_districts
    ob_index = col1.multiselect("Index", list(set(df.Index)), [], key = 'ob_id')
    if not ob_index:
        ob_index = list(set(df.Index))
    ob_ylim = col1.slider('Value limits',float(df.Value.min()), float(df.Value.max()),
     (float(df.Value.min()), float(df.Value.max())))

    # Filtering data
    data = df[np.logical_and(df['Index'].isin(ob_index), df['District'].isin(districts))]
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
    df = pd.read_csv("Data/Probabilities/SPI_probabilities.csv") 

    st.markdown('### Forecasts')

    col1, col, col2 = st.columns([10, 1, 30]) 
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    pb_dist = []
    for d in all_districts:
        b = col1.checkbox(d, True)
        pb_dist.append(b)
    districts = [all_districts[i] for i,d in enumerate(pb_dist) if d]
    if len(districts) == 0:
        districts = all_districts
    pb_index = subcol1.multiselect("Index", list(set(df.Index)), [], key = 'pb_id')
    if not pb_index:
        pb_index = list(set(df.Index))
    pb_cate = subcol2.multiselect("Category", list(set(df.Category)), [], key = 'pb_ct')
    if not pb_cate:
        pb_cate = list(set(df.Category))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df.Month_of_issue)), [], key = 'pb_mo')
    if not pb_month:
        pb_month = list(set(df.Month_of_issue))    
    pb_ylim = col1.slider('Value limits',float(df.Probability.min()), float(df.Probability.max()),
     (float(df.Probability.min()), float(df.Probability.max())))

    # Filtering data
    data = df[np.logical_and(df['Index'].isin(pb_index), df['District'].isin(districts))]
    data = data[np.logical_and(data['Category'].isin(pb_cate), data['Month_of_issue'].isin(pb_month))]
    data = data[np.logical_and(data['Probability'] > pb_ylim[0], data['Probability'] < pb_ylim[1])]
     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Year_of_issue', title = 'Years', scale=alt.Scale(zero=False)),
        alt.Y('Probability',  title = 'Probability Values', scale=alt.Scale(domain=pb_ylim)),
        color = 'District',
        tooltip=['Index', 'District', 'Year_of_issue', 'Probability'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)
    



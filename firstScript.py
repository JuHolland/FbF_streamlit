
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np


df = pd.read_csv("Data/Observations/SPI_observations.csv") 
df = df[df['District'].isin(['Guija', 'Changara'])]


st.title("Definition of drought occurrence \n") 
st.text("\n")
st.text("\n")
st.text("\n")



col1, col2 = st.columns([1,3]) 

# Widgets
col1.write('District')
all_districts = list(set(df.District))
dist1 = col1.checkbox(all_districts[0], True)
dist2 = col1.checkbox(all_districts[1], True)
districts = [all_districts[i] for i,d in enumerate([dist1, dist2]) if d]
index = col1.multiselect("Index", list(set(df.Index)), [])
if not index:
    index = list(set(df.Index))
ylim = col1.slider('Value limits',float(df.Value.min()), float(df.Value.max()), (float(df.Value.min()), float(df.Value.max())))

# Filtering data
data = df[np.logical_and(df['Index'].isin(index), df['District'].isin(districts))]
data = data[np.logical_and(data['Value'] > ylim[0], data['Value'] < ylim[1])]
 
# Displaying data   
c = alt.Chart(data).mark_circle().encode(
    alt.X('Years', scale=alt.Scale(zero=False)),
    alt.Y('Value',  scale=alt.Scale(domain=ylim)),
    color = 'District',
    tooltip=['Index', 'District', 'Years', 'Value'])
line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

col2.altair_chart(layers, use_container_width=True)

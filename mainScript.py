import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

import part1
import part2
import part3
import SessionState

def main():

    st.set_page_config(layout='wide')

    # Initialisation
    df1 = pd.read_csv("Data/Observations/SPI_observations.csv") 
    df2 = pd.read_csv("Data/Probabilities/SPI_probabilities.csv")
    ss = SessionState.get(a1 = True,b1 = True,c1 = True,d1 = True,
                        e1 = [],
                        f1 = True,g1 = False,h1 = False,i1 = False,
                        j1 = [],k1 = [],l1 = [],
                        a2 = True,b2 = True,c2 = True,d2 = True,
                        e2 = [],f2 = (float(df1.Value.min()), float(df1.Value.max())),
                        g2 = True,h2 = True,i2 = True,j2 = True,
                        k2 = [],l2 = [],m2=[],n2=(float(df2.Probability.min()), float(df2.Probability.max())),
                        a3 = [], b3 = [], c3 = [], d3 = [])


    with st.sidebar:

        st.title("Navigation \n") 
        select_part = st.sidebar.radio('Go to', ('Part 1', 'Part 2', 'Part 3'))

        st.markdown('#')
        st.title("Data \n")
        st.info("The datasets are available on GitHub at the following [link](https://github.com/JuHolland/Dashboard_FbF)")



    if select_part == 'Part 1':
        part1.main(ss)
    elif select_part == 'Part 2':
        part2.main(ss)
    elif select_part == 'Part 3':
        part3.main(ss)




if __name__ == "__main__":
    main()


def part1():
    st.title("Rainfall \n") 
    st.markdown('#')

    # Initialisation
    st.write(st.session_state)
    keys = ['a1','b1','c1','d1','e1','f1','g1','h1','i1','j1','k1','l1']

    # TABLE 1
    df = pd.read_csv("Data/Rainfall CHIRPS/CHIRPS_observations.csv") 

    st.markdown('### Observations')

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    ob_dist = []
    for i,d in enumerate(all_districts):
        a = col1.checkbox(d, True, key=keys[i])
        ob_dist.append(a)
    districts = [all_districts[i] for i,d in enumerate(ob_dist) if d]
    if len(districts) == 0:
        districts = all_districts
    ob_accumulation = col1.multiselect("Accumulation", list(set(df.Accumulation)), key = keys[4])
    if not ob_accumulation:
        ob_accumulation = list(set(df.Accumulation))

    # Filtering data
    data = df[np.logical_and(df['Accumulation'].isin(ob_accumulation), df['District'].isin(districts))]
     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Years', scale=alt.Scale(zero=False)),
        alt.Y('Value',  title = 'Precipitation (mm)'),
        color = 'District',
        tooltip=['Years','Accumulation','District','Value'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)


    st.markdown('### Forecasts')

    df = pd.read_csv("Data/Ensemble Rainfall/ECMWF_rainfall.csv")

    col1, col, col2 = st.columns([10, 1, 30]) 
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    pb_dist = []
    for i,d in enumerate(all_districts):
        b = col1.checkbox(d, False, key = keys[i+5])
        pb_dist.append(b)
    districts = [all_districts[i] for i,d in enumerate(pb_dist) if d]
    #if len(districts) == 0:
        #districts = all_districts
    pb_accumulation = subcol1.multiselect("Acumulation", list(set(df.Acumulation)), [], key = keys[9])
    if not pb_accumulation:
        pb_accumulation = list(set(df.Acumulation))
    pb_ensemble = subcol2.multiselect("Ensemble Member", list(set(df.Ensemble_number)), [], key = keys[10])
    if not pb_ensemble:
        pb_ensemble = list(set(df.Ensemble_number))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df.Forecast_month)), [], key = keys[11])
    if not pb_month:
        pb_month = list(set(df.Forecast_month))    

    # Filtering data
    data = df[np.logical_and(df['Acumulation'].isin(pb_accumulation), df['District'].isin(districts))]
    data = data[np.logical_and(data['Ensemble_number'].isin(pb_ensemble), data['Forecast_month'].isin(pb_month))]

     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Year', title = 'Years', scale=alt.Scale(zero=False)),
        alt.Y('Value',  title = 'Precipitation (mm)'),
        color = 'District',
        tooltip=['Year','Ensemble_number', 'Acumulation', 'Value', 'District', 'Forecast_month'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)
     
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
                        f1 = True,g1 = True,h1 = True,i1 = True,
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

        st.markdown('###')
        st.markdown('###')
        reset = st.sidebar.button('Reset')


    if select_part == 'Part 1':
        if reset == True:
            part1.reset(ss)
            part1.tab1(ss)
        else:
            part1.tab1(ss)
    elif select_part == 'Part 2':
        if reset == True:
            part2.reset(ss, (float(df1.Value.min()), float(df1.Value.max())), (float(df2.Probability.min()), float(df2.Probability.max())))
            part2.tab2(ss)
        else:
            part2.tab2(ss)
    elif select_part == 'Part 3':
        if reset == True:
            part3.reset(ss)
            part3.tab3(ss)
        else:
            part3.tab3(ss)



if __name__ == "__main__":
    main()
     
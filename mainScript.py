import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

import part1
import part2
import part3

st.set_page_config(layout='wide')

with st.sidebar:

    st.title("Navigation \n") 
    select_part = st.sidebar.radio('Go to', ('Part 1', 'Part 2', 'Part 3'))

    st.markdown('#')
    st.title("Data \n")
    st.info("The datasets are available on GitHub at the following [link](https://github.com/JuHolland/Dashboard_FbF)")


if select_part == 'Part 1':
    part1.main()
elif select_part == 'Part 2':
    part2.main()
elif select_part == 'Part 3':
    part3.main()
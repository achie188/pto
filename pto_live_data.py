import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
from PIL import Image
import sys
import numpy as np

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/4CC/gkl')

from inputs.pull_sheets import import_gsheet
from inputs.race_sim import race_sim
from inputs.info import info

location = os.getcwd()

live_race = race_sim()
live_race = live_race.drop(columns=['Time_secs', 'Distance', 'Kart #'])

champ_standings = import_gsheet("Championship")
champ_standings['Name'] = champ_standings['Name'].replace('', np.nan)
champ_standings = champ_standings.dropna(subset=['Name'])
champ_standings = champ_standings.sort_values(by='Total', ascending=False)

fastest_laps = import_gsheet("Fastest Laps")
fastest_laps['Name'] = fastest_laps['Name'].replace('', np.nan)
fastest_laps = fastest_laps.dropna(subset=['Name'])
fastest_laps = fastest_laps.sort_values(by='Time', ascending=True)

gkl_logo = Image.open(location + '/inputs/images/gkl_logo.png')
rob = Image.open(location + '/inputs/images/rob.png')
ross = Image.open(location + '/inputs/images/ross.png')
antonio = Image.open(location + '/inputs/images/antonio.png')
paul = Image.open(location + '/inputs/images/paul.png')
silverstone_img = Image.open(location + '/inputs/images/silverstone.png')
# bambino_img = Image.open(location + '/inputs/images/bambino.png')
# cadet_img = Image.open(location + '/inputs/images/cadet.png')
# junior_img = Image.open(location + '/inputs/images/junior.png')


about, silverstone_info, bambino_text, cadet_text, junior_text, champ_info = info()


# Set up Streamlit app
st.set_page_config(
    page_title = "Global Karting League",
    layout = "wide"
)

st_autorefresh(30 * 1000, limit=1000)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.image(gkl_logo, width = 150)

st.subheader("Welcome to the Global Karting League 2024!")

st.write("The following tabs show live data from GKL UK 2024. Select a tab below 👇")

tab1, tab2, tab3 = st.tabs(["Current Race", "Championship Standings", "About GKL"])

###### CURRENT RACE INFO #####
with tab1:
    tab11, tab12, tab13 = st.tabs(["LIVE NOW", "Fastest Laps", "About Silverstone"])
    
    #Live data tab
    with tab11:
        st.subheader("GKL UK Grand Final - Silverstone")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(live_race, hide_index=True)
        with col2:
            st.markdown(champ_info)

    with tab12:
        st.subheader("Fastest Laps")
        st.dataframe(fastest_laps, height = int(35.2*(fastest_laps.shape[0]+1)), hide_index=True)

    with tab13:
        st.subheader("About Silverstone")
        col11, col12 = st.columns([2,2])

        with col11:           
            st.markdown(silverstone_info)
            st.image(silverstone_img, width = 800)



###### CHAMPIONSHIP RESULTS #####
with tab2:
    tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs(["Overall", "Silverstone", "Edinburgh", "Whilton Mill", "Shenington", "Hooton Park"])

    with tab11:
        st.subheader(f"Overall Standings")
        st.dataframe(champ_standings, hide_index=True)

    with tab12:
        st.subheader(f"GKL Grand Final - Silverstone")
        st.dataframe(live_race, hide_index=True)

    with tab13:
        st.subheader(f"Edinburgh")
        st.dataframe(live_race, hide_index=True)

    with tab14:
        st.subheader(f"Whilton Mill")
        st.dataframe(live_race, hide_index=True)

    with tab15:
        st.subheader(f"Shenington")
        st.dataframe(live_race, hide_index=True)

    with tab16:
        st.subheader(f"Hooton Park")
        st.dataframe(live_race, hide_index=True)


###### ABOUT #####
with tab3:
    col1, col2 = st.columns(2)
    
    with col1: 
        st.subheader('About Global Karting League')
        st.markdown(about)
        with st.expander("Bambino Kart"):
            st.markdown(bambino_text)  
        with st.expander("Cadet Kart"):
            st.markdown(cadet_text)       
        with st.expander("Junior Kart"):
            st.markdown(junior_text)

    with col2:
        st.subheader('The Team')
        st.markdown('Look how handsome we are')

        col11, col12 = st.columns(2)
        with col11: 
            st.image(rob, width = 300)
            st.image(antonio, width = 300)
        with col12: 
            st.image(paul, width = 300)
            st.image(ross, width = 300)
        
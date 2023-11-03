import streamlit as st
import plotly.exceptions as px
from Yrkesprogram import show as show_yrkesprogram
from Gymnasieelever import show as show_gymnasieelever
from Forskolebarn import show as show_forskolebarn
from Gymnasieutbildad import show as show_gymnasieutbildad
from Etableradeungdomar import show as show_etableradeungdomar
from Aldreomsorgbehandling import show as show_Aldreomsorgbehandling
from Aldreomsorgasikter import show as show_Aldreomsorgasikter
from Aldreomsorgtrygghet import show as show_Aldreomsorgtrygghet
from Sarskiltaldreomsorgbehandling import show as show_Sarskiltaldreomsorgbehandling
from Sarskiltaldreomsorgasikter import show as show_Sarskiltaldreomsorgasikter
from Sarskiltaldreomsorgtrygghet import show as show_Sarskiltaldreomsorgtrygghet

st.set_page_config(page_title="Falkenberg Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")


with open('styles.css', 'r') as css_file:
    css_text = css_file.read()
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)


st.title(":bar_chart: Falkenberg Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True) 


# Define your list of navigation items
st.sidebar.title("Välj graf")
navigation_utbildning = st.sidebar.selectbox('Utbildning',["Välj","Behorighet yrkesprogram", "Examinerade gymnasieelev", "Förskolebarn", "Gymnasieutbildad", "Etablerade ungdomar"])


if navigation_utbildning == "Behorighet yrkesprogram":
    show_yrkesprogram()
elif navigation_utbildning == "Examinerade gymnasieelev":
    show_gymnasieelever()
elif navigation_utbildning == "Förskolebarn":
     show_forskolebarn()
elif navigation_utbildning == "Gymnasieutbildad":
    show_gymnasieutbildad()
elif navigation_utbildning == "Etablerade ungdomar":
    show_etableradeungdomar()

navigation=["Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter", "Särskilt äldreomsorg trygghet"]
navigation_soc = st.sidebar.multiselect("soc", navigation)
col1, col2 = st.columns(2) 
with col1:
  
     if "Hemtjänst äldreomsorg behandling" in navigation_soc:
        show_Aldreomsorgbehandling()
     if "Hemtjänst äldreomsorg trygghet" in navigation_soc:
        show_Aldreomsorgtrygghet()
     if "Särskilt äldreomsorg åsikter" in navigation_soc:
        show_Sarskiltaldreomsorgasikter()
with col2:    
   if "Hemtjänst äldreomsorg åsikter" in navigation_soc: 
        show_Aldreomsorgasikter()
   if "Särskilt Äldreomsorg Behandling" in navigation_soc:
        show_Sarskiltaldreomsorgbehandling()
   if  "Särskilt äldreomsorg trygghet" in navigation_soc:
        show_Sarskiltaldreomsorgtrygghet()


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
 
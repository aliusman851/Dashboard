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


st.title(":bar_chart: Falkenberg Dasboard")
st.markdown("##") 
 

# Define your list of navigation items
st.sidebar.title("Navigation")
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

navigation_soc = st.sidebar.selectbox('Soc',["Välj","Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter", "Särskilt äldreomsorg trygghet"])

if navigation_soc == "Hemtjänst äldreomsorg behandling":
    show_Aldreomsorgbehandling()
elif navigation_soc == "Hemtjänst äldreomsorg åsikter":
    show_Aldreomsorgasikter()
elif navigation_soc == "Hemtjänst äldreomsorg trygghet":
    show_Aldreomsorgtrygghet()
elif navigation_soc == "Särskilt Äldreomsorg Behandling":
    show_Sarskiltaldreomsorgbehandling()
    
elif navigation_soc == "Särskilt äldreomsorg åsikter":
    show_Sarskiltaldreomsorgasikter()
elif navigation_soc == "Särskilt äldreomsorg trygghet":
       show_Sarskiltaldreomsorgtrygghet()
    
 
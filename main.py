import streamlit as st
import plotly.exceptions as px
from Utbildning.Yrkesprogram import show as show_yrkesprogram
#from Charts.Barchart import show as show_Barchart
from Utbildning.Gymnasieelever import show as show_gymnasieelever
from Utbildning.Forskolebarn import show as show_forskolebarn
from Utbildning.Gymnasieutbildad import show as show_gymnasieutbildad
from Utbildning.Etableradeungdomar import show as show_etableradeungdomar
from Soc.Aldreomsorgasikter import show as show_Aldreomsorgasikter
from Soc.Aldreomsorgbehandling import show as show_Aldreomsorgbehandling
from Soc.Aldreomsorgtrygghet import show as show_Aldreomsorgtrygghet
from Soc.Sarskiltaldreomsorgbehandling import show as show_Sarskiltaldreomsorgbehandling
from Soc.Sarskiltaldreomsorgasikter import show as show_Sarskiltaldreomsorgasikter
from Soc.Sarskiltaldreomsorgtrygghet import show as show_Sarskiltaldreomsorgtrygghet

st.set_page_config(page_title="Falkenberg Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered",
                   )


with open('styles.css', 'r') as css_file:
    css_text = css_file.read()
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)


st.title(":bar_chart: Falkenberg Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True) 


# Define your list of navigation items
st.sidebar.title("Navigation")
options = ["Välj","Behorighet yrkesprogram", "Examinerade gymnasieelev", "Förskolebarn", "Gymnasieutbildad", "Etablerade ungdomar"]
navigation_utbildning = st.sidebar.selectbox('Utbildning', options)


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

#option =  ["Välj", "Bar chart", "Line chart", "Pie chart"]
#navigation_charts = st.sidebar.selectbox("Graf", option)   
#if  navigation_charts == "Pie chart" and navigation_utbildning == "Behorighet yrkesprogram":
 #        show_Barchart()"""

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

Navigation = st.sidebar.radio("Soc", ["Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter", "Särskilt äldreomsorg trygghet"])
if Navigation == "Hemtjänst äldreomsorg behandling":
        show_Aldreomsorgbehandling()
elif Navigation == "Hemtjänst äldreomsorg trygghet":
        show_Aldreomsorgtrygghet()
elif Navigation == "Särskilt äldreomsorg åsikter":
        show_Sarskiltaldreomsorgasikter()   
elif Navigation == "Hemtjänst äldreomsorg åsikter": 
        show_Aldreomsorgasikter()
elif Navigation == "Särskilt Äldreomsorg Behandling":
        show_Sarskiltaldreomsorgbehandling()
elif Navigation == "Särskilt äldreomsorg trygghet":
        show_Sarskiltaldreomsorgtrygghet()

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                
    }}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
 
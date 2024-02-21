import streamlit as st
import plotly.exceptions as px
from Utbildning.Yrkesprogram import show as show_yrkesprogram
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
from Jamforelsekommuner.Kvalitetsindex import show as show_Kvalitetsindex
from Jamforelsekommuner.SarskiltboendeIndex import show as show_SarskiltboendeIndex
from Jamforelsekommuner.ForskolebarnIndex import show as show_ForskolebarnIndex

st.set_page_config(page_title="Falkenberg Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered",
                   )
st.markdown(
    """
    <style>
    @media (max-width: 600px) {
       body {
        font-size: 14px; /* Decrease font size for smaller screens */
    }
    }
    </style>
    """,
    unsafe_allow_html=True
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

# Define your list of navigation items
st.sidebar.title("")
navigation = ["Välj","Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter","Särskilt äldreomsorg trygghet"]
navigation_SOC = st.sidebar.selectbox('SOC', navigation)

if navigation_SOC == "Hemtjänst äldreomsorg behandling" :
        show_Aldreomsorgbehandling()
elif navigation_SOC == "Hemtjänst äldreomsorg trygghet":
        show_Aldreomsorgtrygghet()
elif navigation_SOC == "Hemtjänst äldreomsorg åsikter": 
        show_Aldreomsorgasikter()
elif navigation_SOC == "Särskilt Äldreomsorg Behandling":
        show_Sarskiltaldreomsorgbehandling()
elif  navigation_SOC == "Särskilt äldreomsorg trygghet" :
        show_Sarskiltaldreomsorgtrygghet()

elif navigation_SOC == "Särskilt äldreomsorg åsikter":
        show_Sarskiltaldreomsorgasikter()

st.sidebar.title("Kommuner Jämförelse ")
navigation_options = ["Välj","Kvalitetsindex LSS", "Hemtjänst/särskilt boende)Index", "ForskolebarnIndex", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter","Särskilt äldreomsorg trygghet"]
navigation_Socio = st.sidebar.selectbox('socioekonomi', navigation_options)
if navigation_Socio == "Kvalitetsindex LSS" :
        show_Kvalitetsindex()
elif navigation_Socio == "Hemtjänst/särskilt boende)Index" : 
        show_SarskiltboendeIndex()
elif navigation_Socio == "ForskolebarnIndex" : 
        show_ForskolebarnIndex()        
        
        


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                
    }}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
 
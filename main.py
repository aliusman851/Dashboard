import streamlit as st
from Yrkesprogram import show as show_yrkesprogram
from Gymnasieelever import show as show_gymnasieelever
from Forskolebarn import show as show_forskolebarn
from Gymnasieutbildad import show as show_gymnasieutbildad
from Etableradeungdomar import show as show_etableradeungdomar

with open('styles.css', 'r') as css_file:
    css_text = css_file.read()
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)

st.markdown(f'<h3 class="heading">Falkenberg Dashboard</h3>', unsafe_allow_html=True)    
# Define your list of navigation items
st.sidebar.title("Navigation")
navigation_utbildning = st.sidebar.selectbox('Utbildning',["Behorighet yrkesprogram", "Examinerade gymnasieelev", "Förskolebarn", "Gymnasieutbildad", "Etablerade ungdomar"])

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

# Create a list element for each navigation item
navigation_soc = st.sidebar.selectbox('Soc',["Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter", "Särskilt äldreomsorg trygghet"])

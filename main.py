import streamlit as st
from streamlit_option_menu import option_menu
import base64
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
from Jamforelsekommuner.Gymnasieelever import show as show_Gymnasieelever
from Jamforelsekommuner.Elevmeritavvikelse import show as show_Elevmeritavvikelse
from Jamforelsekommuner.Yrkesprogrambehoriga import show as show_Yrkesprogrambehoriga
from Jamforelsekommuner.Ekonomiskstandard import show as show_Ekonomiskstandard
from Jamforelsekommuner.Avsaknadtillit import show as show_Avsaknadtillit
from Jamforelsekommuner.Skoltrygghet import show as show_Skoltrygghet
from Jamforelsekommuner.Trangboddhet import show as show_Trangboddhet
from Jamforelsekommuner.Deltagartillfallen import show as show_Deltagartillfallen
from Jamforelsekommuner.InvanareArbstud import show as show_InvanareArbstud

st.set_page_config(page_title="Falkenberg Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered",
                   )

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)   
# Load the CSS for responsiveness
load_css("styles.css")

def encode_image(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_str = base64.b64encode(img_bytes).decode()
    return img_str  
img1= encode_image("images/chart1.png")
img2= encode_image("images/chart2.png")
img3= encode_image("images/chart3.png")
fbg= encode_image("images/fbg.jpg")
header_with_image = f"""
                    <header style="background-image: url('data:image/jpeg;base64,{fbg}');
                                   background-size: cover;
                                   background-position: top;
                                   height: 250px;
                                   width:1580px; 
                                   margin-left: -450px;
                                   position: sticky;
                                   top: 0;
                                   right: 0; ">
                    </header>
                    """

st.markdown(header_with_image, unsafe_allow_html=True)

st.title(":bar_chart: Falkenberg Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True) 
st.header('En sida med visualiseringar av data för olika områden') 



page_utbildning = { 
    "Elever i åk 9 som är behöriga till yrkesprogram kommunala (modellberäknat värde), andel(%)": show_yrkesprogram,
    "Gymnasieelever med examen inom 3 år, kommunala skolor, andel(%), avvikelse från modellberäknat värde ": show_gymnasieelever,
    "Barn i kommunala förskola, andel(%) av inskrivna barn": show_forskolebarn,
    "Invånare 25-64 år med eftergymnasial utbildning, andel(%) ": show_gymnasieutbildad,
    
    
}

page_Soc = {
    
    "Brukarbedömning hemtjänst äldreomsorg-bemötande, andel(%) ":show_Aldreomsorgbehandling, 
    "Brukarbedömning hemtjänst äldreomsorg-hänsyn till åsikter och önskemål, andel(%) ":show_Aldreomsorgasikter, 
    "Brukarbedömning hemtjänst äldreomsorg-trygghet, andel(%) ":show_Aldreomsorgtrygghet, 
    "Brukarbedömning särskilt boende äldreomsorg-bemötande, andel(%) ": show_Sarskiltaldreomsorgbehandling, 
    "Brukarbedömning särskilt boende äldreomsorg-hänsyn till åsikter och önskemål, andel(%) ":show_Sarskiltaldreomsorgasikter,
    "Brukarbedömning särskilt boende äldreomsorg-trygghet, andel(%) ":show_Sarskiltaldreomsorgtrygghet
    
    
}
page_socioekonomi = {
   
    "Kvalitetsindex LSS":show_Kvalitetsindex, 
    "Index bemötande, förtroende, trygghet (hemtjänst/särskilt boende)":show_SarskiltboendeIndex,
    "Barn 1-5 år inskrivna i förskola, andel (%)":show_ForskolebarnIndex,
    "Gymnasieelever med examen inom 4 år, hemkommun, andel (%)":show_Gymnasieelever,
    "Elever i åk. 9 genomsnittligt meritvärde avvikelse från modellberäknat värde kommunala skolor, meritvärdespoäng":show_Elevmeritavvikelse, 
    "Elever i åk 9 som är behöriga till yrkesprogram, hemkommun, andel (%)":show_Yrkesprogrambehoriga, 
    "Invånare, 0–19 år, med låg ekonomisk standard, andel (%)":show_Ekonomiskstandard,
    "Invånare 16-84 år med avsaknad av tillit till andra, andel (%)":show_Avsaknadtillit, 
    "Elever i åk 8: Känner du dig trygg i skolan? Andel som svarat, Helt och hållet eller Till stor del, (%)":show_Skoltrygghet,
    "Trångboddhet i flerbostadshus, enligt norm 2, andel (%)":show_Trangboddhet,
    "Deltagartillfällen i idrottsföreningar, antal/inv 7–25 år":show_Deltagartillfallen,
    "Invånare 16-24 år som varken arbetar eller studerar, andel (%)":show_InvanareArbstud
}



with st.sidebar:
    selected = option_menu(
        menu_title="Huvudmenyn",
        options = ['Infosida','Barn och utbildning', 'Omsorg och hjälp','Jämförnyckeltal'],
        icons=['bi-info','bi-backpack4-fill','heart-fill','bi-graph-up-arrow'],
        default_index=0,
    )
    

if selected == 'Barn och utbildning':
    st.markdown("<h2 class='sidebar-title'>Barn och utbildning</h2>", unsafe_allow_html=True)
    navigation_utbildning = st.selectbox('Välj nyckeltal', list(page_utbildning.keys())) 
    #if  navigation_utbildning != "Välj eller sök":
    page_utbildning[navigation_utbildning]() 
if selected == 'Omsorg och hjälp':
    st.markdown("<h2 class='sidebar-title'>Omsorg och hjälp</h2>", unsafe_allow_html=True)
    navigation_Soc = st.selectbox('Välj nyckeltal', list(page_Soc.keys()))
    #if navigation_Soc != "Välj eller sök":
    page_Soc[navigation_Soc]()         
if selected == 'Jämförnyckeltal':
    st.markdown("<h2 class='sidebar-title'>Här kan du jämföra nyckeltal med andra kommuner.</h>", unsafe_allow_html=True)
    navigation_socioekonomi = st.selectbox('Välj nyckeltal', list(page_socioekonomi.keys())) 
    #if navigation_socioekonomi !="Välj eller sök":
    page_socioekonomi[navigation_socioekonomi]() 
   


# Display the image if no option is selected
if selected =='Infosida':
    
    st.sidebar.empty()
   
    col1, col2= st.columns([8,4])  
    
    with col1:
         html_code_col1 = f"""
        <div id="moving-image-col1">
            <img src="data:image/png;base64,{img1}" >
            <img src="data:image/png;base64,{img2}" >
            
         </div>
         """
         st.write(html_code_col1, unsafe_allow_html=True)
    with col2:
         html_code_col2 = f"""
        <div id="moving-image-col2">
            <img src="data:image/png;base64,{img3}" >
            
            
         </div>
         
          """     
         st.write(html_code_col2, unsafe_allow_html=True)     
   


 
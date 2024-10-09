import streamlit as st
import plotly.exceptions as px
from PIL import Image
import io
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
def encode_image(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_str = base64.b64encode(img_bytes).decode()
    return img_str  
img1= encode_image("C:/Users/Ali usman/Dashboard/Image/chart1.png")
img2= encode_image("C:/Users/Ali usman/Dashboard/Image/chart2.png")
img3= encode_image("C:/Users/Ali usman/Dashboard/Image/chart3.png")
img4= encode_image("C:/Users/Ali usman/Dashboard/Image/sunburst.png")
img5= encode_image("C:/Users/Ali usman/Dashboard/Image/barchart.png")
img6= encode_image("C:/Users/Ali usman/Dashboard/Image/linechart.png")
img7= encode_image("C:/Users/Ali usman/Dashboard/Image/img7.png")
fbg= encode_image("C:/Users/Ali usman/Dashboard/Image/fbg.jpg")

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

with open('styles.css', 'r') as css_file:
    css_text = css_file.read()
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)


st.title(":bar_chart: Falkenberg Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True) 
st.header('En sida med visualiseringar av data för olika områden') 
option_selected= False

page_utbildning = {
    "Välj eller sök":"",  
    "Behorighet yrkesprogram": show_yrkesprogram,
    "Examinerade gymnasieelev": show_gymnasieelever,
    "Förskolebarn": show_forskolebarn,
    "Gymnasieutbildad": show_gymnasieutbildad,
    "Etablerade ungdomar": show_etableradeungdomar,
    
}
page_Soc = {
    
    "Välj eller sök":"",
    "Hemtjänst äldreomsorg behandling":show_Aldreomsorgbehandling, 
    "Hemtjänst äldreomsorg åsikter":show_Aldreomsorgasikter, 
    "Hemtjänst äldreomsorg trygghet":show_Aldreomsorgtrygghet, 
    "Särskilt Äldreomsorg Behandling": show_Sarskiltaldreomsorgbehandling, 
    "Särskilt äldreomsorg åsikter":show_Sarskiltaldreomsorgasikter,
    "Särskilt äldreomsorg trygghet":show_Sarskiltaldreomsorgtrygghet
    
    
}
page_socioekonomi = {
   
    "Välj eller sök":"",
    "Kvalitetsindex LSS":show_Kvalitetsindex, 
    "Hemtjänst/särskilt boende)Index":show_SarskiltboendeIndex,
    "Barn inskrivna i förskola":show_ForskolebarnIndex,
    "Gymnasieelever med examen inom 4 år":show_Gymnasieelever,
    "Elever genomsnittligt meritvärde avvikelse":show_Elevmeritavvikelse, 
    "Elever behöriga till yrkesprogram, hemkommun":show_Yrkesprogrambehoriga, 
    "Invånare med låg ekonomisk standard(0-19år)":show_Ekonomiskstandard,
    "Invånare 16-84 år med avsaknad av tillit till andra":show_Avsaknadtillit, 
    "Känner du dig trygg i skolan":show_Skoltrygghet,
    "Trångboddhet i flerbostadshus":show_Trangboddhet,
    "Deltagartillfällen i idrottsföreningar":show_Deltagartillfallen,
    "Invånare 16-24 år som varken arbetar eller studerar":show_InvanareArbstud
}
st.sidebar.title("Välj nyckeltal")
st.sidebar.markdown(
    """
    <style>
    .sidebar-title {
        font-weight: bold;
        font-size: 15px;
        margin: 0; /* Remove margin around title */
        padding: 0; /* Remove padding around title */
    }
    .css-1r7x1e8 {  /* Streamlit selectbox container class */
        margin: 0; /* Remove margin around selectbox */
        padding: 0; /* Remove padding around selectbox */
    }
    .st-ak div {  /* Adjust class names as needed */
        cursor: pointer; /* Change cursor to pointer when hovering */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h4 class='sidebar-title'>Barn och utbildning</h4>", unsafe_allow_html=True)
navigation_utbildning = st.sidebar.selectbox('', list(page_utbildning.keys()))
if navigation_utbildning != "Välj eller sök":
    page_utbildning[navigation_utbildning]()


    
st.sidebar.title("")
st.sidebar.markdown("<h4 class='sidebar-title'>Omsorg och hjälp</h4>", unsafe_allow_html=True)
navigation_Soc = st.sidebar.selectbox('', list(page_Soc.keys()))
if navigation_Soc != "Välj eller sök":
    page_Soc[navigation_Soc]()


st.sidebar.title("Jämför nyckeltal")
st.sidebar.markdown("<h4 class='sidebar-title'>Här kan du jämföra nyckeltal med andra kommuner.</h4>", unsafe_allow_html=True)
navigation_socioekonomi = st.sidebar.selectbox('', list(page_socioekonomi.keys()))
if navigation_socioekonomi !="Välj eller sök":
    page_socioekonomi[navigation_socioekonomi]()

if (navigation_utbildning != "Välj eller sök" or 
    navigation_Soc != "Välj eller sök" or 
    navigation_socioekonomi != "Välj eller sök"):
    option_selected = True 

if option_selected:
    st.sidebar.empty()

# Display the image if no option is selected
if not option_selected:
    st.sidebar.empty()
    col1, col2 = st.columns([8,4])  
    
    with col1:
         html_code_col1 = f"""
        <div id="moving-image-col1" style="position: absolute; top: 50%; left: 50%;  transform: translateX(-50%);  ">
            <img src="data:image/png;base64,{img1}" style="width: 250px; height: auto;">
            <img src="data:image/png;base64,{img2}" style="width: 250px; height: auto;">
            
         </div>
         <style>
             @keyframes moveContinuouslycolone {{
                0% {{ transform: translateX(-50%); }}
                50% {{ transform: translateX(-55%); }}
                100% {{ transform: translateX(-50%); }}
             }}
             #moving-image-col1 img {{
                 animation: moveContinuouslycolone 5s linear infinite;
              }}
         </style>
          """   
         st.write(html_code_col1, unsafe_allow_html=True)
    with col2:
         html_code_col2 = f"""
        <div id="moving-image-col2" style="position: absolute; top: 50%; left: 50%;  transform: translateX(-50%,-50%); ">
            <img src="data:image/png;base64,{img3}" style="width: auto; height: auto; max-width: 450px; max-height: 400px; ">
            
            
         </div>
         <<style>
             @keyframes moveContinuouslycoltwo {{
                0% {{ transform: translateX(-50%); }}
                50% {{ transform: translateX(-55%); }}
                100% {{ transform: translateX(-50%); }}
             }}
             #moving-image-col2 img {{
                 animation: moveContinuouslycoltwo 5s linear infinite;
              }}
         </style>
          """     
         st.write(html_code_col2, unsafe_allow_html=True)     
   




footer_with_image = f"""
                  <footer>
                      <div id="moving-image-footer" style="position: fixed; top: 83%; left: 50%; transform: translateX(-50%);">
                         <img src="data:image/png;base64,{img1}" style="width: 250px; height: 100px; opacity: 1;">
                         <img src="data:image/png;base64,{img2}" style="width: 250px; height: 100px; opacity: 0; margin-left: -50px;">
                         <img src="data:image/png;base64,{img5}" style="width: 250px; height: 100px; opacity: 0; margin-left: -100px; ">
                         <img src="data:image/png;base64,{img7}" style="width: 250px; height: 200px; opacity: 0; margin-left: -150px; ">
                      </div>
                      <style>
                         @keyframes moveContinuously {{
                            0% {{ transform: translateX(-350%);  }}
                            100% {{ transform: translateX(550%); opacity: 50; }}
                        }}
                        #moving-image-footer img {{
                            animation: moveContinuously 24s linear infinite;
                        }}
                        #moving-image-footer img:nth-child(1) {{ animation-delay: 0s; }}
                        #moving-image-footer img:nth-child(2) {{ animation-delay: 8s; }}
                        #moving-image-footer img:nth-child(3) {{ animation-delay: 16s; }}
                        #moving-image-footer img:nth-child(4) {{ animation-delay: 24s; }}
                      </style>
                   </footer>
                 """
    
       
                 
st.markdown(footer_with_image , unsafe_allow_html=True)


# Render the header with the image and hide specified elements


 
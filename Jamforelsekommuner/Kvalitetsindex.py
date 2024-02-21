import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from API")
        return None
    
def merge_data(api1_url, api2_url,api3_url,api4_url,api5_url,api6_url):
    data1 = fetch_data(api1_url)
    data2 = fetch_data(api2_url)
    data3 = fetch_data(api3_url)
    data4 = fetch_data(api4_url)
    data5 = fetch_data(api5_url)
    data6 = fetch_data(api6_url)
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    df4 = pd.DataFrame(data4)
    df5 = pd.DataFrame(data5)
    df6 = pd.DataFrame(data6)
    #st.write('DataFrame 1:')
    #st.write(df1)
    #st.write('DataFrame 2:')
    #st.write(df2)
    df_ar1= pd.json_normalize(df1['data'])
    df_ar2= pd.json_normalize(df2['data'])
    df_ar3= pd.json_normalize(df3['data'])
    df_ar4= pd.json_normalize(df4['data'])
    df_ar5= pd.json_normalize(df5['data'])
    df_ar6= pd.json_normalize(df6['data'])
    #st.write(df_ar1)
    #st.write(df_ar2)

    # Convert data to Pandas DataFrames
   

    # Merge DataFrames (assuming there is a common key/column)
    merged_df = pd.concat([df_ar1,df_ar2,df_ar3,df_ar4,df_ar5,df_ar6], ignore_index=True)

    return merged_df

def show():
   api1_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Falkenberg"
   api2_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Ljungby"
   api3_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Nynashamn"
   api4_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Vetlanda"
   api5_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_ornskoldsvik"
   api6_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Oskarshamn"
   
   merged_data = merge_data(api1_url, api2_url,api3_url,api4_url,api5_url,api6_url)
   merged_data['KvalIndex'] = merged_data['KvalIndex'].round(0)

   #st.dataframe(merged_data)
   #x_id = [0,1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16]
   #merged_data['x_id'] = x_id
   #st.dataframe(merged_data)
   #merged_data['x'] = merged_data['ar'].astype(str) + '_' + merged_data['x_id'].astype(str)
   #st.dataframe(merged_data)
   if merged_data is not None and len(merged_data) > 0:
        # Fetch data
        #data = fetch_data(api_url)
        # Convert data to a Pandas DataFrame
       
        
        
        fig = px.scatter(merged_data,
                       x='ar', 
                       y='KvalIndex',
                       #animation_frame='ar',
                       width=1000,
                       #height=400,
                       color ='Kommun',
                       size_max=35,
                       size='KvalIndex',  # Marker size based on 'KvalIndex' values
                       #opacity=1.0,  # Adjust transparency
                       text='Kommun',
                       template='plotly_dark',
                       title='Kvalitetsindex LSS, andel(%)',
                       labels={'KvalIndex': 'Kvalitetsindex(%)','Kommun': 'Kommun','ar': 'Year'},
                       
                       
                       )
        #col = st.color_picker('Select a plot color')
        #fig.update_layout(showlegend=False)
        fig.update_traces(textposition='bottom center', marker={"opacity":0.7})
        #st.markdown("<h1 style='font-size:15px;'>Kvalitetsindex LSS, andel(%)", unsafe_allow_html=True)
         
        #fig.update_traces(marker=dict(color= col))
        fig.update_layout(
            margin = dict(t=50, l=0, r=200, b=0),
            showlegend=False,
            xaxis_title='Year',
            yaxis_title='KvalIndex',
            plot_bgcolor='black',  # Set background color
            xaxis=dict(
                title_font=dict(size=16),  # Adjust size as needed for x-axis title
                tickfont=dict(size=12)  # Adjust size as needed for x-axis tick labels
            ),
                yaxis=dict(
                title_font=dict(size=16),  # Adjust size as needed for y-axis title
                tickfont=dict(size=12)  # Adjust size as needed for y-axis tick labels
            )
            
         
        )
        st.plotly_chart(fig)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged_data.to_excel(writer, sheet_name='Sheet1', index=False)
        if not merged_data.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='Kvalitetsindex LSS.xlsx', key='LSS')
        else:
            st.warning("No data to display.")
   else:
    st.warning("No data to display.")
    

if __name__ == "__main__":
    show()
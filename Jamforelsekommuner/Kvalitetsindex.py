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
    
def merge_data(api1_url, api2_url,api3_url,api4_url,api5_url):
    data1 = fetch_data(api1_url)
    data2 = fetch_data(api2_url)
    data3 = fetch_data(api3_url)
    data4 = fetch_data(api4_url)
    data5 = fetch_data(api5_url)
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    df4 = pd.DataFrame(data4)
    df5 = pd.DataFrame(data5)
    #st.write('DataFrame 1:')
    #st.write(df1)
    #st.write('DataFrame 2:')
    #st.write(df2)
    df_ar1= pd.json_normalize(df1['data'])
    df_ar2= pd.json_normalize(df2['data'])
    df_ar3= pd.json_normalize(df3['data'])
    df_ar4= pd.json_normalize(df4['data'])
    df_ar5= pd.json_normalize(df5['data'])
    #st.write(df_ar1)
    #st.write(df_ar2)

    # Convert data to Pandas DataFrames
   

    # Merge DataFrames (assuming there is a common key/column)
    merged_df = pd.concat([df_ar1,df_ar2,df_ar3,df_ar4,df_ar5], ignore_index=True)

    return merged_df

def show():
   api1_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Falkenberg"
   api2_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Ljungby"
   api3_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Nynashamn"
   api4_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Vetlanda"
   api5_url = "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_ornskoldsvik"
   
   merged_data = merge_data(api1_url, api2_url,api3_url,api4_url,api5_url)
   

   if merged_data is not None and len(merged_data) > 0:
        # Fetch data
        #data = fetch_data(api_url)
        # Convert data to a Pandas DataFrame
        
        #st.dataframe(merged_data)
      
        fig = px.scatter(merged_data,
                       x='ar', 
                       y='KvalIndex',
                       color ='Kommun',
                       #symbol = 'Kommun',
                       size='KvalIndex',  # Marker size based on 'KvalIndex' values
                       opacity=1.0,  # Adjust transparency
                       text='Kommun',
                       title='Kvalitetsindex LSS, andel(%)',
                       labels={'KvalIndex': 'Kvalitetsindex(%)','Kommun': 'Kommun','ar': 'Year'}
                       
                       )
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='bottom center')
        fig.update_layout(
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
            st.download_button(label='Ladda ner excel', data=output, file_name='Kvalitetsindex LSS.xlsx', key='LSS')
   else:
        st.warning("No data to display.")
    

if __name__ == "__main__":
    show()
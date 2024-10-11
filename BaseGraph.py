import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO


class BaseGraph:
    _instance_counter = 0
    def __init__(self):
        self.df = None #Lagring av dataframen
        self.instance_id = BaseGraph._instance_counter
        BaseGraph._instance_counter += 1
    
    def fetch_data(self):
        if not hasattr(self, 'api_url') or not self.api_url:
            raise ValueError("api_url måste vara satt i subklassen.")

        # Hantera om api_url är en sträng eller lista
        api_urls = self.api_url if isinstance(self.api_url, list) else [self.api_url]

        data_frames = []
        for url in api_urls:
            response = requests.get(url)
            if response.status_code == 200:
                res_data = response.json()
                if 'data' in res_data and len(res_data['data']) > 0:
                    df = pd.DataFrame(res_data['data'])
                    data_frames.append(df)
                else:
                    st.error(f"Misslyckades med att hämta data från API: {url}")
            else:
                st.error(f"Misslyckades med att hämta data från API: {url}")

        if data_frames:
            self.df = pd.concat(data_frames, ignore_index=True)
        else:
            self.df = pd.DataFrame()
    
    def process_data(self) -> pd.DataFrame: # Bearbeta data här, sedan returnera bearbetad data(pd.Dataframe).
        raise NotImplementedError("Underklasser måste implementera denna metod!")
    
    def plot_data(self, data: pd.DataFrame): # Mata in data(pd.Dataframe) här som ska ritas upp
        raise NotImplementedError("Underklasser måste implementera denna metod!")
    
    def export_data(self, data: pd.DataFrame): # Mata in data(pd.Dataframe) som ska laddas ner i excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Sheet1', index=False)
        key = f"download_excel_{self.__class__.__name__}_{self.instance_id}"
        file_name = f"{self.__class__.__name__}_data.xlsx"
        st.download_button(label=f'Ladda ner Excel', data=output.getvalue(), file_name=file_name, key=key)

    def show(self):
        self.fetch_data()
        if self.df is not None and not self.df.empty:
            self.processed_data = self.process_data()
            
            if self.processed_data is not None:
                self.plot_data(self.processed_data)
                self.export_data(self.processed_data)
        else:
            st.warning("Ingen data att visa.")
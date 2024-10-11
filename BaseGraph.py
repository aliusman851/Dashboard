import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO


class BaseGraph:
    def __init__(self):
        self.df = None #Lagring av dataframen
    
    def fetch_data(self):
        if not hasattr(self, 'api_url') or not self.api_url:
            raise ValueError("api_url måste vara satt i subklassen.")
        response = requests.get(self.api_url)
        if response.status_code == 200:
            res_data = response.json()
            if 'data' in res_data and len(res_data['data']) > 0:
                self.df = pd.DataFrame(res_data['data'])
            else:
                st.error("Misslyckades med att hämta data från API")
        else:
            st.error("Misslyckades med att hämta data från API")
    
    def process_data(self) -> pd.DataFrame: # Bearbeta data här, sedan returnera bearbetad data(pd.Dataframe).
        raise NotImplementedError("Underklasser måste implementera denna metod!")
    
    def plot_data(self, data: pd.DataFrame): # Mata in data(pd.Dataframe) här som ska ritas upp
        raise NotImplementedError("Underklasser måste implementera denna metod!")
    
    def export_data(self, data: pd.DataFrame): # Mata in data(pd.Dataframe) som ska laddas ner
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Sheet1', index=False)
        st.download_button(label='Ladda ner Excel', data=output.getvalue(), file_name='data.xlsx', key='download_excel')

    def show(self):
        self.fetch_data()
        if self.df is not None and not self.df.empty:
            self.processed_data = self.process_data()
            
            if self.processed_data is not None:
                self.plot_data(self.processed_data)
                self.export_data(self.processed_data)
        else:
            st.warning("Ingen data att visa.")
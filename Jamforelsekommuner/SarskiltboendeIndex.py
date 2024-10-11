from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class SarskiltboendeIndex(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Vetlanda",
    ]

    def process_data(self):
        self.df["Index_Totalt"] = pd.to_numeric(
            self.df["Index_Totalt"], errors="coerce"
        ).round(0)
        self.df["datum"] = pd.to_datetime(self.df["datum"], errors="coerce")
        self.df.dropna(subset=["Index_Totalt", "datum", "id"], inplace=True)
        return self.df

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.sunburst(
                data,
                path=["ar", "Kommun"],
                values="Index_Totalt",
                color="Kommun",
                maxdepth=2,
                width=1700,
                height=800,
                labels={
                    "Index_Totalt": "Index(%)",
                    "ar": "År",
                    "Kommun": "Kommun",
                },
                branchvalues="total",
            )

            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>År: %{parent}<br>Index(%): %{value:.2f}<extra></extra>"
            )

            fig.update_layout(
                title={
                    "text": "Brukarbedömning särskilt boende äldreomsorg - Bemötande, Förtroende, Medelvärde — Kommuner, Index andel(%)",
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                font=dict(size=14),
                margin=dict(t=50, l=25, r=25, b=25),
                showlegend=True,
            )

            st.plotly_chart(fig)


def show():
    graph = SarskiltboendeIndex()
    graph.show()

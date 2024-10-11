from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Elevmeritaavvikelse(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Vetlanda",
    ]

    def process_data(self):
        self.df["Value"] = self.df["Value"].round(0)
        return self.df

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.histogram(
                data,
                x="ar",
                y="Value",
                color="Kommun",
                width=800,
                title="Elever genomsnittligt meritvärde avvikelse, andel (%)",
                labels={"ar": "År", "Value": "Andel(%)"},
            )

        fig.update_traces(
            marker_line_color="rgb(8,48,107)",
            marker_line_width=1.5,
            opacity=0.8,
            hovertemplate="<br>".join(
                [
                    "År: %{x}",
                    "Andel(%): %{y}",
                    "Kommun: %{customdata[0]}",
                ]
            ),
        )

        fig.update_layout(
            bargap=0.2,
            coloraxis_colorbar=dict(title="Kommun"),
            plot_bgcolor="white",
        )

        st.plotly_chart(fig)


def show():
    graph = Elevmeritaavvikelse()
    graph.show()

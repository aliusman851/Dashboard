from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Kvalitetsindex(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Vetlanda",
    ]

    def process_data(self):
        self.df["KvalIndex"] = pd.to_numeric(
            self.df["KvalIndex"], errors="coerce"
        ).round(0)

        return self.df

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            selected_kommuner = st.multiselect(
                "Välj kommun(er)",
                data["Kommun"].unique(),
                default=data["Kommun"].unique()[0],
            )
            filtered_data = data[data["Kommun"].isin(selected_kommuner)]

            fig = px.scatter(
                filtered_data,
                x="ar",
                y="KvalIndex",
                width=800,
                color="Kommun",
                size_max=35,
                size="KvalIndex",
                text="KvalIndex",
                template="plotly_dark",
                range_y=[0, 110],
                title="Kvalitetsindex LSS, andel(%)",
                labels={
                    "KvalIndex": "Kvalitetsindex(%)",
                    "Kommun": "Kommun",
                    "ar": "År",
                },
            )

            st.plotly_chart(fig)


def show():
    graph = Kvalitetsindex()
    graph.show()

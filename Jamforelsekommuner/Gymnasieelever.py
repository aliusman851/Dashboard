from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Gymnasieelever(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Gymnaiseelever_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasielever_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Vetlanda",
    ]

    def process_data(self):
        self.df["Gymnasieelever_M"] = self.df["Gymnasieelever_M"].round(0)
        self.df["Gymnasieelever_K"] = self.df["Gymnasieelever_K"].round(0)
        self.df["Gymnasieelever_T"] = self.df["Gymnasieelever_T"].round(0)

        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=["Gymnasieelever_T", "Gymnasieelever_M", "Gymnasieelever_K"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "Gymnasieelever_T": "Totalt(kvinnor och män)",
            "Gymnasieelever_M": "Män",
            "Gymnasieelever_K": "Kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)

        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            selected_kommuner = st.multiselect(
                "Välj kommun(er)",
                data["Kommun"].unique(),
                default=data["Kommun"].unique()[0],
            )
            filtered_data = data[data["Kommun"].isin(selected_kommuner)]

            fig = px.line(
                filtered_data,
                x="ar",
                y="Value",
                range_x=[2014, 2024],
                color="kommun",
                line_dash="Type",
                title="Gymnasieelever med examen inom 4 år",
                labels={
                    "ar": "År",
                    "Value": "Andel (%)",
                    "kommun": "Kommun",
                    "Tyep": "typ",
                },
            )
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=14,
                legend_title_font_size=14,
                legend_font_size=12,
                xaxis_tickangle=-45,
                hovermode="x unified",
            )
            fig.update_traces(
                mode="lines+markers",
                line=dict(width=2),
                marker=dict(size=8),
            )

            st.plotly_chart(fig)


def show():
    graph = Gymnasieelever()
    graph.show()

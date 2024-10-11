from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class InvanareArbstud(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/ArbStud_Vetlanda",
    ]

    def process_data(self):
        self.df["Value_K"] = pd.to_numeric(self.df["Value_K"], errors="coerce").round(0)
        self.df["Value_M"] = pd.to_numeric(self.df["Value_M"], errors="coerce").round(0)
        self.df["Value_T"] = pd.to_numeric(self.df["Value_T"], errors="coerce").round(0)

        melted_data = self.df.melt(
            id_vars=["ar", "Kommun"],
            value_vars=["Value_T", "Value_M", "Value_K"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {"Value_T": "Totalt", "Value_M": "Män", "Value_K": "Kvinnor"}
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

            fig = px.area(
                filtered_data,
                x="ar",
                y="Value",
                color="Type",
                markers=True,
                width=800,
                title="Invånare 16-24 år som varken arbetar eller studerar, andel (%) ",
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                template="plotly_white",
                custom_data=["Kommun", "Type"],
            )
            fig.update_traces(
                hovertemplate="<br>".join(
                    [
                        "År: %{x}",
                        "Andel(%): %{y}",
                        "Kommun: %{customdata[0]}",
                        "Typ: %{customdata[1]}",
                    ]
                )
            )
            st.plotly_chart(fig)


def show():
    graph = InvanareArbstud()
    graph.show()

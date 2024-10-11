from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Aldreomsorgbehandling(BaseGraph):
    api_url = (
        "https://nav.utvecklingfalkenberg.se/items/hemtjanst_aldreomsorgbehandling"
    )

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=["behandlas_totalt", "behandlade_man", "behandlade_kvinnor"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "behandlas_totalt": "Totalt",
            "behandlade_man": "Män",
            "behandlade_kvinnor": "kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.line(
                data,
                x="ar",
                y="Value",
                title="Brukarbedömning hemtjänst äldreomsorg-bemötande, andel(%)",
                markers=True,
                width=800,
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                template="plotly_white",
                custom_data=["kommun", "Type"],
                color="Type",
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
    graph = Aldreomsorgbehandling()
    graph.show()
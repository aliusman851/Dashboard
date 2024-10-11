from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Gymnasieutbildad(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/gymnasieutbildad"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=["utbildade_totalt", "utbildade_man", "utbildade_kvinnor"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "utbildade_totalt": "Totalt",
            "utbildade_man": "Män",
            "utbildade_kvinnor": "kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:

            fig = px.bar(
                data,
                y="ar",
                x="Value",
                orientation="h",
                title="Invånare 25-64 år med eftergymnasial utbildning, andel(%)",
                width=800,
                template=("plotly_white"),
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                custom_data=["kommun", "Type"],
                color="Type",
            )
            fig.update_traces(
                hovertemplate="<br>".join(
                    [
                        "År: %{y}",
                        "Andel(%): %{x}",
                        "Kommun: %{customdata[0]}",
                        "Typ: %{customdata[1]}",
                    ]
                )
            )

            st.plotly_chart(fig)


def show():
    graph = Gymnasieutbildad()
    graph.show()

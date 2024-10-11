from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Aldreomsorgtrygghet(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/hemtjanst_aldreomsorgtrygghet"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=[
                "hemtjansttrygghet_totalt",
                "hemtjansttrygghet_man",
                "hemtjansttrygghet_kvinnor",
            ],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "hemtjansttrygghet_totalt": "Totalt",
            "hemtjansttrygghet_man": "Män",
            "hemtjansttrygghet_kvinnor": "kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.bar(
                data,
                x="Value",
                y="ar",
                title="Brukarbedömning hemtjänst äldreomsorg-trygghet, andel(%)",
                orientation="h",
                template=("plotly_white"),
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                width=800,
                custom_data=["kommun", "Type"],
                color="Type",
            )
            fig.update_layout(xaxis=(dict(showgrid=False)))
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
    graph = Aldreomsorgtrygghet()
    graph.show()
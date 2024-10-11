from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Yrkesprogram(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/behorighet_yrkesprogram"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars="elever",
            var_name="Type",
            value_name="Value",
        )
        type_labels = {"elever": "Elever"}
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.histogram(
                data,
                y="Value",
                x="ar",
                title="Elever i åk 9 som är behöriga till yrkesprogram kommunala (modellberäknat värde), andel(%)",
                template=("plotly_white"),
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                # custom_data=['kommun','Type'],
                color="Type",
                width=700,
            )

            fig.update_traces(customdata=data[["kommun", "Type"]].values)
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
            fig.update_layout(
                # plot_bgcolor="rgba(2,0,1,4)",
                xaxis=(dict(showgrid=False)),
            )
            st.plotly_chart(fig)


def show():
    graph = Yrkesprogram()
    graph.show()

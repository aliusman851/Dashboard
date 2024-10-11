from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Ekonomiskstandard(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Vetlanda",
    ]
    all_min_value = []
    all_max_value = []

    def process_data(self):

        self.df["Value_T"] = self.df["Value_T"].round(0)
        min_value, max_value = (
            self.df["Value_T"].min(),
            self.df["Value_T"].max(),
        )
        self.all_min_value.append(min_value)
        self.all_max_value.append(max_value)

        melted_data = melted_data.melt(
            id_vars=["ar", "Kommun"],
            value_vars=["Value_T"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {"Value_T": "Totalt(Kvinnor och män)"}
        melted_data["Type"] = melted_data["Type"].map(type_labels)

        melted_data["Kommun_Value"] = melted_data.apply(
            lambda row: f"{row['Kommun']}: {row['Value']}", axis=1
        )
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.scatter(
                data,
                x="ar",
                y="Value",
                size="Value",
                size_max=30,
                color="Kommun",
                hover_name="Kommun",
                labels={"ar": "År", "Value": "Andel(%)", "Kommun": "Kommun"},
                template="plotly_dark",
            )

            fig.update_traces(
                marker=dict(line=dict(width=2, color="DarkSlateGrey")),
                selector=dict(mode="markers"),
            )

            fig.update_layout(
                width=800,
                height=600,
                xaxis_title="År",
                yaxis_title="Andel(%)",
                coloraxis_colorbar_title="Kommun",
            )

            fig2 = px.scatter(
                data,
                x="Value",
                y="Kommun",
                size="Value",
                size_max=50,
                color="Kommun",
                animation_frame="ar",
                animation_group="Kommun",
                range_x=[min(self.all_min_value), max(self.all_max_value)],
                labels={"Value": "Andel(%)"},
                title="Invånare med låg ekonomisk standard (0-19 år)",
                color_continuous_scale="agsunset",
                hover_name="Kommun",
                text="Kommun_Value",
            )

            fig2.update_traces(
                textposition="top center",
                marker=dict(line=dict(width=2, color="DarkSlateGrey")),
                selector=dict(mode="markers"),
            )

            fig2.update_layout(
                coloraxis_showscale=False,
            )

            st.markdown(
                "<h1 style='font-size:15px;'>Invånare med låg ekonomisk standard (0-19 år)</h1>",
                unsafe_allow_html=True,
            )

            st.plotly_chart(fig)
            st.plotly_chart(fig2)


def show():
    graph = Ekonomiskstandard()
    graph.show()

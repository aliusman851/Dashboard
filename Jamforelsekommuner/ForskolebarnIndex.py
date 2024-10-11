from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class ForskolebarnIndex(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Vetlanda",
    ]
    all_min_value = []
    all_max_value = []

    def process_data(self):
        self.df["Index_Totalt"] = self.df["Index_Totalt"].round(0)
        min_value, max_value = (
            self.df["Index_Totalt"].min(),
            self.df["Index_Totalt"].max(),
        )
        self.all_min_value.append(min_value)
        self.all_max_value.append(max_value)

        return self.df

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            selected_kommuner = st.multiselect(
                "Välj kommun(er)",
                data["Kommun"].unique(),
                default=data["Kommun"].unique()[0],
            )
            filtered_data = data[data["Kommun"].isin(selected_kommuner)]

            fig = px.bar(
                filtered_data,
                x="ar",
                y="Index_Totalt",
                color="Kommun",
                barmode="group",
                width=800,
                template="plotly_dark",
                hover_name="Kommun",
                log_x=True,
                range_y=[30, 100],
                custom_data=["Kommun"],
            )
            fig2 = px.bar(
                data,
                x="Index_Totalt",
                y="Kommun",
                height=800,
                width=800,
                orientation="h",
                color="Kommun",
                labels={
                    "ar": "År",
                    "Index_Totalt": "Barn 1-5 år inskrivna i förskola, andel (%)",
                },
                title="Barn 1-5 år inskrivna i förskola, andel (%)",
                range_x=[10, 100],
                animation_frame="ar",
                color_continuous_scale="agsunset",
                text=data["Index_Totalt"],
            )
            st.markdown(
                "<h1 style='font-size:15px;'>Barn 1-5 år inskrivna i förskola, andel (%)",
                unsafe_allow_html=True,
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(
                xaxis=dict(range=[self.all_min_value, self.all_max_value])
            )
            fig2.update_layout(coloraxis_showscale=False)
            fig.update_layout(
                margin=dict(t=50, l=0, r=200, b=0),
                showlegend=True,
                xaxis_title="År",
                yaxis_title="Index(%)",
            )
            fig.update_traces(
                hovertemplate="<br>".join(
                    [
                        "År: %{x}",
                        "Andel(%): %{y}",
                        "Kommun: %{customdata[0]}",
                    ]
                )
            )
            st.plotly_chart(fig)
            st.plotly_chart(fig2)


def show():
    graph = ForskolebarnIndex()
    graph.show()

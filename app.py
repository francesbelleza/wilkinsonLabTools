import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# … your upload + read_csv + df cleaning above …

# Map your Genotype to 0/1 just to get numeric x
code_map = {"Saline": 0, "VIN": 1}
df["Genotype_code"] = df["Genotype"].map(code_map)

# Add jitter on BOTH axes (optional, but helps if you ever jitter y too)
df["x_jitter"] = df["Genotype_code"] + np.random.uniform(-0.15, 0.15, size=len(df))
df["y_jitter"] = df["Missteps Total"]   + np.random.uniform(-0.15, 0.15, size=len(df))

for run_name, group in df.groupby("Run"):
    # 1) scatter with horizontal jitter
    fig = px.scatter(
        group,
        x="x_jitter",
        y="Missteps Total",       # you could switch to y="y_jitter" if you want vertical spread
        color="Genotype",
        title=f"Missteps by Genotype — Run {run_name}",
        labels={
            "x_jitter": "Genotype",
            "Missteps Total": "Number of Missteps"
        }
    )

    # 2) restore categorical ticks at 0 & 1
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[0,1],
            ticktext=["Saline","VIN"]
        )
    )

    # 3) make points semi-transparent so overlaps look darker
    fig.update_traces(marker=dict(opacity=0.6, size=10))

    st.plotly_chart(fig, use_container_width=True)


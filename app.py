import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Missteps by Genotype — Run Selector")

uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
if not uploaded:
    st.info("Please upload your LadderTestData file.")
    st.stop()

# load data
if uploaded.name.endswith(".csv"):
    df = pd.read_csv(uploaded)
else:
    df = pd.read_excel(uploaded, engine="openpyxl")

# clean
df.columns = df.columns.str.strip()
df["Run"] = df["Run"].astype(str).str.strip()

# choose which runs
runs = sorted(df["Run"].dropna().unique())
sel = st.multiselect("Select Run(s)", runs, default=runs)

# plot each
for run in sel:
    sub = df[df["Run"] == run]
    # scatter of Genotype vs Missteps Total
    fig = px.scatter(
        sub,
        x="Genotype",
        y="Missteps Total",
        color="Genotype",
        title=f"Run: {run}",
        labels={"Missteps Total": "Number of Missteps"}
    )
    fig.update_traces(marker=dict(opacity=0.6, size=10))
    st.plotly_chart(fig, use_container_width=True)

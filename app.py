import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Missteps by Genotype — Run")

# 1) upload
uploaded = st.file_uploader("Upload your LadderTestData.csv", type="csv")
if not uploaded:
    st.info("Please upload a CSV file to get started.")
    st.stop()

# 2) load CSV
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"😕 Could not read CSV:\n{e}")
    st.stop()

# 3) clean column names
df.columns = df.columns.str.strip()

# 4) ensure Run exists
if "Run" not in df.columns:
    st.error("Your CSV must include a `Run` column.")
    st.stop()

# 5) clean & filter Run
df["Run"] = df["Run"].astype(str).str.strip()
df = df[
    df["Run"].notna()
    & (df["Run"] != "")
    & (df["Run"].str.lower() != "nan")
]

# 6) ensure key columns exist
for col in ["Genotype", "Missteps Total"]:
    if col not in df.columns:
        st.error(f"Your CSV must include a `{col}` column.")
        st.stop()

# 7) map & jitter Genotype → numeric
code_map = {"Saline": 0, "VIN": 1}
df["Genotype_code"] = df["Genotype"].map(code_map)
df["x_jitter"] = df["Genotype_code"] + np.random.uniform(-0.1, 0.1, size=len(df))

# 8) loop over runs
for run_name, group in df.groupby("Run"):
    if group.empty:
        continue

    fig = px.scatter(
        group,
        x="x_jitter",
        y="Missteps Total",
        color="Genotype",
        title=f"Run: {run_name}",
        labels={
            "x_jitter": "Genotype",
            "Missteps Total": "Number of Missteps",
        },
    )

    # put ticks back at Saline/VIN
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Saline", "VIN"],
        )
    )
    fig.update_traces(marker=dict(opacity=0.6, size=9))

    st.plotly_chart(fig, use_container_width=True)

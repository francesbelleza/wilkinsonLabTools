import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Missteps by Genotype — Run")

# 1) Upload-only-CSV
uploaded = st.file_uploader("Upload your LadderTestData.csv", type="csv")
if not uploaded:
    st.info("Please upload a CSV file to get started.")
    st.stop()

# 2) Read & initial clean
df = pd.read_csv(uploaded)
df.columns = df.columns.str.strip()

# 3) Ensure 'Run', 'Genotype', 'Missteps Total' exist
required = ["Run", "Genotype", "Missteps Total"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing column(s): {missing}.")
    st.stop()

# 4) Clean 'Run' and drop any blank/NAN runs
df["Run"] = df["Run"].astype(str).str.strip()
df = df[df["Run"].notna() & (df["Run"] != "") & (df["Run"].str.lower() != "nan")]

# 5) Map Genotype → 0/1 then add tiny horizontal jitter
code_map = {"Saline": 0, "VIN": 1}
df["Genotype_code"] = df["Genotype"].map(code_map)
df["x_jitter"]     = df["Genotype_code"] + np.random.uniform(-0.15, 0.15, size=len(df))

# 6) Let user pick which runs to show
all_runs = sorted(df["Run"].unique())
sel_runs = st.multiselect("Select Run(s)", all_runs, default=all_runs)

# 7) Plot each run
for run_name in sel_runs:
    sub = df[df["Run"] == run_name]
    if sub.empty:
        st.warning(f"No data for Run `{run_name}`.")
        continue

    fig = px.scatter(
        sub,
        x="x_jitter",
        y="Missteps Total",
        color="Genotype",
        title=f"Run: {run_name}",
        labels={
            "x_jitter":       "Genotype",
            "Missteps Total": "Number of Missteps"
        }
    )

    # put the ticks back at Saline (0) and VIN (1)
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Saline", "VIN"]
        )
    )

    # semi-transparent so overplotted points look darker
    fig.update_traces(marker=dict(opacity=0.6, size=10))

    st.plotly_chart(fig, use_container_width=True)



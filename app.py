import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def main():
    st.title("Missteps by Genotype — Run")

    # 1) Upload-only-CSV
    uploaded = st.file_uploader("Upload your LadderTestData.csv", type="csv")
    if not uploaded:
        st.info("Please upload a CSV file to get started.")
        return

    # 2) Read & initial clean
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.strip()

    # 3) Ensure required columns exist
    required = ["Run", "Genotype", "Missteps Total"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing column(s): {missing}.")
        return

    # 4) Clean and filter Run
    df["Run"] = df["Run"].astype(str).str.strip()
    df = df[
        df["Run"].notna()
        & (df["Run"] != "")
        & (df["Run"].str.lower() != "nan")
    ]

    # 5) Map Genotype → numeric and jitter both axes
    code_map = {"Saline": 0, "VIN": 1}
    df["Genotype_code"] = df["Genotype"].map(code_map)
    df["x_jitter"] = df["Genotype_code"].astype(float) + np.random.uniform(-0.15, 0.15, size=len(df))
    df["y_jitter"] = df["Missteps Total"].astype(float)  + np.random.uniform(-0.15, 0.15, size=len(df))

    # 6) Let the user pick which Run(s) to show
    all_runs = sorted(df["Run"].unique())
    sel_runs = st.multiselect("Select Run(s)", all_runs, default=all_runs)
    if not sel_runs:
        st.warning("Please select at least one Run.")
        return

    # 7) Loop & plot
    for run_name in sel_runs:
        sub = df[df["Run"] == run_name]
        fig = px.scatter(
            sub,
            x="x_jitter",
            y="Missteps Total",
            color="Genotype",
            title=f"Run: {run_name}",
            labels={
                "x_jitter": "Genotype"
            },
        )
        # restore categorical ticks
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=[0, 1],
                ticktext=["Saline", "VIN"]
            )
        )
        fig.update_traces(marker=dict(opacity=0.6, size=10))
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
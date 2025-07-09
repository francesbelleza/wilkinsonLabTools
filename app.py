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

    # 3) Check required columns
    required = ["Run", "Genotype", "Missteps Total", "Gender", "Walking"]
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

    # 5) Fill missing Genotype entries
    df["Genotype"] = df["Genotype"].astype(str).str.strip()
    df.loc[df["Genotype"].isin(["", "nan", "None", None]), "Genotype"] = "No Genotype Specified"

    # 6) Factorize Genotype and add horizontal jitter for x-axis
    df["Genotype_code"], uniques = pd.factorize(df["Genotype"])
    df["x_jitter"] = df["Genotype_code"] + np.random.uniform(-0.2, 0.2, size=len(df))

    # 7) Clean Gender and Walking columns
    df["Gender"] = df["Gender"].astype(str).str.strip().str.upper().replace({"": "NULL", "NAN": "NULL"})
    df["Walking"] = pd.to_numeric(df["Walking"], errors="coerce").fillna(-1).astype(int)

    # 8) Select which Runs to plot
    all_runs = sorted(df["Run"].unique())
    sel_runs = st.multiselect("Select Run(s)", all_runs, default=all_runs)
    if not sel_runs:
        st.warning("Please select at least one Run.")
        return

    # 9) Loop over each Run and plot separately
    for run_name in sel_runs:
        sub = df[df["Run"] == run_name]
        if sub.empty:
            st.warning(f"No data for Run '{run_name}'.")
            continue

        fig = px.scatter(
            sub,
            x="x_jitter",
            y="Missteps Total",
            color="Gender",
            symbol="Walking",
            color_discrete_map={"M": "blue", "F": "red", "NULL": "grey"},
            symbol_map={-1: "x", 0: "circle", 1: "square", 2: "diamond"},
            labels={
                "x_jitter":       "Genotype",
                "Missteps Total": "Number of Missteps",
                "Gender":         "Gender",
                "Walking":        "Walking Score"
            },
            title=f"Run: {run_name}"
        )

        # restore categorical Genotype labels on x-axis
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(uniques))),
                ticktext=list(uniques)
            )
        )
        fig.update_traces(marker=dict(opacity=0.6, size=10))

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
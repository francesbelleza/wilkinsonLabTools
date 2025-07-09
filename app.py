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
            margin=dict(l=60, r=160, t=60, b=60),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(uniques))),
                ticktext=list(uniques)
            ),
            showlegend=False
        )

        # Style markers with white border for contrast
        fig.update_traces(marker=dict(opacity=0.8, size=10, line=dict(width=1, color='white')))

        # Add simplified legend annotation in top-right corner (key only)
        legend_text = (
            "COLOR KEY<br>🔵 Blue = Male<br>🔴 Red = Female<br>⚪ Grey = Unspecified"
        )
        fig.add_annotation(
            x=1.05, y=0.9,
            xref='paper', yref='paper',
            text=legend_text,
            showarrow=False,
            align='left',
            bgcolor='black',
            bordercolor='white',
            borderwidth=0.5,
            borderpad=6,
            font=dict(size=12, color='white'),
            xanchor='left',
            yanchor='top'
        )
        # walking legend annotation below color key
        walking_legend = (
            "SHAPE KEY<br>◯ Circle = 0<br>◼ Square = 1<br>◆ Diamond = 2"
        )
        fig.add_annotation(
            x=1.05, y=0.60,
            xref='paper', yref='paper',
            text=walking_legend,
            showarrow=False,
            align='left',
            bgcolor='black',
            bordercolor='white',
            borderwidth=0.5,
            borderpad=6,
            font=dict(size=12, color='white'),
            xanchor='left',
            yanchor='top'
        )

        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
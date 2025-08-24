import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# — Back Limbs Steps Scatter Tool —
def back_limbs_steps_tool():
    st.button("◀ back to tools", on_click=lambda: st.session_state.update(tool=None))

    st.header("Back Limbs Steps Scatterplots")

    # 1) Upload-only-CSV
    uploaded = st.file_uploader("upload your csv:", type="csv")
    if not uploaded:
        st.info("upload a csv file to get started")
        return

    # 2) Read & initial clean
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.strip()

    # 3) Check required columns
    required = ["Run", "Genotype", "Back Right", "Back Left", "Gender", "Walking"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing column(s): {missing}.")
        return

    # 4) Calculate Back Limbs Total
    df["Back Right"] = pd.to_numeric(df["Back Right"], errors="coerce").fillna(0)
    df["Back Left"] = pd.to_numeric(df["Back Left"], errors="coerce").fillna(0)
    df["Back Limbs Steps"] = df["Back Right"] + df["Back Left"]

    # 5) Clean and filter Run
    df["Run"] = df["Run"].astype(str).str.strip()
    df = df[
        df["Run"].notna()
        & (df["Run"] != "")
        & (df["Run"].str.lower() != "nan")
    ]

    # 6) Fill missing Genotype entries
    df["Genotype"] = df["Genotype"].astype(str).str.strip()
    df.loc[df["Genotype"].isin(["", "nan", "None", None]), "Genotype"] = "No Genotype Specified"

    # 7) Factorize Genotype and add horizontal jitter for x-axis
    df["Genotype_code"], uniques = pd.factorize(df["Genotype"])
    df["x_jitter"] = df["Genotype_code"] + np.random.uniform(-0.2, 0.2, size=len(df))

    # 8) Clean Gender and Walking columns
    df["Gender"] = df["Gender"].astype(str).str.strip().str.upper().replace({"": "NULL", "NAN": "NULL"})
    df["Walking"] = pd.to_numeric(df["Walking"], errors="coerce").fillna(-1).astype(int)

    # 9) Select which Runs to plot
    all_runs = sorted(df["Run"].unique())
    sel_runs = st.multiselect("Select Run(s)", all_runs, default=all_runs)
    if not sel_runs:
        st.warning("please select at least one Run.")
        return

    # 10) Loop over each Run and plot separately
    for run_name in sel_runs:
        sub = df[df["Run"] == run_name]
        if sub.empty:
            st.warning(f"no data for Run '{run_name}'.")
            continue

        fig = px.scatter(
            sub,
            x="x_jitter",
            y="Back Limbs Steps",
            color="Gender",
            symbol="Walking",
            color_discrete_map={"M": "blue", "F": "red", "NULL": "grey"},
            symbol_map={-1: "x", 0: "circle", 1: "square", 2: "diamond"},
            labels={
                "x_jitter":           "Genotype",
                "Back Limbs Steps":   "Back Limbs Steps",
                "Gender":             "Gender",
                "Walking":            "Walking Score"
            },
            title=f"Back Limbs Steps - Run: {run_name}"
        )

        fig.update_layout(
            margin=dict(l=60, r=250, t=60, b=60),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(uniques))),
                ticktext=list(uniques)
            ),
            showlegend=False
        )
        fig.update_traces(marker=dict(opacity=0.8, size=10, line=dict(width=1, color='white')))

        # Color key
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
            font=dict(size=12, color='white'),
            xanchor='left',
            yanchor='top'
        )

        # Shape key below color key
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
            font=dict(size=12, color='white'),
            xanchor='left',
            yanchor='top'
        )

        st.plotly_chart(fig, use_container_width=True)


def back_limbs_total_steps_tool():
    return None
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# — Wire and Inversion Test Scatter Tool —
def wire_and_inversion_tool():
    st.button("◀ back to tools", on_click=lambda: st.session_state.update(tool=None))

    st.header("Wire Hanging and Inversion Test Scatterplots")

    # 1) Upload-only-CSV
    uploaded = st.file_uploader("upload your csv:", type="csv")
    if not uploaded:
        st.info("upload a csv file to get started")
        return

    # 2) Read & initial clean
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.strip()

    # Display available columns for debugging
    st.write("Available columns:", list(df.columns))

    # 3) Check required columns
    required = ["Genotype HET1 or HET2", "Average Latency to Fall", "Sex"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing column(s): {missing}.")
        st.write("Available columns:", list(df.columns))
        return

    # 4) Clean numeric data
    df["Average Latency to Fall"] = pd.to_numeric(df["Average Latency to Fall"], errors="coerce").fillna(0)

    # 5) Filter for HET1 and HET2 genotypes only and standardize names
    df["Genotype HET1 or HET2"] = df["Genotype HET1 or HET2"].astype(str).str.strip().str.upper()
    # Standardize genotype names (remove spaces)
    df["Genotype HET1 or HET2"] = df["Genotype HET1 or HET2"].str.replace(" ", "")
    df = df[df["Genotype HET1 or HET2"].isin(["HET1", "HET2"])]

    if df.empty:
        st.error("No data found for HET1 or HET2 genotypes.")
        return

    # 6) Map genotypes to numeric positions for x-axis (HET1=0, HET2=1)
    genotype_map = {"HET1": 0, "HET2": 1}
    df["x_position"] = df["Genotype HET1 or HET2"].map(genotype_map)
    df["x_jitter"] = df["x_position"] + np.random.uniform(-0.2, 0.2, size=len(df))

    # 7) Clean Sex column
    df["Sex"] = df["Sex"].astype(str).str.strip().str.upper().replace({"": "NULL", "NAN": "NULL"})

    # 8) Since there's no Run column, we'll plot all data together
    st.subheader("Wire Hanging and Inversion Test Results")

    fig = px.scatter(
        df,
        x="x_jitter",
        y="Average Latency to Fall",
        color="Genotype HET1 or HET2",
        symbol="Sex",
        color_discrete_map={"HET1": "purple", "HET2": "orange"},
        symbol_map={"F": "circle", "M": "x", "NULL": "diamond"},
        labels={
            "x_jitter": "Genotype",
            "Average Latency to Fall": "Average Latency to Fall (seconds)",
            "Genotype HET1 or HET2": "Genotype",
            "Sex": "Sex"
        },
        title="Wire Hanging and Inversion Tests - Average Latency to Fall"
    )

    fig.update_layout(
        margin=dict(l=60, r=250, t=60, b=60),
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["HET1", "HET2"],
            range=[-0.5, 1.5]
        ),
        yaxis=dict(
            range=[0, 130]
        ),
        showlegend=False
    )
    fig.update_traces(marker=dict(opacity=0.8, size=10, line=dict(width=1, color='white')))

    # Color key
    legend_text = (
        "COLOR KEY<br>🟣 Purple = HET1<br>🟠 Orange = HET2"
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
    sex_legend = (
        "SHAPE KEY<br>● = Female<br>✕ = Male<br>◆ Diamond = Unspecified"
    )
    fig.add_annotation(
        x=1.05, y=0.60,
        xref='paper', yref='paper',
        text=sex_legend,
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
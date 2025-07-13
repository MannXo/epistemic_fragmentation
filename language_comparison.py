import streamlit as st
import pandas as pd
import plotly.express as px
import os

INSIGHT_DIR = "insights/language_comparison"

def show_language_comparison():
    st.header("Language Comparison of MEP Narratives")

    st.markdown("""
    This section explores whether Members of the European Parliament (MEPs) present different narratives
    in English versus their native language. It includes:
    
    - A **filtered view** of MEPs with large shifts in narrative between languages
    - A **selectable comparison** for any individual MEP
    """)

    # === 1. Significant Shifts Table ===
    st.markdown("### 🔍 MEPs with Significant Narrative Shift Between English and Native Language")
    st.markdown("These MEPs show at least a 20% difference in narrative distribution between languages.")

    shift_df = pd.read_json(os.path.join(INSIGHT_DIR, "narrative_language_shift_mep.json"))
    st.dataframe(shift_df, use_container_width=True)

    # === 2. Individual Narrative Comparison ===
    st.markdown("### 📊 Narrative Distribution in English vs Native Language (Per MEP)")
    st.markdown("Select an MEP to compare how their narrative stance changes between English and native-language tweets.")

    comp_df = pd.read_json(os.path.join(INSIGHT_DIR, "narrative_language_comparison_mep.json"))
    available_users = comp_df["userName"].unique()
    selected_user = st.selectbox("Select an MEP (by handle)", available_users)

    user_row = comp_df[comp_df["userName"] == selected_user].iloc[0]

    # Extract narrative percentages from each language
    records = []
    for narrative, percent in user_row["narrative_dist_en"].items():
        records.append({"narrative": narrative, "percent": percent, "language": "English"})
    for narrative, percent in user_row["narrative_dist_native"].items():
        records.append({"narrative": narrative, "percent": percent, "language": "Native"})

    melted_df = pd.DataFrame(records)

    fig = px.bar(
        melted_df,
        x="language",
        y="percent",
        color="narrative",
        barmode="group",
        labels={
            "language": "Tweet Language",
            "percent": "Narrative Share (%)",
            "narrative": "Narrative"
        },
        title=f"Narrative Distribution for @{selected_user}"
    )
    st.plotly_chart(fig, use_container_width=True)

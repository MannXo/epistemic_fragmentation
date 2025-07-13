import streamlit as st
import pandas as pd
import plotly.express as px
import os

INSIGHTS_DIR = "insights/rq5"
THEMES_FRAMING_DIR = "insights/rq5_themes_framing"

def load_json(filepath):
    return pd.read_json(filepath)

def melt_code_columns(df, id_vars, prefix):
    """Helper to melt framing/theme data into long format"""
    value_vars = [col for col in df.columns if col.startswith(prefix)]
    df_melted = df.melt(id_vars=id_vars, value_vars=value_vars, var_name=prefix[:-1], value_name="value")
    return df_melted

def show_rq5():
    st.header("RQ5: Variations in Narratives Across Contexts")

    st.markdown("## 🗺️ Narrative, Theme, and Framing by Country")

    # Load data
    df_narrative_country = load_json(os.path.join(INSIGHTS_DIR, "narrative_by_country_block.json"))
    df_theme_country = load_json(os.path.join(THEMES_FRAMING_DIR, "theme_by_country.json"))
    df_framing_country = load_json(os.path.join(THEMES_FRAMING_DIR, "framing_by_country.json"))

    # --- Narrative Distribution by Country ---
    st.markdown("### 📊 Narrative Distribution by Country Group")
    st.markdown("This chart shows the share of each narrative category (Pro-Ukraine, Pro-Russia, Neutral) across country groupings.")
    fig1 = px.bar(
        df_narrative_country,
        x="group",
        y="percent",
        color="narrative",
        barmode="stack",
        labels={"group": "Country Group", "percent": "Narrative Share (%)", "narrative": "Narrative Type"},
        title="Narrative Types Across Countries"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Theme Distribution by Country ---
    st.markdown("### 📚 Theme Distribution by Country")
    st.markdown("This chart shows the distribution of themes (e.g., sovereignty, civilian impact) across different countries.")
    df_theme_country_melted = melt_code_columns(df_theme_country, id_vars=["country"], prefix="T-")
    fig2 = px.bar(
        df_theme_country_melted,
        x="country",
        y="value",
        color="T",
        barmode="stack",
        labels={"country": "Country", "value": "Theme Share (%)", "T": "Theme"},
        title="Themes Across Countries"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Framing Strategies by Country ---
    st.markdown("### 🧠 Framing Strategies by Country")
    st.markdown("This chart shows how rhetorical framing varies across countries (e.g., moral, security, geopolitical).")
    df_framing_country_melted = melt_code_columns(df_framing_country, id_vars=["country"], prefix="F-")
    fig3 = px.bar(
        df_framing_country_melted,
        x="country",
        y="value",
        color="F",
        barmode="stack",
        labels={"country": "Country", "value": "Framing Share (%)", "F": "Framing"},
        title="Framing Strategies Across Countries"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("## 🏛️ Theme and Framing by US Administration")

    # --- Theme Distribution by Administration ---
    df_theme_admin = load_json(os.path.join(THEMES_FRAMING_DIR, "theme_by_administration.json"))
    df_theme_admin_melted = melt_code_columns(df_theme_admin, id_vars=["administration"], prefix="T-")

    st.markdown("### 📚 Theme Distribution by US Administration")
    st.markdown("This chart compares the distribution of themes during the Trump and Biden administrations.")
    fig4 = px.bar(
        df_theme_admin_melted,
        x="administration",
        y="value",
        color="T",
        barmode="stack",
        labels={"administration": "Administration", "value": "Theme Share (%)", "T": "Theme"},
        title="Themes by US Administration"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # --- Framing Distribution by Administration ---
    df_framing_admin = load_json(os.path.join(THEMES_FRAMING_DIR, "framing_by_administration.json"))
    df_framing_admin_melted = melt_code_columns(df_framing_admin, id_vars=["administration"], prefix="F-")

    st.markdown("### 🧠 Framing Strategies by US Administration")
    st.markdown("This chart displays rhetorical framing strategies (moral, geopolitical, security, etc.) used by Trump and Biden administrations.")
    fig5 = px.bar(
        df_framing_admin_melted,
        x="administration",
        y="value",
        color="F",
        barmode="stack",
        labels={"administration": "Administration", "value": "Framing Share (%)", "F": "Framing"},
        title="Framing Strategies by US Administration"
    )
    st.plotly_chart(fig5, use_container_width=True)

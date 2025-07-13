import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def load_json(path):
    return pd.read_json(path)

def show_rq2():
    st.title("📈 RQ2: Narrative Evolution Over Time")
    st.markdown("""
    This section explores **how narrative, theme, and framing codes have evolved over time** during the Ukraine conflict, based on tweets from MEPs and US administrators.

    Use the sidebar filter to focus on specific actor types (MEPs vs US Admins).
    """)

    # Sidebar
    st.sidebar.markdown("### Filters")
    actor_filter = st.sidebar.selectbox("Actor Type", ["All", "MEP", "US_Admin"])
    metric = st.sidebar.radio("Metric", ["Count", "Percent"])

    base_path = Path("insights")

    def filter_df(df, y_field):
        if "created_month" in df.columns and "month" not in df.columns:
            df = df.rename(columns={"created_month": "month"})

        # Fallback to 'count' if 'percent' not in the DataFrame
        ycol = "percent" if y_field == "Percent" and "percent" in df.columns else "count"
        return df, ycol

    #### 1. Narrative Over Time (Overall) ####
    st.subheader("🧭 Narrative Trends Over Time (All Actors)")
    df_narr = load_json(base_path / "rq2" / "narrative_over_time.json")
    df_narr, ycol = filter_df(df_narr, metric)
    fig = px.line(df_narr, x="month", y=ycol, color="narrative",
                  markers=True, labels={"month": "Date", ycol: metric})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Tracks how narrative types (Pro-Ukraine, Pro-Russia, Neutral) shift over time across all accounts.")

    #### 2. Narrative Over Time by Actor ####
    st.subheader("🧑‍⚖️ Narrative Trends by Actor Type")
    df_narr_actor = load_json(base_path / "rq2" / "narrative_over_time_by_actor_type.json")
    if actor_filter != "All":
        df_narr_actor = df_narr_actor[df_narr_actor["actor_type"] == actor_filter]
    df_narr_actor, ycol = filter_df(df_narr_actor, metric)
    fig2 = px.line(df_narr_actor, x="month", y=ycol, color="narrative", line_dash="actor_type",
                   markers=True, facet_col="actor_type", facet_col_wrap=2,
                   labels={"month": "Date", ycol: metric})
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Compares narrative evolution between MEPs and US administrators.")

    #### 3. Narrative Over Time by US Admin ####
    st.subheader("🇺🇸 Narrative Trends by US Administration")
    df_us = load_json(base_path / "rq2" / "narrative_over_time_by_us_admin.json")
    df_us, ycol = filter_df(df_us, metric)
    fig3 = px.line(df_us, x="month", y=ycol, color="narrative", line_dash="administration",
                   markers=True, facet_col="administration", facet_col_wrap=2,
                   labels={"month": "Date", ycol: metric})
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Compares narrative evolution between Trump and Biden administrations.")

    #### 4. Theme Over Time ####
    st.subheader("🎯 Themes Over Time")
    df_theme = load_json(base_path / "rq2_themes_framing" / "theme_monthly_by_actor.json")
    if actor_filter != "All":
        df_theme = df_theme[df_theme["actor_type"] == actor_filter]
    df_theme, ycol = filter_df(df_theme, metric)
    fig_theme = px.line(df_theme, x="month", y=ycol, color="code",
                        markers=True, facet_col="actor_type", facet_col_wrap=2,
                        labels={"month": "Date", ycol: metric})
    st.plotly_chart(fig_theme, use_container_width=True)
    st.caption("Shows which themes (e.g. sanctions, civilian impact, sovereignty) were most discussed over time.")

    #### 5. Framing Over Time ####
    st.subheader("🪞 Framing Over Time")
    df_frame = load_json(base_path / "rq2_themes_framing" / "framing_monthly_by_actor.json")
    if actor_filter != "All":
        df_frame = df_frame[df_frame["actor_type"] == actor_filter]
    df_frame, ycol = filter_df(df_frame, metric)
    fig_frame = px.line(df_frame, x="month", y=ycol, color="code",
                        markers=True, facet_col="actor_type", facet_col_wrap=2,
                        labels={"month": "Date", ycol: metric})
    st.plotly_chart(fig_frame, use_container_width=True)
    st.caption("Displays how rhetorical strategies (e.g. moral framing, security, demonization) changed over time.")

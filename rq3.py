import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def load_json(path):
    return pd.read_json(path)

def show_rq3():
    st.title("📊 RQ3: Engagement Dynamics")

    st.markdown("""
    This section analyzes engagement metrics (likes, retweets, replies, quotes) 
    across narratives, actors, and over time.

    Use the sidebar to select the engagement metric displayed in the charts.
    """)

    # Sidebar filter
    st.sidebar.markdown("### Filters")
    engagement_metric = st.sidebar.selectbox(
        "Select Engagement Metric",
        options=["total_engagement", "likeCount", "retweetCount", "replyCount", "quoteCount"],
        format_func=lambda x: {
            "total_engagement": "Total Engagement",
            "likeCount": "Likes",
            "retweetCount": "Retweets",
            "replyCount": "Replies",
            "quoteCount": "Quotes"
        }[x],
        index=0
    )

    base_path = Path("insights")

    #### 1. Total Engagement by Narrative & Actor Type ####
    st.subheader("Total Engagement by Narrative and Actor Type")
    df_actor = load_json(base_path / "rq3" / "narrative_engagement_by_actor_type.json")

    if engagement_metric != "total_engagement" and engagement_metric not in df_actor.columns:
        st.warning(f"Metric '{engagement_metric}' not available in dataset. Showing Total Engagement instead.")
        y_col = "total_engagement"
    else:
        y_col = engagement_metric

    fig_actor = px.bar(
        df_actor,
        x="narrative",
        y=y_col,
        color="actor_type",
        barmode="group",
        labels={"narrative": "Narrative Type", y_col: engagement_metric.replace("Count", "")},
        title="Engagement by Narrative and Actor Type"
    )
    st.plotly_chart(fig_actor, use_container_width=True)
    st.caption("Shows engagement split by narrative and actor type (MEPs vs US administrators).")

    #### 2. Engagement Trends Over Time ####
    st.subheader("Engagement Trends Over Time")
    df_time = load_json(base_path / "rq3" / "narrative_engagement_over_time.json")

    # Normalize time column
    if "created_month" in df_time.columns and "month" not in df_time.columns:
        df_time = df_time.rename(columns={"created_month": "month"})

    if engagement_metric != "total_engagement" and engagement_metric not in df_time.columns:
        y_col_time = "total_engagement"
    else:
        y_col_time = engagement_metric

    fig_time = px.line(
        df_time,
        x="month",
        y=y_col_time,
        color="narrative",
        markers=True,
        labels={"month": "Date", y_col_time: engagement_metric.replace("Count", "")},
        title="Engagement Over Time by Narrative"
    )
    st.plotly_chart(fig_time, use_container_width=True)
    st.caption("Tracks how engagement changes over time across narratives.")

    #### 3. Average Engagement per Tweet by Actor Type ####
    st.subheader("Average Engagement per Tweet by Actor Type")
    df_avg_actor = load_json(base_path / "rq3" / "narrative_avg_engagement_by_actor_type.json")

    # Always use 'avg_engagement' for average engagement datasets
    y_col_avg_actor = "avg_engagement"

    fig_avg_actor = px.bar(
        df_avg_actor,
        x="narrative",
        y=y_col_avg_actor,
        color="actor_type",
        barmode="group",
        labels={"narrative": "Narrative Type", y_col_avg_actor: f"Average {engagement_metric.replace('Count','')}"},
        title="Average Engagement per Tweet by Narrative and Actor Type"
    )
    st.plotly_chart(fig_avg_actor, use_container_width=True)
    st.caption("Shows average engagement per tweet to normalize popularity.")

    #### 4. Average Engagement per Tweet by US Administration ####
    st.subheader("Average Engagement per Tweet by US Administration")
    df_avg_admin = load_json(base_path / "rq3" / "narrative_avg_engagement_by_us_admin.json")

    # Always use 'avg_engagement' for average engagement datasets
    y_col_avg_admin = "avg_engagement"

    fig_avg_admin = px.bar(
        df_avg_admin,
        x="narrative",
        y=y_col_avg_admin,
        color="administration",
        barmode="group",
        labels={"narrative": "Narrative Type", y_col_avg_admin: f"Average {engagement_metric.replace('Count','')}"},
        title="Average Engagement per Tweet by Narrative and US Administration"
    )
    st.plotly_chart(fig_avg_admin, use_container_width=True)
    st.caption("Comparison of average engagement between Trump and Biden administrations.")

    #### 5. Bonus: Theme Engagement ####
    st.subheader("Bonus: Average Engagement by Themes")
    df_theme_eng = load_json(base_path / "rq3_themes_framing" / "theme_engagement.json")

    if engagement_metric not in df_theme_eng.columns:
        y_col_theme = "total_engagement"
    else:
        y_col_theme = engagement_metric

    fig_theme_eng = px.bar(
        df_theme_eng,
        x="code",
        y=y_col_theme,
        labels={"code": "Theme", y_col_theme: f"Average {engagement_metric.replace('Count','')}"},
        title="Average Engagement by Theme"
    )
    st.plotly_chart(fig_theme_eng, use_container_width=True)
    st.caption("Shows which themes receive more engagement on average.")

    #### 6. Bonus: Framing Engagement ####
    st.subheader("Bonus: Average Engagement by Framing")
    df_frame_eng = load_json(base_path / "rq3_themes_framing" / "framing_engagement.json")

    if engagement_metric not in df_frame_eng.columns:
        y_col_frame = "total_engagement"
    else:
        y_col_frame = engagement_metric

    fig_frame_eng = px.bar(
        df_frame_eng,
        x="code",
        y=y_col_frame,
        labels={"code": "Framing", y_col_frame: f"Average {engagement_metric.replace('Count','')}"},
        title="Average Engagement by Framing"
    )
    st.plotly_chart(fig_frame_eng, use_container_width=True)
    st.caption("Shows which framing strategies receive more engagement on average.")

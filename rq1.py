import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def load_json(path):
    return pd.read_json(path)

def show_rq1():
    st.title("📊 RQ1: Common Narrative, Theme, and Framing Codes")

    st.markdown("""
    This section shows the **distribution** of:
    - Narrative codes (`N-1`, `N-2`, `N-3`)
    - Theme codes (`T-1` to `T-5`)
    - Framing codes (`F-1` to `F-6`)
    
    Use the filters in the sidebar to explore how these codes differ by actor type (MEPs vs. US Admins), country, and administration.
    """)

    # Load data
    base_path = Path("insights")
    df_narr = load_json(base_path / "rq1" / "narrative_by_actor_type.json")
    df_theme = load_json(base_path / "rq1_themes_framing" / "theme_by_actor_type.json")
    df_framing = load_json(base_path / "rq1_themes_framing" / "framing_by_actor_type.json")
    df_authors = load_json(base_path / "rq4" / "narrative_shapers_leaderboard.json")

    # Sidebar filters
    st.sidebar.markdown("### Filters")
    actor_type = st.sidebar.selectbox("Actor Type", ["All", "MEP", "US_Admin"])
    metric = st.sidebar.radio("Metric", ["Count", "Percent"])
    top_n = st.sidebar.slider("Top Narrative Promoters", 5, 30, 15)

    def filter_df(df, code_col):
        if actor_type != "All":
            df = df[df["actor_type"] == actor_type]
        return df.groupby(code_col).agg(
            count=("count", "sum"),
            percent=("percent", "mean")
        ).reset_index()

    ### 1. Narrative ###
    st.subheader("🧭 Narrative Distribution")
    narr_plot = filter_df(df_narr, "narrative")
    ycol = "count" if metric == "Count" else "percent"
    fig_narr = px.bar(narr_plot, x="narrative", y=ycol, color="narrative",
                      text_auto='.2s' if metric == "Count" else '.2f',
                      labels={"narrative": "Narrative Code", ycol: metric})
    fig_narr.update_layout(showlegend=False)
    st.plotly_chart(fig_narr, use_container_width=True)
    st.caption("Distribution of narratives (e.g. N-1: Pro-Ukrainian, N-2: Pro-Russian, N-3: Neutral).")

    ### 2. Themes ###
    st.subheader("🎯 Themes Distribution")
    theme_plot = filter_df(df_theme, "themes")
    fig_theme = px.bar(theme_plot, x=ycol, y="themes", orientation="h", color="themes",
                       text_auto='.2s' if metric == "Count" else '.2f')
    fig_theme.update_layout(showlegend=False)
    st.plotly_chart(fig_theme, use_container_width=True)
    st.caption("Themes represent the focus of the tweet, like sanctions or civilian impact.")

    ### 3. Framing ###
    st.subheader("🪞 Framing Strategy Distribution")
    frame_plot = filter_df(df_framing, "framing")
    fig_frame = px.bar(frame_plot, x=ycol, y="framing", orientation="h", color="framing",
                       text_auto='.2s' if metric == "Count" else '.2f')
    fig_frame.update_layout(showlegend=False)
    st.plotly_chart(fig_frame, use_container_width=True)
    st.caption("Framing reflects how the tweet communicates its message — morally, strategically, emotionally, etc.")

    ### 4. Top Narrative Shapers ###
    st.subheader("🏅 Top Actors by Narrative")

    df_auth = df_authors.copy()

    if actor_type != "All":
        df_auth = df_auth[df_auth["actor_type"] == actor_type]

    # Expand narrative_distribution
    narr_df = df_auth["narrative_distribution"].apply(pd.Series)
    for col in ["N-1", "N-2", "N-3"]:
        narr_df[col] = (narr_df[col] / 100) * df_auth["tweet_count"]
    df_auth = pd.concat([df_auth, narr_df[["N-1", "N-2", "N-3"]]], axis=1)

    df_auth = df_auth.sort_values(by="tweet_count", ascending=False).head(top_n)

    fig_auth = px.bar(
        df_auth,
        x="userName",
        y=["N-1", "N-2", "N-3"],
        barmode="stack",
        labels={"value": "Estimated Tweet Count", "userName": "User", "variable": "Narrative"},
        title="Top Narrative Shapers (by Estimated Narrative Tweet Count)"
    )
    st.plotly_chart(fig_auth, use_container_width=True)
    st.caption("Each bar is estimated from tweet count × narrative distribution %. Helps highlight narrative focus of active accounts.")


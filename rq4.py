import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def load_json_with_rename(path):
    df = pd.read_json(path)
    if "author.userName" in df.columns:
        df.rename(columns={"author.userName": "userName"}, inplace=True)
    return df

def show_rq4():
    st.title("📊 RQ4: Main Narrative Shapers")

    st.markdown("""
    This section identifies and analyzes the key narrative shapers driving engagement.
    Use the filters below to narrow down by actor type, country, administration, or political group.
    Select one or more authors from the leaderboard to explore their narrative, theme, and framing distributions.
    """)

    base_path = Path("insights")

    # Load datasets
    df_leaderboard = load_json_with_rename(base_path / "rq4" / "narrative_shapers_leaderboard.json")
    df_theme_dist = load_json_with_rename(base_path / "rq4_themes_framing" / "theme_distribution_by_author.json")
    df_framing_dist = load_json_with_rename(base_path / "rq4_themes_framing" / "framing_distribution_by_author.json")

    # Fix for list fields to ensure filtering works
    for col in ["administration", "politicalGroup", "country"]:
        df_leaderboard[col] = df_leaderboard[col].apply(lambda x: x if isinstance(x, list) else [])

    # Sidebar Filters
    st.sidebar.header("Filters")
    actor_types = ["All"] + sorted(df_leaderboard["actor_type"].unique())
    selected_actor_type = st.sidebar.selectbox("Actor Type", actor_types)

    countries = ["All"] + sorted({c for sublist in df_leaderboard["country"] for c in sublist})
    selected_country = st.sidebar.selectbox("Country", countries)

    administrations = ["All"] + sorted({a for sublist in df_leaderboard["administration"] for a in sublist})
    selected_admin = st.sidebar.selectbox("Administration", administrations)

    political_groups = ["All"] + sorted({pg for sublist in df_leaderboard["politicalGroup"] for pg in sublist})
    selected_political_group = st.sidebar.selectbox("Political Group", political_groups)

    search_term = st.sidebar.text_input("Search by username or name").strip().lower()

    # Apply filters
    df_filtered = df_leaderboard.copy()

    if selected_actor_type != "All":
        df_filtered = df_filtered[df_filtered["actor_type"] == selected_actor_type]

    if selected_country != "All":
        df_filtered = df_filtered[df_filtered["country"].apply(lambda clist: selected_country in clist)]

    if selected_admin != "All":
        df_filtered = df_filtered[df_filtered["administration"].apply(lambda alist: selected_admin in alist)]

    if selected_political_group != "All":
        df_filtered = df_filtered[df_filtered["politicalGroup"].apply(lambda plist: selected_political_group in plist)]

    if search_term:
        df_filtered = df_filtered[
            df_filtered["userName"].str.lower().str.contains(search_term) |
            df_filtered["name"].str.lower().str.contains(search_term)
        ]

    # Sort by total engagement descending
    df_filtered = df_filtered.sort_values("total_engagement", ascending=False).reset_index(drop=True)

    st.write(f"### Leaderboard ({len(df_filtered)} authors)")

    # Show leaderboard table with selected columns
    leaderboard_display_cols = [
        "userName", "name", "actor_type", "followers", "tweet_count", "total_engagement"
    ]
    # Add narrative distribution columns
    for narrative_code in ["N-1", "N-2", "N-3"]:
        leaderboard_display_cols.append(f"narrative_{narrative_code}")

    # Flatten narrative_distribution dict into separate columns for display
    def flatten_narrative_dist(row):
        dist = row.get("narrative_distribution", {})
        for k in ["N-1", "N-2", "N-3"]:
            row[f"narrative_{k}"] = dist.get(k, 0.0)
        return row

    df_filtered = df_filtered.apply(flatten_narrative_dist, axis=1)

    st.dataframe(df_filtered[leaderboard_display_cols], use_container_width=True)

    # Select authors for detailed analysis
    st.markdown("### Select authors to analyze narrative, theme, and framing distribution")
    selected_authors = st.multiselect(
        "Select authors by username",
        options=df_filtered["userName"].tolist()
    )

    if not selected_authors:
        st.info("Select one or more authors from the leaderboard to see detailed distributions.")
        return

    # Filter theme and framing distributions by selected authors
    df_theme_sel = df_theme_dist[df_theme_dist["userName"].isin(selected_authors)]
    df_framing_sel = df_framing_dist[df_framing_dist["userName"].isin(selected_authors)]

    # Narrative distribution chart for selected authors
    st.markdown("### Narrative Distribution for Selected Authors")
    df_narrative_sel = df_filtered[df_filtered["userName"].isin(selected_authors)][
        ["userName", "narrative_N-1", "narrative_N-2", "narrative_N-3"]
    ]

    # Melt for plotly
    df_narrative_long = df_narrative_sel.melt(
        id_vars=["userName"],
        value_vars=["narrative_N-1", "narrative_N-2", "narrative_N-3"],
        var_name="Narrative",
        value_name="Percentage"
    )
    # Clean narrative names
    df_narrative_long["Narrative"] = df_narrative_long["Narrative"].str.replace("narrative_", "")

    fig_narrative = px.bar(
        df_narrative_long,
        x="userName",
        y="Percentage",
        color="Narrative",
        barmode="stack",
        title="Narrative Distribution per Author",
        labels={"userName": "Author Username", "Percentage": "Narrative Share (%)"}
    )
    st.plotly_chart(fig_narrative, use_container_width=True)

    # Theme distribution chart
    st.markdown("### Theme Distribution for Selected Authors")
    if df_theme_sel.empty:
        st.info("No theme distribution data available for selected authors.")
    else:
        theme_long = df_theme_sel.melt(id_vars=["userName"], var_name="code", value_name="value")
        fig_theme = px.bar(
            theme_long,
            x="userName",
            y="value",
            color="code",
            barmode="stack",
            title="Theme Distribution per Author",
            labels={"userName": "Author Username", "value": "Theme Share (%)", "code": "Theme"}
        )

        st.plotly_chart(fig_theme, use_container_width=True)

    # Framing distribution chart
    st.markdown("### Framing Distribution for Selected Authors")
    if df_framing_sel.empty:
        st.info("No framing distribution data available for selected authors.")
    else:
        framing_long = df_framing_sel.melt(id_vars=["userName"], var_name="code", value_name="value")
        fig_framing = px.bar(
            framing_long,
            x="userName",
            y="value",
            color="code",
            barmode="stack",
            title="Framing Distribution per Author",
            labels={"userName": "Author Username", "value": "Framing Share (%)", "code": "Framing"}
        )

        st.plotly_chart(fig_framing, use_container_width=True)

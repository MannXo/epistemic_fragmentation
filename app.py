# streamlit_app.py

import streamlit as st
import json
import pandas as pd
from pathlib import Path

from language_comparison import show_language_comparison
from rq1 import show_rq1
from rq2 import show_rq2
from rq3 import show_rq3
from rq4 import show_rq4
from rq5 import show_rq5


st.set_page_config(page_title="Ukraine Narrative Dashboard", layout="wide")

# === Load Insight Files ===
INSIGHTS_DIR = Path("output/insights")

# Helper to load JSON
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Intro Tab: Notation Definitions ===
def show_intro():
    st.title("🇺🇦 Narrative Analysis of Ukraine War Discourse")
    st.markdown("### Codebook: Narrative, Themes, and Framing")

    st.markdown("#### 🧭 Narrative Codes")
    st.markdown("""
- **N-1: Pro-Ukrainian** – Support for Ukrainian sovereignty, critique of Russian actions, highlighting resilience.
- **N-2: Pro-Russian** – Support for Russia, critique of Ukraine/NATO, or justification of aggression.
- **N-3: Neutral/Other** – No clear stance, factual, or procedural updates.
    """)

    st.markdown("#### 🧩 Thematic Codes")
    st.markdown("""
- **T-1: Sovereignty & Defense**
- **T-2: Western Support & Sanctions**
- **T-3: Russian Aggression & Justification**
- **T-4: Humanitarian & Civilian Impact**
- **T-5: Geopolitical Strategy & Power**
    """)

    st.markdown("#### 🎭 Framing Strategies")
    st.markdown("""
- **F-1: Moral Framing**
- **F-2: Security/Defense Framing**
- **F-3: Geopolitical/Economic Framing**
- **F-4: Demonization/Othering**
- **F-5: Victory/Resilience**
- **F-6: Crisis & Suffering**
    """)

    st.markdown("#### 👤 Actor Types")
    st.markdown("""
- **MEP** – Members of the European Parliament  
- **US_Admin** – U.S. officials from Trump/Biden administrations
    """)

# === Main App ===
def main():
    tab_names = [
        "📌 Intro",
        "📊 RQ1: Main Competing Narratives",
        "📈 RQ2: Narrative Trends Over Time",
        "🔥 RQ3: Narrative Popularity & Engagement Dynamics",
        "🧑‍🤝‍🧑 RQ4: Main Narrative Shapers and Per-Author View",
        "🌍 RQ5: Contextual Variations and Country/Admin Comparison",
        "🧪 Native vs Non-native Language Comparison",
    ]
    selected_tab = st.sidebar.radio("📂 Select Insight Tab", tab_names)

    if selected_tab == tab_names[0]:
        show_intro()
    elif selected_tab == tab_names[1]:
        show_rq1()
    elif selected_tab == tab_names[2]:
        show_rq2()
    elif selected_tab == tab_names[3]:
        show_rq3()
    elif selected_tab == tab_names[4]:
        show_rq4()
    elif selected_tab == tab_names[5]:
        show_rq5()
    elif selected_tab == tab_names[6]:
        show_language_comparison()
    # Other tabs will go here one-by-one

if __name__ == "__main__":
    main()

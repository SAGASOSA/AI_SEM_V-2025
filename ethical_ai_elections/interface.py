# interface.py
import streamlit as st
from recommender import NewsRecommender
from tracker import UserTracker

st.set_page_config(page_title="Ethical AI Elections", layout="centered")

st.title("🗳️ AI in Elections: Ethical Challenges")
st.markdown("This demo simulates how recommendation bias influences voter opinions.")

beta = st.sidebar.slider("Algorithmic Bias (β)", -1.0, 1.0, 0.0, 0.1)
query = st.text_input("Enter a topic or keyword:", "economy")

if 'recommender' not in st.session_state:
    st.session_state.recommender = NewsRecommender(beta=beta)
if 'tracker' not in st.session_state:
    st.session_state.tracker = UserTracker()

if st.button("Recommend for me"):
    recs = st.session_state.recommender.recommend(query)
    st.session_state.recs = recs

if 'recs' in st.session_state:
    st.subheader("Recommended Articles:")
    for _, row in st.session_state.recs.iterrows():
        st.write(f"**{row['headline']}**")
        st.caption(f"{row['source']} | Bias: {row['political_bias']}")
        col1, col2 = st.columns(2)
        if col1.button(f"Read - {row['headline']}"):
            st.session_state.tracker.log_interaction(row['headline'], row['political_bias'], 'read')
            st.success("Read logged ✅")
        if col2.button(f"Like - {row['headline']}"):
            st.session_state.tracker.log_interaction(row['headline'], row['political_bias'], 'like')
            st.info("Like logged ❤️")

    st.divider()
    st.metric("Left leaning", round(st.session_state.tracker.left_score, 2))
    st.metric("Right leaning", round(st.session_state.tracker.right_score, 2))

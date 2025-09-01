import streamlit as st
import random

st.set_page_config(page_title="Social Media Reel Analyzer", layout="wide")

st.title("📲 Social Media Reel Analyzer")
st.write("Prototype that fetches data from posts automatically and analyzes effects in real-time 🚀")

# ---------------- Dummy Reels Data ----------------
reels_data = [
    {
        "id": 1,
        "username": "travel_with_rahul",
        "caption": "Exploring the beauty of Bali 🌴✨",
        "hashtags": "#travel #bali #nature #wanderlust",
        "comments": ["Wow! Amazing 😍", "I want to go there!", "Scam! This is fake location!"],
        "likes": 1520,
    },
    {
        "id": 2,
        "username": "tech_guru",
        "caption": "5G will destroy your brain! ⚠️",
        "hashtags": "#tech #5G #health #scam",
        "comments": ["This is dangerous 😱", "Fake news, stop spreading lies!", "Thanks for info 👍"],
        "likes": 892,
    },
    {
        "id": 3,
        "username": "funny_memes",
        "caption": "POV: When you wake up late 😂",
        "hashtags": "#funny #meme #relatable #lol",
        "comments": ["Hahaha so true!", "This made my day!", "Toxic content!"],
        "likes": 5021,
    },
]

# ---------------- Dummy AI Analysis ----------------
def analyze_reel(caption, hashtags, comments):
    toxic_keywords = ["hate", "kill", "fake", "scam", "vulgar", "abuse"]
    toxicity_score = random.randint(10, 95)
    fake_score = random.randint(5, 80)
    impact_score = random.randint(20, 95)

    # Keyword-based toxicity boost
    for word in toxic_keywords:
        if word in caption.lower() or any(word in c.lower() for c in comments):
            toxicity_score += 15
            break
    toxicity_score = min(toxicity_score, 100)

    insight = ""
    if toxicity_score > 70:
        insight = "⚠️ High negativity detected in this reel/post."
    elif fake_score > 60:
        insight = "⚠️ Content may contain misinformation."
    else:
        insight = "✅ Looks safe and positive."

    return fake_score, toxicity_score, impact_score, insight

def predict_comment_effect(comment):
    toxic_words = ["stupid", "idiot", "hate", "kill", "abuse"]
    effect_score = random.randint(10, 90)
    for word in toxic_words:
        if word in comment.lower():
            effect_score += 20
            break
    return min(effect_score, 100)

# ---------------- UI: Reels Display ----------------
st.subheader("🎥 Trending Reels / Posts")

# Display all reels like Instagram cards
for reel in reels_data:
    with st.container():
        st.markdown("---")
        st.markdown(f"**👤 {reel['username']}**")
        st.markdown(f"📝 **Caption:** {reel['caption']}")
        st.markdown(f"🏷️ **Hashtags:** {reel['hashtags']}")
        st.markdown(f"❤️ **Likes:** {reel['likes']}")
        st.markdown(f"💬 **Top Comments:**")
        for c in reel['comments']:
            st.markdown(f"- {c}")

        # Analyze button
        if st.button(f"🔍 Analyze Reel #{reel['id']}", key=f"analyze_{reel['id']}"):
            fake_score, toxicity_score, impact_score, insight = analyze_reel(
                reel["caption"], reel["hashtags"], reel["comments"]
            )

            # Show results
            col1, col2, col3 = st.columns(3)
            col1.metric("🕵️ Fake Probability", f"{fake_score}%")
            col2.metric("☣️ Toxicity Level", f"{toxicity_score}%")
            col3.metric("📈 Impact Prediction", f"{impact_score}%")
            st.info(f"**Insight:** {insight}")

            # Mental health alert
            if toxicity_score >= 70:
                st.error("⚠️ ALERT: This content may negatively affect your mental health!")

# ---------------- Comment Impact Predictor ----------------
st.subheader("💬 Predict Your Comment's Impact")
user_comment = st.text_input("Type your comment here...")
if user_comment:
    effect_score = predict_comment_effect(user_comment)
    st.metric("🔮 Comment Effect Score", f"{effect_score}%")
    if effect_score > 70:
        st.warning("⚠️ Your comment may have a negative impact!")

# ---------------- Footer ----------------
st.markdown("---")
st.caption("🚀 Hackathon Prototype | Dummy AI + Streamlit UI | Social Media Integrated Concept")

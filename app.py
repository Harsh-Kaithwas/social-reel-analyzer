import streamlit as st
import random
from typing import List, Dict

st.set_page_config(page_title="Reels Prototype — Instagram-style", layout="centered")

# ----------------- Styling (no HTML comments) -----------------
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] { background: #0b0b0b; color: #f1f5f9; }
    header { visibility: hidden; height: 0; }
    .feed { width: min(480px, 96vw); margin: 10px auto 40px auto; }

    .reel-card {
        position: relative; width: 100%; height: 78vh; border-radius: 16px; overflow: hidden;
        background: #0f1115; margin: 22px 0; box-shadow: 0 10px 30px rgba(0,0,0,.6);
    }
    .reel-media { width: 100%; height: 100%; object-fit: cover; filter: saturate(1.05) contrast(1.02); }

    .actions {
        position: absolute; right: 12px; bottom: 18px; display: flex; flex-direction: column; gap: 12px; z-index: 4;
    }
    .action-btn {
        width: 52px; height: 52px; border-radius: 999px; background: rgba(17,19,24,0.78);
        display: grid; place-items: center; font-size: 22px; color: #fff;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .action-label { text-align:center; font-size:11px; opacity:.8; margin-top:4px; color:#cbd5e1; }

    .meta { position: absolute; left: 14px; bottom: 18px; right: 92px; z-index: 3; text-shadow:0 2px 14px rgba(0,0,0,.55); }
    .user { font-weight:700; font-size:15px; }
    .cap { font-size:14px; margin-top:6px; opacity:.98; }
    .tags { font-size:13px; margin-top:6px; opacity:.82; color:#cbd5e1; }
    .likes { font-size:12px; margin-top:6px; opacity:.7; }

    .overlay { position: fixed; inset: 0; background: rgba(0,0,0,.54); backdrop-filter: blur(4px); z-index: 90; }
    .modal {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%);
        width: min(520px, 94vw); background: #0f1115; border-radius: 12px; padding: 16px;
        z-index: 99; border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 30px 60px rgba(0,0,0,.6);
    }
    .chip { display:inline-block; padding:8px 10px; border-radius:10px; background:#121316; margin-right:8px; border:1px solid rgba(255,255,255,0.04); }

    .drawer {
        position: fixed; left: 0; right: 0; bottom: 0; background: #0e1014;
        border-top-left-radius: 16px; border-top-right-radius:16px; z-index:95;
        max-height: 70vh; padding: 12px 14px 18px 14px; border:1px solid rgba(255,255,255,0.06); overflow-y:auto;
    }
    .drawer-handle { width: 44px; height:6px; background: rgba(255,255,255,0.12); margin:6px auto 12px auto; border-radius:999px; }
    .comment { padding:8px 0; border-bottom: 1px solid rgba(255,255,255,0.04); color:#e6eef8; }
    .muted { color:#cbd5e1; opacity:.7; font-size:12px; margin-bottom:12px; }
    .chip-warn { background: #2a1216; border-color:#b91c1c; padding:8px 10px; border-radius:8px; display:inline-block; color:#ffd7d7; }
    .chip-ok { background:#071b12; border-color:#064e3b; padding:8px 10px; border-radius:8px; display:inline-block; color:#bfeadf; }
    .xbtn { border:1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); padding:6px 10px; border-radius:10px; color:#fff; cursor:pointer; }

    /* small responsive tweak */
    @media (max-width: 520px) {
        .reel-card { height: 70vh; border-radius:12px; }
        .actions { right: 8px; bottom: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Dummy reels -----------------
Reel = Dict[str, str]
reels: List[Reel] = [
    {"id": "1", "user": "travel_with_rahul",
     "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1080&auto=format&fit=crop",
     "caption": "Exploring the beauty of Bali 🌴✨",
     "tags": "#travel #bali #nature #wanderlust", "likes": "1,520",
     "comments": ["Wow! Amazing 😍", "I want to go there!", "Scam! This is fake location!"]},
    {"id": "2", "user": "tech_guru",
     "img": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1080&auto=format&fit=crop",
     "caption": "5G will destroy your brain! ⚠️",
     "tags": "#tech #5G #health #scam", "likes": "892",
     "comments": ["This is dangerous 😱", "Fake news, stop spreading lies!", "Thanks for info 👍"]},
    {"id": "3", "user": "funny_memes",
     "img": "https://images.unsplash.com/photo-1549480017-d76466a4b7b4?q=80&w=1080&auto=format&fit=crop",
     "caption": "POV: When you wake up late 😂", "tags": "#funny #meme #relatable #lol",
     "likes": "5,021", "comments": ["Hahaha so true!", "This made my day!", "Toxic content!"]},
    {"id": "4", "user": "fitness_guru",
     "img": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1080&auto=format&fit=crop",
     "caption": "Daily workout is the best medicine 🏋️‍♂️🔥", "tags": "#fitness #gym #motivation",
     "likes": "2,310", "comments": ["Let's hit the gym!", "Best motivation ever 💪", "Fake body, fake workout!"]},
    {"id": "5", "user": "world_news",
     "img": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1080&auto=format&fit=crop",
     "caption": "BREAKING: Miracle cure discovered for everything 😮", "tags": "#news #health #miracle",
     "likes": "18,420", "comments": ["Seems fake 🤔", "Source??", "If true, this changes everything!"]},
]

# ----------------- Session state -----------------
if "open_drawer_for" not in st.session_state:
    st.session_state.open_drawer_for = None
if "open_modal_for" not in st.session_state:
    st.session_state.open_modal_for = None
if "comment_inputs" not in st.session_state:
    st.session_state.comment_inputs = {r["id"]: "" for r in reels}

# ----------------- Dummy AI functions -----------------
def analyze(caption: str, tags: str, comments: List[str]):
    tox_words = ["hate", "kill", "fake", "scam", "vulgar", "abuse", "destroy"]
    tox = random.randint(10, 95)
    fake = random.randint(5, 80)
    impact = random.randint(20, 95)
    blob = (caption + " " + tags + " " + " ".join(comments)).lower()
    if any(w in blob for w in tox_words):
        tox = min(100, tox + 15)
    if "miracle" in blob or "cure" in blob:
        fake = min(100, fake + 20)
    if tox > 70:
        insight = "⚠️ High negativity detected in this reel/post."
    elif fake > 60:
        insight = "⚠️ Content may contain misinformation."
    else:
        insight = "✅ Looks safe and positive."
    return fake, tox, impact, insight

def predict_comment_effect(text: str) -> int:
    base = random.randint(10, 90)
    if any(w in text.lower() for w in ["stupid","idiot","hate","kill","abuse","fake"]):
        base = min(100, base + 20)
    return base

# ----------------- Header -----------------
st.markdown("<div style='text-align:center;margin-top:6px;margin-bottom:8px;opacity:.85'>"
            "Instagram-style Reels • Prototype (only Comment & Analyze interactive)</div>", unsafe_allow_html=True)

# ----------------- Feed -----------------
st.markdown('<div class="feed">', unsafe_allow_html=True)

for r in reels:
    # Render the reel-card block via HTML
    st.markdown(
        f"""
        <div class="reel-card">
            <img class="reel-media" src="{r['img']}" alt="reel">
            <div class="actions">
                <div class="action-btn" title="Likes">❤️</div>
                <div class="action-label">{r['likes']}</div>

                <div class="action-btn" title="Comment">💬</div>
                <div class="action-label">Comment</div>

                <div class="action-btn" title="Share">📤</div>
                <div class="action-label">Share</div>

                <div class="action-btn" title="More">⋮</div>
                <div class="action-label">More</div>

                <div class="action-btn" title="Analyze">🧠</div>
                <div class="action-label">Analyze</div>
            </div>

            <div class="meta">
                <div class="user">@{r['user']}</div>
                <div class="cap">{r['caption']}</div>
                <div class="tags">{r['tags']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Real (Streamlit) buttons placed right after the card for interaction:
    cols = st.columns([1,1,1,1,1])
    # Only Comment and Analyze will be active/clickable
    _ = cols[0].button("    ❤️    ", key=f"like_{r['id']}", disabled=True)
    if cols[1].button("💬  Open comments", key=f"comment_{r['id']}"):
        st.session_state.open_drawer_for = r["id"]
    _ = cols[2].button("📤  Share", key=f"share_{r['id']}", disabled=True)
    _ = cols[3].button("⋮  More", key=f"more_{r['id']}", disabled=True)
    if cols[4].button("🧠  Analyze", key=f"analyze_{r['id']}"):
        st.session_state.open_modal_for = r["id"]

st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Drawer: Comments -----------------
if st.session_state.open_drawer_for is not None:
    rid = st.session_state.open_drawer_for
    reel = next(x for x in reels if x["id"] == rid)
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)

    # Drawer content
    st.markdown('<div class="drawer">', unsafe_allow_html=True)
    st.markdown('<div class="drawer-handle"></div>', unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'><div style='font-weight:700'>Comments • @{reel['user']}</div>"
                f"<div></div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='muted'>Swipe/scroll to view comments</div>", unsafe_allow_html=True)

    for c in reel["comments"]:
        st.markdown(f'<div class="comment">{c}</div>', unsafe_allow_html=True)

    # comment input
    user_key = f"comment_input_{rid}"
    txt = st.text_input("Type your comment here…", key=user_key, label_visibility="collapsed")
    if txt:
        score = predict_comment_effect(txt)
        if score > 70:
            st.markdown(f'<div style="margin-top:8px;" class="chip-warn">🔮 Comment Effect Score: {score}% — might have negative impact</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-top:8px;" class="chip-ok">🔮 Comment Effect Score: {score}% — looks okay</div>', unsafe_allow_html=True)

    if st.button("Close comments", key="close_comments"):
        st.session_state.open_drawer_for = None

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Modal: Analysis -----------------
if st.session_state.open_modal_for is not None:
    rid = st.session_state.open_modal_for
    reel = next(x for x in reels if x["id"] == rid)
    fake, tox, impact, insight = analyze(reel["caption"], reel["tags"], reel["comments"])

    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="modal">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0 0 10px 0;'>🧠 Reel Analysis • @{reel['user']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:10px;'>"
                f"<span class='chip'>🕵️ Fake: <b>{fake}%</b></span>"
                f"<span class='chip'>☣️ Toxicity: <b>{tox}%</b></span>"
                f"<span class='chip'>📈 Impact: <b>{impact}%</b></span>"
                f"</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:10px;' class='chip'>{insight}</div>", unsafe_allow_html=True)
    if tox >= 70:
        st.markdown("<div class='chip-warn' style='margin-bottom:10px;'>⚠️ This content may negatively affect thinking / mental health.</div>", unsafe_allow_html=True)

    if st.button("Close", key="close_modal"):
        st.session_state.open_modal_for = None

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Footer -----------------
st.markdown("<div style='text-align:center; opacity:.55; margin-top:18px;'>Prototype • Only Comment & Analyze interactive • Dummy AI</div>", unsafe_allow_html=True)

import streamlit as st
import random
from typing import List, Dict

# =========================
# Page / Theme
# =========================
st.set_page_config(page_title="Reels Prototype — Instagram-style", layout="centered")

# Small CSS reset + IG-like styling
st.markdown(
    """
    <style>
        /* Page background + font */
        html, body, [data-testid="stAppViewContainer"] {
            background: #0b0b0b;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji","Segoe UI Emoji";
        }
        /* Remove default top padding */
        [data-testid="stHeader"] { background: transparent; }
        header { visibility: hidden; height: 0; }
        /* Feed wrapper */
        .feed {
            width: min(480px, 96vw);
            margin: 0 auto;
        }
        /* Reel card */
        .reel-card {
            position: relative;
            width: 100%;
            height: 78vh;           /* tall, like reels */
            border-radius: 18px;
            overflow: hidden;
            background: #111318;
            box-shadow: 0 8px 26px rgba(0,0,0,.45);
            margin: 24px 0;
        }
        .reel-media {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: saturate(1.05) contrast(1.02);
            user-select: none;
            -webkit-user-drag: none;
        }
        /* Right actions column (overlaid) */
        .actions {
            position: absolute;
            right: 10px;
            bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            z-index: 4;
        }
        .action-btn {
            width: 48px;
            height: 48px;
            border-radius: 999px;
            background: rgba(17,19,24,0.72);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.08);
            display: grid;
            place-items: center;
            font-size: 22px;
            cursor: default;
            transition: transform .08s ease;
        }
        .action-btn.clickable { cursor: pointer; }
        .action-btn:active { transform: scale(0.96); }
        .action-label {
            text-align: center;
            font-size: 12px;
            opacity: .8;
            margin-top: -6px;
        }

        /* Caption/Meta footer */
        .meta {
            position: absolute;
            left: 14px;
            bottom: 18px;
            right: 80px;  /* leave room for actions */
            color: #f8fafc;
            z-index: 3;
            text-shadow: 0 2px 12px rgba(0,0,0,.55);
        }
        .user { font-weight: 700; font-size: 15px; }
        .cap { font-size: 14px; opacity: .95; margin-top: 4px; }
        .tags { font-size: 13px; opacity: .8; margin-top: 4px; }
        .likes { font-size: 12px; opacity: .75; margin-top: 6px; }

        /* Overlay dimmer */
        .overlay {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,.55);
            -webkit-backdrop-filter: blur(4px);
            backdrop-filter: blur(4px);
            z-index: 90;
        }
        /* Analysis modal */
        .modal {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%,-50%);
            width: min(520px, 94vw);
            background: #0f1115;
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 16px;
            box-shadow: 0 30px 60px rgba(0,0,0,.6);
            padding: 18px;
            z-index: 99;
        }
        .modal h3 { margin: 0 0 10px 0; }
        .chip {
            padding: 8px 10px;
            border-radius: 12px;
            background: #141824;
            border: 1px solid rgba(255,255,255,.06);
            font-size: 14px;
        }
        .warn { background: #2a1216; border-color:#b91c1c; }
        .ok { background: #10271c; border-color:#166534; }

        /* Drawer (comments) */
        .drawer {
            position: fixed;
            left: 0; right: 0;
            bottom: 0;
            background: #0e1014;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
            border: 1px solid rgba(255,255,255,.08);
            z-index: 95;
            max-height: 70vh;
            box-shadow: 0 -24px 48px rgba(0,0,0,.5);
            padding: 12px 14px 16px 14px;
            overflow-y: auto;
        }
        .drawer-handle {
            width: 44px; height: 5px;
            background: rgba(255,255,255,.18);
            margin: 4px auto 12px auto;
            border-radius: 999px;
        }
        .comment { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
        .comment:last-child { border-bottom: none; }
        .muted { color: #cbd5e1; opacity: .7; font-size: 12px; }
        .row { display: flex; gap: 8px; align-items: center; }
        .grow { flex: 1; }

        /* Tiny close button */
        .x {
            border: 1px solid rgba(255,255,255,.12);
            background: rgba(255,255,255,.06);
            border-radius: 10px;
            padding: 6px 10px;
            cursor: pointer;
            font-size: 13px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Dummy data
# =========================
Reel = Dict[str, str]
reels: List[Reel] = [
    {
        "id": "1",
        "user": "travel_with_rahul",
        "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1080&auto=format&fit=crop",
        "caption": "Exploring the beauty of Bali 🌴✨",
        "tags": "#travel #bali #nature #wanderlust",
        "likes": "1,520",
        "comments": ["Wow! Amazing 😍", "I want to go there!", "Scam! This is fake location!"],
    },
    {
        "id": "2",
        "user": "tech_guru",
        "img": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1080&auto=format&fit=crop",
        "caption": "5G will destroy your brain! ⚠️",
        "tags": "#tech #5G #health #scam",
        "likes": "892",
        "comments": ["This is dangerous 😱", "Fake news, stop spreading lies!", "Thanks for info 👍"],
    },
    {
        "id": "3",
        "user": "funny_memes",
        "img": "https://images.unsplash.com/photo-1549480017-d76466a4b7b4?q=80&w=1080&auto=format&fit=crop",
        "caption": "POV: When you wake up late 😂",
        "tags": "#funny #meme #relatable #lol",
        "likes": "5,021",
        "comments": ["Hahaha so true!", "This made my day!", "Toxic content!"],
    },
    {
        "id": "4",
        "user": "fitness_guru",
        "img": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1080&auto=format&fit=crop",
        "caption": "Daily workout is the best medicine 🏋️‍♂️🔥",
        "tags": "#fitness #gym #motivation",
        "likes": "2,310",
        "comments": ["Let's hit the gym!", "Best motivation ever 💪", "Fake body, fake workout!"],
    },
    {
        "id": "5",
        "user": "world_news",
        "img": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1080&auto=format&fit=crop",
        "caption": "BREAKING: Miracle cure discovered for everything 😮",
        "tags": "#news #health #miracle",
        "likes": "18,420",
        "comments": ["Seems fake 🤔", "Source??", "If true, this changes everything!"],
    },
]

# =========================
# Session state
# =========================
if "open_drawer_for" not in st.session_state:
    st.session_state.open_drawer_for = None     # reel.id with drawer open
if "open_modal_for" not in st.session_state:
    st.session_state.open_modal_for = None      # reel.id with analysis open
if "comment_inputs" not in st.session_state:
    st.session_state.comment_inputs = {}        # reel.id -> string

# =========================
# Dummy AI
# =========================
def analyze(caption: str, tags: str, comments: List[str]):
    tox_words = ["hate", "kill", "fake", "scam", "vulgar", "abuse", "destroy"]
    tox = random.randint(10, 95)
    fake = random.randint(5, 80)
    impact = random.randint(20, 95)
    lower_blob = (caption + " " + tags + " " + " ".join(comments)).lower()
    if any(w in lower_blob for w in tox_words):
        tox = min(100, tox + 15)
    if "miracle" in lower_blob or "cure" in lower_blob:
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

# =========================
# Helpers (buttons acting like IG icons)
# =========================
def icon_button(label: str, key: str, clickable=True) -> bool:
    """Render an icon-like button; returns clicked bool."""
    cols = st.columns([1])  # keep it simple; Streamlit reruns anyway
    with cols[0]:
        if clickable:
            return st.button(label, key=key, use_container_width=True)
        else:
            st.button(label, key=key, use_container_width=True, disabled=True)
            return False

# =========================
# Header
# =========================
st.markdown(
    "<div style='text-align:center;margin-top:6px;margin-bottom:8px;opacity:.8'>"
    "Instagram-style Reels • Prototype (only 💬 Comment & 🧠 Analyze are clickable)"
    "</div>",
    unsafe_allow_html=True,
)

# =========================
# Feed
# =========================
st.markdown('<div class="feed">', unsafe_allow_html=True)

for r in reels:
    # Reel container (image + overlaid actions + footer meta)
    st.markdown(f"""
        <div class="reel-card">
            <img class="reel-media" src="{r['img']}" alt="reel" />
            <div class="actions">
                <div class="action-btn">❤️</div>
                <div class="action-label">{r['likes']}</div>

                <!-- Comment (clickable via real button rendered next to it) -->
                <div class="action-btn clickable">💬</div>
                <div class="action-label">Comment</div>

                <div class="action-btn">📤</div>
                <div class="action-label">Share</div>

                <div class="action-btn">⋮</div>
                <div class="action-label">More</div>

                <!-- Analyze (clickable via real button rendered next to it) -->
                <div class="action-btn clickable">🧠</div>
                <div class="action-label">Analyze</div>
            </div>
            <div class="meta">
                <div class="user">@{r['user']}</div>
                <div class="cap">{r['caption']}</div>
                <div class="tags">{r['tags']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Invisible grid of two real buttons positioned just under the card (matches the two clickable icons)
    bcols = st.columns([1,1])
    open_comment = bcols[0].button("💬  Open comments", key=f"btn_comment_{r['id']}")
    open_analyze = bcols[1].button("🧠  Analyze", key=f"btn_analyze_{r['id']}")

    if open_comment:
        st.session_state.open_drawer_for = r["id"]
    if open_analyze:
        st.session_state.open_modal_for = r["id"]

# Close feed wrapper
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Overlays: Drawer (comments)
# =========================
open_draw = st.session_state.open_drawer_for
if open_draw is not None:
    rr = next(x for x in reels if x["id"] == open_draw)
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    # Drawer UI
    st.markdown(
        f"""
        <div class="drawer">
            <div class="drawer-handle"></div>
            <div class="row" style="justify-content: space-between; align-items:center; margin-bottom:6px;">
                <div style="font-weight:700;">Comments • @{rr['user']}</div>
                </div>
            <div class="muted" style="margin-bottom:10px;">Swipe/scroll to view all</div>
        """,
        unsafe_allow_html=True,
    )

    # Existing comments
    for c in rr["comments"]:
        st.markdown(f'<div class="comment">{c}</div>', unsafe_allow_html=True)

    # Comment input + live impact
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    user_key = f"comment_input_{rr['id']}"
    txt = st.text_input("Type your comment here…", key=user_key, label_visibility="collapsed", placeholder="Type your comment here…")
    if txt:
        score = predict_comment_effect(txt)
        if score > 70:
            st.markdown(f'<div class="chip warn">🔮 Comment Effect Score: {score}% — might have negative impact</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chip ok">🔮 Comment Effect Score: {score}% — looks okay</div>', unsafe_allow_html=True)

    # Close button
    if st.button("Close", key="close_drawer", type="secondary"):
        st.session_state.open_drawer_for = None

    # End drawer container
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Overlays: Modal (analysis)
# =========================
open_modal = st.session_state.open_modal_for
if open_modal is not None:
    rr = next(x for x in reels if x["id"] == open_modal)
    fake, tox, imp, insight = analyze(rr["caption"], rr["tags"], rr["comments"])

    # Dim + modal
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="modal">
            <h3>🧠 Reel Analysis • @{rr['user']}</h3>
            <div class="row" style="gap:8px; margin-bottom:10px;">
                <div class="chip">🕵️ Fake Probability: <b>{fake}%</b></div>
                <div class="chip">☣️ Toxicity Level: <b>{tox}%</b></div>
                <div class="chip">📈 Impact Prediction: <b>{imp}%</b></div>
            </div>
            <div class="chip" style="margin-bottom:12px;">{insight}</div>
            {"<div class='chip warn' style='margin-bottom:10px;'>⚠️ This content may negatively affect your thinking / mental health.</div>" if tox >= 70 else ""}
        """,
        unsafe_allow_html=True,
    )

    # Close modal button
    if st.button("Close", key="close_modal", type="secondary"):
        st.session_state.open_modal_for = None

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown(
    "<div style='text-align:center; opacity:.55; margin-top:24px;'>"
    "Prototype • Only 💬 Comment & 🧠 Analyze are interactive • Dummy AI scoring"
    "</div>",
    unsafe_allow_html=True,
)

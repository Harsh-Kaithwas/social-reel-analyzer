# app.py
import streamlit as st
import os
import json
import random
import hashlib
from typing import List, Dict

# ---------------- Page config ----------------
st.set_page_config(page_title="Instagram Reels Prototype", layout="centered", initial_sidebar_state="collapsed")

# ---------------- Paths ----------------
ROOT = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()

# ---------------- Helpers ----------------
def safe_read(path: str) -> str:
    try:
        with open(os.path.join(ROOT, path), "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def load_json(path: str):
    try:
        with open(os.path.join(ROOT, path), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def hash_to_seed(s: str) -> int:
    """Return small deterministic integer from string for picsum seed."""
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    # use last 6 hex digits to create an int (keeps value moderate)
    return int(h[-6:], 16) % 1000 + 1

def icon_img_tag(name: str, size: int = 28, alt: str = "") -> str:
    svg_path = os.path.join(ROOT, "icons", f"{name}.svg")
    if os.path.exists(svg_path):
        # Streamlit serves files from repo root path correctly when used as relative src
        return f'<img src="icons/{name}.svg" width="{size}" height="{size}" alt="{alt}" />'
    emoji_map = {
        "like": "❤️",
        "comment": "💬",
        "share": "📤",
        "more": "⋮",
        "analyze": "🧠"
    }
    return emoji_map.get(name, "❖")

# ---------------- Default dummy data ----------------
DEFAULT_REELS = [
    {"id": "reel1", "user": "world_news", "caption": "NASA confirms water on the Moon! 🌕🚀", "hashtags": "#NASA #Space #Science", "type": "real", "sentiment": "positive", "media": "assets/reel1.jpg", "likes": "18.4K"},
    {"id": "reel2", "user": "trending_now", "caption": "Aliens landed in Times Square! 👽😂", "hashtags": "#Breaking #Aliens #NYC", "type": "fake", "sentiment": "negative", "media": "assets/reel2.jpg", "likes": "9.8K"},
    {"id": "reel3", "user": "motivation_daily", "caption": "Believe in yourself. The world is yours. 💪✨", "hashtags": "#Motivation #Positivity", "type": "real", "sentiment": "positive", "media": "assets/reel3.jpg", "likes": "5.0K"},
    {"id": "reel4", "user": "cancel_trends", "caption": "Famous influencer faces massive backlash! 🚨🔥", "hashtags": "#CancelCulture #Drama", "type": "real", "sentiment": "negative", "media": "assets/reel4.jpg", "likes": "12.1K"},
    {"id": "reel5", "user": "health_tips", "caption": "Drink lemon water every morning 🍋", "hashtags": "#Health #Fitness #Tips", "type": "real", "sentiment": "positive", "media": "assets/reel5.jpg", "likes": "2.3K"},
]

DEFAULT_COMMENTS = {
    "reel1": ["This is amazing! 🚀", "Science rocks!", "Can't wait for Moon missions!"],
    "reel2": ["Lol fake news 🤣", "Where's the proof?", "Clickbait as usual."],
    "reel3": ["Needed this today 💜", "Positive vibes only ✨", "Love it!"],
    "reel4": ["Cancel culture again 😑", "People need to chill ✋", "This is exhausting."],
    "reel5": ["Healthy tips 👍", "Thanks for sharing ❤️", "Great reminder."]
}

# ---------------- Load external data if present ----------------
reels_from_file = load_json("data/reels.json")
comments_from_file = load_json("data/comments.json")

REELS: List[Dict] = reels_from_file if isinstance(reels_from_file, list) and len(reels_from_file) >= 1 else DEFAULT_REELS
COMMENTS_STORE: Dict[str, List[str]] = comments_from_file if isinstance(comments_from_file, dict) else DEFAULT_COMMENTS

# ---------------- Load custom CSS if available, else fallback ----------------
external_css = safe_read("static/style.css")
if external_css.strip():
    st.markdown(f"<style>{external_css}</style>", unsafe_allow_html=True)
else:
    # Fallback CSS (keeps visual polished)
    st.markdown("""
    <style>
      :root{--bg:#050507; --card:#0d0f12; --muted:#9aa6b2}
      html,body,[data-testid="stAppViewContainer"]{background:var(--bg); color:#eef2ff}
      .feed{max-width:520px; margin:8px auto 48px auto; padding:6px}
      .reel{position:relative; width:100%; height:78vh; border-radius:14px; overflow:hidden; background:#000; margin:18px 0; box-shadow:0 12px 30px rgba(0,0,0,0.6)}
      .reel img{width:100%; height:100%; object-fit:cover; display:block}
      .actions{position:absolute; right:12px; bottom:20px; display:flex; flex-direction:column; gap:12px; align-items:center; z-index:5}
      .icon{width:48px; height:48px; border-radius:999px; background:rgba(0,0,0,0.45); display:grid; place-items:center; font-size:20px; color:#fff; border:1px solid rgba(255,255,255,0.04)}
      .meta{position:absolute; left:12px; bottom:20px; right:96px; z-index:4; text-shadow:0 2px 12px rgba(0,0,0,0.6)}
      .user{font-weight:700; font-size:15px}
      .cap{font-size:14px; margin-top:6px}
      .tags{font-size:13px; color:var(--muted); margin-top:6px}
      .likes{font-size:12px; color:var(--muted); margin-top:6px}
      .overlay{position:fixed; inset:0; background:rgba(0,0,0,0.56); z-index:90; backdrop-filter: blur(3px)}
      .modal{position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); z-index:92; background:var(--card); padding:14px; border-radius:12px; border:1px solid rgba(255,255,255,0.03); width:min(520px,92vw)}
      .chip{display:inline-block; padding:8px 10px; border-radius:10px; background:#0b1112; margin-right:8px; border:1px solid rgba(255,255,255,0.02)}
      .warn{background:#2a1216; border-color:#7f1d1d; color:#ffd7d7}
      .drawer{position:fixed; left:0; right:0; bottom:0; background:#0b0d10; z-index:95; border-top-left-radius:12px; border-top-right-radius:12px; padding:12px 14px; max-height:70vh; overflow:auto; border:1px solid rgba(255,255,255,0.03)}
      .comment-row{padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.03); color:#e6eef8}
      .muted{color:#9aa6b2; opacity:.9; margin-bottom:8px}
      .input{width:100%; padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.04); background:#071018; color:#fff; margin-top:8px}
      .btn{padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.03); background:rgba(255,255,255,0.02); color:#fff}
      .footer{opacity:.6; text-align:center; margin-top:14px}
      @media (max-width:520px){ .reel{height:72vh} .actions{right:8px; bottom:14px} }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Session state ----------------
if "open_drawer" not in st.session_state:
    st.session_state.open_drawer = None  # reel id
if "open_modal" not in st.session_state:
    st.session_state.open_modal = None   # reel id
if "comment_inputs" not in st.session_state:
    st.session_state.comment_inputs = {r["id"]: "" for r in REELS}
if "likes" not in st.session_state:
    st.session_state.likes = {r["id"]: r.get("likes", "") for r in REELS}

# ---------------- Simple Dummy Analyzers ----------------
def analyze_reel_dummy(caption: str, tags: str, comments: List[str]) -> Dict[str, int]:
    tox_triggers = ["hate", "kill", "vulgar", "scam", "fake", "destroy"]
    fake_triggers = ["miracle", "cure", "aliens", "conspiracy"]
    blob = (caption + " " + tags + " " + " ".join(comments)).lower()
    tox = random.randint(5, 85)
    fake = random.randint(5, 80)
    impact = random.randint(10, 92)
    if any(w in blob for w in tox_triggers):
        tox = min(100, tox + 12)
    if any(w in blob for w in fake_triggers):
        fake = min(100, fake + 18)
    insight = "✅ Looks safe and positive."
    if tox > 70:
        insight = "⚠️ High negativity detected in this reel/post."
    elif fake > 60:
        insight = "⚠️ Content may contain misinformation."
    return {"fake": fake, "tox": tox, "impact": impact, "insight": insight}

def predict_comment_effect(text: str) -> int:
    base = random.randint(8, 85)
    if any(w in text.lower() for w in ["stupid", "idiot", "hate", "kill", "abuse", "fake"]):
        base = min(100, base + 18)
    return base

# ---------------- Header ----------------
st.markdown("<div style='text-align:center; margin-bottom:6px; font-weight:600;'>Instagram-style Reels Prototype — (Only Comment & Analyze interactive)</div>", unsafe_allow_html=True)

# ---------------- Feed rendering ----------------
st.markdown('<div class="feed">', unsafe_allow_html=True)

for r in REELS:
    # determine media src - prefer provided local asset if exists, else use picsum seed
    media_path = r.get("media", "")
    media_src = ""
    if media_path and os.path.exists(os.path.join(ROOT, media_path)):
        # local asset exists
        media_src = media_path.replace("\\", "/")
    else:
        # fallback to picsum with deterministic seed
        seed = hash_to_seed(r.get("id", str(random.random())))
        media_src = f"https://picsum.photos/520/780?random={seed}"

    # show reel block (HTML for overlay look)
    html = f"""
    <div class="reel">
      <img src="{media_src}" alt="reel media" />
      <div class="actions">
        <div class="icon" title="likes">{icon_img_tag('like')}</div>
        <div class="icon" title="comment">{icon_img_tag('comment')}</div>
        <div class="icon" title="share">{icon_img_tag('share')}</div>
        <div class="icon" title="more">{icon_img_tag('more')}</div>
        <div class="icon" title="analyze">{icon_img_tag('analyze')}</div>
      </div>
      <div class="meta">
        <div class="user">@{r.get('user','user')}</div>
        <div class="cap">{r.get('caption','')}</div>
        <div class="tags">{r.get('hashtags', r.get('tags',''))}</div>
        <div class="likes">{st.session_state.likes.get(r['id'], r.get('likes',''))}</div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # Real Streamlit buttons for interaction
    btn_cols = st.columns([1,1,1,1,1])
    # Like button disabled (visual only)
    btn_cols[0].button("❤", key=f"like_{r['id']}", disabled=True)
    if btn_cols[1].button("💬  Open comments", key=f"open_comment_{r['id']}"):
        st.session_state.open_drawer = r["id"]
    btn_cols[2].button("📤  Share", key=f"share_{r['id']}", disabled=True)
    btn_cols[3].button("⋮  More", key=f"more_{r['id']}", disabled=True)
    if btn_cols[4].button("🧠  Analyze", key=f"analyze_{r['id']}"):
        st.session_state.open_modal = r["id"]

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Comment Drawer ----------------
if st.session_state.open_drawer:
    rid = st.session_state.open_drawer
    reel = next((x for x in REELS if x["id"] == rid), None)
    if reel:
        st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="drawer">', unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'><div style='font-weight:700'>Comments • @{reel.get('user')}</div></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="muted">Scroll to view comments</div>', unsafe_allow_html=True)

        # Show comments from COMMENTS_STORE
        for c in COMMENTS_STORE.get(rid, []):
            st.markdown(f'<div class="comment-row">💬 {c}</div>', unsafe_allow_html=True)

        # input
        input_key = f"comment_input_{rid}"
        txt = st.text_input("Type your comment here…", key=input_key, label_visibility="collapsed", placeholder="Type your comment here…")
        if txt:
            st.session_state.comment_inputs[rid] = txt
            score = predict_comment_effect(txt)
            if score > 70:
                st.markdown(f'<div class="chip warn">🔮 Comment Effect Score: {score}% — might have negative impact</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chip">🔮 Comment Effect Score: {score}% — looks okay</div>', unsafe_allow_html=True)

        if st.button("Close comments", key=f"close_comments_{rid}"):
            st.session_state.open_drawer = None

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Analyze Modal ----------------
if st.session_state.open_modal:
    rid = st.session_state.open_modal
    reel = next((x for x in REELS if x["id"] == rid), None)
    if reel:
        res = analyze_reel_dummy(reel.get("caption",""), reel.get("hashtags", reel.get("tags","")), COMMENTS_STORE.get(rid, []))
        st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'><div style='font-weight:700'>Reel Analysis • @{reel.get('user')}</div></div>", unsafe_allow_html=True)
        st.markdown('<div style="margin-top:10px;margin-bottom:8px">', unsafe_allow_html=True)
        st.markdown(f'<span class="chip">🕵️ Fake: <b>{res["fake"]}%</b></span>', unsafe_allow_html=True)
        st.markdown(f'<span class="chip">☣️ Toxicity: <b>{res["tox"]}%</b></span>', unsafe_allow_html=True)
        st.markdown(f'<span class="chip">📈 Impact: <b>{res["impact"]}%</b></span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom:8px">{res["insight"]}</div>', unsafe_allow_html=True)
        if res["tox"] >= 70:
            st.markdown('<div class="chip warn">⚠️ This content may negatively affect thinking / mental health.</div>', unsafe_allow_html=True)

        if st.button("Close analysis", key=f"close_analysis_{rid}"):
            st.session_state.open_modal = None

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown('<div class="footer">Prototype — modular-ready. Put your images in assets/ and optional data/reels.json & data/comments.json to override defaults.</div>', unsafe_allow_html=True)

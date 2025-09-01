# app.py
import streamlit as st
import json
import random
import os
from typing import List, Dict

# ---------------- Page config ----------------
st.set_page_config(page_title="Instagram-style Reels Prototype", layout="centered")
ROOT = os.path.dirname(__file__) if "__file__" in globals() else "."

# ---------------- Helpers to load files with fallbacks ----------------
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

# ---------------- Default dummy data (used if data files missing) ----------------
DEFAULT_REELS = [
    {
        "id": "1",
        "type": "real_news",
        "user": "world_news",
        "caption": "NASA confirms water on the Moon! 🌕🚀",
        "hashtags": "#NASA #Space #Science",
        "media": "assets/reel1.jpg",
        "likes": "18.4K",
    },
    {
        "id": "2",
        "type": "fake_news",
        "user": "trending_now",
        "caption": "Aliens landed in Times Square! 👽😂",
        "hashtags": "#Breaking #Aliens #NYC",
        "media": "assets/reel2.jpg",
        "likes": "9.8K",
    },
    {
        "id": "3",
        "type": "positive",
        "user": "motivation_daily",
        "caption": "Believe in yourself. The world is yours. 💪✨",
        "hashtags": "#Motivation #Positivity",
        "media": "assets/reel3.jpg",
        "likes": "5.0K",
    },
    {
        "id": "4",
        "type": "negative",
        "user": "toxic_news",
        "caption": "The economy is collapsing soon! 😨📉",
        "hashtags": "#Finance #Crisis",
        "media": "assets/reel4.jpg",
        "likes": "2.3K",
    },
    {
        "id": "5",
        "type": "cancel_culture",
        "user": "social_trends",
        "caption": "Famous influencer faces massive backlash! 🚨🔥",
        "hashtags": "#CancelCulture #Drama",
        "media": "assets/reel5.jpg",
        "likes": "12.1K",
    },
]

DEFAULT_COMMENTS = {
    "1": ["This is amazing! 🚀", "Science rocks!", "Can't wait for Moon missions!"],
    "2": ["Lol fake news 🤣", "Where's the proof?", "Clickbait as usual."],
    "3": ["Needed this today 💜", "Positive vibes only ✨", "Love it!"],
    "4": ["This is scary 😨", "Hope things get better soon.", "Toxic news everywhere."],
    "5": ["Drama again 😂", "People need to chill.", "Cancel culture is crazy!"]
}

# ---------------- Load data if provided ----------------
reels_json = load_json("data/reels.json")
comments_json = load_json("data/comments.json")

reels = reels_json if isinstance(reels_json, list) else DEFAULT_REELS
comments_store = comments_json if isinstance(comments_json, dict) else DEFAULT_COMMENTS

# ---------------- Load CSS and JS (fallbacks) ----------------
css_file = safe_read("static/style.css")
js_file = safe_read("static/script.js")

# basic fallback CSS (keeps it clean)
FALLBACK_CSS = """
<style>
:root{--bg:#070708;--card:#0e1113;--muted:#cbd5e1;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg);color:#eef2ff}
.feed{width:min(520px,96vw);margin:6px auto 60px auto}
.reel{position:relative;width:100%;height:78vh;border-radius:14px;overflow:hidden;background:#000;margin:20px 0;box-shadow:0 10px 30px rgba(0,0,0,.6);}
.reel img{width:100%;height:100%;object-fit:cover;display:block}
.actions{position:absolute;right:12px;bottom:18px;display:flex;flex-direction:column;gap:12px;z-index:5;align-items:center}
.icon{width:52px;height:52px;border-radius:999px;background:rgba(0,0,0,0.45);display:grid;place-items:center;font-size:20px;color:white;border:1px solid rgba(255,255,255,0.04)}
.meta{position:absolute;left:12px;bottom:18px;right:88px;z-index:4;color:#f8fafc;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.user{font-weight:700;font-size:15px}
.cap{font-size:14px;margin-top:6px}
.tags{font-size:13px;color:var(--muted);margin-top:6px}
.likes{font-size:12px;color:var(--muted);margin-top:6px}

/* overlay modal */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:90;backdrop-filter:blur(3px)}
.modal{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:92;background:var(--card);padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.04);width:min(520px,92vw)}
.chips{display:flex;gap:8px;margin-bottom:10px}
.chip{padding:8px 10px;border-radius:10px;background:#0b1112;border:1px solid rgba(255,255,255,0.03)}
.warn{background:#2a1216;border-color:#7f1d1d;color:#ffd7d7}

/* drawer */
.drawer{position:fixed;left:0;right:0;bottom:0;background:#0f1113;border-top-left-radius:12px;border-top-right-radius:12px;padding:12px 14px;z-index:95;max-height:70vh;overflow:auto;border:1px solid rgba(255,255,255,0.03)}
.comment{padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.03);color:#e6eef8}
.muted{color:var(--muted);opacity:.85;font-size:13px;margin-bottom:8px}
.input{width:100%;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);background:#0b0d10;color:#fff;margin-top:8px}
.btn{padding:8px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);background:rgba(255,255,255,0.02);color:#fff}
.footer{opacity:.6;text-align:center;margin-top:18px}
</style>
"""

FALLBACK_JS = """
<script>
function noop(){/*no-op fallback*/}
// we don't rely heavily on JS for actions; Streamlit buttons handle interactivity.
// This placeholder allows projects that include static/script.js to work when present.
</script>
"""

# inject CSS/JS (prefer user files)
if css_file.strip():
    st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)
else:
    st.markdown(FALLBACK_CSS, unsafe_allow_html=True)

if js_file.strip():
    st.markdown(f"<script>{js_file}</script>", unsafe_allow_html=True)
else:
    st.markdown(FALLBACK_JS, unsafe_allow_html=True)

# ---------------- Icons (use local svg if exist else emoji) ----------------
def icon_svg_path(name: str):
    p = os.path.join(ROOT, "icons", f"{name}.svg")
    return p if os.path.exists(p) else None

def icon_img_tag(name: str, size: int = 32, alt: str = "") -> str:
    svg_path = icon_svg_path(name)
    if svg_path:
        # use relative path that Streamlit can serve
        return f'<img src="icons/{name}.svg" width="{size}" height="{size}" alt="{alt}" />'
    # fall back to emoji
    emoji_map = {
        "like": "❤️",
        "comment": "💬",
        "share": "📤",
        "more": "⋮",
        "analyze": "🧠",
    }
    return emoji_map.get(name, "❖")

# ---------------- Session state ----------------
if "open_drawer_for" not in st.session_state:
    st.session_state.open_drawer_for = None
if "open_modal_for" not in st.session_state:
    st.session_state.open_modal_for = None
if "comment_inputs" not in st.session_state:
    st.session_state.comment_inputs = {r["id"]: "" for r in reels}

# ---------------- Dummy AI / scoring ----------------
def analyze_ai(caption: str, tags: str, comments: List[str]):
    tox_words = ["hate", "kill", "fake", "scam", "vulgar", "abuse", "destroy"]
    fake = random.randint(5, 85)
    tox = random.randint(5, 90)
    impact = random.randint(15, 95)
    blob = (caption + " " + tags + " " + " ".join(comments)).lower()
    if any(w in blob for w in tox_words):
        tox = min(100, tox + 12)
    if "miracle" in blob or "cure" in blob:
        fake = min(100, fake + 18)
    insight = "✅ Looks safe and positive."
    if tox > 70:
        insight = "⚠️ High negativity detected in this reel/post."
    elif fake > 60:
        insight = "⚠️ Content may contain misinformation."
    return {"fake": fake, "tox": tox, "impact": impact, "insight": insight}

def predict_comment_effect(text: str) -> int:
    base = random.randint(8, 85)
    if any(w in text.lower() for w in ["stupid","idiot","hate","kill","abuse","fake"]):
        base = min(100, base + 20)
    return base

# ---------------- Page header ----------------
st.markdown("<div style='text-align:center; margin-bottom:6px; opacity:.9'>"
            "<strong>Instagram-like Reels Prototype</strong> — (Only Comment & Analyze interactive)</div>", unsafe_allow_html=True)

# ---------------- Feed rendering ----------------
st.markdown('<div class="feed">', unsafe_allow_html=True)

for r in reels:
    # prepare media source (prefer provided media path; fallback to picsum)
    media_src = r.get("media", "")
    if media_src and os.path.exists(os.path.join(ROOT, media_src)):
        src = media_src.replace("\\", "/")
    else:
        # fallback to picsum random with stable seed per id
        seed = int(''.join([c for c in r["id"] if c.isdigit()]) or 0) + 10
        src = f"https://picsum.photos/520/780?random={seed}"

    # create HTML block for reel (no HTML comments inside)
    html = f"""
    <div class="reel">
        <img src="{src}" alt="reel media" />
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
            <div class="likes">{r.get('likes','')}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # actual Streamlit buttons for interaction (placed under each reel)
    cols = st.columns([1,1,1,1,1])
    cols[0].button("❤", key=f"like_{r['id']}", disabled=True)
    if cols[1].button("💬  Open comments", key=f"open_comment_{r['id']}"):
        st.session_state.open_drawer_for = r["id"]
    cols[2].button("📤  Share", key=f"share_{r['id']}", disabled=True)
    cols[3].button("⋮  More", key=f"more_{r['id']}", disabled=True)
    if cols[4].button("🧠  Analyze", key=f"analyze_{r['id']}"):
        st.session_state.open_modal_for = r["id"]

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Drawer (comments) ----------------
if st.session_state.open_drawer_for is not None:
    rid = st.session_state.open_drawer_for
    reel = next((x for x in reels if x["id"] == rid), None)
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    # Drawer (use Streamlit elements inside for reliability)
    st.markdown('<div class="drawer">', unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<div style='font-weight:700'>Comments • @{reel.get('user')}</div>"
                f"<div><button class='btn' id='close_draw'>Close</button></div></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="muted">Swipe/scroll to view comments</div>', unsafe_allow_html=True)

    # render comments from comments_store if present
    for c in comments_store.get(rid, []):
        st.markdown(f'<div class="comment">💬 {c}</div>', unsafe_allow_html=True)

    # comment input
    txt_key = f"comment_input_{rid}"
    txt = st.text_input("Type your comment here…", key=txt_key, label_visibility="collapsed")
    if txt:
        st.session_state.comment_inputs[rid] = txt
        score = predict_comment_effect(txt)
        if score > 70:
            st.markdown(f'<div class="chip warn">🔮 Comment Effect Score: {score}% — might have negative impact</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chip">🔮 Comment Effect Score: {score}% — looks okay</div>', unsafe_allow_html=True)

    if st.button("Close comments", key=f"close_comments_{rid}"):
        st.session_state.open_drawer_for = None

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Modal (analysis) ----------------
if st.session_state.open_modal_for is not None:
    rid = st.session_state.open_modal_for
    reel = next((x for x in reels if x["id"] == rid), None)
    res = analyze_ai(reel.get("caption",""), reel.get("hashtags", reel.get("tags","")), comments_store.get(rid, []))
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="modal">', unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'><div style='font-weight:700'>Reel Analysis • @{reel.get('user')}</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="chips">', unsafe_allow_html=True)
    st.markdown(f'<div class="chip">🕵️ Fake: <b>{res["fake"]}%</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chip">☣️ Toxicity: <b>{res["tox"]}%</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chip">📈 Impact: <b>{res["impact"]}%</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin-bottom:10px">{res["insight"]}</div>', unsafe_allow_html=True)
    if res["tox"] >= 70:
        st.markdown('<div class="chip warn">⚠️ This content may negatively affect thinking / mental health.</div>', unsafe_allow_html=True)

    if st.button("Close analysis", key=f"close_modal_{rid}"):
        st.session_state.open_modal_for = None

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown('<div class="footer">Prototype — modular structure (assets/, data/, static/, icons/). '
            'If icons or assets not present, emojis + picsum are used as fallback.</div>', unsafe_allow_html=True)

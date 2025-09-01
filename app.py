import streamlit as st
import random
import pandas as pd

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Instagram Reels Prototype", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
    <style>
        /* Hide Streamlit default menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Page background */
        body {
            margin: 0;
            padding: 0;
            background-color: black;
        }

        /* Reels container */
        .reel-container {
            position: relative;
            width: 100%;
            max-width: 450px;
            margin: auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
        }

        /* Reel image */
        .reel-img {
            width: 100%;
            height: 600px;
            object-fit: cover;
            border-radius: 20px;
        }

        /* Right-side action buttons */
        .actions {
            position: absolute;
            right: 10px;
            bottom: 100px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            align-items: center;
        }

        .action-btn {
            background: rgba(0,0,0,0.6);
            padding: 8px;
            border-radius: 50%;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }

        .action-btn:hover {
            background: rgba(255,255,255,0.2);
        }

        /* Drawer for comments */
        .drawer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            max-height: 60%;
            background: white;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            box-shadow: 0px -4px 20px rgba(0,0,0,0.4);
            padding: 15px;
            overflow-y: auto;
            display: none;
            z-index: 9999;
        }

        .drawer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            font-size: 18px;
        }

        .close-btn {
            cursor: pointer;
            font-size: 20px;
        }

        /* Analyzer popup */
        .analyzer-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 20px;
            width: 350px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.6);
            display: none;
            z-index: 99999;
        }

        .popup-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 18px;
            font-weight: bold;
        }

        .close-popup-btn {
            cursor: pointer;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- DUMMY DATA -------------------
reels = [
    {
        "user": "@tech_guru",
        "caption": "5G will destroy your brain! ⚠️",
        "tags": "#tech #5G #health #scam",
        "comments": ["This is scary 😨", "Fake news!", "Thanks for sharing"]
    },
    {
        "user": "@travel_with_rahul",
        "caption": "Exploring the beauty of Bali 🌴✨",
        "tags": "#travel #bali #nature #wanderlust",
        "comments": ["Bali is amazing!", "Take me with you 🥹", "Dream destination ❤️"]
    },
    {
        "user": "@fitness_diva",
        "caption": "Burn 500 calories in 30 mins! 🏋️‍♀️🔥",
        "tags": "#fitness #workout #healthylife",
        "comments": ["This helped me so much 🙌", "Too intense 😅", "Let's gooo! 💪"]
    },
    {
        "user": "@foodie_life",
        "caption": "The best pizza recipe ever 🍕",
        "tags": "#food #pizza #recipe #homemade",
        "comments": ["Mouthwatering 🤤", "Gonna try this!", "Love it 😍"]
    },
    {
        "user": "@motivation_daily",
        "caption": "Believe in yourself, always 🌟",
        "tags": "#motivation #mindset #success",
        "comments": ["Needed this today 🙏", "Facts 💯", "Very inspiring ❤️"]
    }
]

# ------------------- STREAMLIT UI -------------------
st.title("📸 Instagram-style Reels • Prototype")
st.caption("Only Comment & Analyze buttons are clickable")

# Show reels one by one
for i, reel in enumerate(reels):
    with st.container():
        st.markdown(f"""
            <div class="reel-container">
                <img src="https://picsum.photos/500/600?random={i}" class="reel-img">

                <!-- Action buttons -->
                <div class="actions">
                    <div class="action-btn">❤️</div>
                    <div class="action-btn" onclick="openDrawer({i})">💬</div>
                    <div class="action-btn">📤</div>
                    <div class="action-btn">⋮</div>
                    <div class="action-btn" onclick="openAnalyzer({i})">🧠</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <!-- Comment Drawer -->
            <div id="drawer-{i}" class="drawer">
                <div class="drawer-header">
                    Comments
                    <span class="close-btn" onclick="closeDrawer({i})">✖</span>
                </div>
                <br>
                {''.join([f"<p>💬 {c}</p>" for c in reel['comments']])}
                <input type="text" placeholder="Type your comment here..." style="width:100%;padding:8px;border-radius:10px;border:1px solid #ccc;">
            </div>

            <!-- Analyzer Popup -->
            <div id="analyzer-{i}" class="analyzer-popup">
                <div class="popup-header">
                    AI Analysis Report
                    <span class="close-popup-btn" onclick="closeAnalyzer({i})">✖</span>
                </div>
                <hr>
                <p><b>Caption:</b> {reel['caption']}</p>
                <p><b>Tags:</b> {reel['tags']}</p>
                <p><b>Fake Probability:</b> {random.randint(5, 90)}%</p>
                <p><b>Toxic Content:</b> {random.randint(5, 80)}%</p>
                <p><b>Mental Impact:</b> {random.randint(10, 70)}%</p>
            </div>
        """, unsafe_allow_html=True)

# ------------------- JAVASCRIPT -------------------
st.markdown("""
    <script>
        function openDrawer(id) {
            document.getElementById(`drawer-${id}`).style.display = "block";
        }
        function closeDrawer(id) {
            document.getElementById(`drawer-${id}`).style.display = "none";
        }
        function openAnalyzer(id) {
            document.getElementById(`analyzer-${id}`).style.display = "block";
        }
        function closeAnalyzer(id) {
            document.getElementById(`analyzer-${id}`).style.display = "none";
        }
    </script>
""", unsafe_allow_html=True)

import streamlit as st
import random
import time
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Brain Clash 🧠⚡", page_icon="🧠", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #A0AAB0;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .profile-card {
        background: linear-gradient(135deg, #1E2229, #2A2F3A);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #FF4B4B;
        margin-bottom: 20px;
    }
    .level-badge {
        background-color: #FF4B4B;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- LEVEL CALCULATION UTILITY ---
LEVEL_TITLES = [
    (0, 1, "Fresher 🟢"),
    (500, 2, "Fresher II 🟢"),
    (1000, 3, "Fresher III 🟢"),
    (2000, 4, "Sophomore 🔵"),
    (3500, 5, "Sophomore II 🔵"),
    (5000, 6, "Senior Scholar 🟣"),
    (7500, 7, "Senior Scholar II 🟣"),
    (10000, 8, "Campus Veteran 👑"),
    (15000, 13, "Monk / Momma Legend 🏆")
]

def get_player_level(total_xp):
    current_lvl = 1
    current_title = "Fresher 🟢"
    for min_xp, lvl, title in LEVEL_TITLES:
        if total_xp >= min_xp:
            current_lvl = lvl
            current_title = title
        else:
            break
    return current_lvl, current_title

# --- GAME DATA: CATEGORIES & QUESTIONS ---
QUIZ_DATA = {
    "⚽ Football & Sports": [
        {
            "q": "Which player holds the record for the most UEFA Champions League goals in history?",
            "options": ["Lionel Messi", "Cristiano Ronaldo", "Robert Lewandowski", "Karim Benzema"],
            "answer": "Cristiano Ronaldo"
        },
        {
            "q": "Which English Premier League team went completely unbeaten in the 2003–2004 season ('The Invincibles')?",
            "options": ["Manchester United", "Chelsea", "Arsenal", "Liverpool"],
            "answer": "Arsenal"
        },
        {
            "q": "How many total players are on the pitch during a standard basketball game (both teams combined)?",
            "options": ["8", "10", "12", "14"],
            "answer": "10"
        }
    ],
    "🎓 Campus & Student Life": [
        {
            "q": "What is the unspoken rule when a Monk or Momma invites you for a 'quick study session' at 20:00 PM on a Friday night?",
            "options": [
                "Bring 3 heavy textbooks and highlighters",
                "You are actually going to hang out, listen to music, or go out",
                "You will solve 5 past exam papers before midnight",
                "The library is guaranteed to be completely empty"
            ],
            "answer": "You are actually going to hang out, listen to music, or go out"
        },
        {
            "q": "What is the universally accepted strategy when you haven't revised for a 09:00 AM test and your friend calls at 03:00 AM?",
            "options": [
                "Pretend you are on slide 50 and tell them to sleep",
                "Admit you haven't started and join forces for a panic overnight session",
                "Turn off your phone and pray the test gets postponed",
                "Tell them you already know everything"
            ],
            "answer": "Admit you haven't started and join forces for a panic overnight session"
        },
        {
            "q": "What is the most common reason for a sudden loud cheer or noise in the hostel corridors at 2:00 AM?",
            "options": [
                "Someone just passed an assignment",
                "Monks/Mommas playing music, banter, or celebrating a match result",
                "A fire drill exercise",
                "Lecturer posting results online"
            ],
            "answer": "Monks/Mommas playing music, banter, or celebrating a match result"
        }
    ],
    "🎵 Afrobeats & Music": [
        {
            "q": "Which Nigerian Afrobeats star released the chart-topping album 'Love, Damini' featuring 'Last Last'?",
            "options": ["Wizkid", "Davido", "Burna Boy", "Asake"],
            "answer": "Burna Boy"
        },
        {
            "q": "Complete the lyrics from Summer Walker's track 'Playing Games': 'If you want me, show me, you gotta...'",
            "options": ["...buy me things", "...be there for me", "...put in work", "...give me space"],
            "answer": "...put in work"
        },
        {
            "q": "Which artist is famous for the hit track 'Yo Pe' and major Congolese Afro-pop hits?",
            "options": ["Fally Ipupa", "Ya Levis", "Innoss'B", "Diamond Platnumz"],
            "answer": "Innoss'B"
        }
    ],
    "🧠 Mind Benders": [
        {
            "q": "Riddle: 'I have keys but no locks. I have space but no room. You can enter, but you can't go outside.' What am I?",
            "options": ["A map", "A keyboard", "A clock", "A bank vault"],
            "answer": "A keyboard"
        },
        {
            "q": "Which element on the periodic table has the chemical symbol 'Au'?",
            "options": ["Silver", "Copper", "Gold", "Aluminum"],
            "answer": "Gold"
        }
    ]
}

# --- INITIALIZE SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category" not in st.session_state:
    st.session_state.category = None
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "career_xp" not in st.session_state:
    st.session_state.career_xp = 0

# Leaderboard samples (Weekly Tournament vs. Lifetime Career)
if "weekly_leaderboard" not in st.session_state:
    st.session_state.weekly_leaderboard = [
        {"name": "Bwangu_M", "pts": 450, "cat": "⚽ Football & Sports"},
        {"name": "Luyando_K", "pts": 380, "cat": "🎵 Afrobeats & Music"},
        {"name": "Mapalo_Z", "pts": 310, "cat": "🎓 Campus & Student Life"}
    ]

# --- APP HEADER ---
st.markdown("<h1 class='main-title'>Brain Clash 🧠⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>The Ultimate Campus & Youth Trivia Arena</p>", unsafe_allow_html=True)

# Calculate Level & Rank Title
lvl, title = get_player_level(st.session_state.career_xp)

# --- PAGE 1: HOME & PROFILE ---
if st.session_state.page == "home":
    
    # Profile Banner
    if st.session_state.player_name:
        st.markdown(f"""
            <div class='profile-card'>
                <h3>👤 {st.session_state.player_name}</h3>
                <p><span class='level-badge'>Level {lvl}</span> <b>{title}</b></p>
                <p style='margin-bottom:0px;'>⭐ Career XP: <b>{st.session_state.career_xp} XP</b></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("### 👋 Enter your nickname to begin:")
        player = st.text_input("Nickname / Handle:", placeholder="e.g. Mwamba_99")
        if player:
            st.session_state.player_name = player
            st.rerun()

    if st.session_state.player_name:
        st.write("---")
        st.write("### 🎯 Pick a Category to Play:")

        for cat in QUIZ_DATA.keys():
            if st.button(f"Play {cat}"):
                st.session_state.category = cat
                st.session_state.questions = random.sample(QUIZ_DATA[cat], len(QUIZ_DATA[cat]))
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.streak = 0
                st.session_state.start_time = time.time()
                st.session_state.page = "quiz"
                st.rerun()

        st.write("---")
        
        # LEADERBOARD TABS
        tab1, tab2 = st.tabs(["🏆 Weekly Tournament", "⭐ Career XP Ranks"])
        
        with tab1:
            st.caption("Weekly scores reset every Sunday midnight for tournament prizes!")
            for idx, entry in enumerate(st.session_state.weekly_leaderboard, 1):
                st.write(f"**#{idx} {entry['name']}** — {entry['pts']} pts *({entry['cat']})*")
                
        with tab2:
            st.caption("Career XP never resets! This determines your overall Level.")
            st.write(f"**#1 {st.session_state.player_name or 'You'}** — {st.session_state.career_xp} XP *(Level {lvl})*")
            st.write("**#2 Bwangu_M** — 4,200 XP *(Level 5)*")
            st.write("**#3 Luyando_K** — 2,100 XP *(Level 4)*")

# --- PAGE 2: QUIZ INTERFACE ---
elif st.session_state.page == "quiz":
    questions = st.session_state.questions
    q_index = st.session_state.current_q
    
    if q_index < len(questions):
        current_data = questions[q_index]
        
        # Progress Bar & Category Tag
        st.progress((q_index) / len(questions))
        st.caption(f"Question {q_index + 1} of {len(questions)} | {st.session_state.category}")
        
        st.markdown(f"### {current_data['q']}")
        
        # Option Buttons
        for opt in current_data['options']:
            if st.button(opt, key=f"q_{q_index}_{opt}"):
                time_taken = time.time() - st.session_state.start_time
                time_bonus = max(0, int(15 - time_taken) * 10)
                
                if opt == current_data['answer']:
                    st.session_state.streak += 1
                    streak_multiplier = 1.5 if st.session_state.streak >= 3 else 1.0
                    points_earned = int((100 + time_bonus) * streak_multiplier)
                    st.session_state.score += points_earned
                    st.success(f"🎉 Correct! +{points_earned} pts!")
                else:
                    st.session_state.streak = 0
                    st.error(f"❌ Wrong! Correct answer: **{current_data['answer']}**")
                
                time.sleep(1.2)
                st.session_state.current_q += 1
                st.session_state.start_time = time.time()
                st.rerun()
    else:
        st.session_state.page = "results"
        st.rerun()

# --- PAGE 3: RESULTS & LEVEL UP ---
elif st.session_state.page == "results":
    final_score = st.session_state.score
    player_name = st.session_state.player_name
    category = st.session_state.category
    
    old_lvl, _ = get_player_level(st.session_state.career_xp)
    
    # Add to Career XP and Weekly Leaderboard
    st.session_state.career_xp += final_score
    new_lvl, new_title = get_player_level(st.session_state.career_xp)
    
    st.session_state.weekly_leaderboard.append({
        "name": player_name,
        "pts": final_score,
        "cat": category
    })
    st.session_state.weekly_leaderboard = sorted(st.session_state.weekly_leaderboard, key=lambda x: x['pts'], reverse=True)

    st.balloons()
    
    # Check Level Up
    if new_lvl > old_lvl:
        st.success(f"🎊 **LEVEL UP!** You reached **Level {new_lvl}: {new_title}**!")

    st.markdown(f"""
        <div class='profile-card'>
            <h2>Game Over, {player_name}! 🏆</h2>
            <h1 style='color:#FF4B4B;'>+{final_score} PTS</h1>
            <p>Category: <b>{category}</b></p>
            <hr style='border-color:#313742;'>
            <p>⭐ Total Career XP: <b>{st.session_state.career_xp} XP</b></p>
        </div>
    """, unsafe_allow_html=True)

    # WhatsApp Share Generator
    share_text = f"🧠 I just scored {final_score} PTS on Brain Clash ({category}) and reached Level {new_lvl}! Can you beat me? Play here: https://thrive-hub.streamlit.app"
    encoded_share = urllib.parse.quote(share_text)
    whatsapp_url = f"https://wa.me/?text={encoded_share}"

    st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; font-size:16px; cursor:pointer;">
                📲 Challenge a Friend on WhatsApp
            </button>
        </a>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 Return to Main Menu"):
        st.session_state.page = "home"
        st.rerun()

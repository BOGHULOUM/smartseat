import streamlit as st
from pathlib import Path
import sqlite3
import base64

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent.parent
assets_dir = base_dir / "assets"
logo_path = assets_dir / "logo.png"
db_path = base_dir / "tickets.db"

st.set_page_config(
    page_title="SmartSeat - Match Details",
    page_icon=str(logo_path),
    layout="wide"
)

# =========================
# قاعدة البيانات
# =========================
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")
conn.commit()

# =========================
# Session State
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# =========================
# الترجمة
# =========================
TXT = {
    "ar": {
        "lang_label": "اللغة",
        "arabic": "العربية",
        "english": "English",
        "title": "تفاصيل المباريات",
        "subtitle": "Match Details",
        "desc": "قبل الحجز، يمكنك هنا الاطلاع على تفاصيل كل مباراة من حيث نوعها، البطولة، الملعب، الحكم، وتوقيت المباراة، حتى تكون لديك صورة واضحة قبل إتمام الحجز.",
        "match_type": "نوع المباراة",
        "competition": "البطولة",
        "stadium": "الملعب",
        "city": "المدينة",
        "referee": "الحكم",
        "datetime": "التاريخ والوقت",
        "gates": "فتح البوابات",
        "book_now": "احجز الآن",
        "need_login": "يجب تسجيل الدخول أولاً للوصول إلى هذه الصفحة.",
        "back_home": "العودة للرئيسية",
        "quick_access": "التنقل السريع",
        "home": "الرئيسية",
        "booking": "الحجز",
        "support": "الدعم",
        "footer": "SmartSeat Match Details • Final Year Project",
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",
        "title": "Match Details",
        "subtitle": "Match Details",
        "desc": "Before booking, you can review each match details including type, competition, stadium, referee, and date/time.",
        "match_type": "Match Type",
        "competition": "Competition",
        "stadium": "Stadium",
        "city": "City",
        "referee": "Referee",
        "datetime": "Date & Time",
        "gates": "Gates Open",
        "book_now": "Book Now",
        "need_login": "You must login first to access this page.",
        "back_home": "Back to Home",
        "quick_access": "Quick Access",
        "home": "Home",
        "booking": "Booking",
        "support": "Support",
        "footer": "SmartSeat Match Details • Final Year Project",
    }
}

def t(k):
    return TXT[st.session_state.lang][k]

# =========================
# أدوات
# =========================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64(logo_path)

# =========================
# حماية الصفحة
# =========================
if not st.session_state.logged_in:
    st.warning(t("need_login"))
    if st.button(t("back_home")):
        st.switch_page("app.py")
    st.stop()

# =========================
# بيانات المباريات
# =========================
matches = [
    {
        "image": assets_dir / "match1.png",
        "name_ar": "برشلونة × ريال مدريد",
        "name_en": "Barcelona vs Real Madrid",
        "type_ar": "نهائي كأس",
        "type_en": "Cup Final",
        "competition_ar": "كأس السوبر الإسباني",
        "competition_en": "Spanish Super Cup",
        "stadium_ar": "ملعب الملك فهد الدولي",
        "stadium_en": "King Fahd International Stadium",
        "city_ar": "الرياض",
        "city_en": "Riyadh",
        "referee_ar": "Michael Oliver",
        "referee_en": "Michael Oliver",
        "datetime": "18-05-2026 • 20:30",
        "gates_open": "18:30",
        "parking_ar": "مواقف VIP ومواقف عامة متوفرة",
        "parking_en": "VIP and public parking are available",
        "demand_ar": "الطلب مرتفع جداً",
        "demand_en": "Very high demand",
        "note_ar": "مواجهة كلاسيكية نارية بين عملاقين من أكبر أندية العالم.",
        "note_en": "A fiery Clasico between two of the world's biggest clubs."
    },
    {
        "image": assets_dir / "match2.png",
        "name_ar": "الكويت × القادسية",
        "name_en": "Kuwait vs Qadsia",
        "type_ar": "دوري",
        "type_en": "League",
        "competition_ar": "الدوري الكويتي الممتاز",
        "competition_en": "Kuwaiti Premier League",
        "stadium_ar": "ملعب جابر الأحمد الدولي",
        "stadium_en": "Jaber Al-Ahmad International Stadium",
        "city_ar": "الكويت",
        "city_en": "Kuwait",
        "referee_ar": "عبدالرحمن الجاسم",
        "referee_en": "Abdulrahman Al-Jassim",
        "datetime": "22-05-2026 • 19:45",
        "gates_open": "17:45",
        "parking_ar": "مواقف الجماهير متوفرة بالقرب من الملعب",
        "parking_en": "Fan parking is available near the stadium",
        "demand_ar": "الطلب مرتفع",
        "demand_en": "High demand",
        "note_ar": "ديربي كويتي جماهيري متوقع له حضور قوي وأجواء حماسية كبيرة.",
        "note_en": "A major Kuwaiti derby expected to attract strong attendance and exciting atmosphere."
    },
    {
        "image": assets_dir / "match3.png",
        "name_ar": "العربي × السالمية",
        "name_en": "Al Arabi vs Al Salmiya",
        "type_ar": "كأس",
        "type_en": "Cup",
        "competition_ar": "كأس الأمير",
        "competition_en": "Amir Cup",
        "stadium_ar": "ملعب صباح السالم",
        "stadium_en": "Sabah Al-Salem Stadium",
        "city_ar": "الكويت",
        "city_en": "Kuwait",
        "referee_ar": "أحمد العلي",
        "referee_en": "Ahmed Al-Ali",
        "datetime": "25-05-2026 • 18:30",
        "gates_open": "16:30",
        "parking_ar": "تتوفر مواقف خارجية حول الاستاد",
        "parking_en": "Outdoor parking is available around the stadium",
        "demand_ar": "الطلب متوسط إلى مرتفع",
        "demand_en": "Medium to high demand",
        "note_ar": "مواجهة مهمة في بطولة الكأس وفرص التأهل فيها كبيرة للطرفين.",
        "note_en": "An important cup match with strong qualification chances for both teams."
    },
    {
        "image": assets_dir / "match4.png",
        "name_ar": "مانشستر سيتي × ليفربول",
        "name_en": "Manchester City vs Liverpool",
        "type_ar": "ودية",
        "type_en": "Friendly",
        "competition_ar": "International Friendly",
        "competition_en": "International Friendly",
        "stadium_ar": "ويمبلي",
        "stadium_en": "Wembley",
        "city_ar": "لندن",
        "city_en": "London",
        "referee_ar": "Anthony Taylor",
        "referee_en": "Anthony Taylor",
        "datetime": "30-05-2026 • 21:00",
        "gates_open": "19:00",
        "parking_ar": "المواقف محدودة ويُنصح بالحضور المبكر",
        "parking_en": "Parking is limited and early arrival is recommended",
        "demand_ar": "الطلب مرتفع جداً",
        "demand_en": "Very high demand",
        "note_ar": "قمة إنجليزية ممتعة بين فريقين كبيرين في مواجهة استعراضية قوية.",
        "note_en": "An exciting English clash between two major teams in a strong showcase match."
    }
]

# =========================
# التصميم
# =========================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    direction: rtl;
    font-family: 'Segoe UI', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(circle at 15% 20%, rgba(212,175,55,0.08), transparent 30%),
        radial-gradient(circle at 85% 75%, rgba(212,175,55,0.06), transparent 30%),
        repeating-linear-gradient(
            135deg,
            rgba(212,175,55,0.045) 0px,
            rgba(212,175,55,0.045) 2px,
            transparent 2px,
            transparent 40px
        ),
        repeating-linear-gradient(
            -135deg,
            rgba(212,175,55,0.025) 0px,
            rgba(212,175,55,0.025) 2px,
            transparent 2px,
            transparent 48px
        ),
        linear-gradient(135deg, #050505 0%, #0a0a0a 45%, #111111 100%);
    color: white;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0b0b0b 0%, #151515 100%);
    border-left: 1px solid rgba(212,175,55,0.20);
}}

.sidebar-brand-card {{
    background:
        radial-gradient(circle at 20% 25%, rgba(0,0,0,0.08), transparent 28%),
        radial-gradient(circle at 80% 75%, rgba(0,0,0,0.06), transparent 30%),
        repeating-linear-gradient(135deg, rgba(0,0,0,0.07) 0px, rgba(0,0,0,0.07) 2px, transparent 2px, transparent 26px),
        repeating-linear-gradient(-135deg, rgba(0,0,0,0.045) 0px, rgba(0,0,0,0.045) 2px, transparent 2px, transparent 34px),
        linear-gradient(135deg, #f4d46a 0%, #d4af37 55%, #b78d1d 100%);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 24px;
    padding: 22px 16px 18px 16px;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.30);
    margin-bottom: 10px;
}}

.sidebar-logo {{
    width: 120px;
    max-width: 100%;
    display: block;
    margin: 0 auto 12px auto;
}}

.sidebar-brand-title {{
    color: #111111;
    font-size: 30px;
    font-weight: 900;
}}

.sidebar-brand-subtitle {{
    color: #181818;
    font-size: 14px;
    font-weight: 700;
}}

.block-container {{
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}}

.logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -4px;
    margin-bottom: -10px;
}}

.logo-wrap img {{
    width: 210px;
    max-width: 100%;
    filter: drop-shadow(0px 0px 20px rgba(212,175,55,0.68));
}}

.hero-box {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 30px;
    padding: 24px 30px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.36);
    margin-top: 0;
    margin-bottom: 22px;
}}

.hero-title {{
    font-size: 42px;
    font-weight: 900;
    color: #D4AF37;
}}

.hero-subtitle {{
    font-size: 18px;
    color: #E6C86E;
    font-weight: 700;
}}

.hero-text {{
    color: #E6C86E;
    font-size: 16px;
    line-height: 1.9;
    max-width: 900px;
    margin: auto;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    overflow: hidden !important;
}}

.match-title {{
    color: #D4AF37;
    font-size: 24px;
    font-weight: 900;
    text-align: center;
    margin: 12px 0 16px 0;
    line-height: 1.6;
}}

.info-line {{
    color: #F0D98A;
    font-size: 16px;
    line-height: 1.9;
    margin: 6px 0;
    word-break: break-word;
}}

.info-label {{
    color: #D4AF37;
    font-weight: 800;
}}

.note-box {{
    background: linear-gradient(135deg, rgba(45,35,10,0.95), rgba(70,55,15,0.92));
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 18px;
    padding: 14px;
    text-align: center;
    color: #F0D98A;
    font-size: 15px;
    font-weight: 700;
    margin-top: 14px;
    line-height: 1.8;
}}

.status-row {{
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 16px;
    margin-bottom: 8px;
}}

.status-pill {{
    background: rgba(255,215,0,0.10);
    border: 1px solid rgba(212,175,55,0.30);
    color: #E6C86E;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
}}

label {{
    color: #E6C86E !important;
    font-weight: 700 !important;
}}

.stButton > button {{
    width: 100%;
    min-height: 60px;
    border: none;
    border-radius: 18px;
    padding: 12px 18px;
    font-size: 18px;
    font-weight: 800;
    color: black;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
}}

.mobile-nav-only {{
    display:none;
}}

.mobile-nav-box {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 22px;
    padding: 14px 12px 6px 12px;
    margin-bottom: 16px;
}}

.mobile-nav-title {{
    color: #D4AF37;
    text-align: center;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 10px;
}}

.mobile-links {{
    display:flex;
    gap:8px;
    justify-content:center;
    flex-wrap:wrap;
}}

.mobile-links a {{
    text-decoration:none !important;
    color:black !important;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
    padding:10px 14px;
    border-radius:14px;
    font-size:14px;
    font-weight:800;
}}

.footer {{
    text-align:center;
    color:#D4AF37;
    font-size:15px;
    font-weight:600;
    margin-top:24px;
}}

@media (max-width: 768px) {{
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}
    [data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}
    button[kind="header"] {{
        display: none !important;
    }}
    .mobile-nav-only {{
        display:block !important;
    }}
    .block-container {{
        padding-top: 0.7rem !important;
        padding-bottom: 1rem !important;
        padding-right: 0.7rem !important;
        padding-left: 0.7rem !important;
        max-width: 100% !important;
    }}
    .logo-wrap img {{
        width: 165px !important;
        max-width: 86% !important;
    }}
    .hero-box {{
        padding: 18px 14px !important;
        border-radius: 22px !important;
        margin-bottom: 16px !important;
    }}
    .hero-title {{
        font-size: 28px !important;
    }}
    .hero-subtitle {{
        font-size: 15px !important;
    }}
    .hero-text, .info-line, .note-box {{
        font-size: 13px !important;
        line-height: 1.9 !important;
    }}
    .match-title {{
        font-size: 18px !important;
    }}
}}
</style>

<div class="logo-wrap">
    <img src="data:image/png;base64,{logo_base64}">
</div>
""", unsafe_allow_html=True)

# =========================
# السايدبار
# =========================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand-card">
        <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo">
        <div class="sidebar-brand-title">SmartSeat</div>
        <div class="sidebar-brand-subtitle">Smart Stadium Ticket Pricing System</div>
    </div>
    """, unsafe_allow_html=True)

    lang_view = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="lang_match_sidebar"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

# =========================
# تنقل الجوال
# =========================
st.markdown(f"""
<div class="mobile-nav-only">
    <div class="mobile-nav-box">
        <div class="mobile-nav-title">{t('quick_access')}</div>
        <div class="mobile-links">
            <a href="/">{t('home')}</a>
            <a href="/Booking">{t('booking')}</a>
            <a href="/Support">{t('support')}</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# أعلى الصفحة
# =========================
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="lang_match_top"
    )
    st.session_state.lang = "ar" if page_lang == TXT["ar"]["arabic"] else "en"

# =========================
# الهيدر
# =========================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{t('title')}</div>
    <div class="hero-subtitle">{t('subtitle')}</div>
    <div class="hero-text">{t('desc')}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# عرض المباريات
# =========================
col1, col2 = st.columns(2, gap="large")

for i, match in enumerate(matches):
    target_col = col1 if i % 2 == 0 else col2

    with target_col:
        with st.container(border=True):
            if match["image"].exists():
                st.image(str(match["image"]), use_container_width=True)
            else:
                st.warning(f"Missing image: {match['image'].name}")

            name = match["name_ar"] if st.session_state.lang == "ar" else match["name_en"]
            match_type = match["type_ar"] if st.session_state.lang == "ar" else match["type_en"]
            competition = match["competition_ar"] if st.session_state.lang == "ar" else match["competition_en"]
            stadium = match["stadium_ar"] if st.session_state.lang == "ar" else match["stadium_en"]
            city = match["city_ar"] if st.session_state.lang == "ar" else match["city_en"]
            referee = match["referee_ar"] if st.session_state.lang == "ar" else match["referee_en"]
            demand = match["demand_ar"] if st.session_state.lang == "ar" else match["demand_en"]
            note = match["note_ar"] if st.session_state.lang == "ar" else match["note_en"]
            parking = match["parking_ar"] if st.session_state.lang == "ar" else match["parking_en"]

            st.markdown(f'<div class="match-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("match_type")}:</span> {match_type}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("competition")}:</span> {competition}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("stadium")}:</span> {stadium}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("city")}:</span> {city}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("referee")}:</span> {referee}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="info-label">{t("datetime")}:</span> {match["datetime"]}</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="status-row">
                <div class="status-pill">{t("gates")}: {match["gates_open"]}</div>
                <div class="status-pill">{demand}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="note-box">
                {note}<br><br>{parking}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"{t('book_now')} - {name}", key=f"book_{i}"):
                st.session_state["selected_match"] = match["name_ar"]
                st.switch_page("pages/1_Booking.py")

st.markdown(f'<div class="footer">{t("footer")}</div>', unsafe_allow_html=True)
conn.close()

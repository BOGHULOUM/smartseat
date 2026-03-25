import streamlit as st
from pathlib import Path
import sqlite3
import base64
import hashlib
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent
assets_dir = base_dir / "assets"
logo_path = assets_dir / "logo.png"
db_path = base_dir / "tickets.db"

st.set_page_config(
    page_title="SmartSeat",
    page_icon=str(logo_path),
    layout="wide"
)

# =========================
# Session State
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_username" not in st.session_state:
    st.session_state.user_username = ""

# =========================
# الترجمة
# =========================
TXT = {
    "ar": {
        "lang_label": "اللغة",
        "arabic": "العربية",
        "english": "English",
        "app_name": "SmartSeat",
        "app_subtitle": "Smart Stadium Ticket Pricing System",
        "home_desc": "نظام ذكي لحجز تذاكر المباريات، يعرض تجربة حجز احترافية تشمل المباريات، الحجز، السجل، التحليلات، لوحة الإدارة، والدعم الفني.",
        "login_tab": "تسجيل الدخول",
        "signup_tab": "إنشاء حساب",
        "login_title": "تسجيل الدخول",
        "signup_title": "إنشاء حساب جديد",
        "auth_desc": "سجّل الدخول أو أنشئ حسابًا جديدًا للوصول إلى النظام.",
        "full_name": "الاسم الكامل",
        "username": "اسم المستخدم",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "confirm_password": "تأكيد كلمة المرور",
        "login_btn": "دخول",
        "signup_btn": "إنشاء الحساب",
        "logout_btn": "تسجيل خروج",
        "name_required": "يرجى تعبئة جميع الحقول.",
        "password_mismatch": "كلمتا المرور غير متطابقتين.",
        "password_short": "كلمة المرور يجب أن تكون 6 أحرف على الأقل.",
        "signup_success": "تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.",
        "invalid_login": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "user_exists": "اسم المستخدم أو البريد الإلكتروني مستخدم مسبقًا.",
        "welcome": "مرحبًا",
        "quick_access": "الوصول السريع",
        "match_details": "تفاصيل المباريات",
        "booking": "الحجز",
        "history": "السجل",
        "analytics": "التحليلات",
        "admin": "الإدارة",
        "support": "الدعم",
        "project_overview": "نبذة عن المشروع",
        "project_overview_text": "تم بناء هذا المشروع باستخدام Python وStreamlit وSQLite، وتم نشره على Streamlit Cloud وربطه مع GitHub. يهدف إلى تحسين تجربة حجز التذاكر من خلال نظام سهل الاستخدام ومرن.",
        "system_features": "مميزات النظام",
        "system_features_text": """
• عرض تفاصيل المباريات
• حجز التذاكر
• التسعير الديناميكي
• إنشاء QR Code
• تحميل التذكرة PDF
• سجل الحجوزات
• التحليلات والرسوم البيانية
• لوحة إدارة
• دعم العملاء
• دعم العربية والإنجليزية
""",
        "go_matches": "اذهب إلى المباريات",
        "go_booking": "اذهب إلى الحجز",
        "go_support": "اذهب إلى الدعم",
        "footer": "SmartSeat • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",
        "app_name": "SmartSeat",
        "app_subtitle": "Smart Stadium Ticket Pricing System",
        "home_desc": "An intelligent football ticket booking system that provides a professional booking experience including matches, booking, history, analytics, admin panel, and customer support.",
        "login_tab": "Login",
        "signup_tab": "Sign Up",
        "login_title": "Login",
        "signup_title": "Create New Account",
        "auth_desc": "Login or create a new account to access the system.",
        "full_name": "Full Name",
        "username": "Username",
        "email": "Email",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "login_btn": "Login",
        "signup_btn": "Create Account",
        "logout_btn": "Logout",
        "name_required": "Please fill in all fields.",
        "password_mismatch": "Passwords do not match.",
        "password_short": "Password must be at least 6 characters.",
        "signup_success": "Account created successfully. You can now login.",
        "invalid_login": "Invalid username or password.",
        "user_exists": "Username or email already exists.",
        "welcome": "Welcome",
        "quick_access": "Quick Access",
        "match_details": "Match Details",
        "booking": "Booking",
        "history": "History",
        "analytics": "Analytics",
        "admin": "Admin",
        "support": "Support",
        "project_overview": "Project Overview",
        "project_overview_text": "This project was built using Python, Streamlit, and SQLite. It is deployed on Streamlit Cloud and connected to GitHub. The goal is to improve the ticket booking experience through a flexible and user-friendly system.",
        "system_features": "System Features",
        "system_features_text": """
• Match details
• Ticket booking
• Dynamic pricing
• QR Code generation
• PDF ticket download
• Booking history
• Analytics and charts
• Admin panel
• Customer support
• Arabic and English support
""",
        "go_matches": "Go to Matches",
        "go_booking": "Go to Booking",
        "go_support": "Go to Support",
        "footer": "SmartSeat • Final Year Project"
    }
}

def t(key):
    return TXT[st.session_state.lang][key]

# =========================
# أدوات
# =========================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

logo_base64 = get_base64(logo_path)

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT,
    booking_date TEXT,
    match_name TEXT,
    seat_type TEXT,
    seat_section TEXT,
    ticket_count INTEGER,
    demand_level INTEGER,
    payment_method TEXT,
    discount_code TEXT,
    base_price REAL,
    final_price REAL,
    booking_time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pricing_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    elclasico_price REAL,
    kuwait_qadsia_price REAL,
    arabi_salmiya_price REAL,
    city_liverpool_price REAL,
    regular_extra REAL,
    premium_extra REAL,
    vip_extra REAL,
    section_a_extra REAL,
    section_b_extra REAL,
    section_c_extra REAL
)
""")

cursor.execute("SELECT COUNT(*) FROM pricing_settings WHERE id = 1")
exists = cursor.fetchone()[0]
if exists == 0:
    cursor.execute("""
        INSERT INTO pricing_settings (
            id,
            elclasico_price,
            kuwait_qadsia_price,
            arabi_salmiya_price,
            city_liverpool_price,
            regular_extra,
            premium_extra,
            vip_extra,
            section_a_extra,
            section_b_extra,
            section_c_extra
        ) VALUES (1, 28, 22, 18, 26, 0, 8, 18, 10, 6, 3)
    """)
    conn.commit()

# =========================
# CSS
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
        repeating-linear-gradient(
            135deg,
            rgba(0,0,0,0.07) 0px,
            rgba(0,0,0,0.07) 2px,
            transparent 2px,
            transparent 26px
        ),
        repeating-linear-gradient(
            -135deg,
            rgba(0,0,0,0.045) 0px,
            rgba(0,0,0,0.045) 2px,
            transparent 2px,
            transparent 34px
        ),
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
    filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.20));
}}

.sidebar-brand-title {{
    color: #111111;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 6px;
}}

.sidebar-brand-subtitle {{
    color: #181818;
    font-size: 14px;
    font-weight: 700;
    line-height: 1.7;
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
    margin-bottom: 4px;
}}

.hero-subtitle {{
    font-size: 18px;
    color: #E6C86E;
    font-weight: 700;
    margin-bottom: 8px;
}}

.hero-text {{
    color: #E6C86E;
    font-size: 16px;
    line-height: 1.9;
    max-width: 900px;
    margin: auto;
}}

.card {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    height: 100%;
}}

.card-title {{
    color: #D4AF37;
    font-size: 26px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 10px;
}}

.card-text {{
    color: #F0D98A;
    font-size: 16px;
    line-height: 1.9;
    white-space: pre-line;
}}

label {{
    color: #E6C86E !important;
    font-weight: 700 !important;
}}

.stTextInput > div > div {{
    background-color: rgba(15,15,15,0.95) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
}}

input {{
    color: white !important;
}}

.stButton > button {{
    width: 100%;
    min-height: 56px;
    border: none;
    border-radius: 18px;
    padding: 12px 18px;
    font-size: 18px;
    font-weight: 800;
    color: black;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
    box-shadow: 0 0 18px rgba(212,175,55,0.22);
}}

.stButton > button:hover {{
    box-shadow: 0 0 24px rgba(212,175,55,0.36);
}}

.mobile-nav-only {{
    display: none;
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
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
}}

.mobile-links a {{
    text-decoration: none !important;
    color: black !important;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 14px;
    font-weight: 800;
}}

.success-box {{
    background: linear-gradient(135deg, rgba(20,55,20,0.95), rgba(35,85,35,0.92));
    border: 1px solid rgba(80,200,120,0.35);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    color: #d7ffd7;
    font-size: 17px;
    font-weight: 700;
}}

.footer {{
    text-align:center;
    color:#D4AF37;
    font-size:15px;
    font-weight:600;
    margin-top:30px;
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
    }}
    .hero-title {{
        font-size: 28px !important;
    }}
    .hero-subtitle {{
        font-size: 15px !important;
    }}
    .hero-text, .card-text {{
        font-size: 13px !important;
        line-height: 1.9 !important;
    }}
    .card-title {{
        font-size: 20px !important;
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
        key="sidebar_lang_app"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

    if st.session_state.logged_in:
        st.markdown(f"**{t('welcome')} {st.session_state.user_name}**")
        if st.button(t("logout_btn"), key="logout_sidebar_btn"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.user_username = ""
            st.rerun()

# =========================
# تنقل الجوال
# =========================
st.markdown(f"""
<div class="mobile-nav-only">
    <div class="mobile-nav-box">
        <div class="mobile-nav-title">{t('quick_access')}</div>
        <div class="mobile-links">
            <a href="/Match_Details">{t('match_details')}</a>
            <a href="/Booking">{t('booking')}</a>
            <a href="/Support">{t('support')}</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# أعلى الصفحة
# =========================
top_lang_col1, top_lang_col2 = st.columns([4, 1])
with top_lang_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="top_lang_app"
    )
    st.session_state.lang = "ar" if page_lang == TXT["ar"]["arabic"] else "en"

# =========================
# الهيدر
# =========================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{t('app_name')}</div>
    <div class="hero-subtitle">{t('app_subtitle')}</div>
    <div class="hero-text">{t('home_desc')}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# محتوى الصفحة
# =========================
if not st.session_state.logged_in:
    st.markdown(f"""
    <div class="hero-box">
        <div class="hero-title">{t('login_title')} / {t('signup_title')}</div>
        <div class="hero-text">{t('auth_desc')}</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([t("login_tab"), t("signup_tab")])

    with tab1:
        with st.container(border=True):
            login_username = st.text_input(t("username"), key="login_username")
            login_password = st.text_input(t("password"), type="password", key="login_password")

            if st.button(t("login_btn"), key="login_btn_main"):
                if login_username.strip() == "" or login_password.strip() == "":
                    st.error(t("name_required"))
                else:
                    user = cursor.execute(
                        "SELECT full_name, username, password_hash FROM users WHERE username = ?",
                        (login_username.strip(),)
                    ).fetchone()

                    if user and user[2] == hash_password(login_password):
                        st.session_state.logged_in = True
                        st.session_state.user_name = user[0]
                        st.session_state.user_username = user[1]
                        st.success(t("login_success"))
                        st.rerun()
                    else:
                        st.error(t("invalid_login"))

    with tab2:
        with st.container(border=True):
            signup_full_name = st.text_input(t("full_name"), key="signup_full_name")
            signup_username = st.text_input(t("username"), key="signup_username")
            signup_email = st.text_input(t("email"), key="signup_email")
            signup_password = st.text_input(t("password"), type="password", key="signup_password")
            signup_confirm = st.text_input(t("confirm_password"), type="password", key="signup_confirm")

            if st.button(t("signup_btn"), key="signup_btn_main"):
                if not all([
                    signup_full_name.strip(),
                    signup_username.strip(),
                    signup_email.strip(),
                    signup_password.strip(),
                    signup_confirm.strip()
                ]):
                    st.error(t("name_required"))
                elif signup_password != signup_confirm:
                    st.error(t("password_mismatch"))
                elif len(signup_password) < 6:
                    st.error(t("password_short"))
                else:
                    exists_user = cursor.execute(
                        "SELECT id FROM users WHERE username = ? OR email = ?",
                        (signup_username.strip(), signup_email.strip())
                    ).fetchone()

                    if exists_user:
                        st.error(t("user_exists"))
                    else:
                        cursor.execute("""
                            INSERT INTO users (full_name, username, email, password_hash, created_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            signup_full_name.strip(),
                            signup_username.strip(),
                            signup_email.strip(),
                            hash_password(signup_password),
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ))
                        conn.commit()
                        st.markdown(f'<div class="success-box">{t("signup_success")}</div>', unsafe_allow_html=True)
else:
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{t('project_overview')}</div>
            <div class="card-text">{t('project_overview_text')}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{t('system_features')}</div>
            <div class="card-text">{t('system_features_text')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button(t("go_matches"), key="go_matches_btn"):
            st.switch_page("pages/0_Match_Details.py")
    with a2:
        if st.button(t("go_booking"), key="go_booking_btn"):
            st.switch_page("pages/1_Booking.py")
    with a3:
        if st.button(t("go_support"), key="go_support_btn"):
            st.switch_page("pages/5_Support.py")

st.markdown(f'<div class="footer">{t("footer")}</div>', unsafe_allow_html=True)
conn.close()

import streamlit as st
from pathlib import Path
import sqlite3
import pandas as pd
import base64

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent.parent
logo_path = base_dir / "assets" / "logo.png"
db_path = base_dir / "tickets.db"

st.set_page_config(
    page_title="SmartSeat - Admin Panel",
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

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# =========================
# فحص هل الجهاز هاتف
# =========================
try:
    user_agent = st.context.headers.get("User-Agent", "")
except Exception:
    user_agent = ""

is_mobile = any(x in user_agent for x in ["Mobile", "Android", "iPhone"])

# =========================
# الترجمة
# =========================
TXT = {
    "ar": {
        "lang_label": "Language/اللغة",
        "arabic": "العربية",
        "english": "English",

        "sidebar_title": "لوحة الإدارة",
        "sidebar_desc": "لوحة التحكم الخاصة بالإدارة.",

        "login_title": "لوحة الإدارة",
        "login_subtitle": "Admin Control Panel",
        "login_desc": "أدخل كلمة المرور للوصول إلى أدوات الإدارة والتحكم بالحجوزات والأسعار.",
        "admin_login_section": "تسجيل دخول الإدارة",
        "password": "كلمة المرور",
        "login_btn": "🔐 دخول",
        "wrong_password": "كلمة المرور غير صحيحة.",

        "dashboard_title": "لوحة الإدارة",
        "dashboard_subtitle": "SmartSeat Admin Dashboard",
        "dashboard_desc": "من هنا يمكنك مراجعة الحجوزات، حذف أي سجل، وتعديل الأسعار الأساسية للمباريات والمقاعد.",
        "logout": "🚪 تسجيل خروج",

        "metric_total_bookings": "إجمالي الحجوزات",
        "metric_total_revenue": "إجمالي الإيرادات (د.ك)",
        "metric_total_tickets": "إجمالي التذاكر",

        "delete_section": "حذف حجز",
        "delete_booking_id": "رقم الحجز المراد حذفه",
        "delete_btn": "🗑️ حذف الحجز",
        "enter_booking_id": "يرجى إدخال رقم الحجز.",
        "booking_not_found": "رقم الحجز غير موجود.",
        "booking_deleted": "تم حذف الحجز بنجاح.",
        "booking_id_must_be_number": "رقم الحجز يجب أن يكون رقمًا صحيحًا.",

        "pricing_section": "تعديل الأسعار",
        "pricing_note": "أي تعديل هنا ينعكس مباشرة على صفحة الحجز.",
        "save_prices": "💾 حفظ الأسعار",
        "prices_saved": "تم حفظ الأسعار بنجاح.",

        "match1": "برشلونة × ريال مدريد",
        "match2": "الكويت × القادسية",
        "match3": "العربي × السالمية",
        "match4": "مانشستر سيتي × ليفربول",
        "regular_extra": "زيادة Regular",
        "premium_extra": "زيادة Premium",
        "vip_extra": "زيادة VIP",
        "section_a_extra": "زيادة Section A",
        "section_b_extra": "زيادة Section B",
        "section_c_extra": "زيادة Section C",

        "all_bookings": "جميع الحجوزات",
        "no_bookings": "لا توجد حجوزات حالياً.",

        "home": "الرئيسية",
        "matches": "المباريات",
        "booking": "الحجز",
        "history": "السجل",
        "analytics": "التحليلات",
        "support": "الدعم",
        "quick_access": "الوصول السريع",

        "col_id": "رقم الحجز",
        "col_customer_name": "اسم العميل",
        "col_phone": "رقم الهاتف",
        "col_booking_date": "التاريخ",
        "col_match_name": "المباراة",
        "col_seat_type": "نوع المقعد",
        "col_seat_section": "القسم",
        "col_ticket_count": "عدد التذاكر",
        "col_demand_level": "مستوى الطلب",
        "col_payment_method": "طريقة الدفع",
        "col_discount_code": "كود الخصم",
        "col_base_price": "السعر الأساسي",
        "col_final_price": "السعر النهائي",
        "col_booking_time": "وقت الحجز",

        "footer": "SmartSeat Admin Panel • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",

        "sidebar_title": "Admin Panel",
        "sidebar_desc": "Administration control dashboard.",

        "login_title": "Admin Panel",
        "login_subtitle": "Admin Control Panel",
        "login_desc": "Enter the password to access admin tools and control bookings and prices.",
        "admin_login_section": "Admin Login",
        "password": "Password",
        "login_btn": "🔐 Login",
        "wrong_password": "Incorrect password.",

        "dashboard_title": "Admin Panel",
        "dashboard_subtitle": "SmartSeat Admin Dashboard",
        "dashboard_desc": "From here you can review bookings, delete any record, and update the base prices for matches and seats.",
        "logout": "🚪 Logout",

        "metric_total_bookings": "Total Bookings",
        "metric_total_revenue": "Total Revenue (KD)",
        "metric_total_tickets": "Total Tickets",

        "delete_section": "Delete Booking",
        "delete_booking_id": "Booking ID to delete",
        "delete_btn": "🗑️ Delete Booking",
        "enter_booking_id": "Please enter the booking ID.",
        "booking_not_found": "Booking ID not found.",
        "booking_deleted": "Booking deleted successfully.",
        "booking_id_must_be_number": "Booking ID must be a valid number.",

        "pricing_section": "Update Prices",
        "pricing_note": "Any change here will immediately affect the booking page.",
        "save_prices": "💾 Save Prices",
        "prices_saved": "Prices saved successfully.",

        "match1": "Barcelona vs Real Madrid",
        "match2": "Kuwait vs Qadsia",
        "match3": "Al Arabi vs Al Salmiya",
        "match4": "Manchester City vs Liverpool",
        "regular_extra": "Regular Extra",
        "premium_extra": "Premium Extra",
        "vip_extra": "VIP Extra",
        "section_a_extra": "Section A Extra",
        "section_b_extra": "Section B Extra",
        "section_c_extra": "Section C Extra",

        "all_bookings": "All Bookings",
        "no_bookings": "There are no bookings at the moment.",

        "home": "Home",
        "matches": "Matches",
        "booking": "Booking",
        "history": "History",
        "analytics": "Analytics",
        "support": "Support",
        "quick_access": "Quick Access",

        "col_id": "Booking ID",
        "col_customer_name": "Customer Name",
        "col_phone": "Phone Number",
        "col_booking_date": "Date",
        "col_match_name": "Match",
        "col_seat_type": "Seat Type",
        "col_seat_section": "Section",
        "col_ticket_count": "Ticket Count",
        "col_demand_level": "Demand Level",
        "col_payment_method": "Payment Method",
        "col_discount_code": "Discount Code",
        "col_base_price": "Base Price",
        "col_final_price": "Final Price",
        "col_booking_time": "Booking Time",

        "footer": "SmartSeat Admin Panel • Final Year Project"
    }
}

def t(k):
    return TXT[st.session_state.lang][k]

# =========================
# قاعدة البيانات
# =========================
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

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
# الباسورد
# =========================
ADMIN_PASSWORD = "Ktech166"

# =========================
# اللوقو
# =========================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64(logo_path)

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
        radial-gradient(circle at 10% 15%, rgba(212,175,55,0.09), transparent 25%),
        radial-gradient(circle at 90% 85%, rgba(212,175,55,0.06), transparent 30%),
        linear-gradient(135deg, #040404 0%, #0a0a0a 45%, #111111 100%);
    color: white;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0b0b0b 0%, #151515 100%);
    border-left: none;
    border-right: 1px solid rgba(212,175,55,0.20);
}}

[data-testid="stSidebar"] {{
    right: 0 !important;
    left: auto !important;
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

.sidebar-logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 12px;
}}

.sidebar-logo {{
    width: 120px;
    max-width: 100%;
    display: block;
    margin: 0 auto;
    filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.20));
}}

.sidebar-brand-title {{
    color: #111111;
    font-size: 30px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 6px;
    line-height: 1.1;
}}

.sidebar-brand-subtitle {{
    color: #181818;
    font-size: 14px;
    font-weight: 700;
    text-align: center;
    line-height: 1.7;
}}

.block-container {{
    padding-top: 0.45rem !important;
    padding-bottom: 1rem !important;
    max-width: 1250px;
}}

.logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -4px;
    margin-bottom: -8px;
}}

.logo-wrap img {{
    width: 220px;
    max-width: 100%;
    filter: drop-shadow(0px 0px 20px rgba(212,175,55,0.68));
}}

.hero-box {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.28);
    border-radius: 30px;
    padding: 24px 30px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    margin-top: 0;
    margin-bottom: 12px;
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
    max-width: 850px;
    margin: auto;
}}

.section-title {{
    color: #D4AF37;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 14px;
}}

.metric-box {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.28);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 0 18px rgba(212,175,55,0.10);
    transition: all 0.25s ease;
}}

.metric-box:hover {{
    transform: translateY(-4px);
    box-shadow: 0 0 26px rgba(212,175,55,0.24);
}}

.metric-number {{
    color: #FFD700;
    font-size: 32px;
    font-weight: 900;
}}

.metric-label {{
    color: #E6C86E;
    font-size: 16px;
}}

.quick-box {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 24px;
    padding: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    margin-top: 10px;
    margin-bottom: 10px;
}}

.quick-title {{
    color: #D4AF37;
    text-align: center;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 0;
}}

.mobile-only {{
    display: none;
}}

label {{
    color: #E6C86E !important;
    font-weight: 700 !important;
}}

.stTextInput > div > div,
.stNumberInput > div > div {{
    background-color: rgba(15,15,15,0.92) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
}}

input {{
    color: white !important;
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 18px;
    overflow: hidden;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.24);
    overflow: hidden !important;
}}

.stButton > button {{
    width: 100%;
    min-height: 56px;
    border: none;
    border-radius: 16px;
    padding: 10px 16px;
    font-size: 18px;
    font-weight: 800;
    color: black;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
    box-shadow: 0 0 18px rgba(212,175,55,0.22);
    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 0 28px rgba(212,175,55,0.38);
}}

.warning-box {{
    background: linear-gradient(135deg, rgba(70,35,10,0.95), rgba(90,50,15,0.92));
    border: 1px solid rgba(255,190,90,0.35);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    color: #ffe7b3;
    font-size: 17px;
    font-weight: 700;
    margin-top: 10px;
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
    margin-top: 10px;
}}

.gold-note {{
    color: #E6C86E;
    text-align: center;
    font-size: 15px;
}}

.footer {{
    text-align: center;
    color: #D4AF37;
    font-size: 15px;
    font-weight: 600;
    margin-top: 16px;
    opacity: 0.95;
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

    .mobile-only {{
        display: block !important;
    }}

    .block-container {{
        padding-top: 0.3rem !important;
        padding-bottom: 0.7rem !important;
        padding-right: 0.7rem !important;
        padding-left: 0.7rem !important;
        max-width: 100% !important;
    }}

    .logo-wrap {{
        margin-top: 0 !important;
        margin-bottom: -4px !important;
    }}

    .logo-wrap img {{
        width: 170px !important;
        max-width: 88% !important;
    }}

    .hero-box {{
        padding: 18px 14px !important;
        border-radius: 22px !important;
        margin-bottom: 10px !important;
    }}

    .hero-title {{
        font-size: 28px !important;
        line-height: 1.3 !important;
    }}

    .hero-subtitle {{
        font-size: 15px !important;
    }}

    .hero-text {{
        font-size: 13px !important;
        line-height: 1.9 !important;
    }}

    .section-title {{
        font-size: 22px !important;
        margin-bottom: 8px !important;
    }}

    .metric-number {{
        font-size: 24px !important;
    }}

    .metric-label {{
        font-size: 13px !important;
    }}

    .gold-note {{
        font-size: 13px !important;
        line-height: 1.8 !important;
    }}

    .warning-box,
    .success-box {{
        font-size: 14px !important;
        line-height: 1.8 !important;
    }}

    .footer {{
        font-size: 13px !important;
        margin-top: 14px !important;
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
        <div class="sidebar-logo-wrap">
            <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo">
        </div>
        <div class="sidebar-brand-title">SmartSeat</div>
        <div class="sidebar-brand-subtitle">Smart Stadium Ticket Pricing System</div>
    </div>
    """, unsafe_allow_html=True)

    lang_view = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="admin_lang_sidebar"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

    st.markdown("---")
    st.markdown(f"### {t('sidebar_title')}")
    st.markdown(t("sidebar_desc"))

# =========================
# أعلى الصفحة
# =========================
top_lang_col1, top_lang_col2 = st.columns([4, 1])
with top_lang_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="admin_lang_top"
    )
    st.session_state.lang = "ar" if page_lang == TXT["ar"]["arabic"] else "en"

# =========================
# تسجيل الدخول
# =========================
if not st.session_state.admin_logged_in:
    st.markdown(f"""
    <div class="hero-box">
        <div class="hero-title">{t('login_title')}</div>
        <div class="hero-subtitle">{t('login_subtitle')}</div>
        <div class="hero-text">
            {t('login_desc')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f'<div class="section-title">{t("admin_login_section")}</div>', unsafe_allow_html=True)
        password_input = st.text_input(t("password"), type="password")

        if st.button(t("login_btn")):
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.markdown(f'<div class="warning-box">{t("wrong_password")}</div>', unsafe_allow_html=True)

    # التنقل - هاتف فقط - آخر الصفحة
    if is_mobile:
        st.markdown(
            f"""
            <div class="mobile-only">
                <div class="quick-box">
                    <div class="quick-title">{t('quick_access')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # صف 1
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t('home'), key="m_home_4_login", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button(t('matches'), key="m_matches_4_login", use_container_width=True):
                st.switch_page("pages/0_Match_Details.py")

        # صف 2
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t('booking'), key="m_booking_4_login", use_container_width=True):
                st.switch_page("pages/1_Booking.py")
        with col2:
            if st.button(t('history'), key="m_history_4_login", use_container_width=True):
                st.switch_page("pages/2_History.py")

        # صف 3
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t('analytics'), key="m_analytics_4_login", use_container_width=True):
                st.switch_page("pages/3_Analytics.py")
        with col2:
            if st.button(t('support'), key="m_support_4_login", use_container_width=True):
                st.switch_page("pages/5_Support.py")

    st.markdown(f"""
    <div class="footer">
        {t("footer")}
    </div>
    """, unsafe_allow_html=True)

    conn.close()
    st.stop()

# =========================
# الهيدر
# =========================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{t('dashboard_title')}</div>
    <div class="hero-subtitle">{t('dashboard_subtitle')}</div>
    <div class="hero-text">
        {t('dashboard_desc')}
    </div>
</div>
""", unsafe_allow_html=True)

top1, top2 = st.columns([4, 1])
with top2:
    if st.button(t("logout")):
        st.session_state.admin_logged_in = False
        conn.close()
        st.rerun()

# =========================
# قراءة البيانات
# =========================
df = pd.read_sql_query("SELECT * FROM bookings ORDER BY id DESC", conn)
pricing_df = pd.read_sql_query("SELECT * FROM pricing_settings WHERE id = 1", conn)
pricing = pricing_df.iloc[0]

# =========================
# المؤشرات
# =========================
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{len(df)}</div>
        <div class="metric-label">{t('metric_total_bookings')}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    total_revenue = 0 if df.empty else round(df["final_price"].sum(), 2)
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_revenue}</div>
        <div class="metric-label">{t('metric_total_revenue')}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    total_tickets = 0 if df.empty else int(df["ticket_count"].sum())
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_tickets}</div>
        <div class="metric-label">{t('metric_total_tickets')}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# حذف حجز
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("delete_section")}</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        delete_id = st.text_input(t("delete_booking_id"))
    with d2:
        delete_clicked = st.button(t("delete_btn"))

    if delete_clicked:
        if delete_id.strip() == "":
            st.markdown(f'<div class="warning-box">{t("enter_booking_id")}</div>', unsafe_allow_html=True)
        else:
            try:
                delete_id_int = int(delete_id)
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE id = ?", (delete_id_int,))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    st.markdown(f'<div class="warning-box">{t("booking_not_found")}</div>', unsafe_allow_html=True)
                else:
                    cursor.execute("DELETE FROM bookings WHERE id = ?", (delete_id_int,))
                    conn.commit()
                    st.markdown(f'<div class="success-box">{t("booking_deleted")}</div>', unsafe_allow_html=True)
                    conn.close()
                    st.rerun()
            except ValueError:
                st.markdown(f'<div class="warning-box">{t("booking_id_must_be_number")}</div>', unsafe_allow_html=True)

# =========================
# تعديل الأسعار
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("pricing_section")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="gold-note">{t("pricing_note")}</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        elclasico_price = st.number_input(t("match1"), value=float(pricing["elclasico_price"]), step=1.0)
        kuwait_qadsia_price = st.number_input(t("match2"), value=float(pricing["kuwait_qadsia_price"]), step=1.0)
        arabi_salmiya_price = st.number_input(t("match3"), value=float(pricing["arabi_salmiya_price"]), step=1.0)
        city_liverpool_price = st.number_input(t("match4"), value=float(pricing["city_liverpool_price"]), step=1.0)

    with a2:
        regular_extra = st.number_input(t("regular_extra"), value=float(pricing["regular_extra"]), step=1.0)
        premium_extra = st.number_input(t("premium_extra"), value=float(pricing["premium_extra"]), step=1.0)
        vip_extra = st.number_input(t("vip_extra"), value=float(pricing["vip_extra"]), step=1.0)
        section_a_extra = st.number_input(t("section_a_extra"), value=float(pricing["section_a_extra"]), step=1.0)
        section_b_extra = st.number_input(t("section_b_extra"), value=float(pricing["section_b_extra"]), step=1.0)
        section_c_extra = st.number_input(t("section_c_extra"), value=float(pricing["section_c_extra"]), step=1.0)

    if st.button(t("save_prices")):
        cursor.execute("""
            UPDATE pricing_settings
            SET
                elclasico_price = ?,
                kuwait_qadsia_price = ?,
                arabi_salmiya_price = ?,
                city_liverpool_price = ?,
                regular_extra = ?,
                premium_extra = ?,
                vip_extra = ?,
                section_a_extra = ?,
                section_b_extra = ?,
                section_c_extra = ?
            WHERE id = 1
        """, (
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
        ))
        conn.commit()
        st.markdown(f'<div class="success-box">{t("prices_saved")}</div>', unsafe_allow_html=True)

# =========================
# جدول الحجوزات
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("all_bookings")}</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown(f'<div class="warning-box">{t("no_bookings")}</div>', unsafe_allow_html=True)
    else:
        display_df = df.copy()
        display_df = display_df.rename(columns={
            "id": t("col_id"),
            "customer_name": t("col_customer_name"),
            "phone": t("col_phone"),
            "booking_date": t("col_booking_date"),
            "match_name": t("col_match_name"),
            "seat_type": t("col_seat_type"),
            "seat_section": t("col_seat_section"),
            "ticket_count": t("col_ticket_count"),
            "demand_level": t("col_demand_level"),
            "payment_method": t("col_payment_method"),
            "discount_code": t("col_discount_code"),
            "base_price": t("col_base_price"),
            "final_price": t("col_final_price"),
            "booking_time": t("col_booking_time")
        })
        st.dataframe(display_df, use_container_width=True)

# =========================
# التنقل - هاتف فقط - آخر الصفحة
# =========================
if is_mobile:
    st.markdown(
        f"""
        <div class="mobile-only">
            <div class="quick-box">
                <div class="quick-title">{t('quick_access')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # صف 1
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('home'), key="m_home_4", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button(t('matches'), key="m_matches_4", use_container_width=True):
            st.switch_page("pages/0_Match_Details.py")

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('booking'), key="m_booking_4", use_container_width=True):
            st.switch_page("pages/1_Booking.py")
    with col2:
        if st.button(t('history'), key="m_history_4", use_container_width=True):
            st.switch_page("pages/2_History.py")

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('analytics'), key="m_analytics_4", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")
    with col2:
        if st.button(t('support'), key="m_support_4", use_container_width=True):
            st.switch_page("pages/5_Support.py")

# =========================
# الفوتر
# =========================
st.markdown(f"""
<div class="footer">
    {t("footer")}
</div>
""", unsafe_allow_html=True)

conn.close()

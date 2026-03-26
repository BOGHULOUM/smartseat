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
    page_title="SmartSeat - History",
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

        "need_login": "يجب تسجيل الدخول أولاً للوصول إلى هذه الصفحة.",
        "back_home": "العودة للرئيسية",

        "page_title": "سجل الحجوزات",
        "page_subtitle": "Booking History Dashboard",
        "page_desc": "يمكنك من هنا عرض جميع الحجوزات المسجلة، والبحث عن عميل محدد، واستخدام الفلاتر للوصول السريع إلى البيانات المطلوبة.",

        "sidebar_title": "سجل الحجوزات",
        "sidebar_desc": "راجع جميع الحجوزات، وابحث أو فلتر حسب البيانات المطلوبة.",
        "sidebar_note_title": "ملاحظة",
        "sidebar_note_text": "الحذف متاح فقط من لوحة الإدارة.",

        "metric_total_bookings": "إجمالي الحجوزات",
        "metric_total_revenue": "إجمالي الإيرادات (د.ك)",
        "metric_total_tickets": "إجمالي التذاكر",

        "filter_section": "البحث والفلترة",
        "search_label": "بحث باسم العميل أو رقم الهاتف",
        "match_filter": "فلترة حسب المباراة",
        "seat_filter": "فلترة حسب نوع المقعد",
        "payment_filter": "فلترة حسب طريقة الدفع",
        "all": "الكل",
        "filter_note": "لحذف أي حجز، استخدم لوحة الإدارة فقط.",

        "table_section": "جدول الحجوزات",
        "no_results": "لا توجد حجوزات مطابقة للبحث أو الفلاتر الحالية.",

        "home": "الرئيسية",
        "matches": "المباريات",
        "booking": "الحجز",
        "analytics": "التحليلات",
        "admin": "الإدارة",
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

        "footer": "SmartSeat History • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",

        "need_login": "You must login first to access this page.",
        "back_home": "Back to Home",

        "page_title": "Booking History",
        "page_subtitle": "Booking History Dashboard",
        "page_desc": "From here, you can view all recorded bookings, search for a specific customer, and use filters for quick access to the required data.",

        "sidebar_title": "Booking History",
        "sidebar_desc": "Review all bookings and search or filter by the required details.",
        "sidebar_note_title": "Note",
        "sidebar_note_text": "Deleting bookings is only available from the Admin panel.",

        "metric_total_bookings": "Total Bookings",
        "metric_total_revenue": "Total Revenue (KD)",
        "metric_total_tickets": "Total Tickets",

        "filter_section": "Search & Filters",
        "search_label": "Search by customer name or phone number",
        "match_filter": "Filter by match",
        "seat_filter": "Filter by seat type",
        "payment_filter": "Filter by payment method",
        "all": "All",
        "filter_note": "To delete any booking, please use the Admin panel only.",

        "table_section": "Bookings Table",
        "no_results": "No bookings match the current search or filters.",

        "home": "Home",
        "matches": "Matches",
        "booking": "Booking",
        "analytics": "Analytics",
        "admin": "Admin",
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

        "footer": "SmartSeat History • Final Year Project"
    }
}

def t(k):
    return TXT[st.session_state.lang][k]

# =========================
# اللوقو
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
    background: linear-gradient(135deg, rgba(18,18,18,0.95), rgba(30,30,30,0.92));
    border: 1px solid rgba(212,175,55,0.34);
    border-radius: 30px;
    padding: 24px 30px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.42);
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
    background: linear-gradient(180deg, rgba(255,215,0,0.14), rgba(212,175,55,0.08));
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 0 18px rgba(212,175,55,0.12);
    transition: all 0.25s ease;
}}

.metric-box:hover {{
    transform: translateY(-4px);
    box-shadow: 0 0 26px rgba(212,175,55,0.30);
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
div[data-baseweb="select"] > div {{
    background-color: rgba(15,15,15,0.95) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
    transition: all 0.25s ease !important;
}}

.stTextInput > div > div:hover,
div[data-baseweb="select"] > div:hover {{
    box-shadow: 0 0 14px rgba(212,175,55,0.25) !important;
    border: 1px solid rgba(212,175,55,0.45) !important;
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
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    overflow: hidden !important;
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

.gold-note {{
    color: #E6C86E;
    text-align: center;
    font-size: 15px;
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
    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 0 24px rgba(212,175,55,0.36);
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

    .warning-box {{
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
conn.commit()

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
        key="history_lang_sidebar"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

    st.markdown("---")
    st.markdown(f"### {t('sidebar_title')}")
    st.markdown(t("sidebar_desc"))
    st.markdown(f"### {t('sidebar_note_title')}")
    st.markdown(t("sidebar_note_text"))

# =========================
# أعلى الصفحة
# =========================
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="history_lang_top"
    )
    st.session_state.lang = "ar" if page_lang == TXT["ar"]["arabic"] else "en"

# =========================
# الهيدر
# =========================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{t('page_title')}</div>
    <div class="hero-subtitle">{t('page_subtitle')}</div>
    <div class="hero-text">
        {t('page_desc')}
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# قراءة البيانات
# =========================
df = pd.read_sql_query("SELECT * FROM bookings ORDER BY id DESC", conn)

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
# البحث والفلترة
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("filter_section")}</div>', unsafe_allow_html=True)

    match_options = sorted(df["match_name"].dropna().unique().tolist()) if not df.empty else []
    seat_options = sorted(df["seat_type"].dropna().unique().tolist()) if not df.empty else []
    payment_options = sorted(df["payment_method"].dropna().unique().tolist()) if not df.empty else []

    f1, f2 = st.columns(2)
    with f1:
        search_text = st.text_input(t("search_label"))
    with f2:
        selected_match = st.selectbox(
            t("match_filter"),
            [t("all")] + match_options
        )

    f3, f4 = st.columns(2)
    with f3:
        selected_seat = st.selectbox(
            t("seat_filter"),
            [t("all")] + seat_options
        )
    with f4:
        selected_payment = st.selectbox(
            t("payment_filter"),
            [t("all")] + payment_options
        )

    st.markdown(f'<div class="gold-note">{t("filter_note")}</div>', unsafe_allow_html=True)

# =========================
# الفلترة
# =========================
filtered_df = df.copy()

if search_text.strip():
    s = search_text.strip()
    filtered_df = filtered_df[
        filtered_df["customer_name"].astype(str).str.contains(s, case=False, na=False) |
        filtered_df["phone"].astype(str).str.contains(s, case=False, na=False)
    ]

if selected_match != t("all"):
    filtered_df = filtered_df[filtered_df["match_name"] == selected_match]

if selected_seat != t("all"):
    filtered_df = filtered_df[filtered_df["seat_type"] == selected_seat]

if selected_payment != t("all"):
    filtered_df = filtered_df[filtered_df["payment_method"] == selected_payment]

# =========================
# الجدول
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("table_section")}</div>', unsafe_allow_html=True)

    if filtered_df.empty:
        st.markdown(f'<div class="warning-box">{t("no_results")}</div>', unsafe_allow_html=True)
    else:
        display_df = filtered_df.copy()
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
        if st.button(t('home'), key="m_home_2", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button(t('matches'), key="m_matches_2", use_container_width=True):
            st.switch_page("pages/0_Match_Details.py")

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('booking'), key="m_booking_2", use_container_width=True):
            st.switch_page("pages/1_Booking.py")
    with col2:
        if st.button(t('analytics'), key="m_analytics_2", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('admin'), key="m_admin_2", use_container_width=True):
            st.switch_page("pages/4_Admin.py")
    with col2:
        if st.button(t('support'), key="m_support_2", use_container_width=True):
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

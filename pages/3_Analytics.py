import streamlit as st
from pathlib import Path
import sqlite3
import pandas as pd
import base64
import matplotlib.pyplot as plt

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent.parent
logo_path = base_dir / "assets" / "logo.png"
db_path = base_dir / "tickets.db"

st.set_page_config(
    page_title="SmartSeat - Analytics",
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

        "page_title": "التحليلات",
        "page_subtitle": "Analytics Dashboard",
        "page_desc": "من هذه الصفحة يمكنك متابعة الأداء العام للنظام، وتحليل الحجوزات، والإيرادات، وأنواع المقاعد، ومستوى الطلب بشكل واضح واحترافي.",

        "sidebar_title": "التحليلات",
        "sidebar_desc": "تابع الأداء العام، الإيرادات، الطلب، وأنواع المقاعد.",

        "no_data": "لا توجد بيانات كافية لعرض التحليلات حالياً. قم بإضافة حجوزات أولاً.",

        "metric_total_bookings": "إجمالي الحجوزات",
        "metric_total_tickets": "إجمالي التذاكر",
        "metric_total_revenue": "إجمالي الإيرادات (د.ك)",
        "metric_avg_demand": "متوسط الطلب",

        "best_match_title": "أفضل مباراة مبيعاً",
        "best_seat_title": "أكثر نوع مقعد طلباً",
        "best_payment_title": "أكثر طريقة دفع استخداماً",
        "tickets_count": "بعدد تذاكر",
        "operations_count": "بعدد عمليات",

        "chart_match_tickets": "عدد التذاكر حسب المباراة",
        "chart_match_revenue": "الإيرادات حسب المباراة",
        "chart_seat_tickets": "عدد التذاكر حسب نوع المقعد",
        "chart_payment_methods": "طرق الدفع الأكثر استخداماً",
        "chart_avg_demand": "متوسط الطلب حسب المباراة",

        "x_match": "المباراة",
        "x_seat": "نوع المقعد",
        "y_tickets": "عدد التذاكر",
        "y_revenue": "الإيرادات",
        "y_avg_demand": "متوسط الطلب",

        "plot_bookings_by_match": "الحجوزات حسب المباراة",
        "plot_revenue_by_match": "الإيرادات حسب المباراة",
        "plot_top_seats": "المقاعد الأكثر طلباً",
        "plot_payment_distribution": "توزيع طرق الدفع",
        "plot_avg_demand": "متوسط مستوى الطلب",

        "summary_table": "ملخص البيانات",

        "home": "الرئيسية",
        "matches": "المباريات",
        "booking": "الحجز",
        "history": "السجل",
        "admin": "الإدارة",
        "support": "الدعم",
        "quick_access": "الوصول السريع",

        "col_customer_name": "اسم العميل",
        "col_match_name": "المباراة",
        "col_seat_type": "نوع المقعد",
        "col_seat_section": "القسم",
        "col_ticket_count": "عدد التذاكر",
        "col_demand_level": "مستوى الطلب",
        "col_payment_method": "طريقة الدفع",
        "col_final_price": "السعر النهائي",

        "footer": "SmartSeat Analytics • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",

        "need_login": "You must login first to access this page.",
        "back_home": "Back to Home",

        "page_title": "Analytics",
        "page_subtitle": "Analytics Dashboard",
        "page_desc": "From this page, you can monitor the overall system performance and analyze bookings, revenue, seat types, and demand level in a clear and professional way.",

        "sidebar_title": "Analytics",
        "sidebar_desc": "Track overall performance, revenue, demand, and seat types.",

        "no_data": "There is not enough data to display analytics right now. Please add bookings first.",

        "metric_total_bookings": "Total Bookings",
        "metric_total_tickets": "Total Tickets",
        "metric_total_revenue": "Total Revenue (KD)",
        "metric_avg_demand": "Average Demand",

        "best_match_title": "Best-Selling Match",
        "best_seat_title": "Most Requested Seat Type",
        "best_payment_title": "Most Used Payment Method",
        "tickets_count": "Tickets Count",
        "operations_count": "Operations Count",

        "chart_match_tickets": "Tickets by Match",
        "chart_match_revenue": "Revenue by Match",
        "chart_seat_tickets": "Tickets by Seat Type",
        "chart_payment_methods": "Most Used Payment Methods",
        "chart_avg_demand": "Average Demand by Match",

        "x_match": "Match",
        "x_seat": "Seat Type",
        "y_tickets": "Tickets",
        "y_revenue": "Revenue",
        "y_avg_demand": "Average Demand",

        "plot_bookings_by_match": "Bookings by Match",
        "plot_revenue_by_match": "Revenue by Match",
        "plot_top_seats": "Most Requested Seats",
        "plot_payment_distribution": "Payment Methods Distribution",
        "plot_avg_demand": "Average Demand Level",

        "summary_table": "Data Summary",

        "home": "Home",
        "matches": "Matches",
        "booking": "Booking",
        "history": "History",
        "admin": "Admin",
        "support": "Support",
        "quick_access": "Quick Access",

        "col_customer_name": "Customer Name",
        "col_match_name": "Match",
        "col_seat_type": "Seat Type",
        "col_seat_section": "Section",
        "col_ticket_count": "Ticket Count",
        "col_demand_level": "Demand Level",
        "col_payment_method": "Payment Method",
        "col_final_price": "Final Price",

        "footer": "SmartSeat Analytics • Final Year Project"
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
        radial-gradient(circle at 10% 15%, rgba(212,175,55,0.09), transparent 25%),
        radial-gradient(circle at 90% 85%, rgba(212,175,55,0.06), transparent 30%),
        linear-gradient(135deg, #040404 0%, #0a0a0a 45%, #111111 100%);
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

.insight-card {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.24);
    margin-bottom: 18px;
    transition: all 0.25s ease;
}}

.insight-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 0 24px rgba(212,175,55,0.22);
}}

.insight-title {{
    color: #D4AF37;
    font-size: 24px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 12px;
}}

.insight-line {{
    color: #F0D98A;
    font-size: 18px;
    text-align: center;
    margin: 10px 0;
    line-height: 1.8;
    word-break: break-word;
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

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.24);
    overflow: hidden !important;
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 18px;
    overflow: hidden;
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

    .insight-title {{
        font-size: 18px !important;
    }}

    .insight-line {{
        font-size: 14px !important;
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
        key="analytics_lang_sidebar"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

    st.markdown("---")
    st.markdown(f"### {t('sidebar_title')}")
    st.markdown(t("sidebar_desc"))

# =========================
# أعلى الصفحة
# =========================
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="analytics_lang_top"
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

df = pd.read_sql_query("SELECT * FROM bookings ORDER BY id DESC", conn)

if df.empty:
    st.markdown(f'<div class="warning-box">{t("no_data")}</div>', unsafe_allow_html=True)
    conn.close()
    st.stop()

# =========================
# تجهيز البيانات
# =========================
df["ticket_count"] = pd.to_numeric(df["ticket_count"], errors="coerce").fillna(0)
df["demand_level"] = pd.to_numeric(df["demand_level"], errors="coerce").fillna(0)
df["final_price"] = pd.to_numeric(df["final_price"], errors="coerce").fillna(0)

total_bookings = len(df)
total_tickets = int(df["ticket_count"].sum())
total_revenue = round(df["final_price"].sum(), 2)
avg_demand = round(df["demand_level"].mean(), 1)

top_match = df.groupby("match_name")["ticket_count"].sum().sort_values(ascending=False)
top_seat = df.groupby("seat_type")["ticket_count"].sum().sort_values(ascending=False)
payment_stats = df.groupby("payment_method")["ticket_count"].sum().sort_values(ascending=False)
revenue_by_match = df.groupby("match_name")["final_price"].sum().sort_values(ascending=False)
demand_by_match = df.groupby("match_name")["demand_level"].mean().sort_values(ascending=False)

best_match_name = top_match.index[0] if not top_match.empty else "-"
best_match_tickets = int(top_match.iloc[0]) if not top_match.empty else 0

best_seat_name = top_seat.index[0] if not top_seat.empty else "-"
best_seat_tickets = int(top_seat.iloc[0]) if not top_seat.empty else 0

best_payment_name = payment_stats.index[0] if not payment_stats.empty else "-"
best_payment_count = int(payment_stats.iloc[0]) if not payment_stats.empty else 0

# =========================
# المؤشرات
# =========================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_bookings}</div>
        <div class="metric-label">{t('metric_total_bookings')}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_tickets}</div>
        <div class="metric-label">{t('metric_total_tickets')}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_revenue}</div>
        <div class="metric-label">{t('metric_total_revenue')}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{avg_demand}/10</div>
        <div class="metric-label">{t('metric_avg_demand')}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# بطاقات ذكية
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">{t('best_match_title')}</div>
        <div class="insight-line"><b>{best_match_name}</b></div>
        <div class="insight-line">{t('tickets_count')}: <b>{best_match_tickets}</b></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">{t('best_seat_title')}</div>
        <div class="insight-line"><b>{best_seat_name}</b></div>
        <div class="insight-line">{t('tickets_count')}: <b>{best_seat_tickets}</b></div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">{t('best_payment_title')}</div>
        <div class="insight-line"><b>{best_payment_name}</b></div>
        <div class="insight-line">{t('operations_count')}: <b>{best_payment_count}</b></div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# الرسوم البيانية
# =========================
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown(f'<div class="section-title">{t("chart_match_tickets")}</div>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.bar(top_match.index, top_match.values)
    ax1.set_xlabel(t("x_match"))
    ax1.set_ylabel(t("y_tickets"))
    ax1.set_title(t("plot_bookings_by_match"))
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

with chart2:
    st.markdown(f'<div class="section-title">{t("chart_match_revenue")}</div>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    ax2.bar(revenue_by_match.index, revenue_by_match.values)
    ax2.set_xlabel(t("x_match"))
    ax2.set_ylabel(t("y_revenue"))
    ax2.set_title(t("plot_revenue_by_match"))
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

chart3, chart4 = st.columns(2)

with chart3:
    st.markdown(f'<div class="section-title">{t("chart_seat_tickets")}</div>', unsafe_allow_html=True)
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    ax3.bar(top_seat.index, top_seat.values)
    ax3.set_xlabel(t("x_seat"))
    ax3.set_ylabel(t("y_tickets"))
    ax3.set_title(t("plot_top_seats"))
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

with chart4:
    st.markdown(f'<div class="section-title">{t("chart_payment_methods")}</div>', unsafe_allow_html=True)
    fig4, ax4 = plt.subplots(figsize=(8, 4.5))
    ax4.pie(payment_stats.values, labels=payment_stats.index, autopct="%1.1f%%")
    ax4.set_title(t("plot_payment_distribution"))
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("chart_avg_demand")}</div>', unsafe_allow_html=True)
    fig5, ax5 = plt.subplots(figsize=(10, 4.8))
    ax5.plot(demand_by_match.index, demand_by_match.values, marker="o")
    ax5.set_xlabel(t("x_match"))
    ax5.set_ylabel(t("y_avg_demand"))
    ax5.set_title(t("plot_avg_demand"))
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# =========================
# الجدول
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("summary_table")}</div>', unsafe_allow_html=True)

    summary_df = df[[
        "customer_name",
        "match_name",
        "seat_type",
        "seat_section",
        "ticket_count",
        "demand_level",
        "payment_method",
        "final_price"
    ]].copy()

    summary_df = summary_df.rename(columns={
        "customer_name": t("col_customer_name"),
        "match_name": t("col_match_name"),
        "seat_type": t("col_seat_type"),
        "seat_section": t("col_seat_section"),
        "ticket_count": t("col_ticket_count"),
        "demand_level": t("col_demand_level"),
        "payment_method": t("col_payment_method"),
        "final_price": t("col_final_price")
    })

    st.dataframe(summary_df, use_container_width=True)

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
        if st.button(t('home'), key="m_home_3", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button(t('matches'), key="m_matches_3", use_container_width=True):
            st.switch_page("pages/0_Match_Details.py")

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('booking'), key="m_booking_3", use_container_width=True):
            st.switch_page("pages/1_Booking.py")
    with col2:
        if st.button(t('history'), key="m_history_3", use_container_width=True):
            st.switch_page("pages/2_History.py")

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('admin'), key="m_admin_3", use_container_width=True):
            st.switch_page("pages/4_Admin.py")
    with col2:
        if st.button(t('support'), key="m_support_3", use_container_width=True):
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

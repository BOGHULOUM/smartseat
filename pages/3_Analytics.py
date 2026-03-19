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

/* سايدبار الكمبيوتر */
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
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}}

.logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -5px;
    margin-bottom: -16px;
}}

.logo-wrap img {{
    width: 240px;
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
    margin-top: 0px;
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
    display: inline-block;
    box-shadow: 0 0 14px rgba(212,175,55,0.20);
}}

.mobile-links a:hover {{
    transform: translateY(-2px);
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

.footer {{
    text-align: center;
    color: #D4AF37;
    font-size: 15px;
    font-weight: 600;
    margin-top: 24px;
    opacity: 0.95;
}}

/* الجوال فقط */
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
        display: block !important;
    }}

    .block-container {{
        padding-top: 0.7rem !important;
        padding-bottom: 1rem !important;
        padding-right: 0.7rem !important;
        padding-left: 0.7rem !important;
        max-width: 100% !important;
    }}

    .logo-wrap {{
        margin-top: 0 !important;
        margin-bottom: -6px !important;
    }}

    .logo-wrap img {{
        width: 170px !important;
        max-width: 88% !important;
    }}

    .hero-box {{
        padding: 18px 14px !important;
        border-radius: 22px !important;
        margin-bottom: 16px !important;
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
        margin-top: 16px !important;
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

    st.markdown("---")
    st.markdown("### التحليلات")
    st.markdown("تابع الأداء العام، الإيرادات، الطلب، وأنواع المقاعد.")

# =========================
# تنقل الجوال فقط
# =========================
st.markdown("""
<div class="mobile-nav-only">
    <div class="mobile-nav-box">
        <div class="mobile-nav-title">التنقل السريع</div>
        <div class="mobile-links">
            <a href="/">الرئيسية</a>
            <a href="/History">السجل</a>
            <a href="/Admin">الإدارة</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">التحليلات</div>
    <div class="hero-subtitle">Analytics Dashboard</div>
    <div class="hero-text">
        من هذه الصفحة يمكنك متابعة الأداء العام للنظام، وتحليل الحجوزات،
        والإيرادات، وأنواع المقاعد، ومستوى الطلب بشكل واضح واحترافي.
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
    st.markdown('<div class="warning-box">لا توجد بيانات كافية لعرض التحليلات حالياً. قم بإضافة حجوزات أولاً.</div>', unsafe_allow_html=True)
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
        <div class="metric-label">إجمالي الحجوزات</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_tickets}</div>
        <div class="metric-label">إجمالي التذاكر</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_revenue}</div>
        <div class="metric-label">إجمالي الإيرادات (د.ك)</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{avg_demand}/10</div>
        <div class="metric-label">متوسط الطلب</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# بطاقات ذكية
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">أفضل مباراة مبيعاً</div>
        <div class="insight-line"><b>{best_match_name}</b></div>
        <div class="insight-line">بعدد تذاكر: <b>{best_match_tickets}</b></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">أكثر نوع مقعد طلباً</div>
        <div class="insight-line"><b>{best_seat_name}</b></div>
        <div class="insight-line">بعدد تذاكر: <b>{best_seat_tickets}</b></div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">أكثر طريقة دفع استخداماً</div>
        <div class="insight-line"><b>{best_payment_name}</b></div>
        <div class="insight-line">بعدد عمليات: <b>{best_payment_count}</b></div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# الرسوم البيانية
# =========================
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown('<div class="section-title">عدد التذاكر حسب المباراة</div>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.bar(top_match.index, top_match.values)
    ax1.set_xlabel("المباراة")
    ax1.set_ylabel("عدد التذاكر")
    ax1.set_title("الحجوزات حسب المباراة")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig1)

with chart2:
    st.markdown('<div class="section-title">الإيرادات حسب المباراة</div>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    ax2.bar(revenue_by_match.index, revenue_by_match.values)
    ax2.set_xlabel("المباراة")
    ax2.set_ylabel("الإيرادات")
    ax2.set_title("الإيرادات حسب المباراة")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig2)

chart3, chart4 = st.columns(2)

with chart3:
    st.markdown('<div class="section-title">عدد التذاكر حسب نوع المقعد</div>', unsafe_allow_html=True)
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    ax3.bar(top_seat.index, top_seat.values)
    ax3.set_xlabel("نوع المقعد")
    ax3.set_ylabel("عدد التذاكر")
    ax3.set_title("المقاعد الأكثر طلباً")
    plt.tight_layout()
    st.pyplot(fig3)

with chart4:
    st.markdown('<div class="section-title">طرق الدفع الأكثر استخداماً</div>', unsafe_allow_html=True)
    fig4, ax4 = plt.subplots(figsize=(8, 4.5))
    ax4.pie(payment_stats.values, labels=payment_stats.index, autopct="%1.1f%%")
    ax4.set_title("توزيع طرق الدفع")
    plt.tight_layout()
    st.pyplot(fig4)

with st.container(border=True):
    st.markdown('<div class="section-title">متوسط الطلب حسب المباراة</div>', unsafe_allow_html=True)
    fig5, ax5 = plt.subplots(figsize=(10, 4.8))
    ax5.plot(demand_by_match.index, demand_by_match.values, marker="o")
    ax5.set_xlabel("المباراة")
    ax5.set_ylabel("متوسط الطلب")
    ax5.set_title("متوسط مستوى الطلب")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    st.pyplot(fig5)

# =========================
# الجدول
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">ملخص البيانات</div>', unsafe_allow_html=True)

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
        "customer_name": "اسم العميل",
        "match_name": "المباراة",
        "seat_type": "نوع المقعد",
        "seat_section": "القسم",
        "ticket_count": "عدد التذاكر",
        "demand_level": "مستوى الطلب",
        "payment_method": "طريقة الدفع",
        "final_price": "السعر النهائي"
    })

    st.dataframe(summary_df, use_container_width=True)

# =========================
# الفوتر
# =========================
st.markdown("""
<div class="footer">
    SmartSeat Analytics • Final Year Project
</div>
""", unsafe_allow_html=True)

conn.close()

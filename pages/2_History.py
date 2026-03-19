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
    animation: fadeUp 0.7s ease;
}}

.logo-wrap img {{
    width: 240px;
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
    margin-top: 0px;
    margin-bottom: 22px;
    animation: fadeUp 0.8s ease;
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
    animation: fadeUp 0.9s ease;
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
    animation: fadeUp 1s ease;
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

.footer {{
    text-align: center;
    color: #D4AF37;
    font-size: 15px;
    font-weight: 600;
    margin-top: 24px;
    opacity: 0.95;
}}

@keyframes fadeUp {{
    from {{
        opacity: 0;
        transform: translateY(14px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
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

    st.markdown("---")
    st.markdown("### سجل الحجوزات")
    st.markdown("راجع جميع الحجوزات، وابحث أو فلتر حسب البيانات المطلوبة.")
    st.markdown("### ملاحظة")
    st.markdown("الحذف متاح فقط من لوحة الإدارة.")

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">سجل الحجوزات</div>
    <div class="hero-subtitle">Booking History Dashboard</div>
    <div class="hero-text">
        يمكنك من هنا عرض جميع الحجوزات المسجلة، والبحث عن عميل محدد،
        واستخدام الفلاتر للوصول السريع إلى البيانات المطلوبة.
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
        <div class="metric-label">إجمالي الحجوزات</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    total_revenue = 0 if df.empty else round(df["final_price"].sum(), 2)
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_revenue}</div>
        <div class="metric-label">إجمالي الإيرادات (د.ك)</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    total_tickets = 0 if df.empty else int(df["ticket_count"].sum())
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{total_tickets}</div>
        <div class="metric-label">إجمالي التذاكر</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# البحث والفلترة
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">البحث والفلترة</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        search_text = st.text_input("بحث باسم العميل أو رقم الهاتف")
    with f2:
        selected_match = st.selectbox(
            "فلترة حسب المباراة",
            ["الكل"] + (sorted(df["match_name"].dropna().unique().tolist()) if not df.empty else [])
        )

    f3, f4 = st.columns(2)
    with f3:
        selected_seat = st.selectbox(
            "فلترة حسب نوع المقعد",
            ["الكل"] + (sorted(df["seat_type"].dropna().unique().tolist()) if not df.empty else [])
        )
    with f4:
        selected_payment = st.selectbox(
            "فلترة حسب طريقة الدفع",
            ["الكل"] + (sorted(df["payment_method"].dropna().unique().tolist()) if not df.empty else [])
        )

    st.markdown('<div class="gold-note">لحذف أي حجز، استخدم لوحة الإدارة فقط.</div>', unsafe_allow_html=True)

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

if selected_match != "الكل":
    filtered_df = filtered_df[filtered_df["match_name"] == selected_match]

if selected_seat != "الكل":
    filtered_df = filtered_df[filtered_df["seat_type"] == selected_seat]

if selected_payment != "الكل":
    filtered_df = filtered_df[filtered_df["payment_method"] == selected_payment]

# =========================
# الجدول
# =========================
st.write("")
with st.container(border=True):
    st.markdown('<div class="section-title">جدول الحجوزات</div>', unsafe_allow_html=True)

    if filtered_df.empty:
        st.markdown('<div class="warning-box">لا توجد حجوزات مطابقة للبحث أو الفلاتر الحالية.</div>', unsafe_allow_html=True)
    else:
        display_df = filtered_df.copy()
        display_df = display_df.rename(columns={
            "id": "رقم الحجز",
            "customer_name": "اسم العميل",
            "phone": "رقم الهاتف",
            "booking_date": "التاريخ",
            "match_name": "المباراة",
            "seat_type": "نوع المقعد",
            "seat_section": "القسم",
            "ticket_count": "عدد التذاكر",
            "demand_level": "مستوى الطلب",
            "payment_method": "طريقة الدفع",
            "discount_code": "كود الخصم",
            "base_price": "السعر الأساسي",
            "final_price": "السعر النهائي",
            "booking_time": "وقت الحجز"
        })
        st.dataframe(display_df, use_container_width=True)

# =========================
# الفوتر
# =========================
st.markdown("""
<div class="footer">
    SmartSeat History • Final Year Project
</div>
""", unsafe_allow_html=True)

conn.close()
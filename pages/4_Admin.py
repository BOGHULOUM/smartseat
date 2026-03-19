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

button[kind="header"] {{
    right: 0.75rem !important;
    left: auto !important;
}}

[data-testid="stSidebarCollapsedControl"] {{
    right: 0.75rem !important;
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
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.28);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 0 18px rgba(212,175,55,0.10);
    animation: fadeUp 0.9s ease;
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
    animation: fadeUp 1s ease;
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
    st.markdown("### Admin Panel")
    st.markdown("لوحة التحكم الخاصة بالإدارة.")

# =========================
# تسجيل الدخول
# =========================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">لوحة الإدارة</div>
        <div class="hero-subtitle">Admin Control Panel</div>
        <div class="hero-text">
            أدخل كلمة المرور للوصول إلى أدوات الإدارة والتحكم بالحجوزات والأسعار.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">تسجيل دخول الإدارة</div>', unsafe_allow_html=True)
        password_input = st.text_input("كلمة المرور", type="password")

        if st.button("🔐 دخول"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.markdown('<div class="warning-box">كلمة المرور غير صحيحة.</div>', unsafe_allow_html=True)

    st.stop()

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">لوحة الإدارة</div>
    <div class="hero-subtitle">SmartSeat Admin Dashboard</div>
    <div class="hero-text">
        من هنا يمكنك مراجعة الحجوزات، حذف أي سجل، وتعديل الأسعار الأساسية للمباريات والمقاعد.
    </div>
</div>
""", unsafe_allow_html=True)

top1, top2 = st.columns([4, 1])
with top2:
    if st.button("🚪 تسجيل خروج"):
        st.session_state.admin_logged_in = False
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
# حذف حجز
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">حذف حجز</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        delete_id = st.text_input("رقم الحجز المراد حذفه")
    with d2:
        delete_clicked = st.button("🗑️ حذف الحجز")

    if delete_clicked:
        if delete_id.strip() == "":
            st.markdown('<div class="warning-box">يرجى إدخال رقم الحجز.</div>', unsafe_allow_html=True)
        else:
            try:
                delete_id_int = int(delete_id)
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE id = ?", (delete_id_int,))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    st.markdown('<div class="warning-box">رقم الحجز غير موجود.</div>', unsafe_allow_html=True)
                else:
                    cursor.execute("DELETE FROM bookings WHERE id = ?", (delete_id_int,))
                    conn.commit()
                    st.markdown('<div class="success-box">تم حذف الحجز بنجاح.</div>', unsafe_allow_html=True)
                    st.rerun()
            except ValueError:
                st.markdown('<div class="warning-box">رقم الحجز يجب أن يكون رقمًا صحيحًا.</div>', unsafe_allow_html=True)

# =========================
# تعديل الأسعار
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">تعديل الأسعار</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-note">أي تعديل هنا ينعكس مباشرة على صفحة الحجز.</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        elclasico_price = st.number_input("برشلونة × ريال مدريد", value=float(pricing["elclasico_price"]), step=1.0)
        kuwait_qadsia_price = st.number_input("الكويت × القادسية", value=float(pricing["kuwait_qadsia_price"]), step=1.0)
        arabi_salmiya_price = st.number_input("العربي × السالمية", value=float(pricing["arabi_salmiya_price"]), step=1.0)
        city_liverpool_price = st.number_input("مانشستر سيتي × ليفربول", value=float(pricing["city_liverpool_price"]), step=1.0)

    with a2:
        regular_extra = st.number_input("Regular زيادة", value=float(pricing["regular_extra"]), step=1.0)
        premium_extra = st.number_input("Premium زيادة", value=float(pricing["premium_extra"]), step=1.0)
        vip_extra = st.number_input("VIP زيادة", value=float(pricing["vip_extra"]), step=1.0)
        section_a_extra = st.number_input("Section A زيادة", value=float(pricing["section_a_extra"]), step=1.0)
        section_b_extra = st.number_input("Section B زيادة", value=float(pricing["section_b_extra"]), step=1.0)
        section_c_extra = st.number_input("Section C زيادة", value=float(pricing["section_c_extra"]), step=1.0)

    if st.button("💾 حفظ الأسعار"):
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
        st.markdown('<div class="success-box">تم حفظ الأسعار بنجاح.</div>', unsafe_allow_html=True)

# =========================
# جدول الحجوزات
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">جميع الحجوزات</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown('<div class="warning-box">لا توجد حجوزات حالياً.</div>', unsafe_allow_html=True)
    else:
        display_df = df.copy()
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
    SmartSeat Admin Panel • Final Year Project
</div>
""", unsafe_allow_html=True)

conn.close()
import streamlit as st
from pathlib import Path
import base64

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent
logo_path = base_dir / "assets" / "logo.png"

st.set_page_config(
    page_title="SmartSeat",
    page_icon=str(logo_path),
    layout="wide"
)

# =========================
# تحويل الصورة
# =========================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64(logo_path)

# =========================
# CSS كامل + دعم الجوال 🔥
# =========================
st.markdown(f"""
<style>

/* عام */
html, body, [class*="css"] {{
    direction: rtl;
    font-family: 'Segoe UI', sans-serif;
}}

/* خلفية */
.stApp {{
    background: linear-gradient(135deg, #050505, #111111);
    color: white;
}}

/* اللوقو */
.logo-wrap {{
    display: flex;
    justify-content: center;
    margin-bottom: -20px;
}}

.logo-wrap img {{
    width: 400px;
    max-width: 100%;
    filter: drop-shadow(0px 0px 20px rgba(212,175,55,0.6));
}}

/* البوكس الرئيسي */
.hero-box {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 25px;
    padding: 30px;
    text-align: center;
    margin-bottom: 20px;
}}

/* النصوص */
.hero-title {{
    font-size: 50px;
    color: #D4AF37;
    font-weight: bold;
}}

.hero-subtitle {{
    font-size: 20px;
    color: #E6C86E;
}}

.hero-text {{
    font-size: 16px;
    color: #E6C86E;
}}

/* الكروت */
.card {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 20px;
    padding: 20px;
}}

.card h3 {{
    color: #D4AF37;
    text-align: center;
}}

.card p, .card li {{
    color: #E6C86E;
}}

/* الأزرار */
.stButton > button {{
    width: 100%;
    border-radius: 15px;
    font-size: 18px;
    background: linear-gradient(#FFD700, #D4AF37);
    color: black;
    font-weight: bold;
}}

/* =========================
   📱 دعم الجوال
========================= */
@media (max-width: 768px) {{

    .block-container {{
        padding: 1rem !important;
    }}

    .logo-wrap img {{
        width: 220px !important;
    }}

    .hero-title {{
        font-size: 30px !important;
    }}

    .hero-subtitle {{
        font-size: 16px !important;
    }}

    .hero-text {{
        font-size: 14px !important;
    }}

    .card {{
        padding: 15px !important;
    }}

    .card h3 {{
        font-size: 18px !important;
    }}

    .card p, .card li {{
        font-size: 14px !important;
    }}

    /* إخفاء السايدبار */
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}
}}

</style>

<div class="logo-wrap">
    <img src="data:image/png;base64,{logo_base64}">
</div>
""", unsafe_allow_html=True)

# =========================
# الصفحة الرئيسية
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">SmartSeat</div>
    <div class="hero-subtitle">Smart Stadium Ticket Pricing System</div>
    <div class="hero-text">
        نظام ذكي لتسعير التذاكر يعتمد على نوع المباراة والمقعد والطلب.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>نبذة عن المشروع</h3>
        <p>نظام حديث لتسعير التذاكر بشكل ذكي بدل التسعير الثابت.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>مميزات النظام</h3>
        <ul>
            <li>تسعير ذكي</li>
            <li>واجهة فخمة</li>
            <li>تحليل بيانات</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# الأزرار
# =========================
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    if st.button("Match"):
        st.switch_page("pages/0_Match_Details.py")

with c2:
    if st.button("Booking"):
        st.switch_page("pages/1_Booking.py")

with c3:
    if st.button("History"):
        st.switch_page("pages/2_History.py")

with c4:
    if st.button("Analytics"):
        st.switch_page("pages/3_Analytics.py")

with c5:
    if st.button("Admin"):
        st.switch_page("pages/4_Admin.py")

with c6:
    if st.button("Support"):
        st.switch_page("pages/5_Support.py")

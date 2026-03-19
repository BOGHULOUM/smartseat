import streamlit as st
from pathlib import Path
import base64

base_dir = Path(__file__).parent
logo_path = base_dir / "assets" / "logo.png"

st.set_page_config(
    page_title="SmartSeat",
    page_icon=str(logo_path),
    layout="wide"
)

def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64(logo_path)

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
    max-width: 1200px;
}}

.logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -5px;
    margin-bottom: -30px;
    animation: fadeUp 0.7s ease;
}}

.logo-wrap img {{
    width: 420px;
    max-width: 100%;
    filter: drop-shadow(0px 0px 24px rgba(212,175,55,0.68));
}}

.hero-box {{
    background: linear-gradient(135deg, rgba(18,18,18,0.95), rgba(30,30,30,0.92));
    border: 1px solid rgba(212,175,55,0.34);
    border-radius: 30px;
    padding: 30px 34px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.42);
    margin-top: 0px;
    margin-bottom: 22px;
    animation: fadeUp 0.8s ease;
}}

.hero-title {{
    font-size: 54px;
    font-weight: 900;
    color: #D4AF37;
    margin-bottom: 4px;
}}

.hero-subtitle {{
    font-size: 21px;
    color: #E6C86E;
    font-weight: 700;
    margin-bottom: 8px;
}}

.sponsor {{
    font-size: 18px;
    color: #D4AF37;
    font-weight: 700;
    margin-bottom: 14px;
}}

.hero-text {{
    color: #E6C86E;
    font-size: 17px;
    line-height: 1.95;
    max-width: 900px;
    margin: auto;
}}

.card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 24px;
    padding: 24px 24px 20px 24px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    min-height: 240px;
    animation: fadeUp 0.9s ease;
}}

.card h3 {{
    color: #D4AF37 !important;
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 26px;
    text-align: center;
}}

.card p, .card li {{
    color: #E6C86E !important;
    line-height: 1.9;
    font-size: 17px;
}}

.card ul {{
    padding-right: 22px;
    margin: 0;
}}

.members-box {{
    background: linear-gradient(135deg, rgba(18,18,18,0.95), rgba(28,28,28,0.95));
    border: 1px solid rgba(212,175,55,0.32);
    border-radius: 28px;
    padding: 26px 20px;
    box-shadow: 0 10px 22px rgba(0,0,0,0.34);
    margin-top: 22px;
    animation: fadeUp 1s ease;
}}

.members-title {{
    color: #D4AF37;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 18px;
    text-align: center;
}}

.member-line {{
    color: #D4AF37;
    font-size: 22px;
    text-align: center;
    margin: 14px 0;
    font-weight: 800;
    font-family: Garamond, Georgia, "Times New Roman", serif;
    text-shadow: 0 0 8px rgba(212,175,55,0.25);
}}

.supervisor-line {{
    color: #D4AF37;
    font-size: 21px;
    text-align: center;
    margin-top: 18px;
    font-weight: 800;
    font-family: Garamond, Georgia, "Times New Roman", serif;
    text-shadow: 0 0 8px rgba(212,175,55,0.25);
}}

.section-title {{
    color: #D4AF37;
    text-align: center;
    font-size: 26px;
    font-weight: 800;
    margin-top: 26px;
    margin-bottom: 12px;
}}

.stButton > button {{
    width: 100%;
    min-height: 78px;
    border: none;
    border-radius: 20px;
    padding: 14px 18px;
    font-size: 20px;
    font-weight: 800;
    color: black;
    background: linear-gradient(180deg, #FFD700 0%, #D4AF37 100%);
    box-shadow: 0 0 18px rgba(212,175,55,0.22);
    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 0 28px rgba(212,175,55,0.42);
}}

.footer {{
    text-align: center;
    color: #D4AF37;
    font-size: 16px;
    font-weight: 600;
    margin-top: 30px;
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

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="sidebar-logo-wrap">
            <img src="data:image/png;base64,%s" class="sidebar-logo">
        </div>
        <div class="sidebar-brand-title">SmartSeat</div>
        <div class="sidebar-brand-subtitle">Smart Stadium Ticket Pricing System</div>
    </div>
    """ % logo_base64, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### التنقل")
    st.markdown("استخدم القائمة للانتقال بين صفحات المشروع.")

st.markdown("""
<div class="hero-box">
    <div class="hero-title">SmartSeat</div>
    <div class="hero-subtitle">Smart Stadium Ticket Pricing System</div>
    <div class="sponsor">Sponsored by Ktech</div>
    <div class="hero-text">
        SmartSeat هو نظام ذكي لتسعير تذاكر الملاعب باستخدام التسعير الديناميكي،
        حيث يتم احتساب السعر النهائي بناءً على نوع المباراة، نوع المقعد، ومستوى الطلب،
        بهدف تحسين تجربة المستخدم وتطوير نظام حجز أكثر كفاءة وحداثة.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <h3>نبذة عن المشروع</h3>
        <p>
            يهدف هذا المشروع إلى تطوير نظام حديث وذكي لتسعير تذاكر الملاعب بدلاً من التسعير التقليدي الثابت،
            بحيث يتم تعديل السعر بشكل مرن حسب أهمية المباراة، نوع المقعد، ومستوى الإقبال.
            يساعد هذا النظام على تحسين إدارة بيع التذاكر ورفع كفاءة الحجز بشكل احترافي.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>مميزات النظام</h3>
        <ul>
            <li>تسعير ذكي للتذاكر حسب الطلب</li>
            <li>واجهة حديثة وفخمة وسهلة الاستخدام</li>
            <li>حفظ بيانات الحجوزات داخل قاعدة بيانات</li>
            <li>عرض سجل كامل لجميع الحجوزات</li>
            <li>تحليل البيانات برسوم ومؤشرات واضحة</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="members-box">
    <div class="members-title">أعضاء المشروع والمشرفة</div>
    <div class="member-line">Abdulaziz Ghuloum / 230100166</div>
    <div class="member-line">Anas Alkandari – 240100716</div>
    <div class="supervisor-line">المشرفة / Ms. Annet Noel</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">استكشف النظام</div>', unsafe_allow_html=True)

b1, b2, b3, b4 = st.columns(4, gap="large")

with b1:
    if st.button("🎟️الانتقال إلى الحجز"):
        st.switch_page("pages/1_Booking.py")

with b2:
    if st.button("📜عرض سجل الحجوزات"):
        st.switch_page("pages/2_History.py")

with b3:
    if st.button("📊عرض التحليلات"):
        st.switch_page("pages/3_Analytics.py")

with b4:
    if st.button("🛠️لوحة الإدارة"):
        st.switch_page("pages/4_Admin.py")

st.markdown("""
<div class="footer">
    Final Year Project • SmartSeat
</div>
""", unsafe_allow_html=True)

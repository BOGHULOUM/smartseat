import streamlit as st
from pathlib import Path
import base64

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent.parent
assets_dir = base_dir / "assets"
logo_path = assets_dir / "logo.png"

st.set_page_config(
    page_title="SmartSeat - Support",
    page_icon=str(logo_path),
    layout="wide"
)

# =========================
# تحويل اللوقو
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
    max-width: 1150px;
}}

.logo-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -5px;
    margin-bottom: -16px;
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

.contact-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    transition: all 0.25s ease;
    height: 100%;
}}

.contact-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 0 24px rgba(212,175,55,0.26);
}}

.contact-title {{
    color: #D4AF37;
    font-size: 24px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 16px;
}}

.contact-line {{
    color: #F0D98A;
    font-size: 18px;
    line-height: 2;
    text-align: center;
    word-break: break-word;
}}

.contact-label {{
    color: #D4AF37;
    font-weight: 800;
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

label {{
    color: #E6C86E !important;
    font-weight: 700 !important;
}}

.stTextInput > div > div,
.stTextArea textarea {{
    background-color: rgba(15,15,15,0.95) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
    color: white !important;
}}

.stTextInput > div > div:hover,
.stTextArea textarea:hover {{
    box-shadow: 0 0 14px rgba(212,175,55,0.25) !important;
    border: 1px solid rgba(212,175,55,0.45) !important;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    overflow: hidden !important;
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
    box-shadow: 0 0 18px rgba(212,175,55,0.22);
    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 0 24px rgba(212,175,55,0.36);
}}

.success-box {{
    background: linear-gradient(135deg, rgba(20,55,20,0.95), rgba(35,85,35,0.92));
    border: 1px solid rgba(80,200,120,0.35);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    color: #d7ffd7;
    font-size: 18px;
    font-weight: 700;
    margin-top: 18px;
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
        width: 160px !important;
        max-width: 86% !important;
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

    .contact-title {{
        font-size: 18px !important;
    }}

    .contact-line {{
        font-size: 14px !important;
        line-height: 1.9 !important;
    }}

    .success-box {{
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
    st.markdown("### Customer Support")
    st.markdown("لأي مشكلة أو استفسار أو شكوى، تواصل معنا مباشرة.")

# =========================
# تنقل الجوال فقط
# =========================
st.markdown("""
<div class="mobile-nav-only">
    <div class="mobile-nav-box">
        <div class="mobile-nav-title">التنقل السريع</div>
        <div class="mobile-links">
            <a href="/">الرئيسية</a>
            <a href="/Booking">الحجز</a>
            <a href="/History">السجل</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">دعم العملاء</div>
    <div class="hero-subtitle">Customer Support</div>
    <div class="hero-text">
        إذا واجهتك أي مشكلة في الحجز أو الدفع أو احتجت إلى مساعدة إضافية،
        يمكنك التواصل معنا من خلال أرقام الدعم أو البريد الإلكتروني، أو إرسال رسالتك مباشرة من النموذج أدناه.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# معلومات التواصل
# =========================
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-title">📞 أرقام الدعم والتواصل</div>
        <div class="contact-line"><span class="contact-label">هاتف / واتساب 1:</span><br>+965 99474516</div>
        <div class="contact-line"><span class="contact-label">هاتف / واتساب 2:</span><br>+965 50284185</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-title">📧 البريد الإلكتروني</div>
        <div class="contact-line">230100166@Ktech.edu.kw</div>
        <div class="contact-line">240100716@Ktech.edu.kw</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# نموذج الدعم
# =========================
with st.container(border=True):
    st.markdown('<div class="section-title">إرسال شكوى أو استفسار</div>', unsafe_allow_html=True)

    name = st.text_input("الاسم")
    phone = st.text_input("رقم الهاتف")
    message = st.text_area("اكتب رسالتك", height=180)

    send_clicked = st.button("📨 إرسال الطلب")

    if send_clicked:
        if name.strip() and phone.strip() and message.strip():
            st.markdown("""
            <div class="success-box">
                ✅ تم إرسال طلبك بنجاح، وسيتم التواصل معك في أقرب وقت ممكن.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("يرجى تعبئة جميع الحقول قبل الإرسال.")

# =========================
# الفوتر
# =========================
st.markdown("""
<div class="footer">
    SmartSeat Support • Final Year Project
</div>
""", unsafe_allow_html=True)

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

        "sidebar_title": "دعم العملاء",
        "sidebar_desc": "لأي مشكلة أو استفسار أو شكوى، تواصل معنا مباشرة.",

        "page_title": "دعم العملاء",
        "page_subtitle": "Customer Support",
        "page_desc": "إذا واجهتك أي مشكلة في الحجز أو الدفع أو احتجت إلى مساعدة إضافية، يمكنك التواصل معنا من خلال أرقام الدعم أو البريد الإلكتروني، أو إرسال رسالتك مباشرة من النموذج أدناه.",

        "phones_title": "📞 أرقام الدعم والتواصل",
        "phone1": "هاتف / واتساب 1",
        "phone2": "هاتف / واتساب 2",

        "email_title": "📧 البريد الإلكتروني",

        "form_title": "إرسال شكوى أو استفسار",
        "name": "الاسم",
        "phone": "رقم الهاتف",
        "message": "اكتب رسالتك",
        "send_btn": "📨 إرسال الطلب",
        "success_msg": "✅ تم إرسال طلبك بنجاح، وسيتم التواصل معك في أقرب وقت ممكن.",
        "fill_all": "يرجى تعبئة جميع الحقول قبل الإرسال.",

        "home": "الرئيسية",
        "matches": "المباريات",
        "booking": "الحجز",
        "history": "السجل",
        "analytics": "التحليلات",
        "admin": "الإدارة",
        "quick_access": "الوصول السريع",

        "footer": "SmartSeat Support • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",

        "sidebar_title": "Customer Support",
        "sidebar_desc": "For any issue, inquiry, or complaint, contact us directly.",

        "page_title": "Customer Support",
        "page_subtitle": "Customer Support",
        "page_desc": "If you face any issue with booking or payment, or need additional help, you can contact us through the support numbers or email, or send your message directly using the form below.",

        "phones_title": "📞 Support Contact Numbers",
        "phone1": "Phone / WhatsApp 1",
        "phone2": "Phone / WhatsApp 2",

        "email_title": "📧 Email Address",

        "form_title": "Send a Complaint or Inquiry",
        "name": "Name",
        "phone": "Phone Number",
        "message": "Write your message",
        "send_btn": "📨 Send Request",
        "success_msg": "✅ Your request has been sent successfully, and we will contact you as soon as possible.",
        "fill_all": "Please fill in all fields before sending.",

        "home": "Home",
        "matches": "Matches",
        "booking": "Booking",
        "history": "History",
        "analytics": "Analytics",
        "admin": "Admin",
        "quick_access": "Quick Access",

        "footer": "SmartSeat Support • Final Year Project"
    }
}

def t(k):
    return TXT[st.session_state.lang][k]

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
    max-width: 1150px;
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

.ltr-text {{
    direction: ltr;
    unicode-bidi: embed;
    display: inline-block;
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
        width: 160px !important;
        max-width: 86% !important;
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
        key="support_lang_sidebar"
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
        key="support_lang_top"
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
# معلومات التواصل
# =========================
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown(f"""
    <div class="contact-card">
        <div class="contact-title">{t('phones_title')}</div>
        <div class="contact-line"><span class="contact-label">{t('phone1')}:</span><br><span class="ltr-text">+965 99474516</span></div>
        <div class="contact-line"><span class="contact-label">{t('phone2')}:</span><br><span class="ltr-text">+965 50284185</span></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="contact-card">
        <div class="contact-title">{t('email_title')}</div>
        <div class="contact-line"><span class="ltr-text">230100166@Ktech.edu.kw</span></div>
        <div class="contact-line"><span class="ltr-text">240100716@Ktech.edu.kw</span></div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# نموذج الدعم
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("form_title")}</div>', unsafe_allow_html=True)

    name = st.text_input(t("name"))
    phone = st.text_input(t("phone"))
    message = st.text_area(t("message"), height=180)

    send_clicked = st.button(t("send_btn"))

    if send_clicked:
        if name.strip() and phone.strip() and message.strip():
            st.markdown(f"""
            <div class="success-box">
                {t("success_msg")}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(t("fill_all"))

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
        if st.button(t('home'), key="m_home_5", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button(t('matches'), key="m_matches_5", use_container_width=True):
            st.switch_page("pages/0_Match_Details.py")

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('booking'), key="m_booking_5", use_container_width=True):
            st.switch_page("pages/1_Booking.py")
    with col2:
        if st.button(t('history'), key="m_history_5", use_container_width=True):
            st.switch_page("pages/2_History.py")

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('analytics'), key="m_analytics_5", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")
    with col2:
        if st.button(t('admin'), key="m_admin_5", use_container_width=True):
            st.switch_page("pages/4_Admin.py")

# =========================
# الفوتر
# =========================
st.markdown(f"""
<div class="footer">
    {t("footer")}
</div>
""", unsafe_allow_html=True)

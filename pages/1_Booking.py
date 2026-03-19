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
    page_title="SmartSeat - Match Details",
    page_icon=str(logo_path),
    layout="wide"
)

# =========================
# تحويل اللوقو إلى base64
# =========================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64(logo_path)

# =========================
# بيانات المباريات
# =========================
matches = [
    {
        "image": assets_dir / "match1.png",
        "name": "الكويت × القادسية",
        "type": "دوري",
        "competition": "الدوري الكويتي الممتاز",
        "stadium": "ملعب جابر الأحمد الدولي",
        "city": "الكويت",
        "referee": "عبدالرحمن الجاسم",
        "datetime": "22-05-2026 • 19:45",
        "gates_open": "17:45",
        "parking": "مواقف الجماهير متوفرة بالقرب من الملعب",
        "demand": "الطلب مرتفع",
        "note": "ديربي كويتي جماهيري متوقع له حضور قوي وأجواء حماسية كبيرة."
    },
    {
        "image": assets_dir / "match2.png",
        "name": "العربي × السالمية",
        "type": "كأس",
        "competition": "كأس الأمير",
        "stadium": "ملعب صباح السالم",
        "city": "الكويت",
        "referee": "أحمد العلي",
        "datetime": "25-05-2026 • 18:30",
        "gates_open": "16:30",
        "parking": "تتوفر مواقف خارجية حول الاستاد",
        "demand": "الطلب متوسط إلى مرتفع",
        "note": "مواجهة مهمة في بطولة الكأس وفرص التأهل فيها كبيرة للطرفين."
    },
    {
        "image": assets_dir / "match3.png",
        "name": "برشلونة × ريال مدريد",
        "type": "نهائي كأس",
        "competition": "كأس السوبر الإسباني",
        "stadium": "ملعب الملك فهد الدولي",
        "city": "الرياض",
        "referee": "Michael Oliver",
        "datetime": "18-05-2026 • 20:30",
        "gates_open": "18:30",
        "parking": "مواقف VIP ومواقف عامة متوفرة",
        "demand": "الطلب مرتفع جداً",
        "note": "مواجهة كلاسيكية نارية بين عملاقين من أكبر أندية العالم."
    },
    {
        "image": assets_dir / "match4.png",
        "name": "مانشستر سيتي × ليفربول",
        "type": "ودية",
        "competition": "International Friendly",
        "stadium": "ويمبلي",
        "city": "لندن",
        "referee": "Anthony Taylor",
        "datetime": "30-05-2026 • 21:00",
        "gates_open": "19:00",
        "parking": "المواقف محدودة ويُنصح بالحضور المبكر",
        "demand": "الطلب مرتفع جداً",
        "note": "قمة إنجليزية ممتعة بين فريقين كبيرين في مواجهة استعراضية قوية."
    }
]

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
    max-width: 1280px;
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
    width: 220px;
    max-width: 100%;
    filter: drop-shadow(0px 0px 20px rgba(212,175,55,0.68));
}}

.hero-box {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 30px;
    padding: 24px 30px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.36);
    margin-top: 0;
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
    max-width: 900px;
    margin: auto;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.28);
    animation: fadeUp 0.9s ease;
    overflow: hidden !important;
}}

.match-title {{
    color: #D4AF37;
    font-size: 25px;
    font-weight: 900;
    text-align: center;
    margin: 10px 0 18px 0;
}}

.info-line {{
    color: #F0D98A;
    font-size: 16px;
    line-height: 1.9;
    margin: 6px 0;
    word-break: break-word;
}}

.info-label {{
    color: #D4AF37;
    font-weight: 800;
}}

.note-box {{
    background: linear-gradient(135deg, rgba(45,35,10,0.95), rgba(70,55,15,0.92));
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 18px;
    padding: 14px;
    text-align: center;
    color: #F0D98A;
    font-size: 15px;
    font-weight: 700;
    margin-top: 14px;
    line-height: 1.8;
}}

.status-row {{
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 16px;
    margin-bottom: 8px;
}}

.status-pill {{
    background: rgba(255,215,0,0.10);
    border: 1px solid rgba(212,175,55,0.30);
    color: #E6C86E;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
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
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 0 28px rgba(212,175,55,0.42);
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

/* =========================
   دعم الجوال
========================= */
@media (max-width: 768px) {{

    .block-container {{
        padding-top: 0.7rem !important;
        padding-bottom: 1rem !important;
        padding-right: 0.7rem !important;
        padding-left: 0.7rem !important;
        max-width: 100% !important;
    }}

    .logo-wrap {{
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

    .match-title {{
        font-size: 18px !important;
        line-height: 1.5 !important;
        margin: 8px 0 12px 0 !important;
        word-break: break-word !important;
    }}

    .info-line {{
        font-size: 13px !important;
        line-height: 1.8 !important;
        text-align: right !important;
    }}

    .note-box {{
        font-size: 13px !important;
        line-height: 1.8 !important;
        padding: 12px !important;
    }}

    .status-pill {{
        font-size: 12px !important;
        padding: 7px 10px !important;
    }}

    .stButton > button {{
        min-height: 52px !important;
        font-size: 15px !important;
        border-radius: 15px !important;
        padding: 8px 10px !important;
        white-space: normal !important;
        line-height: 1.35 !important;
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
    st.markdown("### Match Details")
    st.markdown("راجع تفاصيل المباريات قبل الانتقال إلى الحجز.")

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">تفاصيل المباريات</div>
    <div class="hero-subtitle">Match Details</div>
    <div class="hero-text">
        قبل الحجز، يمكنك هنا الاطلاع على تفاصيل كل مباراة من حيث نوعها، البطولة،
        الملعب، الحكم، وتوقيت المباراة، حتى تكون لديك صورة واضحة قبل إتمام الحجز.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# عرض المباريات
# =========================
col1, col2 = st.columns(2, gap="large")

for i, match in enumerate(matches):
    target_col = col1 if i % 2 == 0 else col2

    with target_col:
        with st.container(border=True):
            if match["image"].exists():
                st.image(str(match["image"]), use_container_width=True)
            else:
                st.warning(f"الصورة غير موجودة: {match['image'].name}")

            st.markdown(
                f'<div class="match-title">{match["name"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">نوع المباراة:</span> {match["type"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">البطولة:</span> {match["competition"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">الملعب:</span> {match["stadium"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">المدينة:</span> {match["city"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">الحكم:</span> {match["referee"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="info-line"><span class="info-label">التاريخ والوقت:</span> {match["datetime"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div class="status-row">
                <div class="status-pill">فتح البوابات: {match["gates_open"]}</div>
                <div class="status-pill">{match["demand"]}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="note-box">
                {match["note"]}<br><br>{match["parking"]}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🎟️ احجز الآن - {match['name']}", key=f"book_{i}"):
                st.session_state["selected_match"] = match["name"]
                st.switch_page("pages/1_Booking.py")

# =========================
# الفوتر
# =========================
st.markdown("""
<div class="footer">
    SmartSeat Match Details • Final Year Project
</div>
""", unsafe_allow_html=True)

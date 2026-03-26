import streamlit as st
from pathlib import Path
import sqlite3
import base64
from datetime import date, datetime
from io import BytesIO
import qrcode
import time

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# =========================
# إعداد الصفحة
# =========================
base_dir = Path(__file__).parent.parent
logo_path = base_dir / "assets" / "logo.png"
db_path = base_dir / "tickets.db"

st.set_page_config(
    page_title="SmartSeat - Booking",
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

        "page_title": "حجز التذاكر",
        "page_subtitle": "Smart Booking Experience",
        "page_desc": "أدخل بيانات الحجز وسيتم حساب السعر النهائي بشكل مباشر حسب المباراة، نوع المقعد، عدد التذاكر، مستوى الطلب، وكود الخصم إن وجد.",

        "need_login": "يجب تسجيل الدخول أولاً للوصول إلى هذه الصفحة.",
        "back_home": "العودة للرئيسية",

        "booking_section": "بيانات الحجز",
        "summary_section": "ملخص الحجز",

        "customer_name": "اسم العميل",
        "phone": "رقم الهاتف",
        "booking_date": "اختيار التاريخ",
        "ticket_count": "عدد التذاكر",
        "match_name": "اختيار المباراة",
        "seat_type": "نوع المقعد",
        "seat_section": "اختيار المقعد",
        "demand_level": "مستوى الطلب",
        "payment_method": "طريقة الدفع",
        "discount_code": "كود الخصم",
        "discount_placeholder": "مثال: KTECH10",

        "final_price": "السعر النهائي",
        "before_discount": "الإجمالي قبل الخصم",
        "discount_value": "قيمة الخصم",

        "confirm_booking": "✅ تأكيد الحجز الآن",
        "processing": "جاري تأكيد الحجز وتجهيز التذكرة...",

        "name_error": "يرجى إدخال اسم العميل.",
        "phone_error": "يرجى إدخال رقم الهاتف.",

        "success": "🎉 تم تأكيد الحجز بنجاح!",
        "customer": "العميل",
        "match": "المباراة",
        "seat": "المقعد",
        "payment": "الدفع",
        "booking_number": "رقم الحجز",

        "download_pdf": "📄 تحميل التذكرة PDF",
        "qr_title": "🎟️ رمز التذكرة (QR Code)",
        "qr_caption": "اعرض هذا الرمز عند الدخول",
        "download_qr": "📥 تحميل QR كصورة",

        "no_discount": "لا يوجد",

        "regular": "عادي",
        "premium": "مميز",
        "vip": "VIP",

        "home": "الرئيسية",
        "matches": "المباريات",
        "history": "السجل",
        "analytics": "التحليلات",
        "admin": "الإدارة",
        "support": "الدعم",
        "quick_access": "الوصول السريع",

        "footer": "SmartSeat Booking • Final Year Project"
    },
    "en": {
        "lang_label": "Language",
        "arabic": "العربية",
        "english": "English",

        "page_title": "Ticket Booking",
        "page_subtitle": "Smart Booking Experience",
        "page_desc": "Enter your booking details and the final ticket price will be calculated instantly based on the match, seat type, number of tickets, demand level, and discount code if available.",

        "need_login": "You must login first to access this page.",
        "back_home": "Back to Home",

        "booking_section": "Booking Details",
        "summary_section": "Booking Summary",

        "customer_name": "Customer Name",
        "phone": "Phone Number",
        "booking_date": "Select Date",
        "ticket_count": "Ticket Count",
        "match_name": "Choose Match",
        "seat_type": "Seat Type",
        "seat_section": "Choose Section",
        "demand_level": "Demand Level",
        "payment_method": "Payment Method",
        "discount_code": "Discount Code",
        "discount_placeholder": "Example: KTECH10",

        "final_price": "Final Price",
        "before_discount": "Total Before Discount",
        "discount_value": "Discount Value",

        "confirm_booking": "✅ Confirm Booking Now",
        "processing": "Confirming booking and preparing ticket...",

        "name_error": "Please enter the customer name.",
        "phone_error": "Please enter the phone number.",

        "success": "🎉 Booking confirmed successfully!",
        "customer": "Customer",
        "match": "Match",
        "seat": "Seat",
        "payment": "Payment",
        "booking_number": "Booking Number",

        "download_pdf": "📄 Download Ticket PDF",
        "qr_title": "🎟️ Ticket QR Code",
        "qr_caption": "Show this code at entry",
        "download_qr": "📥 Download QR Image",

        "no_discount": "None",

        "regular": "Regular",
        "premium": "Premium",
        "vip": "VIP",

        "home": "Home",
        "matches": "Matches",
        "history": "History",
        "analytics": "Analytics",
        "admin": "Admin",
        "support": "Support",
        "quick_access": "Quick Access",

        "footer": "SmartSeat Booking • Final Year Project"
    }
}

def t(key):
    return TXT[st.session_state.lang][key]

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
# قراءة إعدادات الأسعار
# =========================
pricing_row = cursor.execute("SELECT * FROM pricing_settings WHERE id = 1").fetchone()

pricing = {
    "برشلونة × ريال مدريد": float(pricing_row[1]),
    "الكويت × القادسية": float(pricing_row[2]),
    "العربي × السالمية": float(pricing_row[3]),
    "مانشستر سيتي × ليفربول": float(pricing_row[4]),
}

seat_prices = {
    "Regular": float(pricing_row[5]),
    "Premium": float(pricing_row[6]),
    "VIP": float(pricing_row[7]),
}

section_prices = {
    "A": float(pricing_row[8]),
    "B": float(pricing_row[9]),
    "C": float(pricing_row[10]),
}

# =========================
# تحويل اللوقو إلى base64
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
    font-size: 30px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 10px;
}}

.summary-line {{
    color: #F0D98A;
    font-size: 18px;
    margin: 12px 0;
    line-height: 1.9;
    word-break: break-word;
}}

.price-box {{
    background: linear-gradient(180deg, rgba(255,215,0,0.14), rgba(212,175,55,0.08));
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    margin-top: 18px;
    box-shadow: 0 0 18px rgba(212,175,55,0.16);
}}

.price-label {{
    color: #E6C86E;
    font-size: 18px;
    margin-bottom: 8px;
}}

.price-number {{
    color: #FFD700;
    font-size: 42px;
    font-weight: 900;
    text-shadow: 0 0 12px rgba(212,175,55,0.18);
}}

.small-note {{
    color: #D9C27A;
    font-size: 14px;
    text-align: center;
    margin-top: 8px;
}}

.gold-center {{
    color: #D4AF37 !important;
    text-align: center;
    font-weight: 800;
}}

.gold-caption {{
    color: #E6C86E !important;
    text-align: center;
    font-size: 15px;
    margin-top: 8px;
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

.stSlider p {{
    color: #E6C86E !important;
}}

.stDateInput > div > div,
.stTextInput > div > div,
.stNumberInput > div > div,
div[data-baseweb="select"] > div {{
    background-color: rgba(15,15,15,0.95) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
    transition: all 0.25s ease !important;
}}

.stDateInput > div > div:hover,
.stTextInput > div > div:hover,
.stNumberInput > div > div:hover,
div[data-baseweb="select"] > div:hover {{
    box-shadow: 0 0 14px rgba(212,175,55,0.25) !important;
    border: 1px solid rgba(212,175,55,0.45) !important;
}}

input {{
    color: white !important;
}}

hr {{
    border: 1px solid rgba(212,175,55,0.18);
    margin: 10px 0 18px 0;
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
    min-height: 64px;
    border: none;
    border-radius: 18px;
    padding: 12px 18px;
    font-size: 20px;
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

.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #FFD700, #D4AF37) !important;
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
        width: 180px !important;
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

    .summary-line {{
        font-size: 14px !important;
        line-height: 1.8 !important;
        margin: 8px 0 !important;
    }}

    .price-label {{
        font-size: 15px !important;
    }}

    .price-number {{
        font-size: 30px !important;
    }}

    .small-note {{
        font-size: 12px !important;
        line-height: 1.8 !important;
    }}

    .gold-center {{
        font-size: 18px !important;
        line-height: 1.6 !important;
    }}

    .gold-caption {{
        font-size: 13px !important;
    }}

    .stButton > button {{
        min-height: 54px !important;
        font-size: 15px !important;
        border-radius: 15px !important;
        padding: 9px 10px !important;
        white-space: normal !important;
        line-height: 1.35 !important;
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
# سايدبار الكمبيوتر
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
        key="booking_lang_sidebar"
    )
    st.session_state.lang = "ar" if lang_view == TXT["ar"]["arabic"] else "en"

# =========================
# أعلى الصفحة
# =========================
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    page_lang = st.selectbox(
        t("lang_label"),
        [TXT["ar"]["arabic"], TXT["en"]["english"]],
        index=0 if st.session_state.lang == "ar" else 1,
        key="booking_lang_top"
    )
    st.session_state.lang = "ar" if page_lang == TXT["ar"]["arabic"] else "en"

# =========================
# الهيدر
# =========================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{t("page_title")}</div>
    <div class="hero-subtitle">{t("page_subtitle")}</div>
    <div class="hero-text">
        {t("page_desc")}
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# الخيارات
# =========================
match_options = list(pricing.keys())
payment_methods = ["Apple Pay", "KNET", "Visa", "PayPal", "Samsung Pay"]

discount_codes = {
    "KTECH10": 0.10,
    "SMART15": 0.15,
    "VIP20": 0.20
}

def seat_type_label(value):
    mapping = {
        "Regular": t("regular"),
        "Premium": t("premium"),
        "VIP": t("vip")
    }
    return mapping.get(value, value)

def calculate_price(match_name, seat_type, seat_section, ticket_count, demand_level, discount_code):
    base_price = pricing[match_name]
    seat_extra = seat_prices[seat_type]
    section_extra = section_prices[seat_section]
    demand_extra = demand_level * 1.5

    subtotal_per_ticket = base_price + seat_extra + section_extra + demand_extra
    subtotal = subtotal_per_ticket * ticket_count

    discount_value = 0
    if discount_code in discount_codes:
        discount_value = subtotal * discount_codes[discount_code]

    final_price = subtotal - discount_value
    return base_price, round(final_price, 2), round(discount_value, 2), round(subtotal, 2)

def make_qr_image(data_text: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("RGB")

def create_ticket_pdf(
    booking_id,
    customer_name,
    phone,
    booking_date,
    match_name,
    seat_type,
    seat_section,
    ticket_count,
    payment_method,
    final_price
):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 26)
    c.drawString(60, height - 70, "SmartSeat Ticket")

    c.setFont("Helvetica", 13)
    c.drawString(60, height - 95, "Sponsored by Ktech")

    c.roundRect(50, height - 430, 500, 300, 16, stroke=1, fill=0)

    y = height - 160
    gap = 28

    details = [
        f"Booking ID: {booking_id}",
        f"Customer Name: {customer_name}",
        f"Phone: {phone}",
        f"Date: {booking_date}",
        f"Match: {match_name}",
        f"Seat Type: {seat_type}",
        f"Section: {seat_section}",
        f"Tickets: {ticket_count}",
        f"Payment Method: {payment_method}",
        f"Final Price: {final_price} KD",
    ]

    c.setFont("Helvetica", 12)
    for line in details:
        c.drawString(70, y, line)
        y -= gap

    qr_text = (
        f"SmartSeat | ID:{booking_id} | {customer_name} | {match_name} | "
        f"{seat_type} | Section:{seat_section} | Tickets:{ticket_count} | {final_price} KD"
    )
    qr_img = make_qr_image(qr_text)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    c.drawImage(ImageReader(qr_buffer), 390, height - 395, width=120, height=120)

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(60, 60, "Generated by SmartSeat Final Year Project")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# تحديد المباراة تلقائيًا
# =========================
default_index = 0
if "selected_match" in st.session_state:
    selected_match = st.session_state["selected_match"]
    if selected_match in match_options:
        default_index = match_options.index(selected_match)

# =========================
# بيانات الحجز
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("booking_section")}</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input(t("customer_name"))
    with c2:
        phone = st.text_input(t("phone"))

    c3, c4 = st.columns(2)
    with c3:
        booking_date = st.date_input(t("booking_date"), value=date.today(), min_value=date.today())
    with c4:
        ticket_count = st.number_input(t("ticket_count"), min_value=1, max_value=10, value=1, step=1)

    c5, c6 = st.columns(2)
    with c5:
        match_name = st.selectbox(t("match_name"), match_options, index=default_index)
    with c6:
        seat_type = st.selectbox(t("seat_type"), list(seat_prices.keys()), format_func=seat_type_label)

    c7, c8 = st.columns(2)
    with c7:
        seat_section = st.selectbox(t("seat_section"), list(section_prices.keys()))
    with c8:
        demand_level = st.slider(t("demand_level"), min_value=1, max_value=10, value=5)

    c9, c10 = st.columns(2)
    with c9:
        payment_method = st.selectbox(t("payment_method"), payment_methods)
    with c10:
        discount_code = st.text_input(t("discount_code"), placeholder=t("discount_placeholder"))

# =========================
# حساب السعر
# =========================
base_price, final_price, discount_value, subtotal = calculate_price(
    match_name,
    seat_type,
    seat_section,
    ticket_count,
    demand_level,
    discount_code.strip().upper()
)

# =========================
# ملخص الحجز
# =========================
with st.container(border=True):
    st.markdown(f'<div class="section-title">{t("summary_section")}</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown(f'<div class="summary-line"><b>{t("customer_name")}:</b> {customer_name if customer_name else "-"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("phone")}:</b> {phone if phone else "-"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("booking_date")}:</b> {booking_date}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("match_name")}:</b> {match_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("seat_type")}:</b> {seat_type_label(seat_type)}</div>', unsafe_allow_html=True)

    with s2:
        st.markdown(f'<div class="summary-line"><b>{t("seat_section")}:</b> {seat_section}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("ticket_count")}:</b> {ticket_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("demand_level")}:</b> {demand_level}/10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("payment_method")}:</b> {payment_method}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>{t("discount_code")}:</b> {discount_code if discount_code else t("no_discount")}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="price-box">
        <div class="price-label">{t("final_price")}</div>
        <div class="price-number">{final_price} د.ك</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="small-note">{t("before_discount")}: {subtotal} د.ك | {t("discount_value")}: {discount_value} د.ك</div>',
        unsafe_allow_html=True
    )

# =========================
# التأكيد
# =========================
confirm = st.button(t("confirm_booking"))

if confirm:
    phone_clean = phone.strip()
    discount_clean = discount_code.strip().upper()

    if customer_name.strip() == "":
        st.error(t("name_error"))
    elif phone_clean == "":
        st.error(t("phone_error"))
    else:
        progress_text = st.markdown(
            f"<div class='gold-center' style='font-size:18px; margin-top:10px;'>{t('processing')}</div>",
            unsafe_allow_html=True
        )
        progress_bar = st.progress(0)

        for i in range(1, 101):
            time.sleep(0.01)
            progress_bar.progress(i)

        booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bookings (
                customer_name, phone, booking_date, match_name, seat_type,
                seat_section, ticket_count, demand_level, payment_method,
                discount_code, base_price, final_price, booking_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            phone_clean,
            str(booking_date),
            match_name,
            seat_type,
            seat_section,
            ticket_count,
            demand_level,
            payment_method,
            discount_clean,
            base_price,
            final_price,
            booking_time
        ))
        conn.commit()

        booking_id = cursor.lastrowid

        pdf_buffer = create_ticket_pdf(
            booking_id=booking_id,
            customer_name=customer_name,
            phone=phone_clean,
            booking_date=str(booking_date),
            match_name=match_name,
            seat_type=seat_type,
            seat_section=seat_section,
            ticket_count=ticket_count,
            payment_method=payment_method,
            final_price=final_price
        )

        qr_text = f"{customer_name} | {match_name} | {seat_type} | {seat_section} | {final_price} KD | ID:{booking_id}"
        qr_img = make_qr_image(qr_text)

        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_bytes = qr_buffer.getvalue()

        progress_bar.empty()
        progress_text.empty()

        st.markdown(f"""
        <div class="success-box">
            {t("success")}<br><br>
            👤 {t("customer")}: <b>{customer_name}</b><br>
            🎟️ {t("match")}: <b>{match_name}</b><br>
            💺 {t("seat")}: <b>{seat_type_label(seat_type)} - {seat_section}</b><br>
            💰 {t("final_price")}: <b>{final_price} د.ك</b><br>
            💳 {t("payment")}: <b>{payment_method}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div class='gold-center' style='font-size:22px; margin-top:10px;'>{t('booking_number')}: #{booking_id}</div>",
            unsafe_allow_html=True
        )

        st.download_button(
            label=t("download_pdf"),
            data=pdf_buffer,
            file_name=f"SmartSeat_Ticket_{booking_id}.pdf",
            mime="application/pdf"
        )

        with st.container(border=True):
            st.markdown(f'<div class="gold-center"><h3>{t("qr_title")}</h3></div>', unsafe_allow_html=True)
            qr_col1, qr_col2, qr_col3 = st.columns([1, 1.2, 1])
            with qr_col2:
                st.image(qr_img, width=220)
            st.markdown(f'<div class="gold-caption">{t("qr_caption")}</div>', unsafe_allow_html=True)

            st.download_button(
                label=t("download_qr"),
                data=qr_bytes,
                file_name=f"SmartSeat_QR_{booking_id}.png",
                mime="image/png"
            )

        st.session_state.pop("selected_match", None)

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
        if st.button(t('home'), key="m_home_1", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button(t('matches'), key="m_matches_1", use_container_width=True):
            st.switch_page("pages/0_Match_Details.py")

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('history'), key="m_history_1", use_container_width=True):
            st.switch_page("pages/2_History.py")
    with col2:
        if st.button(t('analytics'), key="m_analytics_1", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('admin'), key="m_admin_1", use_container_width=True):
            st.switch_page("pages/4_Admin.py")
    with col2:
        if st.button(t('support'), key="m_support_1", use_container_width=True):
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

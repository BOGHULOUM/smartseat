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
    max-width: 1150px;
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
    width: 260px;
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
}}

.price-box {{
    background: linear-gradient(180deg, rgba(255,215,0,0.14), rgba(212,175,55,0.08));
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    margin-top: 18px;
    box-shadow: 0 0 18px rgba(212,175,55,0.16);
    animation: glowPulse 2.2s infinite ease-in-out;
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
    animation: fadeUp 0.9s ease;
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
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 0 26px rgba(212,175,55,0.42);
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
    animation: fadeUp 0.6s ease;
}}

.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #FFD700, #D4AF37) !important;
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

@keyframes glowPulse {{
    0% {{
        box-shadow: 0 0 10px rgba(212,175,55,0.10);
    }}
    50% {{
        box-shadow: 0 0 24px rgba(212,175,55,0.28);
    }}
    100% {{
        box-shadow: 0 0 10px rgba(212,175,55,0.10);
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
    st.markdown("### صفحة الحجز")
    st.markdown("أدخل بيانات الحجز وسيتم احتساب السعر النهائي بشكل مباشر.")

# =========================
# الهيدر
# =========================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">حجز التذاكر</div>
    <div class="hero-subtitle">Smart Booking Experience</div>
    <div class="hero-text">
        أدخل بيانات الحجز وسيتم حساب السعر النهائي بشكل مباشر حسب المباراة، نوع المقعد،
        عدد التذاكر، مستوى الطلب، وكود الخصم إن وجد.
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

def create_ticket_pdf(booking_id, customer_name, phone, booking_date, match_name, seat_type,
                      seat_section, ticket_count, payment_method, final_price):
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
    st.markdown('<div class="section-title">بيانات الحجز</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("اسم العميل")
    with c2:
        phone = st.text_input("رقم الهاتف")

    c3, c4 = st.columns(2)
    with c3:
        booking_date = st.date_input("اختيار التاريخ", value=date.today(), min_value=date.today())
    with c4:
        ticket_count = st.number_input("عدد التذاكر", min_value=1, max_value=10, value=1, step=1)

    c5, c6 = st.columns(2)
    with c5:
        match_name = st.selectbox("اختيار المباراة", match_options, index=default_index)
    with c6:
        seat_type = st.selectbox("نوع المقعد", list(seat_prices.keys()))

    c7, c8 = st.columns(2)
    with c7:
        seat_section = st.selectbox("اختيار المقعد", list(section_prices.keys()))
    with c8:
        demand_level = st.slider("مستوى الطلب", min_value=1, max_value=10, value=5)

    c9, c10 = st.columns(2)
    with c9:
        payment_method = st.selectbox("طريقة الدفع", payment_methods)
    with c10:
        discount_code = st.text_input("كود الخصم", placeholder="مثال: KTECH10")

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
    st.markdown('<div class="section-title">ملخص الحجز</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown(f'<div class="summary-line"><b>اسم العميل:</b> {customer_name if customer_name else "-"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>رقم الهاتف:</b> {phone if phone else "-"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>التاريخ:</b> {booking_date}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>المباراة:</b> {match_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>نوع المقعد:</b> {seat_type}</div>', unsafe_allow_html=True)

    with s2:
        st.markdown(f'<div class="summary-line"><b>المقعد / القسم:</b> {seat_section}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>عدد التذاكر:</b> {ticket_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>مستوى الطلب:</b> {demand_level}/10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>طريقة الدفع:</b> {payment_method}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-line"><b>كود الخصم:</b> {discount_code if discount_code else "لا يوجد"}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="price-box">
        <div class="price-label">السعر النهائي</div>
        <div class="price-number">{final_price} د.ك</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="small-note">الإجمالي قبل الخصم: {subtotal} د.ك | قيمة الخصم: {discount_value} د.ك</div>',
        unsafe_allow_html=True
    )

# =========================
# التأكيد
# =========================
confirm = st.button("✅ تأكيد الحجز الآن")

if confirm:
    phone_clean = phone.strip()
    discount_clean = discount_code.strip().upper()

    if customer_name.strip() == "":
        st.error("يرجى إدخال اسم العميل.")
    elif phone_clean == "":
        st.error("يرجى إدخال رقم الهاتف.")
    else:
        progress_text = st.markdown(
            "<div class='gold-center' style='font-size:18px; margin-top:10px;'>جاري تأكيد الحجز وتجهيز التذكرة...</div>",
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
            🎉 تم تأكيد الحجز بنجاح!<br><br>
            👤 العميل: <b>{customer_name}</b><br>
            🎟️ المباراة: <b>{match_name}</b><br>
            💺 المقعد: <b>{seat_type} - {seat_section}</b><br>
            💰 السعر النهائي: <b>{final_price} د.ك</b><br>
            💳 الدفع: <b>{payment_method}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div class='gold-center' style='font-size:22px; margin-top:10px;'>رقم الحجز: #{booking_id}</div>",
            unsafe_allow_html=True
        )

        st.download_button(
            label="📄 تحميل التذكرة PDF",
            data=pdf_buffer,
            file_name=f"SmartSeat_Ticket_{booking_id}.pdf",
            mime="application/pdf"
        )

        with st.container(border=True):
            st.markdown('<div class="gold-center"><h3>🎟️ رمز التذكرة (QR Code)</h3></div>', unsafe_allow_html=True)
            qr_col1, qr_col2, qr_col3 = st.columns([1, 1.2, 1])
            with qr_col2:
                st.image(qr_img, width=220)
            st.markdown('<div class="gold-caption">اعرض هذا الرمز عند الدخول</div>', unsafe_allow_html=True)

            st.download_button(
                label="📥 تحميل QR كصورة",
                data=qr_bytes,
                file_name=f"SmartSeat_QR_{booking_id}.png",
                mime="image/png"
            )

        st.session_state.pop("selected_match", None)

# =========================
# الفوتر
# =========================
st.markdown("""
<div class="footer">
    SmartSeat Booking • Final Year Project
</div>
""", unsafe_allow_html=True)

conn.close()
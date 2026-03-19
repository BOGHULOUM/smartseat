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
# بيانات المباريات (مصححة)
# =========================
matches = [
    {
        "image": assets_dir / "match1.png",
        "name": "برشلونة × ريال مدريد",
        "type": "نهائي",
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
        "image": assets_dir / "match2.png",
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
        "image": assets_dir / "match3.png",
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
# التصميم (نفس القديم)
# =========================
st.markdown(f"""
<style>
html, body {{
    direction: rtl;
    font-family: 'Segoe UI';
}}

.stApp {{
    background: linear-gradient(135deg,#050505,#111111);
    color: white;
}}

.block-container {{
    max-width: 1200px;
}}

.match-title {{
    color: #D4AF37;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}}

.info-line {{
    color: #F0D98A;
    font-size: 15px;
    margin: 4px 0;
}}

.status {{
    margin-top:10px;
}}

.btn {{
    background: gold;
    color: black;
}}

.footer {{
    text-align:center;
    margin-top:30px;
    color:#D4AF37;
}}

@media (max-width:768px) {{
    section[data-testid="stSidebar"] {{
        display:none;
    }}
}}
</style>

<div style="text-align:center">
<img src="data:image/png;base64,{logo_base64}" width="180">
</div>
""", unsafe_allow_html=True)

# =========================
# العنوان
# =========================
st.markdown("""
<div style="text-align:center">
<h1 style="color:#D4AF37;">تفاصيل المباريات</h1>
<p style="color:#E6C86E;">Match Details</p>
</div>
""", unsafe_allow_html=True)

# =========================
# عرض المباريات
# =========================
col1, col2 = st.columns(2)

for i, match in enumerate(matches):
    with (col1 if i % 2 == 0 else col2):
        with st.container():
            st.image(str(match["image"]), use_container_width=True)

            st.markdown(f"<div class='match-title'>{match['name']}</div>", unsafe_allow_html=True)

            st.markdown(f"<div class='info-line'>نوع المباراة: {match['type']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-line'>البطولة: {match['competition']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-line'>الملعب: {match['stadium']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-line'>المدينة: {match['city']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-line'>الحكم: {match['referee']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-line'>التاريخ: {match['datetime']}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='status'>
            فتح البوابات: {match['gates_open']} | {match['demand']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<div class='info-line'>{match['note']}</div>", unsafe_allow_html=True)

            if st.button(f"🎟️ احجز الآن - {match['name']}", key=i):
                st.session_state["selected_match"] = match["name"]
                st.switch_page("pages/1_Booking.py")

# =========================
# الفوتر
# =========================
st.markdown("<div class='footer'>SmartSeat • Final Year Project</div>", unsafe_allow_html=True)

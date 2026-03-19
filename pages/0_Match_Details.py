import streamlit as st
from pathlib import Path

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(layout="wide")

base_dir = Path(__file__).parent.parent

# =========================
# CSS + دعم الجوال 🔥
# =========================
st.markdown("""
<style>

/* عام */
html, body {
    direction: rtl;
    font-family: 'Segoe UI', sans-serif;
}

/* الكارد */
.match-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 20px;
    text-align: center;
}

/* العنوان */
.match-title {
    color: #D4AF37;
    font-size: 22px;
    font-weight: bold;
}

/* النص */
.match-text {
    color: #E6C86E;
    font-size: 15px;
    line-height: 1.8;
}

/* الصور */
img {
    border-radius: 15px;
}

/* =========================
   📱 الجوال
========================= */
@media (max-width: 768px) {

    .block-container {
        padding: 1rem !important;
    }

    .match-title {
        font-size: 18px !important;
    }

    .match-text {
        font-size: 13px !important;
    }

    img {
        width: 100% !important;
        height: auto !important;
    }

    /* إخفاء السايدبار */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# العنوان
# =========================
st.markdown("<h1 style='text-align:center; color:#D4AF37;'>Match Details</h1>", unsafe_allow_html=True)

# =========================
# المباريات (4)
# =========================
matches = [
    {
        "title": "القادسية 🆚 الكويت",
        "image": "assets/match1.png",
        "stadium": "استاد جابر الدولي",
        "ref": "حكم دولي",
        "type": "نهائي كأس",
        "time": "7:00 مساءً"
    },
    {
        "title": "العربي 🆚 السالمية",
        "image": "assets/match2.png",
        "stadium": "استاد صباح السالم",
        "ref": "حكم محلي",
        "type": "دوري",
        "time": "6:30 مساءً"
    },
    {
        "title": "برشلونة 🆚 ريال مدريد",
        "image": "assets/match3.png",
        "stadium": "كامب نو",
        "ref": "حكم أوروبي",
        "type": "كلاسيكو",
        "time": "10:00 مساءً"
    },
    {
        "title": "ليفربول 🆚 مانشستر سيتي",
        "image": "assets/match4.png",
        "stadium": "أنفيلد",
        "ref": "حكم إنجليزي",
        "type": "دوري إنجليزي",
        "time": "9:30 مساءً"
    }
]

# =========================
# عرض المباريات
# =========================
col1, col2 = st.columns(2)

for i, match in enumerate(matches):

    with (col1 if i % 2 == 0 else col2):

        st.markdown(f"""
        <div class="match-card">
            <div class="match-title">{match["title"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.image(str(base_dir / match["image"]))

        st.markdown(f"""
        <div class="match-text">
            📍 الملعب: {match["stadium"]}<br>
            👨‍⚖️ الحكم: {match["ref"]}<br>
            🏆 نوع المباراة: {match["type"]}<br>
            ⏰ التوقيت: {match["time"]}
        </div>
        """, unsafe_allow_html=True)

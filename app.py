import streamlit as st

st.set_page_config(page_title="AA Çapraz Bulmaca", layout="centered")

# CSS ile kutucukları güzelleştirelim
st.markdown("""
    <style>
    .letter-input {
        width: 40px !important;
        height: 40px !important;
        text-align: center !important;
        font-weight: bold !important;
        font-size: 20px !important;
        text-transform: uppercase !important;
    }
    .hint-text {
        color: #555;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 Amino Asit Çapraz Bulmaca")
st.write("Her kutucuğa bir harf gelecek şekilde kelimeleri tamamlayın!")

def crossword_row(label, answer, hint):
    st.subheader(f"❓ {label}")
    st.caption(hint)
    
    # Harf sayısı kadar sütun oluştur
    cols = st.columns(len(answer) + 1)
    user_answer = ""
    
    for i, letter in enumerate(answer):
        with cols[i]:
            # Her kutucuk için benzersiz key
            char = st.text_input("", key=f"input_{label}_{i}", max_chars=1).upper()
            user_answer += char
            
    if user_answer == answer:
        st.success(f"✅ Doğru: {answer}")
        return True
    elif len(user_answer) == len(answer):
        st.error("❌ Hatalı harf var!")
    return False

# Bulmaca Soruları
score = 0
questions = [
    ("SORU 1", "VALIN", "Dallı zincirli, en basit esansiyel amino asitlerden biri."),
    ("SORU 2", "LIZIN", "Bazik yan zincirli, sadece ketojenik olan amino asit."),
    ("SORU 3", "METIYONIN", "Başlangıç kodonu olan, sülfür içeren esansiyel AA."),
    ("SORU 4", "HISTIDIN", "Yarı esansiyel, çocukluk döneminde dışarıdan alınması zorunlu AA.")
]

for label, ans, hint in questions:
    if crossword_row(label, ans, hint):
        score += 1

# İlerleme Durumu
st.divider()
if score == len(questions):
    st.balloons()
    st.success("Tüm bulmacayı çözdünüz! 🏆")
else:
    st.info(f"Kalan kelime sayısı: {len(questions) - score}")

with st.expander("İpucu Kelimeler"):
    st.write("VALIN, LIZIN, METIYONIN, HISTIDIN")

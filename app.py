import streamlit as st

st.set_page_config(page_title="AA Kare Bulmaca", layout="centered")

# CSS ile gerçek bulmaca görünümü (Siyah kareler ve harf kutuları)
st.markdown("""
    <style>
    .stTextInput input {
        width: 45px !important;
        height: 45px !important;
        padding: 0px !important;
        text-align: center !important;
        font-weight: bold !important;
        font-size: 20px !important;
        background-color: white;
        border: 2px solid #333 !important;
    }
    .black-cell {
        width: 45px;
        height: 45px;
        background-color: #333;
        border: 2px solid #333;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Esansiyel AA Kare Bulmaca")
st.write("9 Esansiyel Amino Asidi bulmacaya yerleştirin! (Büyük harf kullanın)")

# Bulmaca Matrisi (9 satır x 10 sütun örneği)
# 'X' siyah kutuları, harfler ise doğru cevapları temsil eder.
grid_data = [
    ['L', 'İ', 'Z', 'İ', 'N', 'X', 'X', 'X', 'X'],
    ['Ö', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['S', 'X', 'V', 'A', 'L', 'İ', 'N', 'X', 'X'],
    ['İ', 'X', 'A', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['N', 'X', 'L', 'İ', 'N', 'X', 'M', 'E', 'T'], # Kısaltılmış örnek dizilim
    ['X', 'X', 'İ', 'X', 'X', 'X', 'E', 'X', 'X'],
    ['T', 'R', 'E', 'O', 'N', 'İ', 'N', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
]

# Sorular ve İpuçları
st.sidebar.header("📝 İpuçları")
st.sidebar.markdown("""
1. **Yatay:** Bazik, sadece ketojenik AA.
2. **Dikey:** Sadece ketojenik, dallı zincirli.
3. **Yatay:** En küçük dallı zincirli AA.
4. **Yatay:** OH grubu içeren esansiyel AA.
5. **Dikey:** Sülfür içeren başlangıç AA.
""")

# Bulmacayı oluştur
correct_count = 0
total_letters = 0

for r, row in enumerate(grid_data):
    cols = st.columns(len(row))
    for c, cell in enumerate(row):
        with cols[c]:
            if cell == 'X':
                # Siyah kutu
                st.markdown('<div class="black-cell"></div>', unsafe_allow_html=True)
            else:
                total_letters += 1
                user_char = st.text_input("", key=f"cell_{r}_{c}", max_chars=1).upper()
                if user_char == cell:
                    correct_count += 1

# Durum çubuğu ve başarı mesajı
st.divider()
if total_letters > 0:
    progress = correct_count / total_letters
    st.progress(progress)
    
    if correct_count == total_letters:
        st.balloons()
        st.success("Tebrikler! Amino asit kalesini fethettiniz! 🏆")
    else:
        st.info(f"Doğru harf sayısı: {correct_count} / {total_letters}")

with st.expander("Kullanılacak Amino Asitler Listesi"):
    st.write("FENİALANİN, VALİN, TREONİN, TRİPTOFAN, İZOLÖSİN, LÖSİN, LİZİN, METİYONİN, HİSTİDİN")

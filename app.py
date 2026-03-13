import streamlit as st
import time
import random
import string

st.set_page_config(page_title="AA Kelime Avı", layout="centered")

# --- CSS: TELEFON İÇİN ÖZEL TASARIM ---
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(10, 1fr); /* 10 sütunlu ızgara */
        gap: 4px;
        margin-bottom: 20px;
        justify-content: center;
    }
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    /* Basılan harf gri, bulunan kelime yeşil (Streamlit button state ile yönetilir) */
    </style>
""", unsafe_allow_html=True)

# --- OYUN VERİLERİ ---
target_words = ["FENILALANIN", "VALIN", "TREONIN", "TRIPTOFAN", "IZOLOSIN", "LOSIN", "LIZIN", "METIYONIN", "HISTIDIN"]

# Matrisi hazırlama (10x12)
if 'grid' not in st.session_state:
    # Boş matris oluştur
    base_grid = [["" for _ in range(10)] for _ in range(12)]
    
    # Kelimeleri yerleştir (Basit dikey/yatay yerleştirme)
    for i, word in enumerate(target_words):
        for char_idx, char in enumerate(word):
            if i < 12 and char_idx < 10:
                base_grid[i][char_idx] = char
    
    # Boş kalan yerleri rastgele harflerle doldur
    for r in range(12):
        for c in range(10):
            if base_grid[r][c] == "":
                base_grid[r][c] = random.choice(string.ascii_uppercase).replace('Q','A').replace('W','S')
    
    st.session_state.grid = base_grid

# --- SESSION STATE ---
if 'selected_coords' not in st.session_state:
    st.session_state.selected_coords = []
if 'found_coords' not in st.session_state:
    st.session_state.found_coords = []
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# --- BAŞLIK VE GİRİŞ ---
st.title("🏆 AA Hız Yarışması")
user_name = st.text_input("Yarışmacı Adı:", placeholder="Adınızı yazın...")

if not user_name:
    st.info("👆 Lütfen önce adınızı yazın.")
    st.stop()

# --- OYUN MANTIĞI ---
def check_word():
    # Seçilen koordinatlardaki harfleri birleştir
    current_word = "".join([st.session_state.grid[r][c] for r, c in st.session_state.selected_coords])
    if current_word in target_words and current_word not in st.session_state.found_words:
        st.session_state.found_words.append(current_word)
        st.session_state.found_coords.extend(st.session_state.selected_coords)
        st.session_state.selected_coords = []
        return True
    return False

# --- BULMACA EKRANI (HTML & Streamlit Karma) ---
st.write(f"Bulunan: {len(st.session_state.found_words)} / 9")

# Izgarayı oluştur
for r in range(12):
    cols = st.columns(10) # Telefondaki "alt alta binme" sorununu önlemek için columns sayısını sabitliyoruz
    for c in range(10):
        char = st.session_state.grid[r][c]
        coord = (r, c)
        
        # Renk Belirleme
        if coord in st.session_state.found_coords:
            btn_type = "primary" # Yeşilimsi/Mavi (Tema ayarına göre)
            label = f"✅" # Veya sadece char
        elif coord in st.session_state.selected_coords:
            label = char
            btn_type = "secondary" # Gri görünüm için standart buton
        else:
            label = char
            btn_type = "secondary"

        if cols[c].button(label, key=f"btn_{r}_{c}", use_container_width=True, type="primary" if coord in st.session_state.found_coords else "secondary"):
            if coord not in st.session_state.found_coords:
                if coord in st.session_state.selected_coords:
                    st.session_state.selected_coords.remove(coord)
                else:
                    st.session_state.selected_coords.append(coord)
                check_word()
                st.rerun()

if st.button("Seçimi Sıfırla 🧹", use_container_width=True):
    st.session_state.selected_cells = []
    st.session_state.selected_coords = []
    st.rerun()

# --- BİTİŞ ---
if len(st.session_state.found_words) == 9:
    total_time = round(time.time() - st.session_state.start_time, 2)
    st.balloons()
    st.success(f"MÜKEMMEL! {user_name}, süren: {total_time} saniye.")
    st.divider()
    st.subheader("Öğretmene bu ekranı göster!")
    st.write(f"Kod: {user_name.upper()}-{int(total_time*100)}")

st.sidebar.markdown("### Bulunacak Liste")
for w in target_words:
    status = "✅" if w in st.session_state.found_words else "⬜"
    st.sidebar.write(f"{status} {w}")

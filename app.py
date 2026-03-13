import streamlit as st
import time
import random
import string

# Sayfa Ayarları
st.set_page_config(page_title="AA Yarışma Paneli", layout="centered")

# --- KRİTİK AYARLAR ---
ADMIN_PASSWORD = "hocam123" # Kendi şifreni buradan değiştirebilirsin
random.seed(2024) # Herkesin bulmacası aynı olsun diye sabitliyoruz

# Skorları tutmak için merkezi bir hafıza oluşturuyoruz
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# --- CSS TASARIMI ---
st.markdown("""
    <style>
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        font-size: 11px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BULMACA HAZIRLIĞI ---
words = ["FENILALANIN", "VALIN", "TREONIN", "TRIPTOFAN", "IZOLOSIN", "LOSIN", "LIZIN", "METIYONIN", "HISTIDIN"]
GRID_SIZE = 14

if 'grid' not in st.session_state:
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    def place_word(word):
        placed = False
        while not placed:
            direction = random.choice(['H', 'V'])
            row = random.randint(0, GRID_SIZE - (len(word) if direction == 'V' else 1))
            col = random.randint(0, GRID_SIZE - (len(word) if direction == 'H' else 1))
            if all(grid[row + (i if direction == 'V' else 0)][col + (i if direction == 'H' else 0)] in ["", word[i]] for i in range(len(word))):
                for i in range(len(word)):
                    grid[row + (i if direction == 'V' else 0)][col + (i if direction == 'H' else 0)] = word[i]
                placed = True
    for w in words: place_word(w)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == "": grid[r][c] = random.choice(string.ascii_uppercase)
    st.session_state.grid = grid

# --- SESSION STATE ---
if 'selected' not in st.session_state: st.session_state.selected = []
if 'found_coords' not in st.session_state: st.session_state.found_coords = set()
if 'found_words' not in st.session_state: st.session_state.found_words = []
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'is_finished' not in st.session_state: st.session_state.is_finished = False

# --- YÖNETİCİ GİRİŞİ (SOLDA GİZLİ) ---
with st.sidebar:
    st.title("🔐 Yönetici")
    admin_input = st.text_input("Şifre:", type="password")
    if admin_input == ADMIN_PASSWORD:
        st.success("Giriş Yapıldı")
        st.write("### 🏆 Bitirenler Listesi")
        if st.session_state.leaderboard:
            for entry in sorted(st.session_state.leaderboard, key=lambda x: x['time']):
                st.write(f"⏱️ {entry['time']}s - **{entry['name']}**")
        else:
            st.write("Henüz bitiren yok.")
        if st.button("Skorları Sıfırla"):
            st.session_state.leaderboard = []
            st.rerun()

# --- OYUN EKRANI ---
st.title("🧩 Amino Asit Avı")
name = st.text_input("Yarışmacı Adı:", placeholder="İsminizi yazın...", key="user_name")

if not name:
    st.warning("Devam etmek için adınızı yazın.")
    st.stop()

# Oyun Mantığı
def check_selection():
    current_str = "".join([st.session_state.grid[r][c] for r, c in st.session_state.selected])
    if current_str in words and current_str not in st.session_state.found_words:
        st.session_state.found_words.append(current_str)
        for coord in st.session_state.selected:
            st.session_state.found_coords.add(coord)
        st.session_state.selected = []
        return True
    return False

st.write(f"Bulunan Kelimeler: **{len(st.session_state.found_words)} / 9**")

# Grid Çizimi
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        coord = (r, c)
        char = st.session_state.grid[r][c]
        
        # Renk Belirleme
        if coord in st.session_state.found_coords:
            btn_type, label = "primary", char
        elif coord in st.session_state.selected:
            btn_type, label = "secondary", "🔘" # Seçilince gri ve işaretli
        else:
            btn_type, label = "secondary", char

        if cols[c].button(label, key=f"{r}_{c}", type=btn_type):
            if coord not in st.session_state.found_coords:
                if coord in st.session_state.selected:
                    st.session_state.selected.remove(coord)
                else:
                    st.session_state.selected.append(coord)
                check_selection()
                st.rerun()

if st.button("Seçimi Temizle 🗑️", use_container_width=True):
    st.session_state.selected = []
    st.rerun()

# --- BİTİŞ ---
if len(st.session_state.found_words) == 9 and not st.session_state.is_finished:
    final_time = round(time.time() - st.session_state.start_time, 2)
    st.session_state.is_finished = True
    st.session_state.leaderboard.append({"name": name, "time": final_time})
    st.balloons()
    st.success(f"BİTTİ! {name}, süren: {final_time} saniye.")

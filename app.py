import streamlit as st
import time
import random
import string

st.set_page_config(page_title="AA Yarışma Paneli", layout="centered")

# --- AYARLAR ---
ADMIN_PASSWORD = "hocam123" 
random.seed(2024) # Herkes için aynı bulmaca

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

st.markdown("""
    <style>
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BULMACA HAZIRLIĞI ---
words = ["FENILALANIN", "VALIN", "TREONIN", "TRIPTOFAN", "IZOLOSIN", "LOSIN", "LIZIN", "METIYONIN", "HISTIDIN"]
GRID_SIZE = 14

if 'grid' not in st.session_state:
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    def place_word_no_overlap(word):
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            direction = random.choice(['H', 'V'])
            row = random.randint(0, GRID_SIZE - (len(word) if direction == 'V' else 1))
            col = random.randint(0, GRID_SIZE - (len(word) if direction == 'H' else 1))
            
            # CRITICAL: Sadece tamamen boş yerlere koy (Çakışma engelleme)
            if all(grid[row + (i if direction == 'V' else 0)][col + (i if direction == 'H' else 0)] == "" for i in range(len(word))):
                for i in range(len(word)):
                    grid[row + (i if direction == 'V' else 0)][col + (i if direction == 'H' else 0)] = word[i]
                placed = True
    
    for w in words: place_word_no_overlap(w)
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

# --- YÖNETİCİ GİRİŞİ ---
with st.sidebar:
    st.title("🔐 Yönetici")
    admin_input = st.text_input("Şifre:", type="password")
    if admin_input == ADMIN_PASSWORD:
        st.write("### 🏆 Bitirenler")
        for entry in sorted(st.session_state.leaderboard, key=lambda x: x['time']):
            st.write(f"⏱️ {entry['time']}s - **{entry['name']}**")

# --- OYUN MANTIĞI ---
def check_selection():
    # Seçim sırasına göre harfleri birleştir
    current_str = "".join([st.session_state.grid[r][c] for r, c in st.session_state.selected])
    if current_str in words and current_str not in st.session_state.found_words:
        st.session_state.found_words.append(current_str)
        for coord in st.session_state.selected:
            st.session_state.found_coords.add(coord)
        st.session_state.selected = []
        return True
    return False

# --- EKRAN ---
st.title("🧩 Amino Asit Avı, Dr. Muammer ÖZDEMİR tarafından hazırlanmıştır")
name = st.text_input("Yarışmacı Adı:", key="user_name")

if not name:
    st.info("Lütfen adınızı yazarak yarışmaya başlayın.")
    st.stop()
    st.markdown('<div class="footer">Hazırlayan: Dr. Öğr. Üyesi Muammer Özdemir</div>', unsafe_allow_html=True)
    st.stop()

st.write(f"Bulunan Kelimeler: **{len(st.session_state.found_words)} / 9**")

for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        coord = (r, c)
        char = st.session_state.grid[r][c]
        
        is_found = coord in st.session_state.found_coords
        is_selected = coord in st.session_state.selected
        
        # Stil Ayarları
        if is_found:
            btn_type, label = "primary", char # Kalıcı Yeşil
        elif is_selected:
            btn_type, label = "secondary", "🔘" # Gri Nokta (Senin istediğin)
        else:
            btn_type, label = "secondary", char # Normal Harf

        if cols[c].button(label, key=f"{r}_{c}", type=btn_type):
            if not is_found:
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
    st.success(f"Tebrikler {name}! Süren: {final_time} sn")

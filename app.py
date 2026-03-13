import streamlit as st
import time
import random
import string

st.set_page_config(page_title="AA Kelime Avı", layout="centered")

# --- CSS: MODERN MOBİL TASARIM ---
st.markdown("""
    <style>
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        font-size: 12px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        border: 1px solid #ddd !important;
    }
    /* Seçili (Gri) Buton */
    button[kind="secondary"]:active, button[kind="secondary"]:focus {
        background-color: #d3d3d3 !important;
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
            direction = random.choice(['H', 'V']) # H: Yatay, V: Dikey
            if direction == 'H':
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - len(word))
                if all(grid[row][col+i] == "" or grid[row][col+i] == word[i] for i in range(len(word))):
                    for i in range(len(word)): grid[row][col+i] = word[i]
                    placed = True
            else:
                row = random.randint(0, GRID_SIZE - len(word))
                col = random.randint(0, GRID_SIZE - 1)
                if all(grid[row+i][col] == "" or grid[row+i][col] == word[i] for i in range(len(word))):
                    for i in range(len(word)): grid[row+i][col] = word[i]
                    placed = True

    for w in words: place_word(w)
    # Boşlukları doldur
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == "": grid[r][c] = random.choice(string.ascii_uppercase)
    st.session_state.grid = grid

# --- SESSION STATE ---
if 'selected' not in st.session_state: st.session_state.selected = []
if 'found_coords' not in st.session_state: st.session_state.found_coords = set()
if 'found_words' not in st.session_state: st.session_state.found_words = []
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# --- BAŞLIK ---
st.title("🧩 Amino Asit Avı")
name = st.text_input("Yarışmacı Adı:", placeholder="İsminizi girin...")

if not name:
    st.warning("Lütfen başlamak için isminizi yazın.")
    st.stop()

# --- OYUN MANTIĞI ---
def check_selection():
    # Seçili koordinatlardaki harfleri birleştir
    current_str = "".join([st.session_state.grid[r][c] for r, c in st.session_state.selected])
    if current_str in words and current_str not in st.session_state.found_words:
        st.session_state.found_words.append(current_str)
        for coord in st.session_state.selected:
            st.session_state.found_coords.add(coord)
        st.session_state.selected = []
        return True
    return False

# --- EKRAN ---
st.write(f"Bulunan: **{len(st.session_state.found_words)} / 9**")

for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        coord = (r, c)
        char = st.session_state.grid[r][c]
        
        # Renk ve Tip Belirleme
        if coord in st.session_state.found_coords:
            btn_type = "primary" # Yeşil (Found)
            btn_label = char
        elif coord in st.session_state.selected:
            btn_type = "secondary" # Gri (Selected)
            btn_label = f"🔘" # Görsel geri bildirim için simge veya harf
        else:
            btn_type = "secondary"
            btn_label = char

        if cols[c].button(btn_label, key=f"{r}_{c}", type=btn_type):
            if coord not in st.session_state.found_coords:
                if coord in st.session_state.selected:
                    st.session_state.selected.remove(coord) # Tekrar basınca kaldır
                else:
                    st.session_state.selected.append(coord)
                check_selection()
                st.rerun()

if st.button("Seçimi Temizle 🗑️", use_container_width=True):
    st.session_state.selected = []
    st.rerun()

# --- BİTİŞ ---
if len(st.session_state.found_words) == 9:
    final_time = round(time.time() - st.session_state.start_time, 2)
    st.balloons()
    st.success(f"Tebrikler {name}! Hızın: {final_time} sn")
    st.subheader("Skor Tablosu İçin Bildir:")
    st.code(f"{name} | {final_time}s | {time.strftime('%H:%M')}")

st.sidebar.markdown("### Amino Asit Listesi")
for w in words:
    st.sidebar.write(f"{'✅' if w in st.session_state.found_words else '⬜'} {w}")

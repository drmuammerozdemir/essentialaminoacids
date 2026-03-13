import streamlit as st
import time
import random
import string

st.set_page_config(page_title="AA Yarışma Paneli", layout="centered")

# --- AYARLAR ---
ADMIN_PASSWORD = "hocam123" 
random.seed(2024) 

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# --- ÖZEL CSS: BUTON RENKLERİ VE STİLLERİ ---
st.markdown("""
    <style>
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    /* Seçili harf için gri arka plan (Streamlit varsayılanı secondary buton) */
    /* Bulunmuş harf için yeşil/mavi arka plan (Streamlit primary buton) */
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
if 'selected' not in st.session_state: st.session_state.selected = set()
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
    # Seçili tüm koordinatlardaki harfleri bir araya getir
    # Sıralama bağımsız kontrol için kelime listesini tarıyoruz
    found_any = False
    for word in words:
        if word in st.session_state.found_words:
            continue
            
        # Mevcut seçimdeki harfler bu kelimeyi oluşturuyor mu?
        # Not: Kelime avında harfler yan yana olmalı.
        # Bu mantık seçili harfler arasında kelimenin varlığını kontrol eder.
        
        # Kelimenin harflerini ve koordinatlarını bulmaca üzerinde eşleştirme:
        # (Basitlik için: Seçilen harflerden herhangi bir hedef kelime oluşuyor mu?)
        chars_in_selection = "".join([st.session_state.grid[r][c] for r, c in sorted(list(st.session_state.selected))])
        
        # Daha kesin bir kontrol: Seçilen koordinatlar bir kelimeyi tam olarak karşılıyor mu?
        # Kelimelerin yerlerini önceden bildiğimiz için direkt koordinat kontrolü yapabiliriz.
        # Ancak burada kullanıcı deneyimi için seçilen harflerin "kümesi" üzerinden gidiyoruz.
        
        # Hedef kelime kontrolü (Sıralı veya sırasız seçimi destekler)
        if any(word == "".join([st.session_state.grid[r][c] for r, c in sorted(list(st.session_state.selected))]) for word in words):
            matched_word = ""
            for w in words:
                if w == "".join([st.session_state.grid[r][c] for r, c in sorted(list(st.session_state.selected))]):
                    matched_word = w
            
            if matched_word and matched_word not in st.session_state.found_words:
                st.session_state.found_words.append(matched_word)
                st.session_state.found_coords.update(st.session_state.selected)
                st.session_state.selected = set()
                found_any = True
    return found_any

# --- EKRAN ---
st.title("🧩 Amino Asit Avı")
name = st.text_input("Adınız:", key="user_name")

if not name:
    st.info("Lütfen adınızı girerek başlayın.")
    st.stop()

st.write(f"Bulunan: **{len(st.session_state.found_words)} / 9**")

# Grid Çizimi
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        coord = (r, c)
        char = st.session_state.grid[r][c]
        
        is_found = coord in st.session_state.found_coords
        is_selected = coord in st.session_state.selected
        
        # Renk Belirleme: Bulunduysa Yeşil (Primary), Seçiliyse Gri (Secondary ama görsel fark için harf kalacak)
        # Streamlit'te butona basıldığında rengi "active" haliyle hissettiririz.
        btn_type = "primary" if is_found else "secondary"
        
        # Harf her zaman görünür, seçiliyse kutu stili (CSS ile desteklenir) veya basit buton hali
        if cols[c].button(char, key=f"{r}_{c}", type=btn_type):
            if coord in st.session_state.selected:
                st.session_state.selected.remove(coord)
            else:
                st.session_state.selected.add(coord)
            
            check_selection()
            st.rerun()

if st.button("Seçimi Temizle 🗑️", use_container_width=True):
    st.session_state.selected = set()
    st.rerun()

# --- BİTİŞ ---
if len(st.session_state.found_words) == 9 and not st.session_state.is_finished:
    final_time = round(time.time() - st.session_state.start_time, 2)
    st.session_state.is_finished = True
    st.session_state.leaderboard.append({"name": name, "time": final_time})
    st.balloons()
    st.success(f"Tebrikler {name}! Süre: {final_time} sn")

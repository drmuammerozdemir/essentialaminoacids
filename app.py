import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="AA Kelime Avı", layout="centered")

# CSS: Hücrelerin kare olması ve mobil dokunmatiğe uygunluğu için
st.markdown("""
    <style>
    div.stButton > button {
        width: 45px !important;
        height: 45px !important;
        padding: 0px !important;
        margin: 2px !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    .found { background-color: #28a745 !important; color: white !important; }
    .selected { background-color: #ffc107 !important; }
    </style>
""", unsafe_allow_html=True)

# 1. VERİ VE MATRİS HAZIRLIĞI
target_words = ["FENILALANIN", "VALIN", "TREONIN", "TRIPTOFAN", "IZOLOSIN", "LOSIN", "LIZIN", "METIYONIN", "HISTIDIN"]

# Örnek 12x12 matris (Basitleştirilmiş, siz bunu geliştirebilirsiniz)
grid = [
    list("FENILALANINX"),
    list("VALINXXXXXXX"),
    list("TREONINXXXXX"),
    list("TRIPTOFANXXX"),
    list("IZOLOSINXXXX"),
    list("LOSINXXXXXXX"),
    list("LIZINXXXXXXX"),
    list("METIYONINXXX"),
    list("HISTIDINXXXX"),
    list("XXXXXXXXXXXX"),
    list("XXXXXXXXXXXX"),
    list("XXXXXXXXXXXX")
]

# 2. SESSION STATE BAŞLATMA
if 'selected_cells' not in st.session_state:
    st.session_state.selected_cells = []
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

st.title("🧪 Amino Asit Kelime Avı")
user_name = st.text_input("Yarışmacı Adı:", placeholder="Adınızı yazın...")

if not user_name:
    st.warning("Lütfen yarışmaya başlamak için adınızı girin.")
    st.stop()

# 3. OYUN MANTIĞI
st.write(f"Bulunan Kelimeler: {len(st.session_state.found_words)} / {len(target_words)}")

def check_selection():
    # Seçili harfleri birleştir
    current_string = "".join([grid[r][c] for r, c in st.session_state.selected_cells])
    for word in target_words:
        if word == current_string and word not in st.session_state.found_words:
            st.session_state.found_words.append(word)
            st.session_state.selected_cells = [] # Seçimi sıfırla
            return True
    return False

# 4. BULMACA EKRANI
for r in range(len(grid)):
    cols = st.columns(len(grid[r]))
    for c in range(len(grid[r])):
        char = grid[r][c]
        
        # Hücrenin durumu (Seçili mi? Bulundu mu?)
        is_found = any(word == "".join([grid[r_f][c_f] for r_f, c_f in st.session_state.selected_cells]) for word in st.session_state.found_words) # Bu basitleştirilmiş bir kontroldür
        
        # Kelime içindeki harfin koordinatı daha önce bulunan bir kelimeye ait mi?
        # (Bu kısım biraz daha karmaşık bir 'found_coordinates' listesi gerektirir, 
        # şimdilik temel mantığı kuruyoruz)
        
        button_key = f"btn_{r}_{c}"
        if cols[c].button(char, key=button_key):
            if (r, c) not in st.session_state.selected_cells:
                st.session_state.selected_cells.append((r, c))
                check_selection()
                st.rerun()

if st.button("Seçimi Temizle"):
    st.session_state.selected_cells = []
    st.rerun()

# 5. BİTİŞ VE LİDERLİK
if len(st.session_state.found_words) == len(target_words):
    end_time = time.time() - st.session_state.start_time
    st.balloons()
    st.success(f"Tebrikler {user_name}! Süren: {end_time:.2f} saniye")
    
    # Skor Kaydı (Gerçek bir DB için st.connection kullanılmalı)
    st.write("🏆 Skorun kaydedildi! (Liderlik tablosu için öğretmeninize ekran görüntüsü atın)")

st.sidebar.header("Bulunacak Kelimeler")
for w in target_words:
    if w in st.session_state.found_words:
        st.sidebar.write(f"✅ ~~{w}~~")
    else:
        st.sidebar.write(f"⬜ {w}")

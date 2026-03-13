import streamlit as st
import time
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="AA Yarışması", layout="centered")

# Sabit Veriler
aa_data = {
    "FENILALANIN": "Hem glikojenik hem ketojenik, tirozin öncülü olan esansiyel AA.",
    "TREONIN": "Hem glikojenik hem ketojenik, OH grubu içeren esansiyel AA.",
    "TRIPTOFAN": "Hem glikojenik hem ketojenik, serotonin sentezinde kullanılan AA.",
    "IZOLOSIN": "Hem glikojenik hem ketojenik, dallı zincirli esansiyel AA."
}

# Session State Hazırlığı
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'finished' not in st.session_state:
    st.session_state.finished = False

st.title("🏆 Amino Asit Hız Yarışması")

# 1. Giriş Ekranı
user_name = st.text_input("Yarışmacı Adı:", placeholder="Adınızı yazın...")

if user_name:
    if st.button("Yarışmayı Başlat"):
        st.session_state.start_time = time.time()
        st.session_state.finished = False
        st.rerun()

# 2. Yarışma Alanı
if st.session_state.start_time and not st.session_state.finished:
    current_time = time.time() - st.session_state.start_time
    st.write(f"⏱️ Geçen Süre: *{current_time:.2f}* saniye")
    
    selected = st.radio("Soru: Hangisi hem glikojenik hem ketojeniktir?", list(aa_data.keys()))
    
    if st.button("Cevabı Onayla"):
        # Burada tüm AA'lar doğru kategoride olduğu için testi bitiriyoruz
        st.session_state.finished = True
        final_time = time.time() - st.session_state.start_time
        st.success(f"Tebrikler {user_name}! Yarışmayı {final_time:.2f} saniyede tamamladın.")
        
        # Skor Kaydı (Simülasyon - Gerçek tablo için DB bağlantısı gerekir)
        st.session_state.last_score = {"İsim": user_name, "Süre (sn)": round(final_time, 2)}

# 3. Liderlik Tablosu (Örnek)
st.divider()
st.subheader("Leaderboard (Top 5)")
# Not: Bu tablo her sayfa yenilendiğinde sıfırlanır. 
# Kalıcı olması için Streamlit "Secrets" üzerinden bir DB bağlamalıyız.
sample_data = pd.DataFrame([
    {"İsim": "Ahmet", "Süre (sn)": 12.4},
    {"İsim": "Ayşe", "Süre (sn)": 15.1}
])
st.table(sample_data)

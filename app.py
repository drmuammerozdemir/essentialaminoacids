import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="AA Bulmaca", layout="centered")

# Esansiyel Amino Asit Veri Seti
essential_aas = {
    "FENİLALANİN": "Tirozin öncülüdür, aromatik bir halkaya sahiptir.",
    "VALİN": "Dallı zincirli bir amino asittir (BCAA).",
    "TİREONİN": "Yapısında hidroksil (-OH) grubu bulunduran esansiyel AA.",
    "TRİPTOFAN": "Serotonin ve Melatonin öncülüdür, en büyük yan zincire sahiptir.",
    "İZOLÖSİN": "Hem ketojenik hem glikojenik olan dallı zincirli AA.",
    "LÖSİN": "Sadece ketojenik olan dallı zincirli AA.",
    "LİZİN": "Bazik karakterli, sadece ketojenik olan esansiyel AA.",
    "METİYONİN": "Sülfür (kükürt) içeren, başlangıç kodonu (AUG) amino asidi.",
    "HİSTİDİN": "Yarı esansiyel kabul edilir, çocuklarda büyüme için kritiktir."
}

st.title("🧩 Amino Asit Çengel Bulmaca")
st.write("Aşağıdaki ipuçlarını kullanarak esansiyel amino asitleri bulun. Doğru yazarsanız bilgi kartı açılacaktır!")

# Skor takibi için session state
if 'found_count' not in st.session_state:
    st.session_state.found_count = 0

# Bulmaca Alanı
found_list = []

st.divider()

cols = st.columns(2) # Görseli güzelleştirmek için iki sütun

for i, (answer, hint) in enumerate(essential_aas.items()):
    # Her 2 soruda bir sütun değiştir
    col = cols[0] if i % 2 == 0 else cols[1]
    
    with col:
        user_input = st.text_input(f"İpucu: {hint[:40]}...", key=f"aa_{i}", placeholder="Hangi AA?")
        
        # Büyük harf ve Türkçe karakter toleransı için düzenleme
        if user_input.strip().upper().replace('İ', 'İ').replace('I', 'I') == answer:
            st.success(f"✅ Doğru: **{answer}**")
            st.caption(f"💡 *Bilgi: {hint}*")
            found_list.append(answer)
        elif user_input:
            st.error("❌ Henüz doğru değil...")

# İlerleme Çubuğu
st.divider()
progress = len(found_list) / len(essential_aas)
st.subheader(f"Tamamlanma Oranı: %{int(progress*100)}")
st.progress(progress)

if len(found_list) == len(essential_aas):
    st.balloons()
    st.success("Tebrikler! Tüm esansiyel amino asitleri başarıyla buldunuz! 🏆")

# Alt Bilgi
with st.expander("Yardım / Listeyi Gör"):
    st.write("Aradığımız Amino Asitler: PVT TIM HALL (Esansiyel AA kısaltması)")
    st.write(", ".join(essential_aas.keys()))

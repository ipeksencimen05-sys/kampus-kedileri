import streamlit as st
import pandas as pd
import os

st.title("Kampüs Kedileri Veri Girişi 🐾")

# --- Fotoğraflar için klasör oluştur ---
os.makedirs("kediler_fotolar", exist_ok=True)

# --- Veri giriş alanları ---
name = st.text_input("🐱 Kedinin Adı")
gender = st.selectbox("🚻 Cinsiyeti", ["Erkek", "Dişi", "Bilinmiyor"])
neutered = st.selectbox("✂️ Kısır mı?", ["Evet", "Hayır", "Bilinmiyor"])
location = st.text_input("📍 Bulunduğu Yer (örnek: Kütüphane önü)")
age = st.text_input("🎂 Yaş Tahmini (örnek: 2 yaş, yavru, yetişkin)")
notes = st.text_area("📝 Özel Notlar")

uploaded_file = st.file_uploader("📷 Kedi Fotoğrafı Ekle", type=["jpg", "jpeg", "png"])

# --- Kaydet butonu ---
if st.button("Kaydet"):
    photo_path = ""
    if uploaded_file:
        photo_path = os.path.join("kediler_fotolar", uploaded_file.name)
        with open(photo_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    new_data = pd.DataFrame({
        "Ad": [name],
        "Cinsiyet": [gender],
        "Kısır mı": [neutered],
        "Konum": [location],
        "Yaş Tahmini": [age],
        "Notlar": [notes],
        "Fotoğraf": [photo_path]
    })
    new_data.to_csv("kediler.csv", mode="a", header=False, index=False, encoding="utf-8-sig")
    st.success("✅ Kedi kaydedildi!")

# --- Kayıtlı kedileri göster ---
st.write("📋 Şu ana kadar kaydedilen kediler:")

try:
    data = pd.read_csv(
        "kediler.csv",
        names=["Ad", "Cinsiyet", "Kısır mı", "Konum", "Yaş Tahmini", "Notlar", "Fotoğraf"]
    )

    for i, row in data.iterrows():
        st.markdown(f"### 🐾 {row['Ad']}")
        st.write(f"- **Cinsiyet:** {row['Cinsiyet']}")
        st.write(f"- **Kısır mı:** {row['Kısır mı']}")
        st.write(f"- **Konum:** {row['Konum']}")
        st.write(f"- **Yaş Tahmini:** {row['Yaş Tahmini']}")
        st.write(f"- **Notlar:** {row['Notlar']}")
        if pd.notna(row["Fotoğraf"]) and os.path.exists(row["Fotoğraf"]):
            st.image(row["Fotoğraf"], width=200)
        st.markdown("---")

except FileNotFoundError:
    st.info("Henüz veri yok. İlk kaydı sen ekle! 🐾")

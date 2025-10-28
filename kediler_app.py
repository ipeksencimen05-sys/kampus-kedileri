import streamlit as st
import pandas as pd
import os

st.title("Kampüs Kedileri Veri Girişi 🐾")

os.makedirs("kediler_fotolar", exist_ok=True)

# --- CSV oku ---
csv_file = "kediler.csv"
columns = ["Ad", "Cinsiyet", "Kısır mı", "Konum", "Yaş Tahmini", "Notlar", "Fotoğraf"]

if os.path.exists(csv_file):
    data = pd.read_csv(csv_file, names=columns)
else:
    data = pd.DataFrame(columns=columns)

# --- Veri ekleme ---
st.header("Yeni Kayıt Ekle")
name = st.text_input("🐱 Kedinin Adı")
gender = st.selectbox("🚻 Cinsiyeti", ["Erkek", "Dişi", "Bilinmiyor"])
neutered = st.selectbox("✂️ Kısır mı?", ["Evet", "Hayır", "Bilinmiyor"])
location = st.text_input("📍 Bulunduğu Yer")
age = st.text_input("🎂 Yaş Tahmini")
notes = st.text_area("📝 Özel Notlar")
uploaded_file = st.file_uploader("📷 Kedi Fotoğrafı Ekle", type=["jpg", "jpeg", "png"])

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
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(csv_file, index=False, header=False, encoding="utf-8-sig")
    st.success("✅ Kedi kaydedildi!")

# --- Mevcut kayıtları göster ve düzenle ---
st.header("Mevcut Kayıtlar")
edited_data = st.experimental_data_editor(data, num_rows="dynamic")

# --- Kaydet butonu ---
if st.button("Değişiklikleri Kaydet"):
    edited_data.to_csv(csv_file, index=False, header=False, encoding="utf-8-sig")
    st.success("✅ Değişiklikler kaydedildi!")

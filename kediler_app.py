import streamlit as st
import pandas as pd
import os

st.title("Kampüs Kedileri Veri Girişi 🐾")

# --- Fotoğraflar için klasör ---
os.makedirs("kediler_fotolar", exist_ok=True)

# --- CSV dosyası ve kolonlar ---
csv_file = "kediler.csv"
columns = ["Ad", "Cinsiyet", "Kısır mı", "Konum", "Yaş Tahmini", "Notlar", "Fotoğraf"]

if os.path.exists(csv_file):
    data = pd.read_csv(csv_file, names=columns)
else:
    data = pd.DataFrame(columns=columns)

# --- Yeni kayıt ekleme ---
st.header("Yeni Kayıt Ekle")
with st.form("new_entry_form"):
    name = st.text_input("🐱 Kedinin Adı")
    gender = st.selectbox("🚻 Cinsiyeti", ["Erkek", "Dişi", "Bilinmiyor"])
    neutered = st.selectbox("✂️ Kısır mı?", ["Evet", "Hayır", "Bilinmiyor"])
    location = st.text_input("📍 Bulunduğu Yer")
    age = st.text_input("🎂 Yaş Tahmini")
    notes = st.text_area("📝 Özel Notlar")
    uploaded_file = st.file_uploader("📷 Kedi Fotoğrafı Ekle", type=["jpg", "jpeg", "png"])
    
    submitted = st.form_submit_button("Kaydet")
    if submitted:
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
st.info("Tablodaki hücreleri düzenleyip 'Değişiklikleri Kaydet' butonuna basın. Fotoğraflar değiştirilemez.")

# Fotoğraf kolonunu ayrı gösteriyoruz, tablo düzenleme sadece diğer alanlar için
editable_columns = ["Ad", "Cinsiyet", "Kısır mı", "Konum", "Yaş Tahmini", "Notlar"]
edited_data = st.experimental_data_editor(data[editable_columns], num_rows="dynamic")

# Fotoğrafı tekrar ekleyerek tam tabloyu kaydet
if st.button("Değişiklikleri Kaydet"):
    # Fotoğraf kolonunu koruyarak birleştir
    full_data = pd.concat([edited_data, data[["Fotoğraf"]]], axis=1)
    full_data.to_csv(csv_file, index=False, header=False, encoding="utf-8-sig")
    st.success("✅ Değişiklikler kaydedildi!")

# Fotoğrafları göster
st.header("Kedi Fotoğrafları")
for _, row in data.iterrows():
    st.markdown(f"### 🐾 {row['Ad']}")
    st.write(f"- **Cinsiyet:** {row['Cinsiyet']}")
    st.write(f"- **Kısır mı:** {row['Kısır mı']}")
    st.write(f"- **Konum:** {row['Konum']}")
    st.write(f"- **Yaş Tahmini:** {row['Yaş Tahmini']}")
    st.write(f"- **Notlar:** {row['Notlar']}")
    if pd.notna(row["Fotoğraf"]) and os.path.exists(row["Fotoğraf"]):
        st.image(row["Fotoğraf"], width=200)
    st.markdown("---")


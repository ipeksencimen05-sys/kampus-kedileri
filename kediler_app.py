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
    location = st.selectbox("📍 Bulunduğu Yer", [
        "Doğu Kampüs", "Lojmanlar", "Merkez Kampüs", "Bilbak", "Bilenerji"
    ])
    age = st.text_input("🎂 Yaş Tahmini (örnek: 2 yaş, yavru, yetişkin)")
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

# --- Mevcut kayıtları kampüse göre göster ve Kısır mı? değiştir ---
st.header("Mevcut Kediler ve Kısırlık Durumunu Güncelleme")
kampusler = ["Doğu Kampüs", "Lojmanlar", "Merkez Kampüs", "Bilbak", "Bilenerji"]

for kampus in kampusler:
    st.subheader(f"🏢 {kampus}")
    subset = data[data["Konum"] == kampus].copy()
    
    if subset.empty:
        st.info("Henüz veri yok.")
        continue

    # Her kayıt için "Kısır mı?" güncelleme
    for idx, row in subset.iterrows():
        st.markdown(f"### 🐾 {row['Ad']}")
        st.write(f"- **Cinsiyet:** {row['Cinsiyet']}")
        st.write(f"- **Yaş Tahmini:** {row['Yaş Tahmini']}")
        st.write(f"- **Notlar:** {row['Notlar']}")
        if pd.notna(row["Fotoğraf"]) and os.path.exists(row["Fotoğraf"]):
            st.image(row["Fotoğraf"], width=200)

        new_neutered = st.selectbox(f"✂️ Kısır mı? ({row['Ad']})", ["Evet", "Hayır", "Bilinmiyor"], index=["Evet","Hayır","Bilinmiyor"].index(row["Kısır mı"]))
        data.loc[idx, "Kısır mı"] = new_neutered
        st.markdown("---")

# --- Güncellenmiş veriyi kaydet ---
if st.button("Kısırlık Durumunu Kaydet"):
    data.to_csv(csv_file, index=False, header=False, encoding="utf-8-sig")
    st.success("✅ Kısırlık durumu güncellendi!")

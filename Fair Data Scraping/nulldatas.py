import pandas as pd
import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import re
import time

api_key = "serpapi gir orda api key var ona bas kopyala bu yazıyı sil yapıştır"

df = pd.read_excel("katilimcilar.xlsx")

# excelde bulunamadı olanları tespit etme
eksik_bilgili = df[(df["Email"] == "Bulunamadı") | (df["Telefon"] == "Bulunamadı")].head(20)

sonuclar = []

for idx, row in eksik_bilgili.iterrows():
    sirket_ismi = row["İsim"]

    print(f"Aranıyor: {sirket_ismi} iletişim")

    # google arama ayarları
    params = {
        "engine": "google",
        "q": f"{sirket_ismi} iletişim",
        "api_key": api_key,
        "num": 1
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    first_link = None
    if "organic_results" in results and results["organic_results"]:
        first_link = results["organic_results"][0].get("link")

    if first_link:
        print(f"Bulunan link: {first_link}")
        try:
            page = requests.get(first_link, timeout=10)
            soup = BeautifulSoup(page.content, "html.parser")

            # Sayfadan mail ve telefonları regex ile bulma
            email_matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text)
            phone_matches = re.findall(r"(\+?\d[\d\s\-\(\)]{7,}\d)", soup.text)

            email = email_matches[0] if email_matches else "Bulunamadı"
            telefon = phone_matches[0] if phone_matches else "Bulunamadı"

        except Exception as e:
            print(f"Hata oluştu: {e}")
            email = "Bulunamadı"
            telefon = "Bulunamadı"
    else:
        email = "Bulunamadı"
        telefon = "Bulunamadı"

    sonuclar.append({
        "Şirket": sirket_ismi,
        "Bulunan Email": email,
        "Bulunan Telefon": telefon
    })

    time.sleep(2)  #IP ban yememek için

# excele kaydetme
df_sonuclar = pd.DataFrame(sonuclar)
df_sonuclar.to_excel("otomatik_cekilen_iletisim_bilgileri.xlsx", index=False)

print("İlk 20 şirket için iletişim bilgileri kaydedildi: otomatik_cekilen_iletisim_bilgileri.xlsx")

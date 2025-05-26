import pandas as pd
from serpapi import GoogleSearch
import time

api_key = "serpapi gir orda api key var ona bas kopyala bu yazıyı sil yapıştır"

df = pd.read_excel("katilimcilar.xlsx")

eksik_bilgili = df[(df["Email"] == "Bulunamadı") | (df["Telefon"] == "Bulunamadı")]

sonuclar = []

for idx, row in eksik_bilgili.iterrows():
    sirket_ismi = row["İsim"]

    query = f"{sirket_ismi} iletişim"

    print(f"Aranıyor: {query}")

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 3  # ilk 3 sonuç için burası eğer ilk 1-2 sonuç yeter diyosan değiştir.
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    links = []
    if "organic_results" in results:
        for result in results["organic_results"][:3]:  # ilk 3 sonuç için burası eğer ilk 1-2 sonuç yeter diyosan değiştir.
            links.append(result.get("link"))

    sonuclar.append({
        "Şirket": sirket_ismi,
        "Arama Sonuçları": "\n".join(links) if links else "Sonuç bulunamadı"
    })

    time.sleep(1)  # çok hızlı gitmeyelim

df_sonuclar = pd.DataFrame(sonuclar)
df_sonuclar.to_excel("eksik_bilgili_sirketler_arama.xlsx", index=False)

print("Arama sonuçları kaydedildi: eksik_bilgili_sirketler_arama.xlsx")


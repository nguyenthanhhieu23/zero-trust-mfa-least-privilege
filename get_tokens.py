import requests
import json

KEYCLOAK_URL = "http://localhost:8080"
REALM = "zero-trust"
CLIENT_ID = "zero-trust-demo"

ACCOUNTS = {
    "admin": {"user": "admin", "pass": "ChangeMe_AdminUser_123!"},
    "user":  {"user": "user",  "pass": "ChangeMe_User_123!"},
    "guest": {"user": "guest", "pass": "ChangeMe_Guest_123!"}
}

TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
tokens = {}

print("=== BẮT ĐẦU LẤY TOKEN CHO 3 TÀI KHOẢN ===")

for role, acc in ACCOUNTS.items():
    payload = {
        "client_id": CLIENT_ID,
        "grant_type": "password",
        "username": acc["user"],
        "password": acc["pass"]
    }

    try:
        res = requests.post(TOKEN_URL, data=payload)
        
        # Nếu tài khoản yêu cầu mã OTP (MFA)
        if res.status_code == 400 and "totp" in res.text.lower():
            otp_code = input(f"[!] Tài khoản {role.upper()} đang bật MFA, nhập mã OTP: ")
            payload["totp"] = otp_code
            res = requests.post(TOKEN_URL, data=payload)

        if res.status_code == 200:
            access_token = res.json()["access_token"]
            tokens[role] = access_token
            print(f"[✓] Lấy Token thành công cho: {role.upper()}")
        else:
            print(f"[✗] Thất bại {role.upper()}: Mã {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[!] Lỗi kết nối tới Keycloak: {e}")

if tokens:
    with open("tokens.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)
    print("\n[OK] Đã lưu thành công token vào file 'tokens.json'!")

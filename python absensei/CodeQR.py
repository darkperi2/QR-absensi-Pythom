import cv2  # OpenCV untuk akses kamera dan pemrosesan gambar
from pyzbar.pyzbar import decode  # Pyzbar untuk deteksi dan pembacaan QR Code
import pandas as pd  # Untuk manajemen data dan penyimpanan ke Excel
from datetime import datetime  # Untuk mencatat waktu absensi saat ini
import os  # Untuk cek dan manipulasi file
import time  # Untuk delay saat scan

filename = "absensi_qr.xlsx"  # Nama file bisa diubah tapi harus .xlsx buat excel

# =========================
# Cek & Buat File Absensi
# =========================
if not os.path.exists(filename):
    df = pd.DataFrame(columns=["NIM", "Nama", "Prodi", "Kelas", "Waktu"])
    df.to_excel(filename, index=False)

# ======================
# Inisialisasi Kamera
# ======================
kamera = cv2.VideoCapture(0)  # Buka kamera default (biasanya webcam)
print("🔍 Mulai scan... (Tekan 'q' untuk keluar)")

# ======================
# Variabel Kontrol Scan
# ======================
last_time = 0  # Waktu scan terakhir
status_text = ""  # Teks status ditampilkan di layar
status_color = (0, 255, 0)  # Warna status (Hijau = berhasil)
status_timer = 0  # Waktu ketika status terakhir muncul
delay_after_scan = 3  # Delay 3 detik setelah satu QR discan, supaya nggak spam. Bisa diubah juga sih senyamannya aja

# =======================
# Loop untuk scan QR Code
# =======================
while True:
    ret, frame = kamera.read()  # Ambil gambar dari kamera
    decoded_objs = decode(frame)  # Deteksi QR code dari gambar kamera

    # ===========================
    # PROSES SETIAP QR TERDETEKSI
    # ===========================
    for obj in decoded_objs: # Proses scan QR Code
        data = obj.data.decode("utf-8")  # Decode dari bytes ke string UTF-8, baru tau sumpah ada kek begini

        # ==========================
        # KOTAK QR & TULISAN VISUAL
        # ==========================
        pts = obj.polygon
        if len(pts) >= 4:
            pts = [(p.x, p.y) for p in pts]
            for i in range(len(pts)):
                # Gambar kotak biru di sekitar QR
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (255, 0, 0), 2)
            x, y = pts[0]
            cv2.putText(frame, "QR Terdeteksi!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # =========================================
        # ANTI SPAM: Cek delay sebelum proses data
        # =========================================
        current_time = time.time()
        if current_time - last_time < delay_after_scan:
            continue  # Lewati proses absensi, tapi tetap gambar kotak QR-nya

        print(f"📦 Data terbaca: {data}")
        last_time = current_time  # Update waktu terakhir QR diproses

        # ==============================
        # CEK FORMAT DATA (FORMAT SALAH)
        # ==============================
        parts = data.split("|")  # Format data yang diharapkan: NIM|Nama|Prodi|Kelas
        if len(parts) != 4:
            print("⚠️ Format QR salah! Harus: NIM|Nama|Prodi|Kelas")
            status_text = "Format QR Salah"
            status_color = (0, 165, 255)  # Orange
            status_timer = time.time()
            continue

        # ==================================
        # CEK DUPLIKAT ABSENSI (SUDAH ABSEN)
        # ==================================
        nim, nama, prodi, kelas = parts
        df = pd.read_excel(filename)  # Baca data absensi yang sudah ada

        if nim in df["NIM"].astype(str).values:
            print(f"❌ {nama} ({nim}) sudah pernah absen!")
            status_text = "Sudah Pernah Absen"
            status_color = (0, 0, 255)  # Merah
            status_timer = time.time()
            continue

        # =========================
        # SIMPAN KE EXCEL
        # =========================
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Catat waktu saat absen

        new_data = pd.DataFrame([{
            "NIM": nim,
            "Nama": nama,
            "Prodi": prodi,
            "Kelas": kelas,
            "Waktu": waktu
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(filename, index=False)

        # ==============
        # ABSEN BERHASIL
        # ==============Q
        print(f"✅ {nama} berhasil absen pada {waktu}")
        status_text = "Absen Berhasil"
        status_color = (0, 255, 0)  # Hijau
        status_timer = time.time()

    # =========================
    # TAMPILKAN STATUS DI LAYAR
    # =========================
    if status_text and time.time() - status_timer < 2:
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

    # =========================
    # TAMPILKAN KAMERA & KELUAR
    # =========================
    cv2.imshow("Scan QR", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # Tekan 'q' untuk keluar
        break

# ==============
# AKHIR PROGRAM
# ==============
kamera.release()
cv2.destroyAllWindows()

# Makasih Google, YouTube, GitHub, ChatGPT, udah bantuin bikin QR Code dan absensi! EAAAAAAAAAAAAA MERASA KEREN
# Terima kasih juga buat dosen-dosen yang udah ngajarin, semoga bisa bermanfaat buat kita semua! EAAAAAAAAAAAAA MERASA KEREN
# Oh iya excelnya harus di quit dulu baru bisa dibuka ya, soalnya kalo dibuka pas program jalan itu bakal error, accsess denied gitu

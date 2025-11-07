import qrcode

nim = input("Masukkan NIM: ")
nama = input("Masukkan Nama: ")
prodi = input("Masukkan Prodi: ")
kelas = input("Masukkan Kelas: ")

data = f"{nim}|{nama}|{prodi}|{kelas}"
qr = qrcode.make(data)
qr.save(f"qr_{nim}.png")

print(f"✅ QR untuk {nama} berhasil dibuat sebagai 'qr_{nim}.png'")

# Untuk nama variablenya beda juga keknya gak apa apa deh, soalnya pas scan yah yang diambil itu
# data.split("|") terus diambil yang pertama, kedua, ketiga, keempat gitu kan
# jadi gak ngaruh ke nama variabelnya, yang penting formatnya sesuai. Udah coba juga tadi

import json
import os
import sys
from datetime import datetime, timedelta
from prettytable import PrettyTable
import pwinput

# Path file JSON untuk data buku dan pengguna
jsonPath = r"C:\Users\user\OneDrive\ドキュメント\PA KEL 4\data.json"
FileDataPeminjam = r"C:\Users\user\OneDrive\ドキュメント\PA KEL 4\dataPeminjam.json"

# Fungsi untuk menyimpan data buku ke file JSON
def saveJson(Data):
    with open(jsonPath, "w") as jsonProduk:
        json.dump(Data, jsonProduk, indent=4)

# Fungsi untuk membaca data buku dari file JSON
def BacaData():
    if os.path.exists(jsonPath):
        with open(jsonPath, "r") as file:
            return json.load(file)
    else:
        return []

# Fungsi untuk membaca data peminjam dari file JSON
def baca_data_peminjam():
    if os.path.exists(FileDataPeminjam):
        with open(FileDataPeminjam, "r") as file:
            return json.load(file)
    else:
        return {}

# Fungsi untuk menyimpan data peminjam ke file JSON
def simpan_data_peminjam(dataPeminjam):
    with open(FileDataPeminjam, "w") as file:
        json.dump(dataPeminjam, file, indent=4)

# Fungsi untuk menampilkan data peminjam
def tampilkanPeminjam(dataPeminjam):
    tabel = PrettyTable(["Nomor", "Nama Peminjam", "Buku", "Tanggal Peminjaman", "Tanggal Pengembalian"])
    for i, peminjam in enumerate(dataPeminjam.values(), start=1):
        nama_peminjam = peminjam.get("Nama Peminjam", "-")
        buku_dipinjam = ", ".join(peminjam.get("Buku Dipinjam", []))
        tanggal_peminjaman = ", ".join(peminjam.get("Tanggal Peminjaman", []))
        tanggal_pengembalian = ", ".join(peminjam.get("Tanggal Pengembalian", []))
        
        tabel.add_row([i, nama_peminjam, buku_dipinjam, tanggal_peminjaman, tanggal_pengembalian])
    print(tabel)


# Fungsi untuk membersihkan layar console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Fungsi untuk menampilkan daftar buku
def tampilkanBuku(daftarBuku):
    tabel = PrettyTable(["Nomor", "Judul", "Penerbit", "Tahun", "Harga Sewa"])
    for i, buku in enumerate(daftarBuku, start=1):
        tabel.add_row([i, buku["Judul Buku"], buku["Penerbit"], buku["Tahun Rilis"], buku["Harga Sewa"]])
    print(tabel)

# Fungsi Registrasi
def registrasi():
    dataPeminjam = baca_data_peminjam()
    username = input("Masukkan Username Baru: ")
    password = pwinput.pwinput("Masukkan Password: ")
    saldo = float(input("Masukkan Saldo Awal: "))

    if username in dataPeminjam:
        print("Username sudah ada.")
    else:
        dataPeminjam[username] = {"password": password, "saldo": saldo, "Buku Dipinjam": [], "Tanggal Peminjaman": [], "Tanggal Pengembalian": []}
        simpan_data_peminjam(dataPeminjam)
        print("Registrasi berhasil!")

# Fungsi Login
def login():
    print("=" * 6 + " Selamat Datang di Sistem Penyewaan Buku Digital " + "=" * 6)
    print("[1]. Admin")
    print("[2]. User")
    print("[3]. Registrasi")
    print("[4]. Keluar")
    pilihan = input("Silakan pilih Mode Login: ")

    if pilihan == "1":
        username = input("Masukkan Username Admin: ")
        password = pwinput.pwinput("Masukkan Password Admin: ")
        if username == "admin" and password == "punyaadmin":
            admin_menu()
        else:
            print("Login gagal, username atau password salah.")
            login()

    elif pilihan == "2":
        username = input("Masukkan Username: ")
        password = pwinput.pwinput("Masukkan Password: ")
        dataPeminjam = baca_data_peminjam()
        if username in dataPeminjam and dataPeminjam[username]["password"] == password:
            peminjam_menu(username)
        else:
            print("Login gagal, username atau password salah.")

    elif pilihan == "3":
        registrasi()
        login()

    elif pilihan == "4":
        print("Terima kasih sudah menggunakan program ini")
        sys.exit()
    else:
        print("Pilihan tidak tersedia.")

from datetime import timedelta

# Fungsi peminjam_menu untuk pengguna
def peminjam_menu(username):
    dataPeminjam = baca_data_peminjam()
    daftarBuku = BacaData()
    
    while True:
        print("\n=== Menu Peminjam ===")
        print("1. Lihat Daftar Buku")
        print("2. Lihat Saldo")
        print("3. Pinjam Buku")
        print("4. Logout")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            tampilkanBuku(daftarBuku)
        
        elif pilihan == "2":
            saldo = dataPeminjam[username]["saldo"]
            print(f"Saldo Anda: Rp {saldo}")
        
        elif pilihan == "3":
            tampilkanBuku(daftarBuku)
            try:
                nomorBuku = int(input("Masukkan Nomor Buku yang Ingin Dipinjam: "))
                
                if 0 < nomorBuku <= len(daftarBuku):
                    buku_dipinjam = daftarBuku[nomorBuku - 1]
                    harga_sewa = buku_dipinjam["Harga Sewa"]
                    
                    if dataPeminjam[username]["saldo"] >= harga_sewa:
                        dataPeminjam[username]["saldo"] -= harga_sewa
                        
                        # Meminta nama peminjam saat meminjam buku
                        nama_peminjam = input("Masukkan Nama Peminjam: ")
                        
                        # Input durasi peminjaman
                        durasi_peminjaman = int(input("Masukkan Durasi Peminjaman (dalam hari): "))
                        
                        # Menghitung tanggal pengembalian
                        tanggal_peminjaman = datetime.now().date()
                        tanggal_pengembalian = tanggal_peminjaman + timedelta(days=durasi_peminjaman)
                        
                        # Menambahkan informasi peminjaman ke dalam data peminjam
                        dataPeminjam[username]["Buku Dipinjam"].append(buku_dipinjam["Judul Buku"])
                        dataPeminjam[username]["Tanggal Peminjaman"].append(str(tanggal_peminjaman))
                        dataPeminjam[username]["Tanggal Pengembalian"].append(str(tanggal_pengembalian))
                        dataPeminjam[username]["Nama Peminjam"] = nama_peminjam

                        simpan_data_peminjam(dataPeminjam)
                        print(f"Buku '{buku_dipinjam['Judul Buku']}' berhasil dipinjam!")
                        
                        # Membuat invoice
                        print("\n--- INVOICE ---")
                        print(f"Nama Peminjam: {nama_peminjam}")
                        print(f"Judul Buku: {buku_dipinjam['Judul Buku']}")
                        print(f"Harga Sewa: Rp {harga_sewa}")
                        print(f"Tanggal Peminjaman: {tanggal_peminjaman}")
                        print(f"Tanggal Pengembalian: {tanggal_pengembalian}")
                    else:
                        print("Saldo Anda tidak cukup untuk meminjam buku ini.")
                else:
                    print("Buku Tidak Ada!")
            except ValueError:
                print("Input tidak valid.")
        
        elif pilihan == "4":
            clear_console()
            print("Anda telah logout.")
            login()
        
        else:
            print("Pilihan tidak tersedia.")

# Fungsi Admin (admin_menu) untuk Admin
def admin_menu():
    daftarBuku = BacaData()
    dataPeminjam = baca_data_peminjam()
    
    while True:
        print("+=================================+")
        print("| [1]. Tambah Buku                |")
        print("| [2]. Lihat Daftar Buku          |")
        print("| [3]. Update Buku                |")
        print("| [4]. Hapus Buku                 |")
        print("| [5]. Lihat Daftar Peminjam Buku |")
        print("| [6]. Top-Up Saldo               |")
        print("| [7]. Keluar                     |")
        print("+=================================+")
        pilihan = input("Masukkan Pilihan: ")

        if pilihan == "1":
            BukuBaru = input("Masukkan Judul Buku: ").strip()
            Penerbit = input("Masukkan Penerbit: ").strip()
            try:
                Tahun_RilisBuku = int(input("Masukkan Tahun Rilis Buku: "))
            except ValueError:
                print("Tahun Rilis harus berupa angka.")
                continue
            try:
                Harga_Sewa = float(input("Masukkan Harga Sewa Buku: "))
            except ValueError:
                print("Harga Sewa harus berupa angka.")
                continue

            daftarBuku.append({
                "Judul Buku": BukuBaru,
                "Penerbit": Penerbit,
                "Tahun Rilis": Tahun_RilisBuku,
                "Harga Sewa": Harga_Sewa
            })
            saveJson(daftarBuku)
            print(f"Buku '{BukuBaru}' berhasil ditambahkan!")

        elif pilihan == "2":
            tampilkanBuku(daftarBuku)

        elif pilihan == "3":
            tampilkanBuku(daftarBuku)
            nomorBuku = int(input("Masukkan Nomor Buku: "))
            if 0 < nomorBuku <= len(daftarBuku):
                index = nomorBuku - 1
                BukuBaru = input("Masukkan Judul Buku: ")
                Penerbit = input("Masukkan Penerbit: ")
                Tahun_RilisBuku = int(input("Masukkan Tahun Rilis Buku: "))
                Harga_Sewa = float(input("Masukkan Harga Sewa Buku: "))

                daftarBuku[index] = {
                    "Judul Buku": BukuBaru,
                    "Penerbit": Penerbit,
                    "Tahun Rilis": Tahun_RilisBuku,
                    "Harga Sewa": Harga_Sewa
                }
                saveJson(daftarBuku)
                print("Data buku berhasil diperbarui!")

        elif pilihan == "4":
            tampilkanBuku(daftarBuku)
            nomorBuku = int(input("Masukkan Nomor Buku: "))
            if 0 < nomorBuku <= len(daftarBuku):
                daftarBuku.pop(nomorBuku - 1)
                saveJson(daftarBuku)
                print("Buku berhasil dihapus!")

        elif pilihan == "5":
            tampilkanPeminjam(dataPeminjam)

        elif pilihan == "6":
            username = input("Masukkan Username yang akan di-top-up: ")
            if username in dataPeminjam:
                topup_amount = float(input("Masukkan Jumlah Top-Up: Rp "))
                dataPeminjam[username]["saldo"] += topup_amount
                simpan_data_peminjam(dataPeminjam)
                print(f"Saldo {username} berhasil di-top-up sebesar Rp {topup_amount}")
            else:
                print("Username tidak ditemukan.")

        elif pilihan == "7":
            print("Keluar dari menu admin.")
            break

        else:
            print("Pilihan tidak valid!")

# Fungsi utama
def main():
    login()

main()
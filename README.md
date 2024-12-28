# Authentication - My UBAYA

![Banner](https://img.shields.io/badge/Authentication-My%20UBAYA-brightgreen)

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

> **"Simplifying Your Login and Logout Process for My UBAYA"**  
> *By TheLoLNA15*

## 📚 **Deskripsi Proyek**

**Authentication - My UBAYA** adalah sebuah skrip Python sederhana yang dirancang untuk mengotomatiskan proses login dan logout di platform **My UBAYA**. Dengan menggunakan skrip ini, pengguna dapat dengan mudah masuk ke akun mereka, menjalankan sesi autentikasi, dan keluar secara otomatis setelah durasi tertentu, memastikan keamanan dan kenyamanan dalam penggunaan layanan My UBAYA.

## 🚀 **Fitur Utama**

- **Credential Input:** Memasukkan username dan password dengan input password.
- **Auto Logout Countdown:** Menunggu selama 2 menit sebelum melakukan logout otomatis dengan opsi untuk logout segera melalui `Ctrl+C`.
- **Automatically Generate Cookies:** Menampilkan cookie secara otomatis apabila kresdensial valid.

## 🛠️ **Instalasi**

### 1. **Clone Repository**

```bash
git clone https://github.com/thelolna15/myubaya-auth.git
cd myubaya-auth
```

### 2. **Instalasi Dependensi**

Pastikan memiliki **Python 3.8** atau yang lebih baru terinstal di sistem. Kemudian, instal dependensi yang diperlukan menggunakan `pip`:

```bash
pip install -r requirements.txt
```

*Jika belum memiliki `pip`, dapat menginstalnya [di sini](https://pip.pypa.io/en/stable/installation/).*

### 3. **Menyiapkan Environment (Opsional)**

Disarankan untuk menggunakan virtual environment untuk mengelola dependensi:

```bash
python -m venv venv
source venv/bin/activate  # Untuk Unix atau MacOS
venv\Scripts\activate     # Untuk Windows
pip install -r requirements.txt
```

## 📥 **Penggunaan**

1. **Jalankan Skrip**

   ```bash
   python app.py
   ```

2. **Masukkan Kredensial**

   - **Username:** Masukkan username saat diminta.
   - **Password:** Masukkan password. Input akan tersembunyi untuk keamanan.

3. **Proses Autentikasi**

   - Skrip akan mengakses halaman login, mengambil CSRF token, dan melakukan proses login.
   - Setelah login berhasil, skrip akan memulai countdown selama 2 menit sebelum logout otomatis.
   - Menghentikan countdown dan melakukan logout segera dengan menekan `Ctrl+C`.

4. **Logout Otomatis**

   - Setelah countdown selesai, skrip akan secara otomatis melakukan logout dari akun.

## 📝 **Catatan**

- **Keamanan:** Pastikan untuk tidak membagikan skrip ini dengan menghard code kredensial. Simpan informasi sensitif dengan aman.
- **Privasi:** Skrip ini hanya digunakan untuk autentikasi mandiri dan tidak melacak atau menyimpan informasi pribadi.

## 📜 **Lisensi**

Distribusi bebas untuk digunakan secara pribadi. Untuk informasi lebih lanjut, lihat [LICENSE](LICENSE).

---

**Terima kasih, salam hangat - TheLoLNA15** 😊

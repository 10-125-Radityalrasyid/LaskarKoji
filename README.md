# TUGAS BESAR STRATEGI ALGORITMA 
## Kelompok Laskar Koji
## Kelas RD

```bash
Anggota Kelompok:
Raditya Alrasyid Nugroho     123140125
Muhamad Rafi Ilham           123140173
Rian Rafael Sangap Tamba     123140190
```
---

# Deskripsi Program

Diamonds adalah sebuah tantangan pemrograman di mana kamu akan membuat sebuah bot untuk bertanding melawan bot milik pemain lain. Setiap peserta akan memiliki satu bot, dan misi utama bot tersebut adalah mengumpulkan diamond sebanyak mungkin. Tapi tentu saja, mengumpulkan diamond tidak semudah kedengarannya — akan ada berbagai macam rintangan yang membuat permainan ini jadi lebih menantang dan seru. Untuk bisa keluar sebagai pemenang, setiap pemain perlu merancang dan menerapkan strategi yang efektif pada bot mereka masing-masing.

Program permainan Diamonds terdiri atas:
1. Game engine, yang secara umum berisi:
   - Kode backend permainan merupakan inti dari game ini, yang menangani seluruh logika permainan serta menyediakan API untuk menghubungkan dengan tampilan depan (frontend)     dan bot dari para pemain.

2. Bot starter pack, yang secara umum berisi:
   - Program pemanggil API, digunakan untuk mengakses API yang disediakan oleh backend.
   - Program logika bot, yaitu bagian yang akan kalian kembangkan sendiri menggunakan algoritma greedy sebagai strategi untuk bot tim kalian.
   - Program utama (main) dan berbagai utilitas pendukung lainnya yang diperlukan untuk menjalankan sistem secara keseluruhan.

Repositori ini berisi implementasi strategi greedy by highest density untuk mengembangkan bot dalam permainan Diamonds. Strategi ini merupakan pendekatan greedy yang memprioritaskan diamond dengan nilai densitas tertinggi, yaitu perbandingan antara poin yang diperoleh dari sebuah diamond dengan jarak yang harus ditempuh untuk mengambilnya.

## Komponen Permainan yang dibutuhkan

### 1. Game Engine yang harus di install adalah
- Node.js (https://nodejs.org/en)
- Docker Desktop (https://www.docker.com/products/docker-desktop/)

### 2. Bot Starter Pack Requirement yang harus di install
- Python (https://www.python.org/downloads/)


---

## Set Up Untuk Menjalankan Program
1. Game Engine yang harus di install:
   - Node.js (https://nodejs.org/en)
   - Docker Desktop (https://www.docker.com/products/docker-desktop/)
   - Yarn
     ```bash
     npm install --global yarn

2. Bot Starter pack yang harus di install:
   - Python (https://www.python.org/downloads/)

## Cara menjalankan program

1. **Jalankan game engine** dengan cara mengunduh starter pack game engine dalam bentuk file `.zip` yang terdapat pada tautan berikut:  
   [Link Starter Pack Game Engine](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)  
   Setelah melakukan instalasi, lakukan ekstraksi file `.zip` tersebut, lalu masuk ke root folder dari hasil ekstraksi file tersebut kemudian jalankan terminal.

   A. **Masuk ke direktori root dari game engine:**
   ```bash
   cd tubes1-IF2110-game-engine-1.1.0
   ```

   B. Instal dependencies menggunakan yarn:
   ```bash
   yarn
   ```
   C. Lakukan setup environment variable
   ```bash
   ./scripts/copy-env.bat
   ```

   D. Lakukan setup local database dengan membuka aplikasi docker desktop terlebih dahulu lalu jalankan perintah berikut di terminal
   ```bash
   docker compose up -d database
   ```

   E. Kemudian jalankan script berikut. Untuk Windows
   ```bash
   ./scripts/setup-db-prisma.bat
   ```
   F. Jalankan perintah berikut untuk melakukan build frontend dari game engine
   ```bash
   npm run build
   ```
   G. Jalankan perintah dibawah untuk memulai game engine
   ```bash
   npm run start
   ```
   H.Jika berhasil, tampilan terminal akan terlihat seperti gambar di bawah ini
   ![Deskripsi Gambar](./assets/nama-gambar.png)



---

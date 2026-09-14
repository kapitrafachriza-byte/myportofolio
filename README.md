Nama : Kapitra Fachriza Utomo
NPM  : 2506623231
Kelas: E

Link Deploy: http://kapitra-fachriza-myportofolio.pbp.cs.ui.ac.id/

## Tugas 1: Pertanyaan & Jawaban

### 1. Penggunaan Elemen Semantik HTML5

Saya sengaja memanfaatkan elemen semantik agar struktur kode lebih teratur dan ramah aksesibilitas:

* **`<nav>`** — Membungkus bilah menu utama (Profile, Skills, dll.) agar langsung dikenali oleh browser dan *screen reader*.
* **`<main>`** — Menandai area inti konten tiap tab, membedakannya dari elemen pendukung.
* **`<aside>`** — Dipakai untuk panel kartu profil di sisi kiri karena sifatnya melengkapi konten utama di sebelah kanan.
* **`<section>`** — Mengelompokkan rak foto (*shelf-wall*) dan kartu keahlian sebagai satu kesatuan tematik.

Penggunaan tag ini membuat struktur halaman jauh lebih mudah dibaca dibanding sekadar memakai `<div>` untuk semuanya, sekaligus meningkatkan keramahan SEO dan aksesibilitas (*a11y*).

### 2. Tantangan Responsivitas CSS

Tantangan terbesarnya ada pada adaptasi layout saat berpindah dari layar desktop ke ponsel:

* **Grid 2 kolom yang bertabrakan** — Rasio `3.5fr 6.5fr` pas di desktop, tetapi sempit di layar $\le$1000px. Solusinya, saya ubah menjadi satu kolom bertumpuk (`grid-template-columns: 1fr`) menggunakan media query.
* **Foto polaroid meluber** — Dimensi foto awalnya berukuran tetap (210×275px). Pada breakpoint ponsel ($\le$640px), ukurannya saya perkecil menjadi 70×95px agar tidak keluar dari container.
* **Menu terlalu panjang** — Teks label navigasi disembunyikan (`display: none`) di layar kecil, menyisakan ikonnya saja agar tetap ringkas dan fungsional.

Prinsip prioritas saya: informasi teks esensial (nama, bio, data diri) tetap harus terbaca jelas, elemen visual dekoratif dikompromikan ukurannya, dan kontrol navigasi tetap mudah disentuh.

### 3. Batasan Static Web & Rencana Fungsionalitas Dinamis

Membangun portofolio murni HTML/CSS memperlihatkan beberapa keterbatasan:

* **Navigasi masih menggunakan trik CSS** — Perpindahan halaman mengandalkan trik *hidden radio button* dan `transform: translateX()`. Cara ini kurang fleksibel jika halaman bertambah dan tidak mendukung tombol *back/forward* browser.
* **Konten serba *hardcoded*** — Setiap ada pembaruan skill atau proyek baru, saya harus mengubah kode di file `index.html` secara manual.
* **Tidak ada interaksi nyata** — Formulir kontak belum bisa benar-benar memproses atau mengirim pesan.

Rencana integrasi dengan Django ke depannya:

1. **Form kontak aktif** — Memanfaatkan views dan models Django untuk menyimpan pesan pengunjung ke database serta mengirim notifikasi email.
2. **Dashboard Django Admin** — Mempermudah pembaruan data proyek, portofolio, dan keahlian langsung melalui panel admin tanpa perlu menyentuh kode.
3. **Sistem URL routing** — Menyediakan path halaman yang rapi (seperti `/skills/` atau `/projects/`) sehingga mendukung riwayat navigasi browser dan *deep linking*.

---

## Tugas 2: Implementasi MVT — Halaman Skills
1. **Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.**

   Ketika pengguna mengakses URL baru (misalnya `http://localhost:8000/skills/`), terjadi siklus *request-response* berbasis pola MVT:
   - **`urls.py` Proyek (`portofolio/urls.py`)**: Bertindak sebagai gerbang utama (*router* level proyek) yang menangkap permintaan masuk dan meneruskannya ke router level aplikasi via `include('main.urls')`.
   - **`urls.py` Aplikasi (`main/urls.py`)**: Memetakan path spesifik (`skills/`) ke fungsi view yang dituju (`show_skills`).
   - **View (`main/views.py`)**: Berperan sebagai pengendali logika bisnis (*controller*). View `show_skills` berinteraksi dengan model untuk mengambil data, memproses atau mengelompokkannya, lalu menyusunnya ke dalam dictionary `context`.
   - **Model (`main/models.py`)**: Merepresentasikan struktur data tabel database lewat Django ORM. Model mengeksekusi query ke database (misal `Skill.objects.filter(...)`) dan mengembalikan data dalam bentuk objek Python ke view.
   - **Template (`templates/skills.html`)**: Bertindak sebagai lapisan presentasi. Template menerima `context` dan menggunakan sintaks Django Template Language (DTL) seperti `{% for %}`, `{% if %}`, dan `{% empty %}` untuk menyisipkan data dinamis ke dalam markup HTML.
   - **Response ke Browser**: Django mengompilasi template tersebut menjadi dokumen HTML utuh dan mengembalikannya ke browser sebagai HTTP Response (status 200 OK) untuk ditampilkan ke pengguna.

2. **Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**

   Menyimpan data pada Model menerapkan prinsip *Separation of Concerns* (pemisahan tanggung jawab antara data dan tampilan):
   - **Kemudahan Pemeliharaan (*Maintainability*)**: Jika ada penambahan, pembaruan, atau penghapusan data (misal menambah skill baru), kita cukup mengubah data di database atau lewat Django Admin tanpa menyentuh berkas HTML. Hal ini mencegah risiko kesalahan sintaks markup atau rusaknya styling CSS saat memperbarui informasi.
   - **Konsistensi (*Single Source of Truth*)**: Jika data yang sama perlu ditampilkan di berbagai tempat (misalnya preview ringkas di beranda dan daftar lengkap di halaman khusus), semuanya mengambil dari satu sumber data yang sama sehingga tidak terjadi inkonsistensi.
   - **Skalabilitas & Pengembangan Lanjutan (*Extensibility*)**: Data di model dapat dengan mudah di-*filter*, diurutkan (*sorting*), dicari (*search*), atau bahkan diekspos menjadi REST API (JSON) tanpa mengubah template. Hal ini juga memungkinkan aplikasi dikembangkan menjadi dinamis dengan fitur input/formulir dari pengguna.

3. **Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**

   - **`python manage.py makemigrations`**: Membaca perubahan struktur skema data pada `models.py` dan membuat berkas migrasi baru (skrip Python di folder `migrations/`) sebagai cetak biru (*blueprint*) instruksi perubahan. Perintah ini **belum** mengubah atau membuat tabel di database nyata.
   - **`python manage.py migrate`**: Membaca berkas-berkas migrasi yang belum diaplikasikan, lalu mengeksekusinya ke database sesungguhnya (menerjemahkan instruksi Python menjadi perintah SQL seperti `CREATE TABLE` atau `ALTER TABLE`) sehingga struktur database benar-benar terbuat atau diperbarui.

   **Contoh Perubahan Model yang Mengharuskan Keduanya:**
   - **Membuat Model Baru**: Saat membuat `class Skill(models.Model)` di `main/models.py`, kita menjalankan `makemigrations` untuk membuat berkas `0002_skill.py`, kemudian menjalankan `migrate` agar tabel `main_skill` terbentuk di `db.sqlite3`.
   - **Menambahkan Field Baru**: Jika nanti kita menambahkan atribut baru pada model yang sudah ada, misalnya `level = models.CharField(max_length=20, default='Beginner')` pada `Skill`, kita wajib menjalankan `makemigrations` untuk mendeteksi penambahan field tersebut, lalu `migrate` agar kolom baru ditambahkan ke tabel database.



### Setup & Menjalankan Proyek

```bash
# Clone & masuk ke direktori
git clone https://github.com/kapitrafachriza-byte/myportofolio.git
cd myportofolio

# Buat virtual environment & install dependencies
python -m venv env
env\Scripts\activate        # Windows
pip install -r requirements.txt

# Jalankan migrasi & server
python manage.py migrate
python manage.py runserver
```

Buka `http://localhost:8000/` untuk halaman Profile, `http://localhost:8000/skills/` untuk Skills, dan `http://localhost:8000/experience/` untuk Experience.

### Menjalankan Test

```bash
python manage.py test main --verbosity=2
```

### Apa yang Dikerjakan

Pada tugas ini, saya menerapkan pola **Model-View-Template (MVT)** untuk bagian **Skills** portofolio:

1. **Model `Skill`** — Field: `name` (CharField), `category` (CharField + choices), `dot_color` (CharField + choices), `display_order` (PositiveIntegerField). Primary key UUID.
2. **View `show_skills`** — Mengelompokkan skill berdasarkan kategori (Programming, Info Systems, Soft Skills) dan mengirimnya ke template.
3. **Template `skills.html`** — Menampilkan kartu skill menggunakan `{% for %}` loop dengan `{% empty %}` fallback.
4. **URL `/skills/`** — Named route `main:show_skills` di `main/urls.py`.
5. **Navbar** — Semua halaman menggunakan `{% url %}` tag, konsisten di `index.html`, `experience.html`, dan `skills.html`.
6. **Refactor `index.html`** — Menghapus mekanisme CSS radio-button tab sliding, karena Skills kini punya halaman terpisah.
7. **Unit test** — 9 test case (6 untuk Experience, 3 untuk Skills).

### AI Disclosure

Saya menggunakan **Google Antigravity (Gemini-based AI coding assistant)** untuk membantu pengerjaan tugas ini. Berikut detail penggunaannya:

**Tools yang dipakai:**
- Google Antigravity (Claude model) sebagai pair-programming assistant di IDE

**Strategi prompting:**
- Meminta AI memecah pekerjaan menjadi 3 tahap (Model → View/Template → Test/README) agar commit history bertahap
- Memberikan constraint jelas, dengan tidak melalui Prompt chat tetapi dengan file markdown lengkap berisi briefing dan konteks*

**Bagian yang dibantu AI:**

- Refactoring `index.html` untuk menghapus radio-button tab mechanism
- Penulisan 9 unit test di `tests.py`
- Update `README.md` dan `.gitignore`

**Bagian yang saya kerjakan sendiri:**
- Keputusan desain untuk memilih Skills sebagai model baru (bukan Projects/Education)
- Keputusan untuk menggunakan pendekatan halaman terpisah (bukan tab dalam satu halaman)
- Review dan verifikasi semua kode yang dihasilkan AI
- Menjalankan dan memverifikasi test secara manual
- Penulisan model `Skill` di `models.py` (struktur field dan choices)
- Pembuatan view `show_skills` dengan logic pengelompokan kategori
- Pembuatan template `skills.html` dengan DTL loop

---

## Tutorial 3: Implementasi Skeleton, Form & Data Delivery

Pada tutorial ini, saya mempelajari dan mengimplementasikan konsep utama pengembangan web modern dengan Django:

1. **Pewarisan Template (Template Inheritance / Skeleton)**:
   - Membuat template induk `templates/base.html` sebagai kerangka utama terpusat untuk elemen berulang (navbar top bar, link font, CSS, dan bingkai Retro CRT).
   - Menghubungkan seluruh template anak (`index.html`, `skills.html`, `experience.html`) menggunakan `{% extends 'base.html' %}` dan `{% block content %}`.

2. **Implementasi Form dengan `ModelForm`**:
   - Membuat `ExperienceForm` di `main/forms.py` untuk menerima input data pengalaman (`title`, `description`, `category`).
   - Membuat view `create_experience` dan template `create_experience.html` yang dilengkapi token keamanan `{% csrf_token %}`.
   - Menambahkan tombol akses form pada halaman Experience.

3. **Data Delivery dengan JSON & Fitur Search**:
   - Membuat endpoint `get_experience_json` di rute `/experience/json/` yang mengembalikan data serialisasi JSON dari Django ORM.
   - Menambahkan dukungan parameter pencarian berbasis query string (`?title=...`) dengan filter `title__icontains`.
   - Mengubah view `show_experience` agar mengonsumsi data dari endpoint JSON secara dinamis.
   - Menambahkan formulir pencarian (*search bar*) dan tampilan thumbnail gambar pada kartu pengalaman.

4. **Pengujian (Unit Testing)**:
   - Menambahkan test case untuk verifikasi akses form `create_experience`, pengiriman POST form, endpoint JSON `/experience/json/`, serta fungsionalitas filter pencarian (total 14 test cases lulus).
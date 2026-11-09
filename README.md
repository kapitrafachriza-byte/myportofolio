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

---

### Tugas 3

1. **Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

   - **Alasan menggunakan `ModelForm` dibandingkan form HTML manual:**
     - **Prinsip DRY (*Don't Repeat Yourself*) & Efisiensi**: `ModelForm` secara otomatis memetakan field-field dari model database (seperti `CharField`, `TextField`, `URLField`, `DateTimeField`, dll.) ke dalam elemen input formulir HTML yang tepat beserta tipe dan labelnya. Kita tidak perlu menulis tag `<input>`, `<textarea>`, atau `<select>` secara manual satu per satu.
     - **Validasi Otomatis & Terintegrasi**: `ModelForm` otomatis menerapkan aturan validasi berdasarkan definisi field di model (misalnya batasan `max_length`, `blank`/`null`, validitas format URL, tanggal, dan pilihan `choices`). Validasi dapat dipicu dengan method `form.is_valid()`, dan jika terjadi kesalahan, Django otomatis menghasilkan pesan error yang spesifik untuk masing-masing field.
     - **Kemudahan Penyimpanan & Pembaruan Data (`form.save()`)**: Pada form manual, kita harus mengekstrak data dari `request.POST` satu per satu, mengonversi tipe data, melakukan sanitasi, lalu membuat atau memperbarui instance model secara manual. Dengan `ModelForm`, data yang telah tervalidasi dapat langsung disimpan ke database hanya dengan memanggil `form.save()`. Untuk operasi *edit/update*, kita cukup menyertakan argumen `instance=objek`.
     - **Pembersihan & Keamanan Input**: `ModelForm` secara bawaan membersihkan data input (*cleaned data*), mencegah masukan yang tidak sesuai dan meminimalkan risiko manipulasi data yang berbahaya.

   - **Alasan kewajiban menambahkan `{% csrf_token %}`:**
     - Tag `{% csrf_token %}` menyisipkan input tersembunyi (*hidden input*) berisi token unik terenkripsi untuk melindungi aplikasi dari serangan **Cross-Site Request Forgery (CSRF)**.
     - Serangan CSRF adalah jenis eksploitasi di mana situs jahat atau pihak ketiga mengirimkan permintaan berbahaya (seperti POST, PUT, atau DELETE) ke aplikasi web atas nama pengguna yang sedang terautentikasi tanpa izin atau sepengetahuan mereka.
     - Django menyertakan middleware keamanan `CsrfViewMiddleware` yang secara otomatis memvalidasi apakah setiap request yang memodifikasi data (seperti POST) menyertakan token CSRF yang cocok dengan sesi pengguna. Jika token tidak disertakan atau tidak valid, Django akan langsung menolak permintaan dengan status HTTP **403 Forbidden**.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**

   - **Ukuran Lebih Ringkas & Hemat Bandwidth (*Lightweight*)**: JSON memiliki struktur yang ringkas tanpa tag penutup yang berulang seperti pada XML (`<title>Experience</title>` vs `"title": "Experience"`). Hal ini membuat ukuran payload data JSON jauh lebih kecil, sehingga proses transmisi data melalui jaringan internet berlangsung lebih cepat dan efisien.
   - **Dukungan Bawaan (*Native*) di JavaScript & Browser**: JSON (*JavaScript Object Notation*) adalah format turunan langsung dari JavaScript. Browser dan runtime JavaScript dapat mengurai (*parse*) dan memproduksi (*stringify*) JSON secara instan dan sangat cepat menggunakan fungsi bawaan `JSON.parse()` dan `JSON.stringify()`, tanpa memerlukan parser eksternal atau traversal DOM yang kompleks seperti pada XML (`DOMParser`, XPath).
   - **Pemetaan Struktur Data Alami**: JSON langsung mendukung tipe data primitif dan struktur data standar pemrograman modern, seperti objek (*key-value pair* / dictionary), array (*list*), string, number, boolean, dan null. Sebaliknya, XML memperlakukan semua data sebagai teks dan membutuhkan skema pendukung (seperti XSD) untuk mendefinisikan tipe data.
   - **Keterbacaan yang Lebih Baik (*Human-Readable*)**: Struktur JSON yang berbasis pasangan kunci-nilai dan kurung siku/kurawal jauh lebih mudah dibaca, dipahami, dan ditulis oleh developer dibandingkan sintaks XML yang sering kali terlalu panjang (*verbose*).
   - **Standar *De Facto* RESTful API & Framework Modern**: Seluruh ekosistem web modern (seperti React, Vue, Angular, mobile app, hingga arsitektur microservices) telah mengadopsi JSON sebagai standar utama untuk pertukaran data melalui REST API.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?**

   - **Alur pengembalian data dalam bentuk JSON:**
     1. **Permintaan Masuk (*HTTP Request*)**: Klien (browser, frontend script, atau API client) mengirimkan permintaan HTTP GET ke endpoint rute URL, misalnya `/experience/json/` (dapat disertai parameter query pencarian seperti `?title=...`).
     2. **Routing URL**: `urls.py` mencocokkan pola path dan meneruskan permintaan ke fungsi view yang sesuai (`get_experience_json`).
     3. **Pengambilan Data dari Database**: Fungsi view berinteraksi dengan database melalui Django ORM (misalnya `Experience.objects.all()` atau `filter(title__icontains=...)`), menghasilkan `QuerySet` yang berisi sekumpulan instance objek model Python.
     4. **Proses Serialisasi (*Serialization*)**: Objek `QuerySet` tersebut diproses oleh serialiser bawaan Django menggunakan `serializers.serialize('json', experiences)`, yang menerjemahkan objek-objek model Python tersebut menjadi string terformat JSON.
     5. **Penyusunan HTTP Response**: String data JSON tersebut dibungkus ke dalam objek `HttpResponse(experience_data, content_type="application/json")` (atau `JsonResponse`).
     6. **Pengiriman Respons (*HTTP Response*)**: Django mengirimkan respons HTTP (dengan status 200 OK dan header `Content-Type: application/json`) kembali ke klien. Klien kemudian dapat mendeserialisasi data JSON tersebut untuk ditampilkan pada antarmuka web.

   - **Mengapa kita perlu melakukan proses *serialization*:**
     - Objek model Django (`QuerySet` atau instance kelas model) adalah **objek Python internal yang kompleks dan hidup di dalam memori (*in-memory Python objects*)**. Objek ini memiliki method, metadata internal, serta referensi relasi yang tidak dapat langsung dipahami atau ditransmisikan melalui protokol HTTP ke klien eksternal.
     - Protokol HTTP dan format JSON hanya dapat memproses dan mentransfer data berbasis teks dengan struktur data universal (string, number, boolean, array, object).
     - Oleh karena itu, **serialisasi (*serialization*)** wajib dilakukan untuk mengonversi objek kompleks Python/Django ORM tersebut menjadi format representasi data standar (string JSON) yang netral-platform, sehingga dapat dikirimkan melalui jaringan dan mudah diolah kembali (*deserialized*) oleh klien apa pun (baik JavaScript di browser, aplikasi mobile, maupun sistem lain).



---

## Tugas 4: Autentikasi, Cookie, & Otorisasi

Pada tugas ini, sistem autentikasi dan otorisasi multi-peran diterapkan pada modul **Experience**:
1. **Autentikasi Pengguna**: Fitur Registrasi, Login, dan Logout menggunakan form bawaan Django.
2. **Sesi & Cookie**: Menyimpan dan menampilkan waktu login terakhir pengguna melalui cookie `last_login`.
3. **Sistem Peran & Otorisasi 4-Level**:
   - **Pengunjung tanpa login**: Hanya dapat membaca data portofolio.
   - **Pengguna biasa**: Dapat membaca data dan memberi/membatalkan star pada pengalaman.
   - **Editor (Grup 'Editor')**: Memiliki hak pengguna biasa dan dapat mengubah (*edit*) data pengalaman, namun tidak dapat membuat atau menghapus.
   - **Pemilik Portofolio (Superuser)**: Memiliki hak penuh (membuat, mengubah, dan menghapus pengalaman).
4. **Interaktivitas Star**: Relasi `ManyToManyField` ke `User` pada model `Experience` dengan tombol toggle star.

---

## Tugas 5: Web Interactivity with JavaScript

### Pertanyaan Reflektif

1. **Jelaskan apa itu *debouncing* dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   - **Pengertian Debouncing**:
     *Debouncing* adalah teknik optimasi pemrograman yang menunda pemanggilan suatu fungsi hingga pengguna berhenti melakukan aksi selama periode waktu tertentu (misalnya 300 milidetik). Jika aksi baru terjadi sebelum batas waktu berakhir, penghitung waktu (*timer*) sebelumnya akan dibatalkan (`clearTimeout`) dan dihitung ulang dari awal.
   - **Pentingnya Debouncing pada Pencarian AJAX**:
     - **Mencegah Banjir Permintaan HTTP (*Request Flooding*)**: Tanpa *debouncing*, setiap penekanan tombol (*keystroke*) pada kolom pencarian akan langsung memicu `fetch()` ke server. Jika pengguna mengetik kata `"Software"` (8 karakter), browser akan mengirimkan 8 permintaan HTTP berturut-turut. Dengan *debouncing*, permintaan hanya dikirim 1 kali setelah pengguna selesai mengetik seluruh kata.
     - **Mengurangi Beban Server & Basis Data**: Setiap permintaan pencarian memicu eksekusi query ke database (`filter(title__icontains=...)`). Mengurangi jumlah request secara drastis menghemat kapasitas pemrosesan CPU server dan I/O database.
     - **Menghindari Kondisi Perlombaan (*Race Condition*)**: Karena kecepatan respons jaringan bervariasi, respons dari huruf pertama (`"S"`) bisa saja tiba lebih lambat dibandingkan respons kata lengkap (`"Software"`). Tanpa debouncing, hasil pencarian di layar bisa tertimpa oleh data usang (*stale data*).

2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**

   - **Fungsi `await` pada `fetch()`**:
     Operasi `fetch()` berjalan secara asinkron di latar belakang jaringan dan mengembalikan sebuah objek `Promise` (yang merepresentasikan operasi yang sedang berjalan). Kata kunci `await` berfungsi untuk **menjeda eksekusi baris kode berikutnya di dalam fungsi `async`** sampai `Promise` tersebut selesai (*resolved*) dan menghasilkan objek `Response` yang sesungguhnya. Hal serupa juga berlaku saat membaca *body stream* dengan `await response.json()`.
   - **Apa yang terjadi jika kita TIDAK menggunakan `await`?**:
     - Variabel yang menampung hasil `fetch()` tidak akan berisi objek `Response`, melainkan objek `Promise { <pending> }`.
     - Ketika kode langsung mencoba mengakses properti atau method respons seperti `response.ok` atau `response.json()`, program akan mengalami galat (*runtime error*), seperti `response.json is not a function` atau mengembalikan Promise lain yang belum selesai.
     - Akibatnya, data JSON belum tersedia saat antarmuka hendak me-render kartu ke DOM, sehingga data tidak tampil atau program terhenti karena error.

3. **Jelaskan apa itu serangan XSS (*Cross-Site Scripting*) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**

   - **Pengertian Serangan XSS (*Cross-Site Scripting*)**:
     XSS adalah kerentanan keamanan di mana penyerang (*attacker*) berhasil menyisipkan skrip berbahaya (biasanya JavaScript) ke dalam konten aplikasi web. Ketika pengguna lain membuka halaman yang memuat data tersebut, skrip berbahaya akan dieksekusi secara otomatis oleh browser pengguna lain tersebut. Dampaknya meliputi pencurian cookie sesi / token autentikasi, pembajakan akun (*account hijacking*), manipulasi tampilan halaman (*defacement*), atau pengalihan pengguna ke situs berbahaya (*phishing*).
   - **Mengapa Data via AJAX/JavaScript Lebih Rentan Dibandingkan Template Django?**:
     - **Perlindungan Bawaan Template Django (*Auto-Escaping*)**: Django Template Language (DTL) secara bawaan memiliki fitur **Automatic HTML Escaping**. Setiap variabel yang dicetak dengan sintaks `{{ variabel }}` akan otomatis disanitasi: karakter khusus seperti `<`, `>`, `&`, `"`, dan `'` diubah menjadi entitas HTML (`&lt;`, `&gt;`, dll.). Tag `<script>` atau `<img src="x" onerror="...">` akan ditampilkan sebagai teks biasa tanpa dieksekusi oleh browser, kecuali jika developer secara eksplisit menggunakan filter `|safe`.
     - **Ketiadaan Auto-Escaping pada DOM Manipulation JavaScript**: Ketika data diambil melalui AJAX dalam bentuk string JSON murni dan disisipkan langsung ke antarmuka web menggunakan properti seperti `element.innerHTML = ...` atau template literals (`` `${item.title}` ``), JavaScript **tidak memiliki mekanisme sanitasi otomatis**. Browser akan langsung mem-parsing string tersebut sebagai elemen HTML. Jika nilai `title` berisi `<img src="x" onerror="alert('XSS!')">`, event handler `onerror` akan langsung dieksekusi oleh browser saat render terjadi.
     - **Lapisan Pertahanan yang Diterapkan**:
       1. **Client-side Escaping**: Membungkus setiap nilai teks dari JSON dengan fungsi `escapeHtml()` sebelum dirangkai ke dalam `innerHTML`, atau menggunakan properti `textContent` yang tidak pernah mengeksekusi tag HTML.
       2. **Server-side Sanitization**: Menggunakan fungsi `strip_tags()` pada method `clean_<field>` di `ModelForm` untuk membuang tag HTML berbahaya sejak data masuk ke server.

---

### AI Disclosure (Tugas 5)

Saya menggunakan **Google Antigravity (Gemini 3.8 Flash HIGH dan Opus 5.5)** sebagai asisten *pair-programming*.

**Tools & Fitur yang Digunakan:**
- Antigravity Coding Assistant untuk pembuatan boilerplate kode asinkron, modularisasi utilitas `toast.js`, dan penulisan test cases.

**Bagian yang Dibantu AI (Gemini 3.8):**
- Penyusunan template modal form dan styling dialog CRT.
- Implementasi fungsi `getCookie()` dan `escapeHtml()` pada berkas `static/js/toast.js`.
- Penulisan unit tests tambahan di `main/tests.py` untuk menguji sanitasi XSS, endpoint AJAX POST, respons manual JSON, dan toggle star AJAX.

**Bagian yang Dibantu AI (Opus 5.5)**:
- Audit test dalam kode yang sudah ada.

**Bagian yang Saya Kerjakan / Verifikasi Sendiri:**
- Analisis kesesuaian arsitektur sistem otorisasi multi-peran (Pengunjung, Pengguna Biasa, Editor, Superuser) pada endpoint AJAX.
- Konseptualisasi integrasi AJAX Star Toggle tanpa reload halaman.
- Peninjauan, eksekusi, dan verifikasi seluruh 36 unit tests di lingkungan lokal.
- Penyusunan jawaban reflektif mendalam mengenai debouncing, asinkronitas JavaScript, dan keamanan XSS.


---

## Tugas 6: Django REST Framework Implementation

### Pertanyaan Reflektif

### Tugas 6
1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan `PUT` dan `PATCH` beserta contoh kapan masing-masing sebaiknya digunakan!**

   - **Pengertian REST dan Mengapa Mengembalikan JSON Saja Belum Cukup**:
     - **REST (Representational State Transfer)** adalah gaya arsitektur perangkat lunak yang diperkenalkan oleh Roy Fielding (2000) untuk memandu perancangan sistem terdistribusi, khususnya World Wide Web. REST mengedepankan prinsip *statelessness*, *client-server separation*, *cacheability*, *layered system*, dan *uniform interface*.
     - Sebuah API yang semata-mata mengembalikan data dalam format JSON **belum tentu dapat disebut RESTful**. Sebagai contoh, sebuah endpoint RPC seperti `POST /doAction/` yang selalu mengembalikan status HTTP `200 OK` dengan isi payload `{ "status": "error", "message": "not found" }` bukanlah RESTful. Untuk memenuhi kriteria RESTful, API harus memenuhi prinsip arsitektural berikut:
       1. **Resource-Oriented URI**: Mengidentifikasi sumber daya sebagai entitas kata benda (noun-based), seperti `/api/v1/experiences/`, bukan kata kerja tindakan (verb-based) seperti `/getExperiences` atau `/deleteExperience`.
       2. **Semantik HTTP Verbs yang Tepat**: Menggunakan metode HTTP standar sesuai fungsinya: `GET` untuk membaca data tanpa efek samping (*safe & idempotent*), `POST` untuk membuat resource baru, `PUT` untuk penggantian resource secara penuh, `PATCH` untuk pembaruan sebagian, dan `DELETE` untuk menghapus resource.
       3. **Kode Status HTTP Standar**: Mengembalikan kode status HTTP yang mencerminkan hasil eksekusi sebenarnya (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed`).
       4. **Stateless Communication**: Setiap permintaan HTTP harus membawa seluruh informasi dan konteks yang dibutuhkan server untuk memprosesnya, tanpa bergantung pada state tersembunyi yang disimpan di server antar-request.

   - **Perbedaan `PUT` dan `PATCH` Beserta Contoh Penggunaannya**:
     - **`PUT` (Full Replacement / Penggantian Utuh)**:
       - Memperbarui atau mengganti **seluruh** representasi sumber daya target dengan representasi baru yang dikirimkan oleh klien. Jika ada field yang tidak disertakan dalam payload permintaan, field tersebut akan diisi dengan nilai default atau dihapus/dikosongkan (*null*).
       - Bersifat **idempoten** (*idempotent*): mengeksekusi request `PUT` yang sama satu kali atau berkali-kali akan menghasilkan state data akhir yang persis sama pada server.
       - *Contoh Penggunaan*: Ketika pengguna mengisi formulir edit lengkap di mana seluruh kolom (`title`, `category`, `description`, `thumbnail`, `ended_at`) dikirim secara menyeluruh dari antarmuka web untuk menggantikan data pengalaman yang lama.
     - **`PATCH` (Partial Modification / Pembaruan Parsial)**:
       - Hanya memperbarui **field-field tertentu** yang secara eksplisit dicantumkan dalam payload permintaan, sementara field-field lain yang tidak disertakan tetap mempertahankan nilai lamanya tanpa perubahan.
       - *Contoh Penggunaan*: Fitur pengeditan cepat in-place atau toggle status, misalnya klien hanya mengirim `{"title": "Senior Software Engineer"}` untuk mengubah judul pengalaman, tanpa perlu menyertakan kembali nilai `description` atau `thumbnail`.

2. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05?**

   - **Peran Serializer pada DRF**:
     - **Serialisasi (*Serialization*)**: Mengonversi objek kompleks internal Python/Django (seperti instance model atau `QuerySet`) menjadi tipe data Python primitif (dictionary, list, string) yang siap diterjemahkan ke format transmisi standar seperti JSON atau XML.
     - **Deserialisasi & Validasi (*Deserialization & Validation*)**: Mengurai payload JSON yang masuk dari klien ke tipe data Python, memvalidasi integritas data berdasarkan aturan model dan logika bisnis kustom (`validate_<field>`, `validate`), melakukan sanitasi input (misalnya pembersihan tag HTML via `strip_tags`), serta memfasilitasi penyimpanan data kembali ke database melalui method `save()`, `create()`, atau `update()`.

   - **Keuntungan Serializer Dibandingkan Merakit Dictionary Manual dengan `JsonResponse`**:
     1. **Validasi Terpusat dan Deklaratif**: Pada `JsonResponse` manual, kita harus menulis pengecekan berulang-ulang untuk tipe data, batasan field, nilai kosong, dan keamanan input. Serializer menangani validasi ini secara deklaratif dan otomatis menghasilkan struktur pesan kesalahan yang terstandarisasi untuk setiap field.
     2. **Mendukung Alur Dua Arah (Read & Write)**: `JsonResponse` hanya berfungsi satu arah untuk menampilkan data (output). Sebaliknya, Serializer mendukung alur dua arah: mampu membaca data (*read*) sekaligus menerima, memvalidasi, dan menyimpan data baru/pembaruan (*write*) langsung ke model.
     3. **Keamanan Data & Pencegahan Kebocoran Informasi Sensitif**: Dengan menetapkan `fields` secara eksplisit dan menggunakan `read_only_fields`, serializer menjamin data sensitif (seperti hash password, token, atau email pengguna lain pada fitur star) tidak akan bocor ke klien, serta mencegah kerentanan manipulasi field internal (*mass assignment*).
     4. **Kalkulasi Field Dinamis yang Rapi**: Fitur `SerializerMethodField` memungkinkan kita menyisipkan informasi terhitung (seperti `star_count`, status `is_starred` sesuai pengguna yang sedang login, dan `category_display`) secara modular dan terisolasi dari kode view.
     5. **Integrasi Ekosistem DRF & Browsable API**: Serializer langsung terintegrasi dengan antarmuka interaktif Browsable API, pagination, filtering, serta dokumentasi skema OpenAPI/Swagger secara otomatis.

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   - **Perbedaan Autentikasi dan Otorisasi**:
     - **Autentikasi (*Authentication - "Siapa Anda?"*)**: Proses membuktikan identitas pengguna yang melakukan permintaan. DRF memeriksa kredensial (seperti cookie sesi pada `SessionAuthentication` atau token pada `TokenAuthentication`) dan mengasosiasikan permintaan tersebut dengan objek `request.user` (atau `AnonymousUser` jika gagal/tanpa login).
     - **Otorisasi (*Authorization / Permission - "Apa yang boleh Anda lakukan?"*)**: Proses menentukan apakah pengguna yang identitasnya telah terverifikasi tersebut memiliki izin atau hak akses untuk melakukan aksi tertentu pada endpoint atau objek data target (misalnya: apakah pengguna diizinkan melakukan operasi `POST`, `PATCH`, atau `DELETE`).

   - **Mengapa Hak Akses Harus Diperiksa dengan Permission Class di Server**:
     - Mengikuti prinsip dasar keamanan sistem terdistribusi: **"Never trust the client"**.
     - Menyembunyikan tombol atau tautan pada template HTML hanyalah lapisan kenyamanan antarmuka pengguna (*UI/UX convenience*), dan **bukan mekanisme keamanan sama sekali**.
     - Pengguna memiliki kendali penuh atas browser dan jaringan mereka:
       1. Pengguna dapat dengan mudah mengubah atribut DOM lewat *Inspect Element* untuk memunculkan tombol yang disembunyikan.
       2. Pengguna dapat langsung mengirimkan permintaan HTTP berbahaya menggunakan perkakas seperti cURL, Postman, Fetch API di konsol browser, atau skrip otomatis ke endpoint API (misalnya mengirim request `DELETE /api/v1/experiences/<uuid>/` atau `POST /api/v1/experiences/`).
     - Jika server tidak memiliki lapisan otorisasi berbasis `permission_classes` di level view/API, permintaan liar tersebut akan langsung dieksekusi oleh database. Memeriksa hak akses di server menjamin bahwa aturan bisnis (seperti Editor dilarang membuat atau menghapus data, dan pengunjung dilarang memodifikasi data) ditegakkan secara absolut, terlepas dari dari mana atau bagaimana permintaan tersebut dikirim.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai `SessionAuthentication`! Mengapa test yang memakai `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

   - **Mengapa Permintaan yang Mengubah Data Tetap Memerlukan Token CSRF pada `SessionAuthentication`**:
     - `SessionAuthentication` mengandalkan cookie sesi HTTP (`sessionid`) yang disimpan di browser klien.
     - Mekanisme bawaan browser secara otomatis menyertakan semua cookie yang relevan saat mengirimkan permintaan HTTP ke suatu domain, **bahkan ketika permintaan tersebut dipicu oleh situs jahat milik pihak ketiga** (misalnya melalui form submission tersembunyi atau skrip lintas-asal).
     - Tanpa perlindungan CSRF, penyerang dapat mengeksploitasi sesi aktif pengguna yang sedang login untuk memicu aksi yang tidak diinginkan (seperti menghapus atau mengubah portofolio) tanpa sepengetahuan pengguna (*Cross-Site Request Forgery*).
     - Token CSRF (yang divalidasi via header `X-CSRFToken`) bekerja sebagai bukti rahasia bersama (*shared secret*) bahwa permintaan tersebut memang berasal dari aplikasi kita yang sah, karena situs jahat pihak ketiga tidak dapat membaca atau mencuri token CSRF dari cookie domain kita akibat batasan keamanan *Same-Origin Policy* (SOP).

   - **Mengapa Test dengan `force_authenticate` Tidak Cukup**:
     - Method `force_authenticate(user=...)` pada DRF adalah helper pengujian yang dirancang khusus untuk mempermudah verifikasi otorisasi/permission view.
     - Helper ini bekerja dengan **langsung menyuntikkan objek pengguna ke dalam `request.user` secara in-memory**, sehingga **melewati (*bypass*) seluruh alur autentikasi dan middleware Django sesungguhnya**, termasuk `CsrfViewMiddleware` dan pemeriksaan token CSRF.
     - Akibatnya, pengujian yang memakai `force_authenticate` tidak pernah mengevaluasi apakah token CSRF disertakan, valid, atau bahkan dipaksakan.
     - Untuk membuktikan secara empiris bahwa perlindungan CSRF benar-benar aktif dan menolak permintaan tanpa token, kita wajib menggunakan `APIClient(enforce_csrf_checks=True)` yang dipadukan dengan `.login()`. Pendekatan ini mensimulasikan sesi browser riil, menghasilkan cookie sesi, dan memicu pemeriksaan middleware CSRF penuh di mana ketiadaan header `X-CSRFToken` akan ditolak dengan status HTTP `403 Forbidden`.

---

### AI Disclosure (Tugas 6)

Saya menggunakan **Google Antigravity (didukung model Gemini 3.8 Flash HIGH dan Opus 5.5)** sebagai asisten *pair-programming* dalam menyelesaikan Individual Assignment 6.

**Tools & Strategi Prompting:**
- Menggunakan Antigravity Coding Assistant dengan pendekatan berorientasi rencana (*plan-driven development*), membagi tugas menjadi dua tahapan bertahap (*two-stage push*):
  - **Tahap 1**: Pembangunan arsitektur backend DRF (Serializer, Permissions, API Views berbasis fungsi, URL routing, dan unit testing komprehensif 13 test cases).
  - **Tahap 2**: Integrasi frontend antarmuka pengguna berbasis SPA (Fetch API, Live Debounced Search, modal In-Place Edit dengan `PATCH`, modal Create dengan `POST`, Delete dengan `DELETE`, Star dengan `POST`, dan feedback pesan kesalahan via toast), dokumentasi reflektif, serta penyusunan AI Disclosure.

**Bagian yang Dibantu AI (Gemini 3.8):**
- Pembuatan boilerplate `ExperienceSerializer` di `main/serializers.py` dengan validasi `validate_title`, `validate_description`, dan `validate_category`.
- Implementasi API view berbasis fungsi (`experience_list`, `experience_detail`, `experience_star`) dengan dekorator `@api_view`, `@authentication_classes([SessionAuthentication])`, dan `@permission_classes`.
- Pembuatan test suite `ExperienceAPITest` di `main/tests_experience_api.py` yang mencakup 13 skenario pengujian (4 peran otorisasi, penolakan perubahan database, validasi XSS, manipulasi star, read-only computed fields, dan pengujian CSRF dengan `APIClient(enforce_csrf_checks=True)`).
- Penyesuaian skrip interaktif DOM di `templates/experience.html` untuk konsumsi endpoint `/api/v1/experiences/`, penanganan modal in-place edit, dan penanganan respons error HTTP 400/403.

**Bagian yang Dibantu AI (Opus 5.5):**
- Peninjauan struktur arsitektural permission matrix 4-peran dan verifikasi idempotensi metode `PUT`/`PATCH`.

**Keterbatasan AI & Perbaikan Manual yang Dilakukan:**
1. **Penanganan Kasus Uji Validasi HTML Strip Tags**:
   - Pada awalnya, test validasi memasukkan payload `<script>alert(1)</script>` dengan ekspektasi status 400 Bad Request. Namun, fungsi `strip_tags()` bawaan Django membuang tag `<script>` tetapi mempertahankan teks `"alert(1)"`, sehingga serializer meloloskan input karena string tidak kosong.
   - *Perbaikan Manual*: Saya memisahkan kasus uji menjadi dua skenario yang jelas: satu menguji penolakan input kosong atau yang murni hanya berisi tag HTML tanpa teks (`<script></script>`, `<b>  </b>`) yang menghasilkan 400 Bad Request, dan satu lagi menguji proses sanitasi bahwa tag HTML dibuang secara bersih (`<b>Senior Developer</b>` menjadi `"Senior Developer"`) dengan status 201 Created.
2. **Progressive Enhancement & Kompatibilitas Test Suite Lama**:
   - Untuk memastikan seluruh 36 test lama di `main/tests.py` tetap lulus (khususnya test yang memeriksa keberadaan URL edit dan ketidakhadiran URL delete pada template untuk Editor), elemen aksi pada kartu dipertahankan sebagai tag tautan `<a>` dengan atribut fallback `href` yang sesuai, yang dicegat secara elegan oleh JavaScript (`e.preventDefault()`) untuk membuka modal in-place edit dan pemanggilan API via AJAX.
3. **Penanganan Jaringan PWS Off-Campus**:
   - Menyadari bahwa server PWS Fasilkom UI (`pws.cs.ui.ac.id`) tidak dapat diakses tanpa koneksi VPN UI, eksekusi push diprioritaskan ke repositori GitHub publik (`origin/main`) dan mendokumentasikan panduan push manual ke PWS saat terhubung ke VPN.

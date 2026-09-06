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
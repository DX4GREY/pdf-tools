# PDF Tools

PDF Tools adalah aplikasi berbasis web sederhana yang menyediakan berbagai alat untuk memanipulasi file PDF, seperti menggabungkan, memisahkan, mengompresi, dan mengonversi file dari format lain ke PDF.

## Fitur

1. **PDF Merger**: Menggabungkan beberapa file PDF menjadi satu file PDF.
2. **PDF Splitter**: Memisahkan file PDF menjadi halaman-halaman individual.
3. **PDF Compressor**: Mengurangi ukuran file PDF dengan mengatur tingkat kompresi.
4. **Image to PDF**: Mengonversi beberapa gambar (JPG, PNG, dll.) menjadi satu file PDF.
5. **HTML to PDF**: Mengonversi file HTML menjadi file PDF.
6. **Word to PDF**: Mengonversi file Word (DOCX) menjadi file PDF.

## Instalasi

### Prasyarat

- Python 3.7 atau lebih baru
- Pip (Python package manager)
- Ghostscript (untuk kompresi PDF)
- Redis (opsional, untuk rate limiting)

### Langkah Instalasi

1. Clone repositori ini:
   ```bash
   git clone <repository-url>
   cd pdf-tools
   ```

2. Instal dependensi Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Instal Ghostscript:
   - **Linux**: 
     ```bash
     sudo apt update && sudo apt install -y ghostscript
     ```
   - **MacOS**:
     ```bash
     brew install ghostscript
     ```
   - **Windows**: Unduh dan instal Ghostscript dari [situs resmi](https://www.ghostscript.com/download/gsdnld.html).

4. Jalankan aplikasi:
   ```bash
   python app.py
   ```

5. Akses aplikasi di browser Anda di `http://localhost:8080`.

## Struktur Proyek

```
pdf-tools/
├── app.py               # File utama aplikasi Flask
├── utils.py             # Fungsi utilitas untuk manipulasi file
├── w2pdf.py             # Konversi Word ke PDF
├── templates/           # Template HTML untuk antarmuka pengguna
│   ├── index.html       # Halaman utama
│   └── 521.html         # Halaman error 521
├── static/              # File statis (CSS, JS, dll.)
│   ├── main.js          # Logika frontend
│   ├── style.css        # Gaya utama
│   └── style.css.bak    # Versi cadangan gaya
├── requirements.txt     # Daftar dependensi Python
├── install-dep.sh       # Skrip instalasi untuk Linux/MacOS
├── install-dep.bat      # Skrip instalasi untuk Windows
└── README.md            # Dokumentasi proyek
```

## Cara Penggunaan

1. **PDF Merger**:
   - Unggah beberapa file PDF.
   - Atur urutan file dengan drag-and-drop.
   - Klik tombol "Merge" untuk menggabungkan file.

2. **PDF Splitter**:
   - Unggah file PDF.
   - Klik tombol "Split" untuk memisahkan file menjadi halaman individual.

3. **PDF Compressor**:
   - Unggah file PDF.
   - Pilih tingkat kompresi menggunakan slider.
   - Klik tombol "Compress" untuk mengurangi ukuran file.

4. **Image to PDF**:
   - Unggah beberapa gambar.
   - Atur urutan gambar dengan drag-and-drop.
   - Klik tombol "Convert to PDF" untuk membuat file PDF.

5. **HTML to PDF**:
   - Unggah file HTML.
   - Klik tombol "Convert" untuk mengonversi file menjadi PDF.

6. **Word to PDF**:
   - Unggah file Word (DOCX).
   - Klik tombol "Convert to PDF" untuk mengonversi file menjadi PDF.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](https://opensource.org/licenses/MIT).

## Kontributor

- **Dx4** - Pengembang utama

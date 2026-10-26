# Tugas Besar 1: Problem Solving Agent

**Mata kuliah:** AI5103 Artificial Intelligence and Data Science Fundamental

## Anggota Kelompok

| NIM | Nama |
| --- | --- |
| 28426006 | Muhammad Faishal Dienul Haq |
| 28426013 | Naufal Izza Fikry |

Proyek ini membandingkan Iterated Tabu Search (ITS), Genetic Algorithm dengan Order Crossover (GA-OX), Genetic Algorithm dengan Partially Mapped Crossover (GA-PMX), dan Particle Swarm Optimization (PSO) untuk rute truk dan trailer berkompartemen. Tujuannya meminimalkan total jarak sambil memenuhi permintaan, kapasitas kompartemen, akses pelanggan, dan batas armada.

## Struktur

| Lokasi | Isi |
| --- | --- |
| `ga_pso/` | Implementasi GA/PSO, decoder, validator, konfigurasi bersama, data dan hasil tersimpan |
| `its_mcttrp/` | Implementasi R/C++ ITS dari penulis paper dengan perbaikan lokal |
| `report/` | Sumber LaTeX serta tabel dan gambar laporan |
| `setup.sh` | Instalasi dependensi Python/R dan kompilasi pustaka C++ |
| `reproduce.py` | Menyiapkan kembali aset laporan atau menjalankan alur eksperimen opsional |
| `run_its_batch.py` | Batch ITS berdasarkan konfigurasi bersama |

## Instalasi

Clone repo lalu masuk ke foldernya. Sediakan Python 3.14, R 4.3 atau lebih baru, compiler C++, dan Bash. Pada macOS, pasang R terlebih dahulu, misalnya melalui Homebrew. Compiler tersedia melalui Xcode Command Line Tools (`xcode-select --install`). Linux membutuhkan toolchain C++ dan header pengembangan R. Windows dapat memakai WSL dengan lingkungan Linux.

Dari root repo, jalankan:

```bash
bash setup.sh
```

Script membuat `.venv`, memasang paket Python yang dipatok versinya, memasang Rcpp jika belum tersedia, lalu membangun `its_mcttrp/src/itsmcttrp.so`. Instalasi membutuhkan internet. Kegagalan satu tahap menghentikan script.

## Reproduksi tabel dan gambar final dalam satu perintah

```bash
.venv/bin/python reproduce.py
```

Perintah ini menyalin aset final yang disimpan di `ga_pso/results/report_assets/` ke `report/tables/` dan `report/figures/`. Aset berasal dari laporan eksperimen 2 yang digunakan sebagai sumber konten presentasi Figma. Perintah ini mempertahankan tabel dan grafik final, tanpa menjalankan optimizer atau menghitung ulang hasil. Bahkan tanpa instalasi paket analisis, perintah ini dapat dijalankan dengan `python3 reproduce.py` karena hanya memakai pustaka standar.

Tersedia tujuh tabel LaTeX, yaitu `summary`, `summary-real`, `summary-chao`, `reproduction`, `stats`, `sensitivity`, dan `sensitivity-compact`. Empat gambar tersedia dalam PNG dan PDF: `gap_by_instance`, `convergence`, `routes_C01`, dan `sensitivity`. Tata letak dan teks tambahan pada Figma tetap dikelola di Figma. Script ini tidak mengekspor slide menjadi gambar.

## Menjalankan eksperimen dari awal (opsional)

```bash
.venv/bin/python reproduce.py --full --fresh
```

Perintah tersebut mengarsipkan hasil mentah lama ke `ga_pso/results/raw_backup_<waktu>/`, menjalankan ITS, GA-OX, GA-PMX, PSO, sensitivitas, lalu membangun tabel dan gambar dari hasil baru. Aset final di `report_assets/` tetap disimpan. Seluruh alur dapat memerlukan beberapa jam. **Eksperimen tidak dijalankan ulang saat pembaruan dokumentasi ini.**

Gunakan `--full` tanpa `--fresh` untuk melanjutkan batch yang terputus. Hasil yang sudah memiliki JSON dilewati. Setelah mengubah konfigurasi, gunakan `--fresh` agar hasil dengan konfigurasi lama tidak tercampur. Untuk menghitung ulang analisis dari JSON yang ada, gunakan `.venv/bin/python reproduce.py --analyze`. Angka dan gambar yang dihitung ulang dapat berbeda dari aset final, terutama bila hasil mentah sudah berubah.

## Seed, parameter, dan cakupan

Konfigurasi bersama berada di `ga_pso/config.json`, termasuk parameter ITS. Kedua runner membacanya langsung.

| Bagian konfigurasi | Pengaturan |
| --- | --- |
| `instances` | P1 sampai P8 dan C01 sampai C06, jumlah truk/trailer serta nilai acuan |
| `seeds` | 1 sampai 10 untuk eksperimen utama |
| `workers` | 8 proses paralel |
| `its` | 100 iterasi, batas pengaman 36.000 detik |
| `ga` | Populasi 100, turnamen 3, crossover 0,9, mutasi inversi 0,2, elitisme 2, varian OX/PMX |
| `pso` | 50 partikel, inersia 0,9 menuju 0,4, c1=c2=2, kecepatan maksimum 0,2 |
| `sensitivity` | C01, seed 1 sampai 5, empat peluang mutasi GA dan empat inersia akhir PSO |
| `experiment_environment` | Perangkat eksperimen dan catatan runtime |

Anggaran GA/PSO adalah rata-rata waktu ITS tersimpan untuk kasus yang sama. Inersia PSO turun linear berdasarkan proporsi waktu yang terpakai. Data P berasal dari distribusi pakan koperasi, sedangkan data C adalah benchmark Chao yang diadaptasi ke MC-TTRP. Seluruh hasil utama mencakup 14 kasus dan 560 solusi akhir. Analisis sensitivitas disimpan terpisah. File data kedua implementasi diperiksa oleh test checksum.

## Pengujian

```bash
.venv/bin/python -m pytest ga_pso/tests -q
```

Pengujian mencakup parser, kelayakan solusi, decoder, operator GA/PSO, runner, dan kesamaan dataset. Pemeriksaan ini berbeda dari menjalankan ulang eksperimen penuh.

## Perangkat dan batas reproduksi

Eksperimen yang dilaporkan menggunakan **Apple M5, CPU 10 inti, RAM 16 GB**, dengan 8 proses paralel. GA/PSO menggunakan Python 3.14 dan Numba, sedangkan ITS menggunakan R dan C++. Dependensi Python dicatat dalam `ga_pso/requirements.txt`.

Runtime dipengaruhi perangkat, jumlah proses yang berjalan bersamaan, dan implementasi. GA/PSO berhenti berdasarkan waktu, sehingga jumlah evaluasi dan hasil akhirnya dapat berbeda pada run ulang walaupun seed sama. Seed membantu mengendalikan bilangan acak, tetapi tidak menjamin hasil identik pada pencarian berbatas waktu. Nilai runtime paper berasal dari lingkungan penulis paper.

## Sumber

Paper acuan: Davila-Pena, Penas, dan Casas-Méndez (2023), [A new two-phase heuristic for a problem of food distribution with compartmentalized trucks and trailers](https://doi.org/10.1111/itor.13071).

Kode dan data ITS berasal dari [LauraDavilaPena/ITS_MC-TTRP](https://github.com/LauraDavilaPena/ITS_MC-TTRP), versi 0.1, berlisensi GPLv3 menurut `its_mcttrp/DESCRIPTION`. Atribusi dan README asli disimpan di `its_mcttrp/README.upstream.md`. Perbaikan lokal ditandai `[fix]` pada sumber terkait.

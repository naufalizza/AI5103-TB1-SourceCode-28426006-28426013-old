# A New Two-Phase Heuristic for a Problem of Food Distribution with Compartmentalized Trucks and Trailers

**Penulis:** Laura Davila-Pena, David R. Penas, Balbina Casas-Méndez (Universidade de Santiago de Compostela)
**Publikasi:** *International Transactions in Operational Research* 30 (2023) 1031–1064, open access (CC BY)
**DOI:** [10.1111/itor.13071](https://doi.org/10.1111/itor.13071)

---

## 1. Tautan Penting

| Sumber | Link | Keterangan |
|---|---|---|
| Source code (resmi) | https://github.com/LauraDavilaPena/ITS_MC-TTRP | Disebut langsung di paper (hlm. 1062): *"The code and instances required to reproduce the results reported herein are available at..."* |
| Dataset | Folder [`instances/`](https://github.com/LauraDavilaPena/ITS_MC-TTRP/tree/main/instances) di repo yang sama | Data studi kasus dan benchmark |
| Benchmark asli Chao (2002) | http://web.ntust.edu.tw/~vincent/ttrp/ | Sumber 21 instance TTRP, menurut footnote 6 paper |

### Isi dataset

| File | Jumlah | Asal | Ukuran |
|---|---|---|---|
| `P1.csv` – `P8.csv` | 8 | Data nyata koperasi pakan ternak di Galicia, Spanyol | 8–10 pelanggan |
| `CHAO_TTRP_01` – `21` | 21 | Benchmark TTRP dari Chao (2002), tanpa kompartemen | 50–199 pelanggan |
| `CHAO_MCTTRP_01` – `21` | 21 | Instance Chao yang dimodifikasi penulis dengan menambahkan kompartemen | 50–199 pelanggan |

### Script reproduksi (folder `reproducibility/`)

- `CHAO_TTRP_repo.R`: hasil Tabel 3 (TTRP)
- `CHAO_MCTTRP_repo.R`: hasil Tabel 4 (MC-TTRP)
- `Real_problems_MCTTRP_repo.R`: hasil Tabel 5 (data nyata)

---

## 2. Ringkasan Singkat

Sebuah koperasi di Spanyol mengirim pakan ternak ke peternak memakai truk dan trailer yang ruang muatnya dibagi menjadi kompartemen. Penulis memodelkan masalah ini sebagai **MC-TTRP** (*Multi-Compartment Truck and Trailer Routing Problem*) dalam bentuk MILP. Model eksak dengan Gurobi butuh 31,2 jam untuk 10 pelanggan, sedangkan koperasi menerima sekitar 40 order per hari. Karena itu penulis membuat heuristik dua fase:

1. **Fase konstruksi:** algoritma Clarke–Wright yang dimodifikasi untuk menghasilkan solusi awal yang feasible.
2. **Fase perbaikan:** *iterated tabu search* (ITS) untuk memperbaiki solusi awal tersebut.

Pada data nyata, heuristik ini mencapai solusi dengan selisih maksimal 2,90% dari solusi Gurobi, dengan waktu kurang dari 10 detik.

---

## 3. Masalahnya

### 3.1 Studi kasus

- Koperasi produsen pakan ternak di Galicia (wilayah barat laut Spanyol, 29.565 km², 4 provinsi).
- Lebih dari 1.500 peternak pelanggan di 60 kota. Produksi pakan lebih dari 150.000 ton per tahun.
- Sekitar 40 order per hari, masing-masing 500 kg sampai lebih dari 14.000 kg.
- Ada **4 jenis pakan**.
- Data jarak dan lokasi diperoleh dari sistem GPS armada yang dirancang tim insinyur pertanian.

Tujuannya adalah membuat alat yang merancang rute setiap kendaraan secara otomatis sehingga semua batasan terpenuhi dan **total jarak tempuh minimal**.

### 3.2 Kenapa rumit: tiga karakteristik sekaligus

**a. Truk dan trailer (TTRP).** Sebagian peternakan tidak bisa dimasuki kendaraan besar. Maka pelanggan dibagi dua jenis:

| Jenis pelanggan | Bisa dilayani oleh |
|---|---|
| *Vehicle customer* (VC) | Kendaraan lengkap (truk + trailer) atau truk saja |
| *Truck customer* (TC) | Truk saja |

Akibatnya ada tiga tipe rute:

| Tipe rute | Penjelasan |
|---|---|
| **PTR** (*pure truck route*) | Truk tanpa trailer. Boleh melayani VC dan TC |
| **PVR** (*pure vehicle route*) | Truk + trailer sepanjang rute. Hanya melayani VC |
| **MVR** (*mixed vehicle route*) | Rute utama dengan truk + trailer. Di salah satu titik VC (atau depot), trailer diparkir, lalu truk berangkat sendiri menjalani *sub-tour* untuk melayani TC dan VC, kemudian kembali mengambil trailer |

**b. Kompartemen (multi-compartment).** Dalam kasus nyata ini:

- Pakan jenis berbeda tidak boleh dicampur dalam satu kompartemen.
- Satu kompartemen tidak boleh diisi untuk dua pelanggan berbeda, karena koperasi tidak punya alat untuk menakar pakan per pelanggan di atas kendaraan.
- Pada contoh nyata yang diselesaikan secara eksak: truk punya 13 kompartemen (masing-masing maks. 1,5 ton), trailer punya 15 kompartemen (masing-masing maks. 2 ton).

**c. Batasan operasional.** Kapasitas legal truk dan trailer, waktu kerja pengemudi maksimal (8 jam per hari), dan kecepatan rata-rata (diestimasi 60 km/jam).

### 3.3 Kenapa tidak cukup diselesaikan secara eksak

Model MILP-nya punya 49 kelompok persamaan (fungsi objektif plus batasan). Hasil dengan Gurobi 8.1.0:

| Ukuran | Waktu Gurobi |
|---|---|
| 10 pelanggan (dengan trailer) | 31,2 jam sampai optimal (207 km) |
| 10 pelanggan (truk saja) | 6,23 jam (232 km) |
| 11 pelanggan | Lebih dari dua minggu |

Untuk 40 pelanggan per hari, pendekatan eksak jelas tidak praktis. Paper juga menyebut rute hanya berguna untuk dua sampai tiga hari ke depan karena order baru, kendaraan rusak, atau perubahan permintaan.

---

## 4. Cara Kerja Metode

```
Input instance
      │
      ▼
┌──────────────────────────────┐
│ FASE 1: Konstruksi           │
│ Clarke–Wright untuk MC-TTRP  │
│ + perbaikan pasca-konstruksi │
└──────────────┬───────────────┘
               │ solusi awal (feasible)
               ▼
┌──────────────────────────────┐
│ FASE 2: Iterated Tabu Search │
│  ulangi max_iterITS kali:    │
│   1. tour improvement        │
│   2. perturbasi              │
│   3. tabu search             │
│   4. update solusi terbaik   │
└──────────────┬───────────────┘
               ▼
        Solusi terbaik
```

### 4.1 Fase 1: Konstruksi (Clarke–Wright yang dimodifikasi)

Ide dasar Clarke–Wright: mulai dengan satu rute per pelanggan (depot → pelanggan → depot), lalu gabungkan dua rute yang memberi **penghematan (*saving*) terbesar**. Penghematan biasa dihitung sebagai `s_ij = c_i0 + c_0j − c_ij`.

Modifikasi untuk MC-TTRP:

- **Dua matriks penghematan.** `S` adalah penghematan biasa. `Ŝ` adalah penghematan khusus untuk mengubah rute TC menjadi *sub-tour* yang berakar di sebuah VC.
- **Empat jenis penggabungan rute:** PVR + PVR, PTR + PTR, MVR + PVR, dan menyisipkan rute VC tunggal ke PTR. Setiap penggabungan mengecek ketersediaan kompartemen.
- **Matriks `T`** menyimpan detail alokasi muatan setiap pelanggan ke kompartemen kendaraan.

Setelah tidak ada penghematan positif, solusi diperbaiki secara berurutan:

1. Menambahkan pelanggan yang belum terlayani.
2. Menyesuaikan jumlah armada: membuat atau melengkapi MVR, memecah rute, menukar rute sisa.
3. *Tour improvement*: gerakan 2-opt, 3-opt, dan 4-opt* per rute.
4. *Local search*: gerakan khusus TTRP (diadaptasi dari Derigs et al., 2013) plus 2-opt, 2-opt*, *exchange*, dan *relocate*.

### 4.2 Fase 2: Iterated Tabu Search (ITS)

Setiap iterasi ITS (Algoritma 2) terdiri dari:

**a. Perturbasi** (agar keluar dari optimum lokal)
- Pilih acak φ pelanggan, yaitu 1% sampai 10% dari total pelanggan.
- Keluarkan pelanggan tersebut dari solusi, lalu sisipkan kembali di posisi dengan kenaikan biaya terkecil. Prosedur hapus dan sisip memakai GENI dan *unstringing and stringing* (Gendreau et al., 1992).
- Rute diperbaiki dengan 3-opt dan 4-opt*.
- Jika ada pelanggan yang gagal disisipkan, solusi infeasible diizinkan sampai batas tertentu.

**b. Tabu search** (Algoritma 3)
- Di setiap langkah, terapkan gerakan *local search* terbaik yang tidak ada di daftar tabu, walaupun gerakan itu memperburuk solusi atau membuatnya infeasible.
- **Daftar tabu** menyimpan pasangan {pelanggan, rute}, sehingga pelanggan tidak dimasukkan kembali ke rute yang sama selama τ iterasi. Nilai τ diambil acak dari U[1, √(n·nr)], dengan n = jumlah pelanggan dan nr = jumlah rute.
- **Kriteria aspirasi:** gerakan tabu tetap boleh dipakai jika menghasilkan solusi lebih baik dari solusi terbaik yang pernah ditemukan.
- **Penalti infeasibility:** biaya rute dihitung sebagai `F(r) = d(r) + α·C(r)`, dengan `d(r)` = jarak dan `C(r)` = kelebihan muatan. Nilai α naik dengan faktor (1+γ) bila solusi infeasible dan turun bila feasible. Akibatnya pencarian bergerak bolak-balik di antara wilayah feasible dan infeasible.
- **Penalti frekuensi:** gerakan yang sering dipakai diberi penalti tambahan (`freqPenList`, bobot ζ) agar pencarian tidak berputar di area yang sama.
- **Berhenti** setelah sejumlah iterasi tanpa perbaikan, yaitu √((max_iterITS − iterITS)·φ).

**c. Pemilihan solusi untuk iterasi berikutnya**
- Dengan probabilitas (iterITS / max_iterITS)², pencarian kembali ke solusi terbaik global. Jadi semakin dekat ke akhir, semakin besar kemungkinan pencarian difokuskan di sekitar solusi terbaik.

---

## 5. Hasil pada Studi Kasus

Penulis membentuk 8 problem dari data koperasi:

- P1–P3: 4 pelanggan VC dan 4 TC.
- P4–P5: 9 pelanggan, 5 di antaranya VC.
- P6–P8: 10 pelanggan, 5 VC dan 5 TC.

Semua problem memakai 2 truk (13 kompartemen, maks. 1,5 ton) dan 1 trailer (15 kompartemen, maks. 2 ton). Heuristik dijalankan 100 iterasi ITS.

Hasilnya dibandingkan dengan solusi eksak Gurobi (Tabel 5 paper):

| Problem | Ukuran | Gurobi (km) | Heuristik (km) | Waktu Gurobi (s) | Waktu heuristik (s) |
|---|---|---|---|---|---|
| P1 | 8 | 189 | 189 | 309,27 | 5,03 |
| P2 | 8 | 140 | 142 | 6.733,20 | 3,88 |
| P3 | 8 | 106 | 106 | 1.275,75 | 3,90 |
| P4 | 9 | 256 | 256 | 16.766,7 | 5,58 |
| P5 | 9 | 109 | 109 | 17.511 | 4,72 |
| P6 | 10 | 222 | 223 | 221.019 | 6,48 |
| P7 | 10 | 237 | 238 | 671.316 | 7,97 |
| P8 | 10 | 207 | 213 | 112.389 | 6,09 |

Catatan:
- Selisih terbesar ada di P8: (213 − 207) / 207 = 6 / 207 ≈ 2,90%. Angka ini sesuai yang dilaporkan paper.
- Teks paper menyebut heuristik mencapai nilai eksak pada P1, P3, dan P4. Di Tabel 5, P5 juga bernilai sama (109 vs 109), tetapi teks tidak menyebutnya.
- Tabel 6 paper menunjukkan bahwa dengan batas waktu 3 jam, Gurobi belum membuktikan optimalitas untuk P6–P8 (gap relatif 0,11, 0,22, dan 0,65).
- Temuan bisnis dari contoh 10 pelanggan: memakai trailer menurunkan total jarak dari 232 km menjadi 207 km (selisih 25 km) dan jumlah pengemudi dari 3 menjadi 2.

### Hasil pada benchmark (ringkas)

- **TTRP (21 instance Chao, Tabel 3):** ITS dijalankan 500 iterasi, diambil nilai terbaik dari 10 run. ITS lebih baik daripada metode Chao (2002) dan Caramia & Guerriero (2010a) pada instance 1, 9, dan 11. Waktu komputasi 7 sampai 200 menit.
- **MC-TTRP (21 instance Chao yang dimodifikasi, Tabel 4):** ITS dijalankan 100 iterasi, diambil nilai terbaik dari 10 run. Heuristik selalu menemukan solusi feasible, dengan rata-rata tingkat okupansi kompartemen 87% (truk), 81% (trailer), dan 87% (total). Belum ada metode lain untuk MC-TTRP di literatur sebagai pembanding.

### Lingkungan eksperimen di paper

| Komponen | Spesifikasi |
|---|---|
| Heuristik | R 4.0.2, superkomputer Finisterrae II (CESGA), CPU Intel Haswell 2680v3 |
| Model eksak | Gurobi 8.1.0, Intel i7-8700, RAM 16 GB |

---

## 6. Relevansi untuk Eksperimen GA dan PSO/ACO

Di bagian kesimpulan (hlm. 1062), penulis menyarankan riset lanjutan berupa *"other metaheuristic methods, such as simulated annealing or evolutionary algorithms, that take our solution as a benchmark to compare with it."* Eksperimen perbandingan dengan GA dan PSO/ACO sejalan dengan saran tersebut.

---

## 7. Catatan Reproduksi

> Bagian ini berasal dari pengecekan repo GitHub, **bukan dari isi paper**.

- Repo tidak mencantumkan lisensi. Untuk keperluan akademik, cantumkan sitasi paper.
- Repo menyertakan file biner hasil compile untuk Windows (`src/itsmcttrp.dll`, `src/movlist.o`). Jangan dipakai. Compile ulang dari `src/movlist.cpp` (Rcpp). Di macOS dibutuhkan Xcode Command Line Tools.
- README menyebut pengujian di CentOS 6.7 dan Windows 10. Di macOS mungkin perlu sedikit penyesuaian.
- Gurobi tidak dibutuhkan untuk menjalankan heuristik. Solusi eksak untuk P1–P8 sudah tersedia di Tabel 5 paper.

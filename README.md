# global-co2-emissions-geospatial-visualization

Visualisasi data geospasial untuk Tugas Sub-CLO-12-2-2 (mata kuliah Visualisasi Data). Topik: kesenjangan emisi CO2 dan kemakmuran ekonomi antarnegara pada tahun 2022.

Berkas yang dikumpulkan hanyalah notebook di `notebooks/`. Folder lain memuat bahan pendukung dan keluaran agar analisis dapat direproduksi.

## Struktur repository

```
notebooks/   Muhammad_Aulia_Muzzaki_Nugraha_2311102051_TugasGeospasial.ipynb (berkas yang dikumpulkan)
scripts/     download_data.py (pengunduh mandiri; notebook memuat logika unduhan yang sama)
data/raw/    berkas unduhan apa adanya (tidak ikut dilacak git)
data/processed/  hasil penyaringan dan penggabungan (GeoJSON dan CSV)
outputs/figures/ peta PNG (200 dpi) dan animasi GIF
requirements.txt versi pustaka yang dipin
```

## Dataset

Dataset terdiri atas dua komponen. Tanggal akses kedua komponen: 24 November 2026.

1. Geometri. Natural Earth 50m Admin 0 Countries (GeoJSON, EPSG:4326), https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson. Situs induk: https://www.naturalearthdata.com. Berdasarkan halaman Terms of Use, data berada di domain publik dan pencantuman kredit tidak diwajibkan. Kredit yang disarankan penyedia: "Made with Natural Earth." Kolom kunci penggabungan adalah ADM0_A3, bukan ISO_A3_EH yang memuat kode ganda dan -99.
2. Atribut. Our World in Data (OWID), CO2 and Greenhouse Gas Emissions (CSV), https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.csv, dengan kodebook https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.codebook.csv. Repositori https://github.com/owid/co2-data tidak lagi diperbarui dan hanya dipakai sebagai cadangan. Data OWID berlisensi CC BY, sedangkan data pihak ketiga mengikuti lisensi aslinya. Kutipan sesuai petunjuk OWID: "Global Carbon Budget (2026) and other sources – with major processing by Our World in Data." Sumber asli menurut kodebook: Global Carbon Budget (2026) milik Global Carbon Project untuk variabel emisi, Maddison Project Database 2023 (Bolt dan van Zanden) untuk GDP, dan sumber beragam yang dihimpun OWID untuk populasi.

Penyaringan: tahun 2022, iso_code terisi dan bukan agregat OWID, serta lengkap pada population, gdp, co2, co2_per_capita, share_global_co2, dan cumulative_co2. Hasilnya 164 negara lengkap, dan 163 di antaranya tergabung dengan geometri (Palestine tidak cocok).

## Cara menjalankan

Python 3.12 atau lebih baru.

```bash
uv venv --python 3.12 .venv            # atau: python -m venv .venv
uv pip install -r requirements.txt     # atau: pip install -r requirements.txt
uv pip install pip                     # sel pemasangan di notebook memakai %pip
```

Buka notebook lalu jalankan semua sel (Run All). Notebook mengunduh data sendiri ke `data/raw/` bila belum ada. Pengunduhan juga dapat dijalankan terpisah:

```bash
python scripts/download_data.py
```

Eksekusi tanpa antarmuka:

```bash
cd notebooks
jupyter nbconvert --to notebook --execute --inplace "Muhammad_Aulia_Muzzaki_Nugraha_2311102051_TugasGeospasial.ipynb"
```

## Catatan

- Satuan variabel dibaca dari kodebook OWID. Seluruh angka pada notebook dihitung dari berkas yang diunduh.
- Kombinasi pustaka yang diuji: geopandas 1.2.0, geoplot 0.5.1, cartopy 0.26.0, mapclassify 2.11.0, shapely 2.2.0.
- Klasifikasi NaturalBreaks memakai inisialisasi acak, sehingga seed NumPy ditetapkan di notebook.

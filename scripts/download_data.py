"""Mengunduh dataset mentah ke data/raw/ untuk Tugas Sub-CLO-12-2-2.

Komponen 1 (geometri) : Natural Earth 50m Admin 0 Countries (GeoJSON)
Komponen 2 (atribut)  : Our World in Data, CO2 and Greenhouse Gas Emissions (CSV)

Berkas yang sudah ada tidak diunduh ulang, kecuali dengan opsi --force.
Bila unduhan gagal dan tidak ada salinan lokal, skrip berhenti dengan kode keluar 1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
TIMEOUT = (15, 120)  # (sambung, baca) dalam detik
HEADERS = {"User-Agent": "geospatial-course-assignment/1.0"}

SOURCES = {
    "ne_50m_admin_0_countries.geojson": [
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson",
    ],
    "owid_co2.csv": [
        "https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.csv",
        "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",  # cadangan
    ],
    "owid_co2.codebook.csv": [
        "https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.codebook.csv",
    ],
}


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True) as resp:
        resp.raise_for_status()
        with open(tmp, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
    if tmp.stat().st_size == 0:
        tmp.unlink()
        raise IOError("berkas unduhan kosong")
    tmp.replace(dest)


def ensure_raw_files(force: bool = False, verbose: bool = True) -> dict[str, Path]:
    """Memastikan seluruh berkas mentah tersedia; mengembalikan peta nama -> jalur."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    failed: list[str] = []
    for name, urls in SOURCES.items():
        dest = RAW_DIR / name
        paths[name] = dest
        if dest.exists() and dest.stat().st_size > 0 and not force:
            if verbose:
                print(f"[ada]    {name} ({dest.stat().st_size / 1e6:.1f} MB), tidak diunduh ulang")
            continue
        ok = False
        for url in urls:
            try:
                if verbose:
                    print(f"[unduh]  {name} <- {url}")
                download(url, dest)
                ok = True
                if verbose:
                    print(f"         selesai ({dest.stat().st_size / 1e6:.1f} MB)")
                break
            except (requests.RequestException, IOError) as exc:
                print(f"[gagal]  {url}: {type(exc).__name__}: {exc}", file=sys.stderr)
        if not ok:
            failed.append(name)
    if failed:
        raise SystemExit(
            "Unduhan gagal untuk: " + ", ".join(failed) + ". Unduh berkas secara manual dari URL pada "
            "scripts/download_data.py lalu simpan di data/raw/ dengan nama yang sama."
        )
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="unduh ulang walau berkas sudah ada")
    ensure_raw_files(force=ap.parse_args().force)

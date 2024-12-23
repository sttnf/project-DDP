import streamlit as st
import pandas as pd
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date, time

@dataclass
class GachaSystem:
    """Mengelola sistem gacha dengan hadiah yang ditentukan pengguna."""
    saran_kegiatan: List[Dict[str, str]] = field(default_factory=list)

    def tambah_saran(self, kegiatan: str, deskripsi: str, durasi: str) -> None:
        self.saran_kegiatan.append({"kegiatan": kegiatan, "deskripsi": deskripsi, "durasi": durasi})

    def tarik_gacha(self) -> Optional[Dict[str, str]]:
        return random.choice(self.saran_kegiatan) if self.saran_kegiatan else None

@dataclass
class PengelolaKegiatan:
    """Mengelola berbagai jenis kegiatan."""
    kegiatan: Dict[str, pd.DataFrame] = field(default_factory=lambda: {
        "kuliah": pd.DataFrame(columns=["Tanggal", "Jam Mulai", "Jam Akhir", "Kegiatan", "Status"]),
        "rumah": pd.DataFrame(columns=["Tanggal", "Jam Mulai", "Jam Akhir", "Kegiatan", "Status"]),
    })
    gacha_system: GachaSystem = field(default_factory=GachaSystem)

    def tambah_kegiatan(self, jenis_kegiatan: str, tanggal: date, jam_mulai: time, jam_akhir: time, kegiatan: str) -> None:
        kegiatan_baru = pd.DataFrame({
            "Tanggal": [tanggal],
            "Jam Mulai": [jam_mulai],
            "Jam Akhir": [jam_akhir],
            "Kegiatan": [kegiatan],
            "Status": ["Belum Selesai"]
        })
        self.kegiatan[jenis_kegiatan] = pd.concat([self.kegiatan[jenis_kegiatan], kegiatan_baru], ignore_index=True)

    def ubah_status_kegiatan(self, jenis_kegiatan: str, index: int) -> None:
        df = self.kegiatan[jenis_kegiatan]
        if 0 <= index < len(df):
            df.at[index, "Status"] = "Selesai" if df.at[index, "Status"] == "Belum Selesai" else "Belum Selesai"

    def tingkat_penyelesaian(self) -> float:
        total = sum(len(df) for df in self.kegiatan.values())
        selesai = sum(len(df[df["Status"] == "Selesai"]) for df in self.kegiatan.values())
        return (selesai / total) * 100 if total > 0 else 0.0

def buat_form_kegiatan(pengelola_kegiatan: PengelolaKegiatan, jenis_kegiatan: str) -> None:
    with st.form(key=f'{jenis_kegiatan}_form'):
        st.subheader(f"Tambah Kegiatan {jenis_kegiatan.capitalize()}")
        tanggal = st.date_input("Tanggal")
        jam_mulai, jam_akhir = st.columns(2)
        jam_mulai = jam_mulai.time_input("Jam Mulai")
        jam_akhir = jam_akhir.time_input("Jam Akhir")
        kegiatan = st.text_input("Kegiatan")

        if st.form_submit_button("Tambah"):
            if jam_akhir <= jam_mulai:
                st.error("Jam akhir harus lebih besar dari jam mulai!")
            elif not kegiatan.strip():
                st.error("Kegiatan tidak boleh kosong!")
            else:
                pengelola_kegiatan.tambah_kegiatan(jenis_kegiatan, tanggal, jam_mulai, jam_akhir, kegiatan)
                st.success("Kegiatan berhasil ditambahkan!")
                st.balloons()

def tampilkan_kegiatan(pengelola_kegiatan: PengelolaKegiatan, jenis_kegiatan: str) -> None:
    df = pengelola_kegiatan.kegiatan[jenis_kegiatan]
    if df.empty:
        st.info("Belum ada kegiatan yang ditambahkan.")
        return

    st.subheader(f"Daftar Kegiatan {jenis_kegiatan.capitalize()}")
    for idx, row in df.iterrows():
        with st.expander(f"Kegiatan {idx + 1}", expanded=True):
            st.write(f"**Tanggal:** {row['Tanggal']}")
            st.write(f"**Jam Mulai:** {row['Jam Mulai']}")
            st.write(f"**Jam Akhir:** {row['Jam Akhir']}")
            st.write(f"**Kegiatan:** {row['Kegiatan']}")
            st.write(f"**Status:** {row['Status']}")
            status = "🟢 Selesai" if row['Status'] == "Selesai" else "🔴 Belum Selesai"
            if st.button(status, key=f"{jenis_kegiatan}_status_{idx}"):
                pengelola_kegiatan.ubah_status_kegiatan(jenis_kegiatan, idx)

def buat_form_gacha(pengelola_kegiatan: PengelolaKegiatan) -> None:
    with st.form(key='gacha_form'):
        st.subheader("Tambah Saran Kegiatan ke Gacha")
        kegiatan = st.text_input("Nama Kegiatan")
        deskripsi = st.text_area("Deskripsi")
        durasi = st.text_input("Durasi (contoh: 30 menit)")

        if st.form_submit_button("Tambah ke Pool Gacha"):
            if not all([kegiatan.strip(), deskripsi.strip(), durasi.strip()]):
                st.error("Semua field harus diisi!")
            else:
                pengelola_kegiatan.gacha_system.tambah_saran(kegiatan, deskripsi, durasi)
                st.success("Saran kegiatan berhasil ditambahkan ke pool gacha!")

def main():
    st.set_page_config(page_title="Jadwal Kegiatan", page_icon="📅", layout="wide")
    if 'pengelola_kegiatan' not in st.session_state:
        st.session_state.pengelola_kegiatan = PengelolaKegiatan()

    st.title("📅 Jadwal Kegiatan Produktif")
    tabs = st.tabs(["Kuliah", "Rumah", "Review", "Gacha"])

    with tabs[0]:
        buat_form_kegiatan(st.session_state.pengelola_kegiatan, "kuliah")
        st.divider()
        tampilkan_kegiatan(st.session_state.pengelola_kegiatan, "kuliah")

    with tabs[1]:
        buat_form_kegiatan(st.session_state.pengelola_kegiatan, "rumah")
        st.divider()
        tampilkan_kegiatan(st.session_state.pengelola_kegiatan, "rumah")

    with tabs[2]:
        st.subheader("Review Kegiatan")
        rate = st.session_state.pengelola_kegiatan.tingkat_penyelesaian()
        st.metric("Tingkat Penyelesaian", f"{rate:.1f}%")

        st.subheader("Semua Kegiatan")
        for jenis_kegiatan, df in st.session_state.pengelola_kegiatan.kegiatan.items():
            st.write(f"### {jenis_kegiatan.capitalize()}")
            if df.empty:
                st.info(f"Tidak ada kegiatan untuk {jenis_kegiatan}.")
            else:
                st.table(df)

    with tabs[3]:
        buat_form_gacha(st.session_state.pengelola_kegiatan)
        st.divider()
        st.subheader("Pool Gacha")

        if not st.session_state.pengelola_kegiatan.gacha_system.saran_kegiatan:
            st.info("Pool gacha kosong.")
        else:
            st.table(pd.DataFrame(st.session_state.pengelola_kegiatan.gacha_system.saran_kegiatan))

        if rate >= 80 and st.button("Tarik Gacha!"):
            saran = st.session_state.pengelola_kegiatan.gacha_system.tarik_gacha()
            if saran:
                st.success(f"🎉 {saran['kegiatan']} | 📝 {saran['deskripsi']} | ⏱️ {saran['durasi']}")
            else:
                st.warning("Pool gacha kosong.")

if __name__ == "__main__":
    main()

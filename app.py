# app.py - KOD LENGKAP & BETUL

import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red, HexColor
from reportlab.lib.units import inch
from PIL import Image
import io
from datetime import date

# --- Fungsi untuk menjana PDF ---
def generate_pdf(no_resit, tarikh, diterima_daripada, jumlah_perkataan, untuk_bayaran, jumlah_rm, cara_bayaran):
    buffer = io.BytesIO()
    template_image = Image.open("template.png")
    img_width, img_height = template_image.size
    page_width = img_width * 72 / 96
    page_height = img_height * 72 / 96
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    c.drawImage("template.png", 0, 0, width=page_width, height=page_height)

    # --- UBAH SUAI KEDUDUKAN & SAIZ DI SINI ---

    # 1. KEDUDUKAN (KOORDINAT x, y)
    #    - Ubah nombor di bawah untuk menggerakkan teks.
    #    - Ingat: (0,0) adalah di sudut KIRI-BAWAH.
    x_no = page_width - 1.4*inch
    y_no = page_height - 0.70*inch
    
    x_tarikh = page_width - 2.0*inch
    y_tarikh = page_height - 2.95*inch
    
    
    x_diterima = 2.35 * inch
    y_diterima = y_tarikh - 0.45 * inch
    x_utama = 3.0 * inch
    y_sebanyak = y_diterima - 0.45 * inch
    x_bayaran = 2.0 * inch
    y_bayaran = y_sebanyak - 0.9 * inch
    
    y_bawah = y_bayaran - 0.88 * inch
    x_rm = 1.0 * inch
    x_bayaran_teks = 2.5 * inch

    # 2. PROSES MEMASUKKAN DATA
    #    - Gunakan c.setFont() sebelum c.drawString() untuk menukar saiz.
    
    # No Resit (warna merah, saiz 16)
    c.setFont("Helvetica-Bold", 16) # Guna Bold dan saiz 12
    c.setFillColor(red)
    c.drawString(x_no, y_no, no_resit)
    c.setFillColor("black") # Kembalikan ke warna hitam

    # Saiz fon biasa untuk data lain (saiz 14)
    c.setFont("Helvetica", 14)

    c.drawString(x_tarikh, y_tarikh, tarikh)
    c.drawString(x_diterima, y_diterima, diterima_daripada)
    c.drawString(x_utama, y_sebanyak, jumlah_perkataan)
    c.drawString(x_bayaran, y_bayaran, untuk_bayaran)
    
    # Jumlah RM (saiz 14, Bold)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_rm, y_bawah, f"{jumlah_rm:.2f}")

    # Cara bayaran (kembali ke saiz 14)
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#385616"))
    c.drawString(x_bayaran_teks, y_bawah, "Tunai / Online Banking")
    c.setFillColor("black")
    if cara_bayaran == "Tunai":
        c.line(x_bayaran_teks + 0.5 * inch, y_bawah + 2, x_bayaran_teks + 2.1 * inch, y_bawah + 2) # Pindaan pada koordinat potong
    else:
        c.line(x_bayaran_teks, y_bawah + 2, x_bayaran_teks + 0.45 * inch, y_bawah + 2)

    c.save()
    buffer.seek(0)
    return buffer


# --- Muka Depan Aplikasi Streamlit ---

st.set_page_config(page_title="Penjana Resit SRITI Al Fateh", layout="centered")
st.title("Penjana Resit SRITI Al Fateh")

with st.form("borang_resit"):
    st.header("Sila Masukkan Maklumat Resit")

    col1, col2 = st.columns(2)

    with col1:
        no_resit = st.text_input("No Resit:", placeholder="Contoh: 2025001")
        diterima_daripada = st.text_input("Diterima daripada:")
        jumlah_rm = st.number_input("Jumlah (RM):", min_value=0.0, format="%.2f")
        
    with col2:
        tarikh_input = st.date_input("Tarikh:", date.today())
        tarikh = tarikh_input.strftime("%d/%m/%Y")
        jumlah_perkataan = st.text_input("Jumlah Dalam Perkataan:")
        cara_bayaran = st.radio("Cara Bayaran:", ("Tunai", "Online Banking"))
        
    untuk_bayaran = st.text_area("Untuk bayaran bagi:")

    submitted = st.form_submit_button("Jana Resit PDF")

if submitted:
    if not no_resit or not diterima_daripada or not untuk_bayaran or jumlah_rm == 0.0:
        st.warning("Sila isi semua medan yang diperlukan.")
    else:
        pdf_buffer = generate_pdf(no_resit, tarikh, diterima_daripada, jumlah_perkataan, untuk_bayaran, jumlah_rm, cara_bayaran)
        
        st.success("Resit PDF berjaya dijanakan!")
        
        st.download_button(
            label="Muat Turun Resit PDF",
            data=pdf_buffer,
            file_name=f"Resit_{no_resit}_{diterima_daripada}.pdf",
            mime="application/pdf"
        )
"""
Script untuk generate Manual Book PDF
Sistem Multi-Agent RAG untuk Komite Audit Indonesia
"""

from fpdf import FPDF


class ManualPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(15, 15, 15)
        self.add_font('DejaVu', '', 'C:/Windows/Fonts/arial.ttf')
        self.add_font('DejaVu', 'B', 'C:/Windows/Fonts/arialbd.ttf')
        self.add_font('DejaVu', 'I', 'C:/Windows/Fonts/ariali.ttf')

    def header(self):
        if self.page_no() > 1:
            self.set_font('DejaVu', 'I', 9)
            self.set_text_color(128, 128, 128)
            self.cell(90, 10, 'Manual Book - Sistem RAG Komite Audit')
            self.cell(90, 10, f'Halaman {self.page_no()}', align='R')
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Confidential - Februari 2026', align='C')

    def h1(self, title):
        self.set_font('DejaVu', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.ln(6)
        self.multi_cell(0, 8, title)
        self.ln(4)

    def h2(self, title):
        self.set_font('DejaVu', 'B', 13)
        self.set_text_color(0, 76, 153)
        self.ln(4)
        self.multi_cell(0, 7, title)
        self.ln(2)

    def h3(self, title):
        self.set_font('DejaVu', 'B', 11)
        self.set_text_color(51, 51, 51)
        self.ln(3)
        self.multi_cell(0, 6, title)
        self.ln(2)

    def p(self, text):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def table(self, headers, rows, widths):
        # Header
        self.set_font('DejaVu', 'B', 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(widths[i], 7, h, 1, 0, 'C', True)
        self.ln()
        # Rows
        self.set_font('DejaVu', '', 9)
        self.set_text_color(0, 0, 0)
        for row in rows:
            for i, cell in enumerate(row):
                self.cell(widths[i], 7, str(cell), 1, 0)
            self.ln()


def create_manual_pdf():
    pdf = ManualPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # === COVER PAGE ===
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font('DejaVu', 'B', 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, 'MANUAL BOOK', align='C')
    pdf.ln(18)
    pdf.set_font('DejaVu', 'B', 16)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 10, 'Sistem Multi-Agent RAG', align='C')
    pdf.ln(8)
    pdf.cell(0, 10, 'untuk Komite Audit Indonesia', align='C')
    pdf.ln(20)
    pdf.set_font('DejaVu', '', 12)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'Versi 1.0 - Februari 2026', align='C')
    pdf.ln(30)

    # Features box
    pdf.set_fill_color(240, 248, 255)
    pdf.set_draw_color(0, 51, 102)
    pdf.rect(25, pdf.get_y(), 160, 50, 'DF')
    pdf.set_xy(30, pdf.get_y() + 5)
    pdf.set_font('DejaVu', 'B', 11)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'Fitur Utama:')
    pdf.ln(7)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(51, 51, 51)
    for f in ["8 Expert Agent untuk Komite Audit", "AI Financial Analyst (CFA/CPA)",
              "Executive Insight Analyzer", "Risk-Audit Mapper (CIA/CRMA)", "Document Chat & RAG System"]:
        pdf.set_x(35)
        pdf.cell(0, 6, f"- {f}")
        pdf.ln(6)

    # === DAFTAR ISI ===
    pdf.add_page()
    pdf.h1("DAFTAR ISI")
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(0, 0, 0)
    for item in ["1. Pendahuluan", "2. Memulai Aplikasi", "3. Panduan Fitur",
                 "   3.1 Beranda", "   3.2 Konsultasi", "   3.3 Dokumen",
                 "   3.4 Analisis Keuangan", "   3.5 Executive Insight", "   3.6 Risk Mapping",
                 "4. 8 Expert Agent", "5. Tips Penggunaan", "6. Troubleshooting", "7. FAQ", "Lampiran"]:
        pdf.cell(0, 7, item)
        pdf.ln()

    # === BAB 1: PENDAHULUAN ===
    pdf.add_page()
    pdf.h1("1. PENDAHULUAN")

    pdf.h2("1.1 Tentang Sistem")
    pdf.p("Sistem Multi-Agent RAG untuk Komite Audit adalah aplikasi AI yang dirancang "
          "untuk mendukung Komite Audit di Indonesia. Sistem menggunakan 8 agen ahli "
          "spesialis untuk menjawab pertanyaan seputar:")
    pdf.p("- Tata kelola Komite Audit\n- Perencanaan dan pelaksanaan audit\n"
          "- Kepatuhan regulasi (OJK, BI, PSAK)\n- Review laporan keuangan\n"
          "- Pelaporan dan pengungkapan\n- ESG dan keberlanjutan\n- Pemetaan risiko dan audit")

    pdf.h2("1.2 Fitur Utama")
    pdf.table(["Fitur", "Deskripsi"], [
        ("Konsultasi", "Tanya jawab dengan 8 agen ahli"),
        ("Upload Dokumen", "Unggah PDF, DOCX, TXT, XLSX"),
        ("Analisis Keuangan", "Analisis oleh AI Financial Analyst"),
        ("Executive Insight", "Ringkasan untuk Dewan Komisaris"),
        ("Risk Mapping", "Pemetaan Risk Register vs PKPT"),
        ("Chat Dokumen", "Tanya jawab pada dokumen spesifik"),
    ], [45, 135])

    pdf.h2("1.3 Arsitektur")
    pdf.p("Sistem terdiri dari tiga layer:\n"
          "- Frontend: Streamlit (port 8501)\n"
          "- Backend: FastAPI (port 8000)\n"
          "- Data: Groq LLM Llama 3.3 70B + Supabase pgvector")

    # === BAB 2: MEMULAI APLIKASI ===
    pdf.add_page()
    pdf.h1("2. MEMULAI APLIKASI")

    pdf.h2("2.1 Akses Aplikasi")
    pdf.p("URL Frontend: http://localhost:8501 (development)\n"
          "Atau URL production yang disediakan administrator.")

    pdf.h2("2.2 Tampilan Awal")
    pdf.p("Halaman Beranda menampilkan:\n"
          "- Executive Insight Cards (jika ada)\n"
          "- Statistik sistem\n"
          "- Daftar 8 agen ahli\n"
          "- Contoh pertanyaan")

    pdf.h2("2.3 Navigasi Menu")
    pdf.table(["Menu", "Fungsi"], [
        ("Beranda", "Dashboard utama"),
        ("Konsultasi", "Tanya jawab dengan agen ahli"),
        ("Dokumen", "Upload dan kelola dokumen"),
        ("Analisis", "Analisis keuangan & executive insight"),
        ("Risk Mapping", "Pemetaan risiko vs audit"),
        ("Analitik", "Statistik sistem"),
        ("Tentang", "Informasi sistem"),
    ], [45, 135])

    # === BAB 3: PANDUAN FITUR ===
    pdf.add_page()
    pdf.h1("3. PANDUAN FITUR")

    pdf.h2("3.1 Beranda (Dashboard)")
    pdf.p("Komponen utama:\n"
          "1. Executive Insight Cards - Top 3 Risiko, Financial Exposure, Sentiment\n"
          "2. Statistik Sistem - Total dokumen, percakapan, analisis\n"
          "3. Daftar Agen Ahli - 8 kartu dengan keahlian\n"
          "4. Contoh Pertanyaan - Klik untuk langsung bertanya")

    pdf.h2("3.2 Konsultasi")
    pdf.p("Fitur utama untuk berkonsultasi dengan agen ahli.\n\n"
          "LANGKAH PENGGUNAAN:\n\n"
          "1. Ketik Pertanyaan\n"
          "   Masukkan pertanyaan dalam Bahasa Indonesia.\n"
          "   Contoh: 'Apa tugas utama Komite Audit menurut OJK?'\n\n"
          "2. Pengaturan (Opsional)\n"
          "   - Gunakan Konteks Dokumen: ON/OFF\n"
          "   - Jumlah Agen: 1-4\n\n"
          "3. Kirim Pertanyaan - Tunggu 5-30 detik\n\n"
          "4. Baca Respons dengan info agen dan waktu proses\n\n"
          "5. Berikan Feedback (Opsional) - Rating 1-5 bintang")

    pdf.ln(2)
    pdf.p("TIPS BERTANYA:")
    pdf.table(["Topik", "Contoh"], [
        ("Charter", "Struktur piagam Komite Audit?"),
        ("Regulasi", "Persyaratan OJK untuk independensi?"),
        ("Keuangan", "Review efektivitas auditor?"),
        ("Perbankan", "Kewajiban Komite Audit bank?"),
        ("ESG", "Peran dalam pengawasan ESG?"),
        ("Risiko", "Menyusun audit berbasis risiko?"),
    ], [40, 140])

    # 3.3 Dokumen
    pdf.add_page()
    pdf.h2("3.3 Dokumen")
    pdf.p("FORMAT YANG DIDUKUNG:\n"
          "- PDF (.pdf) - Rekomendasi utama\n"
          "- Word (.docx)\n"
          "- Text (.txt)\n"
          "- Excel (.xlsx)\n\n"
          "LANGKAH UPLOAD:\n"
          "1. Klik area upload atau drag & drop file\n"
          "2. Pilih file dari komputer\n"
          "3. File diproses otomatis (background)\n"
          "4. Status berubah: Processing -> Processed")

    pdf.ln(2)
    pdf.p("INFORMASI DOKUMEN:")
    pdf.table(["Field", "Keterangan"], [
        ("Nama File", "Nama asli file"),
        ("Status", "Processed / Processing / Error"),
        ("Kategori", "Kategori otomatis"),
        ("Ukuran", "Ukuran file"),
        ("Chunks", "Jumlah potongan teks"),
        ("Tanggal", "Waktu upload"),
    ], [40, 140])

    pdf.ln(2)
    pdf.p("CHAT DENGAN DOKUMEN:\n"
          "1. Temukan dokumen berstatus 'Processed'\n"
          "2. Ketik pertanyaan di 'Chat dengan Dokumen Ini'\n"
          "3. Klik 'Tanya'\n"
          "4. Lihat respons (max 3 chat tersimpan)")

    # 3.4 Analisis Keuangan
    pdf.add_page()
    pdf.h2("3.4 Analisis Keuangan")
    pdf.p("Analisis dokumen keuangan oleh AI Senior Financial Analyst.\n\n"
          "PROFIL ANALYST:\n"
          "- Kredensial: CFA, CPA\n"
          "- Pengalaman: 15+ tahun\n"
          "- Spesialisasi: Laporan keuangan, rasio, risk assessment")

    pdf.ln(2)
    pdf.p("JENIS ANALISIS:")
    pdf.table(["Tipe", "Deskripsi", "Kedalaman"], [
        ("Comprehensive", "Analisis lengkap", "Penuh"),
        ("Quick", "Ringkasan cepat", "Dasar"),
        ("Ratio Only", "Fokus rasio keuangan", "Fokus"),
    ], [50, 70, 60])

    pdf.ln(2)
    pdf.p("OUTPUT (4 Tab):\n\n"
          "Tab 1: Executive Summary\n"
          "- Overall Assessment (STRONG/MODERATE/WEAK/CRITICAL)\n"
          "- Confidence Level, Overview, Key Findings\n\n"
          "Tab 2: Financial Ratios\n"
          "- Profitabilitas: ROE, ROA, NPM, GPM\n"
          "- Likuiditas: Current, Quick, Cash Ratio\n"
          "- Solvabilitas: D/E, D/A, Interest Coverage\n"
          "- Efisiensi: Asset Turnover, Inventory Turnover\n\n"
          "Tab 3: Risk Assessment\n"
          "- Risk Level, Red Flags, Positive Indicators\n\n"
          "Tab 4: Recommendations\n"
          "- Immediate, Short-term, Long-term, Audit Committee")

    # 3.5 Executive Insight
    pdf.add_page()
    pdf.h2("3.5 Executive Insight")
    pdf.p("Ringkasan eksekutif untuk Dewan Komisaris.\n\n"
          "PROFIL ADVISOR:\n"
          "- Kredensial: CFA, CPA, CERP\n"
          "- Pengalaman: 20+ tahun board-level reporting\n"
          "- Peran: CRO/CFO Advisor")

    pdf.ln(2)
    pdf.p("JENIS ANALISIS:")
    pdf.table(["Tipe", "Deskripsi", "Penggunaan"], [
        ("Full Insight", "Insight lengkap", "Laporan kuartalan"),
        ("Quick Summary", "Ringkasan cepat", "Update mingguan"),
        ("Risk Focus", "Fokus risiko", "Rapat khusus"),
    ], [50, 60, 70])

    pdf.ln(2)
    pdf.p("OUTPUT (4 Tab):\n\n"
          "Tab 1: Summary\n"
          "- Risk Rating (LOW/MEDIUM/HIGH/CRITICAL)\n"
          "- Executive Card (Headline, One-liner, Key Number)\n\n"
          "Tab 2: Top 3 Risks\n"
          "- Ranking dengan severity, likelihood, impact\n"
          "- Status mitigasi dan recommended action\n\n"
          "Tab 3: Financial Exposure\n"
          "- Total exposure range (min-max)\n"
          "- Breakdown by category, materiality\n\n"
          "Tab 4: Sentiment Analysis\n"
          "- Management sentiment score (1-10)\n"
          "- Key indicators dan quotes")

    # 3.6 Risk Mapping
    pdf.add_page()
    pdf.h2("3.6 Risk Mapping")
    pdf.p("Pemetaan Risk Register terhadap PKPT.\n\n"
          "PROFIL CONSULTANT:\n"
          "- Kredensial: CIA, CRMA\n"
          "- Framework: COSO ERM, ISO 31000\n"
          "- Pengalaman: 20+ tahun risk-based audit\n\n"
          "PRASYARAT:\n"
          "- Upload Risk Register (processed)\n"
          "- Upload PKPT/Audit Plan (processed)\n"
          "- Kedua dokumen HARUS berbeda")

    pdf.ln(2)
    pdf.p("JENIS PEMETAAN:")
    pdf.table(["Tipe", "Deskripsi", "Output"], [
        ("Comprehensive", "Pemetaan lengkap", "Full matrix"),
        ("Quick", "Fokus high-critical", "Quick view"),
        ("Gap Only", "Identifikasi gap", "Gap report"),
    ], [50, 70, 60])

    pdf.ln(2)
    pdf.p("OUTPUT (5 Tab):\n\n"
          "Tab 1: Ringkasan - Alignment, Coverage %, Critical Gaps\n\n"
          "Tab 2: Coverage Matrix - Risk ID, coverage status, quality\n\n"
          "Tab 3: Gap Analysis - Uncovered, Partially Covered, Over-Audited\n\n"
          "Tab 4: Rekomendasi - Priority actions, PKPT adjustments\n\n"
          "Tab 5: Data Quality - Completeness, issues, assumptions")

    # === BAB 4: 8 EXPERT AGENT ===
    pdf.add_page()
    pdf.h1("4. 8 EXPERT AGENT")
    pdf.p("Sistem menggunakan 8 agen ahli yang dipilih otomatis berdasarkan topik.")

    agents = [
        ("4.1 Charter Expert", "Struktur piagam, best practices governance",
         "Bagaimana struktur ideal piagam Komite Audit?"),
        ("4.2 Planning Expert", "Perencanaan audit, risk assessment, program audit",
         "Bagaimana menyusun PKPT berbasis risiko?"),
        ("4.3 Financial Review Expert", "Review laporan keuangan, efektivitas auditor",
         "Bagaimana mengevaluasi independensi auditor?"),
        ("4.4 Regulatory Expert", "UU Pasar Modal, PSAK, regulasi OJK",
         "Apa persyaratan independensi menurut POJK?"),
        ("4.5 Banking Expert", "Regulasi BI/OJK, manajemen risiko bank",
         "Apa kewajiban Komite Audit bank?"),
        ("4.6 Reporting Expert", "Pelaporan periodik, pengungkapan",
         "Apa yang wajib dilaporkan Komite Audit?"),
        ("4.7 ESG Expert", "Framework ESG (GRI, SASB, TCFD), sustainability",
         "Bagaimana peran dalam pengawasan ESG?"),
        ("4.8 Risk Mapping Expert", "Risk-based audit planning, gap analysis",
         "Bagaimana memetakan risiko ke program audit?"),
    ]

    for title, expertise, example in agents:
        pdf.h3(title)
        pdf.p(f"Keahlian: {expertise}\nContoh: \"{example}\"")

    pdf.p("PEMILIHAN AGEN OTOMATIS:\n"
          "Sistem memilih berdasarkan analisis kata kunci, konteks percakapan, "
          "dan kategori dokumen. Atur jumlah agen (1-4) di halaman Konsultasi.")

    # === BAB 5: TIPS ===
    pdf.add_page()
    pdf.h1("5. TIPS PENGGUNAAN")

    pdf.h2("5.1 Tips Umum")
    pdf.table(["Tips", "Penjelasan"], [
        ("Bahasa Indonesia", "Sistem dioptimalkan untuk Bahasa Indonesia"),
        ("Pertanyaan spesifik", "Semakin spesifik, semakin akurat"),
        ("Upload dokumen", "Dokumen relevan memperkaya konteks"),
        ("Berikan feedback", "Rating membantu sistem belajar"),
    ], [55, 125])

    pdf.h2("5.2 Tips Konsultasi")
    pdf.p("1. Mulai dengan pertanyaan umum, lalu spesifik\n"
          "2. Sebutkan konteks (industri, ukuran perusahaan)\n"
          "3. Gunakan istilah teknis yang tepat\n"
          "4. Aktifkan konteks dokumen jika sudah upload")

    pdf.h2("5.3 Tips Upload Dokumen")
    pdf.p("1. Format rekomendasi: PDF (paling stabil)\n"
          "2. Nama file deskriptif dan jelas\n"
          "3. Upload dokumen utuh, bukan potongan\n"
          "4. Tunggu status 'Processed' sebelum digunakan")

    pdf.h2("5.4 Tips Analisis Keuangan")
    pdf.p("Dokumen yang cocok: Laporan keuangan audited, Financial statements, "
          "Audit report, Management letter\n\n"
          "Pilih tipe: Comprehensive (mendalam), Quick (screening), Ratio Only (benchmarking)")

    pdf.h2("5.5 Tips Risk Mapping")
    pdf.p("Risk Register yang baik: Daftar risiko dengan ID, severity/likelihood, risk owner, mitigasi\n\n"
          "PKPT yang baik: Daftar objek audit, jadwal, resources yang dialokasikan")

    # === BAB 6: TROUBLESHOOTING ===
    pdf.add_page()
    pdf.h1("6. TROUBLESHOOTING")

    pdf.h2("6.1 Masalah Umum")
    pdf.table(["Masalah", "Penyebab", "Solusi"], [
        ("Upload gagal", "Format salah", "Gunakan PDF/DOCX/TXT/XLSX"),
        ("Status Error", "Gagal extract", "Upload ulang/format lain"),
        ("Jawaban tidak relevan", "Terlalu umum", "Buat lebih spesifik"),
        ("Proses lambat", "Dokumen besar", "Tunggu atau coba lagi"),
        ("Analisis gagal", "Dokumen salah", "Gunakan dokumen sesuai"),
    ], [50, 50, 80])

    pdf.h2("6.2 Error Messages")
    pdf.table(["Error", "Penjelasan", "Solusi"], [
        ("No context found", "Tidak ada dokumen", "Upload dokumen"),
        ("Processing timeout", "Proses timeout", "Coba lagi nanti"),
        ("Invalid document", "Dokumen tidak valid", "Format benar"),
        ("API rate limit", "Request berlebih", "Tunggu beberapa menit"),
    ], [50, 55, 75])

    pdf.h2("6.3 Kontak Support")
    pdf.p("Jika masalah tidak dapat diselesaikan:\n"
          "- Hubungi administrator sistem\n"
          "- Sertakan screenshot error\n"
          "- Jelaskan langkah sebelum error")

    # === BAB 7: FAQ ===
    pdf.add_page()
    pdf.h1("7. FAQ")

    faqs = [
        ("Q: Apakah data saya aman?", "A: Ya, data disimpan terenkripsi di server aman."),
        ("Q: Berapa lama dokumen diproses?", "A: Tergantung ukuran, biasanya 10-60 detik."),
        ("Q: Apakah bisa bahasa Inggris?", "A: Sistem dioptimalkan untuk Bahasa Indonesia."),
        ("Q: Berapa batas upload?", "A: Tidak ada batasan, upload yang relevan saja."),
        ("Q: Apakah jawaban bisa rujukan resmi?", "A: Sebagai referensi. Konsultasikan profesional."),
        ("Q: Format dokumen terbaik?", "A: PDF dengan teks selectable (bukan scan)."),
        ("Q: Mengapa beberapa agen menjawab?", "A: Sistem memilih berdasarkan relevansi topik."),
        ("Q: Cara reset session?", "A: Refresh browser memulai session baru."),
        ("Q: Beda Analisis Keuangan vs Executive Insight?", "A: Analisis fokus rasio. Executive untuk board."),
        ("Q: Kapan Risk Mapping?", "A: Memastikan risiko tercakup dalam PKPT."),
    ]

    for q, a in faqs:
        pdf.set_x(15)
        pdf.set_font('DejaVu', 'B', 10)
        pdf.set_text_color(0, 51, 102)
        pdf.multi_cell(0, 5, q)
        pdf.set_x(15)
        pdf.set_font('DejaVu', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, a)
        pdf.ln(2)

    # === LAMPIRAN ===
    pdf.add_page()
    pdf.h1("LAMPIRAN")

    pdf.h2("A. Kategori Dokumen")
    pdf.table(["Kategori", "Contoh"], [
        ("Charter/Piagam", "Piagam Komite Audit, Internal Audit"),
        ("Audit Plan", "PKPT, program audit"),
        ("Financial Report", "Laporan keuangan, neraca"),
        ("Regulatory", "Regulasi, peraturan"),
        ("Banking", "Dokumen perbankan"),
        ("Reporting", "Laporan tahunan"),
        ("ESG", "Sustainability report"),
        ("Risk", "Risk register"),
    ], [50, 130])

    pdf.h2("B. Glossary")
    pdf.table(["Istilah", "Definisi"], [
        ("RAG", "Retrieval-Augmented Generation"),
        ("Embedding", "Representasi numerik teks"),
        ("Chunk", "Potongan teks dari dokumen"),
        ("PKPT", "Program Kerja Pemeriksaan Tahunan"),
        ("Coverage Matrix", "Matriks hubungan risiko-audit"),
        ("Gap Analysis", "Analisis celah/kekurangan"),
    ], [50, 130])

    pdf.ln(10)
    pdf.set_font('DejaVu', 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'Dokumen terakhir diperbarui: Februari 2026', align='C')
    pdf.ln()
    pdf.cell(0, 8, 'Untuk pertanyaan, hubungi tim support.', align='C')

    # Save
    pdf.output("MANUAL_BOOK.pdf")
    print("PDF berhasil dibuat: MANUAL_BOOK.pdf")


if __name__ == "__main__":
    create_manual_pdf()

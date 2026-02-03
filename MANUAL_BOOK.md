# Manual Book
## Sistem Multi-Agent RAG untuk Komite Audit Indonesia

**Versi**: 1.0
**Tanggal**: Februari 2026

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Memulai Aplikasi](#2-memulai-aplikasi)
3. [Panduan Fitur](#3-panduan-fitur)
   - [3.1 Beranda (Dashboard)](#31-beranda-dashboard)
   - [3.2 Konsultasi](#32-konsultasi)
   - [3.3 Dokumen](#33-dokumen)
   - [3.4 Analisis Keuangan](#34-analisis-keuangan)
   - [3.5 Executive Insight](#35-executive-insight)
   - [3.6 Risk Mapping](#36-risk-mapping)
   - [3.7 Analitik](#37-analitik)
4. [8 Expert Agent](#4-8-expert-agent)
5. [Tips Penggunaan](#5-tips-penggunaan)
6. [Troubleshooting](#6-troubleshooting)
7. [FAQ](#7-faq)

---

## 1. Pendahuluan

### 1.1 Tentang Sistem

Sistem Multi-Agent RAG untuk Komite Audit adalah aplikasi kecerdasan buatan yang dirancang khusus untuk mendukung Komite Audit di Indonesia. Sistem ini menggunakan 8 agen ahli spesialis yang dapat menjawab pertanyaan seputar:

- Tata kelola Komite Audit
- Perencanaan dan pelaksanaan audit
- Kepatuhan regulasi (OJK, BI, PSAK, dll.)
- Review laporan keuangan
- Pelaporan dan pengungkapan
- ESG dan keberlanjutan
- Pemetaan risiko dan audit

### 1.2 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Konsultasi Multi-Agent** | Tanya jawab dengan 8 agen ahli yang otomatis dipilih berdasarkan topik |
| **Upload Dokumen** | Unggah dan kelola dokumen audit (PDF, DOCX, TXT, XLSX) |
| **Analisis Keuangan** | Analisis otomatis dokumen keuangan oleh AI Financial Analyst |
| **Executive Insight** | Ringkasan eksekutif untuk laporan ke Dewan Komisaris |
| **Risk Mapping** | Pemetaan Risk Register vs PKPT untuk identifikasi gap |
| **Chat Dokumen** | Tanya jawab spesifik pada satu dokumen |

### 1.3 Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                      │
│  Beranda │ Konsultasi │ Dokumen │ Analisis │ Risk Mapping   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Query Router │  │ 8 Expert     │  │ Specialized  │       │
│  │ (GLM)        │  │ Agents       │  │ Analysts     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  LLM: Groq Llama 3.3 70B  │  Vector Store: Supabase pgvector │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Memulai Aplikasi

### 2.1 Akses Aplikasi

**URL Frontend**: http://localhost:8501 (development) atau URL production yang disediakan

### 2.2 Tampilan Awal

Saat pertama kali membuka aplikasi, Anda akan melihat halaman **Beranda** dengan:
- Executive Insight Cards (jika ada analisis sebelumnya)
- Statistik sistem
- Daftar 8 agen ahli
- Contoh pertanyaan yang bisa diajukan

### 2.3 Navigasi

Gunakan menu di sidebar kiri untuk berpindah antar halaman:

| Menu | Fungsi |
|------|--------|
| 🏠 Beranda | Dashboard utama |
| 💬 Konsultasi | Tanya jawab dengan agen ahli |
| 📄 Dokumen | Upload dan kelola dokumen |
| 📊 Analisis | Analisis keuangan dan executive insight |
| 🎯 Risk Mapping | Pemetaan risiko vs audit |
| 📈 Analitik | Statistik dan performa sistem |
| ℹ️ Tentang | Informasi sistem |

---

## 3. Panduan Fitur

### 3.1 Beranda (Dashboard)

Halaman Beranda menampilkan ringkasan sistem dan insight terbaru.

#### Komponen Utama:

1. **Executive Insight Cards** (jika tersedia)
   - Top 3 Risiko dengan severity
   - Financial Exposure (rentang nilai)
   - Management Sentiment Score (1-10)

2. **Statistik Sistem**
   - Total dokumen
   - Total percakapan
   - Analisis terbaru

3. **Daftar Agen Ahli**
   - 8 kartu agen dengan deskripsi keahlian

4. **Contoh Pertanyaan**
   - Klik untuk langsung mengajukan pertanyaan

#### Cara Menggunakan:
1. Lihat insight terbaru di bagian atas
2. Klik "Mulai Konsultasi" untuk bertanya
3. Atau pilih contoh pertanyaan yang tersedia

---

### 3.2 Konsultasi

Fitur utama untuk berkonsultasi dengan agen ahli tentang topik Komite Audit.

#### Tampilan:

```
┌─────────────────────────────────────────────┐
│ [                 Ketik pertanyaan...     ] │
│                                             │
│ ☑ Gunakan Konteks Dokumen                   │
│ Jumlah Agen: [====2====] (1-4)              │
│                                             │
│ [        Kirim Pertanyaan        ]          │
└─────────────────────────────────────────────┘
```

#### Langkah Penggunaan:

1. **Ketik Pertanyaan**
   - Masukkan pertanyaan Anda di kolom input
   - Gunakan bahasa Indonesia
   - Contoh: "Apa saja tugas utama Komite Audit menurut regulasi OJK?"

2. **Pengaturan (Opsional)**
   - **Gunakan Konteks Dokumen**: Aktifkan untuk menyertakan informasi dari dokumen yang sudah diupload
   - **Jumlah Agen**: Atur berapa banyak agen yang akan menjawab (1-4)

3. **Kirim Pertanyaan**
   - Klik tombol "Kirim Pertanyaan"
   - Tunggu proses (biasanya 5-30 detik)

4. **Baca Respons**
   - Lihat jawaban dari agen yang dipilih sistem
   - Informasi agen yang menjawab ditampilkan
   - Waktu proses dan jumlah konteks ditampilkan

5. **Berikan Feedback (Opsional)**
   - Beri rating 1-5 bintang untuk jawaban
   - Tambahkan komentar jika perlu

#### Tips Bertanya:

| Jenis Pertanyaan | Contoh |
|------------------|--------|
| Charter/Piagam | "Bagaimana struktur piagam Komite Audit yang baik?" |
| Regulasi | "Apa persyaratan OJK untuk independensi Komite Audit?" |
| Keuangan | "Bagaimana review efektivitas auditor eksternal?" |
| Perbankan | "Apa kewajiban Komite Audit bank menurut BI?" |
| ESG | "Bagaimana peran Komite Audit dalam pengawasan ESG?" |
| Risiko | "Bagaimana menyusun audit berbasis risiko?" |

---

### 3.3 Dokumen

Halaman untuk mengelola dokumen yang akan digunakan sebagai referensi sistem.

#### 3.3.1 Upload Dokumen

**Format yang Didukung:**
- PDF (.pdf)
- Word (.docx)
- Text (.txt)
- Excel (.xlsx)

**Langkah Upload:**

1. Klik area upload atau drag & drop file
2. Pilih file dari komputer Anda
3. File akan otomatis diproses (background)
4. Status berubah: `Processing ⏳` → `Processed ✓`

**Proses di Belakang Layar:**
- Ekstraksi teks dari file
- Kategorisasi otomatis (8 kategori)
- Pemotongan teks (chunking)
- Pembuatan embedding untuk pencarian

#### 3.3.2 Daftar Dokumen

Setiap dokumen menampilkan:

| Informasi | Keterangan |
|-----------|------------|
| Nama File | Nama asli file yang diupload |
| Status | ✓ Processed / ⏳ Processing / ✗ Error |
| Kategori | Kategori otomatis (misal: Financial Report) |
| Ukuran | Ukuran file |
| Chunks | Jumlah potongan teks |
| Tanggal | Waktu upload |

#### 3.3.3 Chat dengan Dokumen

Fitur untuk bertanya tentang isi dokumen spesifik.

**Langkah:**
1. Temukan dokumen yang sudah `Processed`
2. Di bagian "Chat dengan Dokumen Ini", ketik pertanyaan
3. Klik "Tanya"
4. Respons akan muncul di bawah (max 3 chat tersimpan)

**Contoh Pertanyaan Chat Dokumen:**
- "Berapa total aset di laporan ini?"
- "Apa temuan audit yang signifikan?"
- "Ringkas rekomendasi auditor"

#### 3.3.4 Hapus Dokumen

1. Klik tombol hapus (🗑️) pada dokumen
2. Konfirmasi penghapusan
3. Dokumen dan semua embedding-nya akan dihapus

---

### 3.4 Analisis Keuangan

Analisis mendalam dokumen keuangan oleh AI Senior Financial Analyst.

#### Profil Analyst:
- **Kredensial**: CFA, CPA
- **Pengalaman**: 15+ tahun analisis keuangan
- **Spesialisasi**: Laporan keuangan, rasio, risk assessment

#### Jenis Analisis:

| Tipe | Deskripsi | Kedalaman |
|------|-----------|-----------|
| **Comprehensive** | Analisis lengkap semua aspek | Penuh |
| **Quick** | Ringkasan cepat temuan utama | Dasar |
| **Ratio Only** | Fokus pada rasio keuangan saja | Fokus |

#### Langkah Penggunaan:

1. **Pilih Dokumen**
   - Pilih dokumen keuangan dari dropdown
   - Pastikan status `Processed`

2. **Pilih Tipe Analisis**
   - Comprehensive (default, rekomendasi)
   - Quick (jika butuh cepat)
   - Ratio Only (jika hanya perlu rasio)

3. **Mulai Analisis**
   - Klik "Mulai Analisis"
   - Tunggu proses (30-120 detik)

4. **Baca Hasil (4 Tab)**

   **Tab 1: Executive Summary**
   ```
   ┌────────────────────────────────────────┐
   │ Overall Assessment: MODERATE           │
   │ Confidence Level: HIGH                 │
   │                                        │
   │ Overview:                              │
   │ Perusahaan menunjukkan kinerja...      │
   │                                        │
   │ Key Findings:                          │
   │ • Profitabilitas meningkat 15%         │
   │ • Likuiditas terjaga baik              │
   │ • Leverage dalam batas aman            │
   └────────────────────────────────────────┘
   ```

   **Tab 2: Financial Ratios**
   - Profitabilitas: ROE, ROA, NPM, GPM
   - Likuiditas: Current Ratio, Quick Ratio, Cash Ratio
   - Solvabilitas: D/E, D/A, Interest Coverage
   - Efisiensi: Asset Turnover, Inventory Turnover

   **Tab 3: Risk Assessment**
   - Overall Risk Level
   - Red Flags (jika ada)
   - Positive Indicators
   - Areas of Concern

   **Tab 4: Recommendations**
   - 🔴 Immediate Actions (segera)
   - 🟡 Short-term (1-6 bulan)
   - 🟢 Long-term (6-12 bulan)
   - 📌 Audit Committee Specific

5. **Download Hasil**
   - Klik "Download JSON" untuk menyimpan hasil

---

### 3.5 Executive Insight

Ringkasan eksekutif untuk laporan ke Dewan Komisaris dan board-level dashboard.

#### Profil Advisor:
- **Kredensial**: CFA, CPA, CERP
- **Pengalaman**: 20+ tahun board-level reporting
- **Peran**: CRO/CFO Advisor

#### Jenis Analisis:

| Tipe | Deskripsi | Penggunaan |
|------|-----------|------------|
| **Full Insight** | Insight lengkap | Laporan kuartalan |
| **Quick Summary** | Ringkasan cepat | Update mingguan |
| **Risk Focus** | Fokus risiko | Rapat khusus risiko |

#### Langkah Penggunaan:

1. Pilih dokumen dari dropdown
2. Pilih tipe analisis
3. Klik "Generate Executive Insight"
4. Tunggu proses (30-90 detik)

#### Output (4 Tab):

**Tab 1: Summary**
```
┌─────────────────────────────────────────────┐
│ Overall Risk Rating: MEDIUM                  │
│ Attention Required: MODERATE                 │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ EXECUTIVE CARD                          │ │
│ │ Headline: Profil Risiko Terkendali      │ │
│ │ One-liner: 3 risiko utama teridentifikasi│ │
│ │ Key Number: Rp 2.5M exposure            │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Tab 2: Top 3 Risks**
- Ranking risiko (1st, 2nd, 3rd)
- Kategori dan severity
- Likelihood dan impact
- Status mitigasi
- Recommended action

**Tab 3: Financial Exposure**
- Total exposure range (min-max)
- Currency
- Breakdown by category
- Materiality classification

**Tab 4: Sentiment Analysis**
- Management sentiment score (1-10)
- Sentiment type (Proactive/Responsive/Neutral/Defensive)
- Indicators:
  - Acknowledgment level
  - Ownership level
  - Action orientation
  - Timeline commitment
- Key quotes dari management

#### Penggunaan Executive Card:

Executive Card cocok untuk:
- Slide presentasi board
- Dashboard eksekutif
- Summary email ke komisaris
- One-page report

---

### 3.6 Risk Mapping

Pemetaan Risk Register terhadap PKPT (Program Kerja Pemeriksaan Tahunan) untuk identifikasi gap audit.

#### Profil Consultant:
- **Kredensial**: CIA, CRMA
- **Framework**: COSO ERM, ISO 31000
- **Pengalaman**: 20+ tahun risk-based audit

#### Prasyarat:
- Sudah upload Risk Register (processed)
- Sudah upload PKPT/Audit Plan (processed)
- Kedua dokumen HARUS berbeda

#### Jenis Pemetaan:

| Tipe | Deskripsi | Output |
|------|-----------|--------|
| **Comprehensive** | Pemetaan lengkap semua risiko | Full matrix |
| **Quick** | Fokus risiko high-critical saja | Quick view |
| **Gap Only** | Identifikasi gap saja | Gap report |

#### Langkah Penggunaan:

1. **Pilih Risk Register**
   - Pilih dari dropdown kolom kiri
   - Dokumen berisi daftar risiko perusahaan

2. **Pilih Audit Plan (PKPT)**
   - Pilih dari dropdown kolom kanan
   - Harus berbeda dengan Risk Register
   - Dokumen berisi program audit tahunan

3. **Pilih Tipe Pemetaan**
   - Comprehensive (rekomendasi)
   - Quick atau Gap Only untuk kebutuhan spesifik

4. **Mulai Pemetaan**
   - Klik "Mulai Pemetaan Risiko"
   - Tunggu proses (60-180 detik)

#### Output (5 Tab):

**Tab 1: Ringkasan (Summary)**
```
┌─────────────────────────────────────────────┐
│ Overall Alignment: MODERATE                  │
│ Coverage Percentage: 72%                     │
│ Critical Gaps: 3                             │
│                                             │
│ Total Risks Identified: 15                   │
│ Total Audit Programs: 8                      │
│                                             │
│ Executive Overview:                          │
│ Dari 15 risiko teridentifikasi, 72%         │
│ sudah tercakup dalam PKPT...                │
└─────────────────────────────────────────────┘
```

**Tab 2: Coverage Matrix**

| Risk ID | Risk Name | Coverage | Quality | Audit Programs |
|---------|-----------|----------|---------|----------------|
| R001 | Risiko Kredit | FULLY | DIRECT | AP001, AP003 |
| R002 | Risiko Likuiditas | PARTIAL | INDIRECT | AP002 |
| R003 | Risiko Operasional | NOT_COVERED | - | - |

**Tab 3: Gap Analysis**
- **Uncovered Risks**: Risiko tanpa audit coverage
  - Severity, reason, potential impact
  - Recommended audit response
- **Partially Covered**: Risiko dengan coverage tidak penuh
  - Current coverage gaps
  - Recommendations
- **Over-Audited Areas**: Area dengan audit berlebihan
  - Optimization recommendations

**Tab 4: Rekomendasi**
- Priority actions dengan estimated resources
- PKPT adjustments needed
- Resource optimization suggestions
- Audit committee recommendations

**Tab 5: Data Quality**
- Data completeness levels
- Issues dan limitations
- Assumptions used

#### Download Hasil:
- Klik "Download JSON" untuk menyimpan
- Gunakan untuk dokumentasi audit planning

---

### 3.7 Analitik

Dashboard statistik dan performa sistem.

#### Metrik yang Ditampilkan:

1. **Statistik Dokumen**
   - Total dokumen per kategori
   - Status processing
   - Trend upload

2. **Performa Agen**
   - Frekuensi penggunaan per agen
   - Response time rata-rata
   - Rating feedback

3. **Statistik Analisis**
   - Jumlah financial analysis
   - Jumlah executive insights
   - Jumlah risk mappings

4. **Aktivitas Percakapan**
   - Total conversations
   - Queries per hari/minggu
   - Session metrics

---

## 4. 8 Expert Agent

### Daftar Lengkap Agen:

#### 4.1 Charter Expert (Ahli Piagam)
**Keahlian**: Struktur piagam, best practices governance, hubungan Board

**Topik yang Ditangani**:
- Piagam Komite Audit
- Piagam Internal Audit
- Tata kelola dan governance
- Hubungan dengan Dewan Komisaris

**Contoh Pertanyaan**:
- "Bagaimana struktur ideal piagam Komite Audit?"
- "Apa saja komponen wajib dalam charter?"

---

#### 4.2 Planning Expert (Ahli Perencanaan)
**Keahlian**: Perencanaan audit, risk assessment, program audit, review performa

**Topik yang Ditangani**:
- Penyusunan PKPT
- Risk-based audit planning
- Evaluasi hasil audit
- KPI audit internal

**Contoh Pertanyaan**:
- "Bagaimana menyusun PKPT berbasis risiko?"
- "Apa metodologi audit yang efektif?"

---

#### 4.3 Financial Review Expert (Ahli Review Keuangan)
**Keahlian**: Review laporan keuangan, efektivitas auditor, quality control

**Topik yang Ditangani**:
- Review laporan keuangan
- Evaluasi auditor eksternal
- Quality control audit
- Seleksi KAP

**Contoh Pertanyaan**:
- "Bagaimana mengevaluasi independensi auditor eksternal?"
- "Apa checklist review laporan keuangan?"

---

#### 4.4 Regulatory Expert (Ahli Regulasi)
**Keahlian**: UU Pasar Modal, PSAK, SPAP, regulasi OJK, standarisasi

**Topik yang Ditangani**:
- Kepatuhan OJK
- PSAK dan standar akuntansi
- UU Pasar Modal
- Regulasi perbankan

**Contoh Pertanyaan**:
- "Apa persyaratan independensi menurut POJK?"
- "Bagaimana kepatuhan terhadap PSAK 71?"

---

#### 4.5 Banking Expert (Ahli Perbankan)
**Keahlian**: Regulasi BI/OJK, manajemen risiko bank, compliance perbankan

**Topik yang Ditangani**:
- POJK Perbankan
- Regulasi Bank Indonesia
- Risk management bank
- Basel framework

**Contoh Pertanyaan**:
- "Apa kewajiban Komite Audit bank menurut POJK?"
- "Bagaimana pengawasan risiko kredit oleh Komite Audit?"

---

#### 4.6 Reporting Expert (Ahli Pelaporan)
**Keahlian**: Pelaporan periodik, pengungkapan annual report, komunikasi stakeholder

**Topik yang Ditangani**:
- Laporan Komite Audit dalam AR
- Pengungkapan wajib
- Komunikasi dengan stakeholder
- Transparansi

**Contoh Pertanyaan**:
- "Apa saja yang wajib dilaporkan Komite Audit?"
- "Bagaimana format laporan yang baik?"

---

#### 4.7 ESG Expert (Ahli ESG)
**Keahlian**: Framework ESG (GRI, SASB, TCFD), sustainability reporting, climate risk

**Topik yang Ditangani**:
- Sustainability reporting
- ESG governance
- Climate risk
- Social responsibility

**Contoh Pertanyaan**:
- "Bagaimana peran Komite Audit dalam pengawasan ESG?"
- "Apa standar pelaporan sustainability yang berlaku?"

---

#### 4.8 Risk Mapping Expert (Ahli Pemetaan Risiko)
**Keahlian**: Risk-based audit planning, gap analysis, coverage matrix, ERM, COSO

**Topik yang Ditangani**:
- Pemetaan risiko vs audit
- Gap analysis
- Coverage matrix
- Enterprise Risk Management

**Contoh Pertanyaan**:
- "Bagaimana memetakan risiko ke program audit?"
- "Apa metodologi gap analysis yang efektif?"

---

### Pemilihan Agen Otomatis

Sistem secara otomatis memilih agen yang paling relevan berdasarkan:
1. Analisis kata kunci dalam pertanyaan
2. Konteks percakapan sebelumnya
3. Kategori dokumen yang digunakan

Anda dapat mengatur jumlah agen (1-4) di halaman Konsultasi.

---

## 5. Tips Penggunaan

### 5.1 Tips Umum

| Tips | Penjelasan |
|------|------------|
| Gunakan bahasa Indonesia | Sistem dioptimalkan untuk Bahasa Indonesia |
| Pertanyaan spesifik | Semakin spesifik pertanyaan, semakin akurat jawaban |
| Upload dokumen relevan | Semakin banyak dokumen relevan, semakin kaya konteks |
| Feedback rating | Berikan rating untuk membantu sistem belajar |

### 5.2 Tips Konsultasi

1. **Mulai dengan pertanyaan umum**, lalu spesifik
2. **Sebutkan konteks** jika ada (industri, ukuran perusahaan)
3. **Gunakan istilah teknis** yang tepat
4. **Aktifkan konteks dokumen** jika sudah upload dokumen relevan

### 5.3 Tips Upload Dokumen

1. **Format yang direkomendasikan**: PDF (paling stabil)
2. **Nama file deskriptif**: Gunakan nama yang jelas
3. **Dokumen lengkap**: Upload dokumen utuh, bukan potongan
4. **Tunggu processing**: Pastikan status `Processed` sebelum digunakan

### 5.4 Tips Analisis Keuangan

1. **Dokumen yang cocok**:
   - Laporan keuangan audited
   - Financial statements
   - Audit report
   - Management letter

2. **Pilih tipe yang tepat**:
   - Comprehensive untuk analisis mendalam
   - Quick untuk screening awal
   - Ratio Only untuk benchmarking

### 5.5 Tips Risk Mapping

1. **Risk Register yang baik** harus memuat:
   - Daftar risiko dengan ID
   - Severity/likelihood rating
   - Risk owner
   - Mitigasi yang ada

2. **PKPT yang baik** harus memuat:
   - Daftar objek audit
   - Jadwal dan timeline
   - Resources yang dialokasikan
   - Tujuan audit

---

## 6. Troubleshooting

### 6.1 Masalah Umum

| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| Dokumen tidak bisa diupload | Format tidak didukung | Gunakan PDF/DOCX/TXT/XLSX |
| Status dokumen "Error" | Gagal extract teks | Coba upload ulang atau format lain |
| Jawaban tidak relevan | Pertanyaan terlalu umum | Buat pertanyaan lebih spesifik |
| Proses terlalu lama | Dokumen besar atau server sibuk | Tunggu atau coba lagi nanti |
| Analisis gagal | Dokumen tidak mengandung data keuangan | Gunakan dokumen yang tepat |

### 6.2 Error Messages

| Error | Penjelasan | Solusi |
|-------|------------|--------|
| "No context found" | Tidak ada dokumen relevan | Upload dokumen yang relevan |
| "Processing timeout" | Proses melebihi batas waktu | Coba lagi atau hubungi admin |
| "Invalid document" | Dokumen tidak valid | Upload dokumen dengan format benar |
| "API rate limit" | Terlalu banyak request | Tunggu beberapa menit |

### 6.3 Kontak Support

Jika mengalami masalah yang tidak dapat diselesaikan:
- Hubungi administrator sistem
- Sertakan screenshot error
- Jelaskan langkah yang dilakukan sebelum error

---

## 7. FAQ

### Pertanyaan Umum

**Q: Apakah data saya aman?**
A: Ya, semua data disimpan terenkripsi di server yang aman. Dokumen hanya dapat diakses oleh pengguna yang berwenang.

**Q: Berapa lama dokumen diproses?**
A: Tergantung ukuran dokumen, biasanya 10-60 detik untuk dokumen standar.

**Q: Apakah bisa menggunakan bahasa Inggris?**
A: Sistem dioptimalkan untuk Bahasa Indonesia. Pertanyaan dalam bahasa Inggris akan dijawab dalam Bahasa Indonesia.

**Q: Berapa banyak dokumen yang bisa diupload?**
A: Tidak ada batasan jumlah dokumen. Namun disarankan upload dokumen yang relevan saja.

**Q: Apakah jawaban sistem dapat dijadikan rujukan resmi?**
A: Sistem memberikan informasi sebagai referensi. Untuk keputusan resmi, tetap konsultasikan dengan profesional yang berkualifikasi.

### Pertanyaan Teknis

**Q: Format dokumen apa yang paling baik?**
A: PDF dengan teks yang dapat dipilih (bukan scan gambar) memberikan hasil terbaik.

**Q: Mengapa ada beberapa agen yang menjawab?**
A: Sistem memilih agen berdasarkan relevansi topik. Pertanyaan kompleks mungkin melibatkan beberapa ahli.

**Q: Bagaimana cara reset session?**
A: Refresh halaman browser akan memulai session baru.

**Q: Apakah ada limit pertanyaan?**
A: Tidak ada limit pertanyaan. Namun ada fair usage policy untuk menjaga performa sistem.

### Pertanyaan Fitur

**Q: Apa bedanya Analisis Keuangan dan Executive Insight?**
A: Analisis Keuangan fokus pada rasio dan metrik keuangan detail. Executive Insight fokus pada ringkasan risiko dan sentimen untuk laporan board.

**Q: Kapan menggunakan Risk Mapping?**
A: Saat ingin memastikan semua risiko di Risk Register sudah tercakup dalam program audit (PKPT).

**Q: Bisakah chat dengan dokumen yang belum diproses?**
A: Tidak, dokumen harus berstatus `Processed` sebelum bisa digunakan untuk chat atau analisis.

---

## Lampiran

### A. Kategori Dokumen

Sistem mengenali 8 kategori dokumen:

1. **Charter/Piagam** - Piagam Komite Audit, Internal Audit
2. **Audit Plan** - PKPT, program audit
3. **Financial Report** - Laporan keuangan, neraca, laba rugi
4. **Regulatory** - Regulasi, peraturan, kebijakan
5. **Banking** - Dokumen khusus perbankan
6. **Reporting** - Laporan tahunan, pengungkapan
7. **ESG** - Sustainability report, ESG disclosure
8. **Risk** - Risk register, risk assessment

### B. Glossary

| Istilah | Definisi |
|---------|----------|
| RAG | Retrieval-Augmented Generation - teknik AI yang menggabungkan pencarian dengan generasi teks |
| Embedding | Representasi numerik dari teks untuk pencarian similarity |
| Chunk | Potongan teks dari dokumen untuk diproses |
| PKPT | Program Kerja Pemeriksaan Tahunan |
| Coverage Matrix | Matriks yang menunjukkan hubungan risiko dengan audit |
| Gap Analysis | Analisis untuk menemukan celah atau kekurangan |

### C. Shortcut & Tips Cepat

| Aksi | Cara Cepat |
|------|------------|
| Mulai konsultasi | Klik "Mulai Konsultasi" di Beranda |
| Upload dokumen | Drag & drop ke area upload |
| Lihat history | Scroll ke bawah di halaman Konsultasi |
| Download hasil | Klik tombol "Download JSON" |

---

**Dokumen ini terakhir diperbarui: Februari 2026**

*Untuk pertanyaan lebih lanjut, silakan hubungi tim support.*

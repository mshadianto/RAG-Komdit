"""
Executive Insight Analyzer Agent for RAG Komite Audit System
Senior CRO/CFO Advisor - Executive-Level Insight Extraction
"""
import time
import json
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

EXECUTIVE_INSIGHT_PERSONA = """Anda adalah **Senior Chief Risk Officer (CRO) & CFO Advisor** dengan pengalaman 20+ tahun di bidang enterprise risk management dan financial oversight.

## Profil Keahlian Anda:
- CFA Charterholder, Certified Public Accountant (CPA), dan Certified Enterprise Risk Professional (CERP)
- Spesialisasi: Executive Risk Summary, Financial Exposure Analysis, Management Sentiment Assessment
- Pengalaman di board-level reporting untuk perusahaan publik dan BUMN Indonesia
- Familiar dengan regulasi OJK, BI, POJK, dan standar pelaporan Indonesia

## Gaya Komunikasi:
- Ringkas, eksekutif, dan berorientasi pada keputusan strategis
- Fokus pada "so what" dan implikasi bisnis bagi Board/Komite Audit
- Menyajikan insight dalam format yang siap dipresentasikan ke Board
- Bahasa Indonesia formal dengan istilah teknis yang dijelaskan

## Prinsip Analisis:
1. **Executive Focus**: Ekstrak hanya insight yang relevan untuk pengambilan keputusan level eksekutif
2. **Risk Prioritization**: Prioritas pada risiko yang memiliki dampak material
3. **Quantification**: Estimasi exposure finansial jika memungkinkan dari data yang tersedia
4. **Sentiment Analysis**: Analisis tone dan kesiapan manajemen dalam merespons temuan"""

EXECUTIVE_INSIGHT_SYSTEM_PROMPT = EXECUTIVE_INSIGHT_PERSONA + """

## Tugas Anda Saat Ini:
Ekstrak insight eksekutif dari dokumen audit/laporan berikut untuk keperluan dashboard Komite Audit.

## Format Output (WAJIB dalam JSON):
{
    "executive_summary": {
        "document_title": "Judul atau nama dokumen yang dianalisis",
        "period_covered": "Periode yang dicakup (jika teridentifikasi)",
        "overall_risk_rating": "LOW/MEDIUM/HIGH/CRITICAL",
        "confidence_level": "HIGH/MEDIUM/LOW"
    },
    "top_3_risks": [
        {
            "rank": 1,
            "risk_title": "Judul risiko (singkat, 5-10 kata)",
            "risk_category": "STRATEGIC/OPERATIONAL/FINANCIAL/COMPLIANCE/TECHNOLOGY/REPUTATIONAL",
            "severity": "LOW/MEDIUM/HIGH/CRITICAL",
            "likelihood": "LOW/MEDIUM/HIGH/VERY_HIGH",
            "description": "Deskripsi risiko dalam 2-3 kalimat",
            "potential_impact": "Dampak potensial terhadap organisasi",
            "affected_areas": ["Area bisnis yang terdampak"],
            "mitigation_status": "NOT_STARTED/IN_PROGRESS/PARTIALLY_ADDRESSED/ADDRESSED",
            "recommended_action": "Tindakan yang direkomendasikan"
        }
    ],
    "financial_exposure": {
        "total_estimated_exposure": {
            "min": null,
            "max": null,
            "currency": "IDR",
            "confidence": "HIGH/MEDIUM/LOW/ESTIMATED",
            "basis": "Dasar estimasi (jika ada)"
        },
        "exposure_breakdown": [
            {
                "category": "Kategori exposure",
                "amount_range": "Rentang nilai (misal: Rp 1-5 miliar)",
                "description": "Penjelasan singkat",
                "materiality": "MATERIAL/SIGNIFICANT/MODERATE/MINOR"
            }
        ],
        "exposure_notes": "Catatan tentang keterbatasan estimasi exposure"
    },
    "management_response_sentiment": {
        "overall_sentiment": "PROACTIVE/RESPONSIVE/NEUTRAL/DEFENSIVE/DISMISSIVE",
        "sentiment_score": 5,
        "indicators": {
            "acknowledgment": "STRONG/MODERATE/WEAK/ABSENT",
            "ownership": "STRONG/MODERATE/WEAK/ABSENT",
            "action_orientation": "STRONG/MODERATE/WEAK/ABSENT",
            "timeline_commitment": "SPECIFIC/GENERAL/VAGUE/ABSENT"
        },
        "sentiment_analysis": "Analisis sentiment dalam 3-4 kalimat",
        "key_quotes": ["Kutipan relevan dari manajemen jika ada"]
    },
    "executive_card_summary": {
        "headline": "Headline 10-15 kata untuk dashboard card",
        "one_liner": "Ringkasan eksekutif dalam 1 kalimat",
        "key_number": "Angka/metrik kunci yang paling penting (misal: 'Rp 2.5T Exposure')",
        "attention_required": "IMMEDIATE/HIGH/MODERATE/MONITOR"
    },
    "data_quality_notes": {
        "completeness": "HIGH/MEDIUM/LOW",
        "data_gaps": ["Area data yang tidak tersedia/tidak lengkap"],
        "assumptions": ["Asumsi yang digunakan dalam analisis"]
    }
}

## Instruksi Penting:
1. Identifikasi TEPAT 3 risiko teratas berdasarkan severity dan likelihood
2. Jika financial exposure tidak dapat diestimasi, set min/max ke null dan jelaskan di notes
3. Sentiment score menggunakan skala 1-10 (1=sangat defensif, 10=sangat proaktif)
4. Executive card summary HARUS ringkas dan siap tampil di dashboard
5. Gunakan bahasa Indonesia profesional
6. Output HARUS valid JSON
7. Jika dokumen bukan laporan audit/risiko, tetap ekstrak insight yang relevan dari konten yang ada"""


class ExecutiveInsightAnalyzer:
    """
    Executive Insight Analyzer Agent
    Extracts top 3 risks, financial exposure, and management sentiment from audit documents
    """

    def __init__(self):
        self.persona = EXECUTIVE_INSIGHT_PERSONA
        self.system_prompt = EXECUTIVE_INSIGHT_SYSTEM_PROMPT
        logger.info("Executive Insight Analyzer Agent initialized")

    async def analyze_document(
        self,
        document_text: str,
        document_metadata: Dict,
        analysis_type: str = "full"
    ) -> Tuple[Dict, int, int]:
        """
        Analyze document and extract executive-level insights

        Args:
            document_text: Full text content of the document
            document_metadata: Document metadata (filename, type, etc.)
            analysis_type: Type of analysis (full, quick, risk_focus)

        Returns:
            Tuple of (insight_result, execution_time_ms, tokens_used)
        """
        from backend.llm_client import llm_client

        start_time = time.time()

        try:
            # Build the analysis prompt
            analysis_prompt = self._build_analysis_prompt(
                document_text,
                document_metadata,
                analysis_type
            )

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": analysis_prompt}
            ]

            # Dynamic max_tokens based on analysis type
            max_tokens_map = {
                "full": 4000,
                "quick": 2000,
                "risk_focus": 2500
            }

            # Generate analysis with JSON mode
            response = await llm_client.generate_completion(
                messages=messages,
                temperature=0.3,  # Lower temperature for factual analysis
                max_tokens=max_tokens_map.get(analysis_type, 4000),
                json_mode=True
            )

            # Parse JSON response
            insight_result = json.loads(response)

            execution_time = int((time.time() - start_time) * 1000)
            tokens_used = llm_client.count_tokens(response)

            logger.info(f"Executive insight analysis completed in {execution_time}ms")
            return insight_result, execution_time, tokens_used

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in executive insight: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

        except Exception as e:
            logger.error(f"Error in executive insight analysis: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

    def _build_analysis_prompt(
        self,
        document_text: str,
        metadata: Dict,
        analysis_type: str
    ) -> str:
        """Build the analysis prompt with document context and dynamic truncation"""

        # Dynamic truncation based on analysis type (fit within Groq TPM limits)
        max_chars_map = {
            "full": 15000,
            "quick": 7000,
            "risk_focus": 10000
        }
        max_chars = max_chars_map.get(analysis_type, 15000)

        if len(document_text) > max_chars:
            document_text = document_text[:max_chars] + \
                "\n\n[... dokumen terpotong karena keterbatasan panjang ...]"

        analysis_instructions = {
            "full": "Lakukan analisis LENGKAP mencakup semua aspek: executive summary, "
                   "top 3 risks dengan detail, financial exposure, sentiment analysis, dan executive card summary.",
            "quick": "Lakukan analisis CEPAT dengan fokus pada top 3 risks dan executive card summary. "
                    "Financial exposure dan sentiment analysis boleh ringkas.",
            "risk_focus": "Fokus pada IDENTIFIKASI RISIKO: top 3 risks dengan detail lengkap. "
                         "Financial exposure dan sentiment analysis ringkas saja."
        }

        prompt = f"""## Informasi Dokumen:
- Nama File: {metadata.get('filename', 'Unknown')}
- Tipe: {metadata.get('file_type', 'Unknown')}
- Kategori: {metadata.get('category', 'Audit Document')}

## Jenis Analisis: {analysis_type.upper()}
{analysis_instructions.get(analysis_type, analysis_instructions['full'])}

## Konten Dokumen:
---
{document_text}
---

Ekstrak insight eksekutif dari dokumen di atas.
Berikan output dalam format JSON sesuai template yang telah ditentukan.
Pastikan output adalah valid JSON yang bisa di-parse."""

        return prompt

    def _generate_fallback_response(self, error: str) -> Dict:
        """Generate fallback response when analysis fails"""
        return {
            "executive_summary": {
                "document_title": "Unknown",
                "period_covered": "Unknown",
                "overall_risk_rating": "UNKNOWN",
                "confidence_level": "LOW"
            },
            "top_3_risks": [
                {
                    "rank": 1,
                    "risk_title": "Analisis Tidak Dapat Diselesaikan",
                    "risk_category": "OPERATIONAL",
                    "severity": "UNKNOWN",
                    "likelihood": "UNKNOWN",
                    "description": "Analisis otomatis tidak dapat diselesaikan karena error teknis.",
                    "potential_impact": "Diperlukan review manual",
                    "affected_areas": ["Unknown"],
                    "mitigation_status": "NOT_STARTED",
                    "recommended_action": "Lakukan analisis ulang atau review manual"
                }
            ],
            "financial_exposure": {
                "total_estimated_exposure": {
                    "min": None,
                    "max": None,
                    "currency": "IDR",
                    "confidence": "LOW",
                    "basis": "Tidak dapat diestimasi"
                },
                "exposure_breakdown": [],
                "exposure_notes": "Analisis exposure tidak dapat diselesaikan"
            },
            "management_response_sentiment": {
                "overall_sentiment": "UNKNOWN",
                "sentiment_score": 5,
                "indicators": {
                    "acknowledgment": "ABSENT",
                    "ownership": "ABSENT",
                    "action_orientation": "ABSENT",
                    "timeline_commitment": "ABSENT"
                },
                "sentiment_analysis": "Analisis sentiment tidak dapat diselesaikan karena error teknis.",
                "key_quotes": []
            },
            "executive_card_summary": {
                "headline": "Analisis Memerlukan Review Manual",
                "one_liner": "Analisis otomatis tidak dapat diselesaikan, diperlukan review manual.",
                "key_number": "N/A",
                "attention_required": "HIGH"
            },
            "data_quality_notes": {
                "completeness": "LOW",
                "data_gaps": ["Analisis tidak dapat diselesaikan"],
                "assumptions": []
            },
            "error": error
        }


# Global instance
executive_insight_analyzer = ExecutiveInsightAnalyzer()

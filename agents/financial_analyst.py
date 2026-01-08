"""
Financial Analyst Agent for RAG Komite Audit System
Senior Expert from McKinsey & Big 4 Consulting
"""
import time
import json
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

FINANCIAL_ANALYST_PERSONA = """Anda adalah **Senior Expert Financial Analyst** dengan pengalaman 15+ tahun di **McKinsey & Company** dan **Big 4 Consulting Firms** (Deloitte, PwC, EY, KPMG).

## Profil Keahlian Anda:
- CFA Charterholder & Certified Public Accountant (CPA)
- Spesialisasi: Financial Statement Analysis, Corporate Valuation, Risk Assessment
- Pengalaman di sektor perbankan, manufaktur, dan perusahaan publik di Indonesia
- Familiar dengan PSAK/IFRS, regulasi OJK, dan standar pelaporan Indonesia

## Gaya Komunikasi:
- Profesional, tegas, dan berbasis data
- Menggunakan terminologi finansial yang tepat dengan penjelasan sederhana
- Memberikan insight strategis yang actionable
- Bahasa Indonesia formal dengan istilah teknis yang dijelaskan

## Prinsip Analisis:
1. **Evidence-Based**: Setiap kesimpulan didukung angka dan data
2. **Risk-Focused**: Identifikasi red flags dan risiko tersembunyi
3. **Strategic View**: Analisis tidak hanya angka, tapi konteks bisnis
4. **Actionable Recommendations**: Rekomendasi konkret dan implementable"""

ANALYSIS_SYSTEM_PROMPT = FINANCIAL_ANALYST_PERSONA + """

## Tugas Anda Saat Ini:
Analisis dokumen keuangan berikut dan berikan laporan analisis komprehensif.

## Format Output (WAJIB dalam JSON):
{
    "executive_summary": {
        "overview": "Ringkasan kondisi keuangan perusahaan dalam 2-3 paragraf",
        "key_findings": ["Temuan utama 1", "Temuan utama 2", "Temuan utama 3"],
        "overall_assessment": "STRONG/MODERATE/WEAK/CRITICAL",
        "confidence_level": "HIGH/MEDIUM/LOW"
    },
    "financial_ratios": {
        "profitability": {
            "roe": {"value": "X%", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "roa": {"value": "X%", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "npm": {"value": "X%", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "gpm": {"value": "X%", "trend": "UP/DOWN/STABLE", "assessment": "text"}
        },
        "liquidity": {
            "current_ratio": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "quick_ratio": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "cash_ratio": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"}
        },
        "solvency": {
            "debt_to_equity": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "debt_to_assets": {"value": "X%", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "interest_coverage": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"}
        },
        "efficiency": {
            "asset_turnover": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "inventory_turnover": {"value": "X.XX", "trend": "UP/DOWN/STABLE", "assessment": "text"},
            "receivable_days": {"value": "X days", "trend": "UP/DOWN/STABLE", "assessment": "text"}
        }
    },
    "risk_assessment": {
        "overall_risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
        "red_flags": [
            {
                "category": "LIQUIDITY/SOLVENCY/PROFITABILITY/OPERATIONAL/FRAUD",
                "severity": "LOW/MEDIUM/HIGH/CRITICAL",
                "description": "Deskripsi red flag",
                "recommendation": "Rekomendasi tindakan"
            }
        ],
        "positive_indicators": ["Indikator positif 1", "Indikator positif 2"],
        "areas_of_concern": ["Area perhatian 1", "Area perhatian 2"]
    },
    "recommendations": {
        "immediate_actions": ["Tindakan segera 1", "Tindakan segera 2"],
        "short_term": ["Rekomendasi jangka pendek 1-6 bulan"],
        "long_term": ["Rekomendasi jangka panjang 6-12 bulan"],
        "for_audit_committee": ["Rekomendasi spesifik untuk Komite Audit"]
    },
    "data_quality_notes": {
        "completeness": "HIGH/MEDIUM/LOW",
        "issues": ["Catatan tentang keterbatasan data"],
        "assumptions": ["Asumsi yang digunakan dalam analisis"]
    }
}

## Instruksi Penting:
1. Jika data rasio tidak tersedia dalam dokumen, tulis "N/A - Data tidak tersedia"
2. Selalu berikan konteks industri jika memungkinkan
3. Identifikasi minimal 3 red flags jika ada indikasi
4. Gunakan bahasa Indonesia profesional
5. Output HARUS valid JSON"""


class FinancialAnalyst:
    """
    Senior Financial Analyst Agent
    Persona: McKinsey & Big 4 Expert
    """

    def __init__(self):
        self.persona = FINANCIAL_ANALYST_PERSONA
        self.system_prompt = ANALYSIS_SYSTEM_PROMPT
        logger.info("Financial Analyst Agent initialized")

    async def analyze_document(
        self,
        document_text: str,
        document_metadata: Dict,
        analysis_type: str = "comprehensive"
    ) -> Tuple[Dict, int, int]:
        """
        Analyze financial document and return structured analysis

        Args:
            document_text: Full text content of the document
            document_metadata: Document metadata (filename, type, etc.)
            analysis_type: Type of analysis (comprehensive, quick, ratio_only)

        Returns:
            Tuple of (analysis_result, execution_time_ms, tokens_used)
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

            # Generate analysis with JSON mode
            response = await llm_client.generate_completion(
                messages=messages,
                temperature=0.3,  # Lower temperature for factual analysis
                max_tokens=4000,  # Longer response for comprehensive analysis
                json_mode=True
            )

            # Parse JSON response
            analysis_result = json.loads(response)

            execution_time = int((time.time() - start_time) * 1000)
            tokens_used = llm_client.count_tokens(response)

            logger.info(f"Financial analysis completed in {execution_time}ms")
            return analysis_result, execution_time, tokens_used

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

        except Exception as e:
            logger.error(f"Error in financial analysis: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

    def _build_analysis_prompt(
        self,
        document_text: str,
        metadata: Dict,
        analysis_type: str
    ) -> str:
        """Build the analysis prompt with document context"""

        # Truncate if too long (LLM context limit)
        max_chars = 50000
        if len(document_text) > max_chars:
            document_text = document_text[:max_chars] + "\n\n[... dokumen terpotong karena keterbatasan panjang ...]"

        analysis_instructions = {
            "comprehensive": "Lakukan analisis finansial LENGKAP mencakup semua aspek: executive summary, rasio keuangan, risk assessment, dan rekomendasi detail.",
            "quick": "Lakukan analisis CEPAT dengan fokus pada executive summary dan temuan utama saja. Rasio dan rekomendasi boleh ringkas.",
            "ratio_only": "Fokus pada KALKULASI RASIO KEUANGAN saja. Executive summary singkat, skip rekomendasi detail."
        }

        prompt = f"""## Informasi Dokumen:
- Nama File: {metadata.get('filename', 'Unknown')}
- Tipe: {metadata.get('file_type', 'Unknown')}
- Kategori: {metadata.get('category', 'Financial Document')}

## Jenis Analisis: {analysis_type.upper()}
{analysis_instructions.get(analysis_type, analysis_instructions['comprehensive'])}

## Konten Dokumen:
---
{document_text}
---

Lakukan analisis finansial berdasarkan konten dokumen di atas.
Berikan output dalam format JSON sesuai template yang telah ditentukan.
Pastikan output adalah valid JSON yang bisa di-parse."""

        return prompt

    def _generate_fallback_response(self, error: str) -> Dict:
        """Generate fallback response when analysis fails"""
        return {
            "executive_summary": {
                "overview": f"Analisis tidak dapat diselesaikan karena error teknis. Silakan coba lagi atau hubungi administrator.",
                "key_findings": ["Analisis gagal - diperlukan review manual"],
                "overall_assessment": "UNKNOWN",
                "confidence_level": "LOW"
            },
            "financial_ratios": {
                "profitability": {},
                "liquidity": {},
                "solvency": {},
                "efficiency": {}
            },
            "risk_assessment": {
                "overall_risk_level": "UNKNOWN",
                "red_flags": [],
                "positive_indicators": [],
                "areas_of_concern": ["Analisis otomatis tidak dapat diselesaikan"]
            },
            "recommendations": {
                "immediate_actions": ["Lakukan analisis ulang atau review manual"],
                "short_term": [],
                "long_term": [],
                "for_audit_committee": ["Pertimbangkan review manual oleh tim keuangan"]
            },
            "data_quality_notes": {
                "completeness": "LOW",
                "issues": [f"Error teknis: {error}"],
                "assumptions": []
            },
            "error": error
        }


# Global instance
financial_analyst = FinancialAnalyst()

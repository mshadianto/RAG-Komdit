"""
Risk-Audit Mapper Agent for RAG Komite Audit System
Strategic Risk-to-Audit Mapping & Gap Analysis
"""
import time
import json
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

RISK_AUDIT_MAPPER_PERSONA = """Anda adalah **Senior Risk & Audit Strategy Consultant** dengan pengalaman 20+ tahun di bidang internal audit, enterprise risk management, dan tata kelola perusahaan di Indonesia.

## Profil Keahlian Anda:
- Certified Internal Auditor (CIA) & Certified Risk Management Assurance (CRMA)
- Spesialisasi: Risk-Based Audit Planning, Enterprise Risk Management (ERM), Audit Universe Mapping
- Pengalaman di sektor BUMN, perbankan, dan perusahaan publik di Indonesia
- Familiar dengan SPPIA (Standar Profesi Praktik Internal Audit), COSO ERM Framework, ISO 31000
- Ahli dalam penyusunan PKPT berbasis risiko dan evaluasi cakupan audit

## Gaya Komunikasi:
- Sistematis, terstruktur, dan berorientasi pada gap analysis
- Menggunakan terminologi audit dan risk management yang tepat
- Memberikan rekomendasi prioritas yang actionable
- Bahasa Indonesia formal dengan istilah teknis yang dijelaskan

## Prinsip Analisis:
1. **Risk-Based**: Setiap risiko dipetakan terhadap program audit yang ada
2. **Gap-Focused**: Identifikasi area risiko yang belum tercakup audit
3. **Priority-Driven**: Prioritas berdasarkan severity risiko dan ketersediaan sumber daya audit
4. **Strategic Alignment**: Memastikan PKPT selaras dengan profil risiko organisasi"""

RISK_MAPPING_SYSTEM_PROMPT = RISK_AUDIT_MAPPER_PERSONA + """

## Tugas Anda Saat Ini:
Analisis dokumen Risk Register dan PKPT (Program Kerja Pengawasan Tahunan) berikut, lalu petakan risiko terhadap program audit untuk mengidentifikasi gap strategis.

## Format Output (WAJIB dalam JSON):
{
    "executive_summary": {
        "overview": "Ringkasan hasil pemetaan risiko terhadap audit plan dalam 2-3 paragraf",
        "total_risks_identified": 0,
        "total_audit_programs": 0,
        "coverage_percentage": "X%",
        "critical_gaps_count": 0,
        "overall_alignment": "STRONG/MODERATE/WEAK/CRITICAL",
        "confidence_level": "HIGH/MEDIUM/LOW"
    },
    "risk_register_summary": [
        {
            "risk_id": "R-001",
            "risk_name": "Nama risiko",
            "risk_category": "STRATEGIC/OPERATIONAL/FINANCIAL/COMPLIANCE/TECHNOLOGY/ESG",
            "likelihood": "LOW/MEDIUM/HIGH/VERY_HIGH",
            "impact": "LOW/MEDIUM/HIGH/VERY_HIGH",
            "inherent_risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
            "risk_owner": "Unit/departemen pemilik risiko",
            "existing_controls": "Deskripsi kontrol yang ada"
        }
    ],
    "audit_plan_summary": [
        {
            "audit_id": "A-001",
            "audit_name": "Nama program audit",
            "audit_type": "ASSURANCE/CONSULTING/SPECIAL/FOLLOW_UP",
            "auditable_entity": "Unit/area yang diaudit",
            "planned_period": "Q1/Q2/Q3/Q4 atau bulan",
            "audit_objective": "Tujuan audit",
            "estimated_days": 0
        }
    ],
    "coverage_matrix": [
        {
            "risk_id": "R-001",
            "risk_name": "Nama risiko",
            "risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
            "mapped_audit_ids": ["A-001", "A-003"],
            "mapped_audit_names": ["Audit X", "Audit Y"],
            "coverage_status": "FULLY_COVERED/PARTIALLY_COVERED/NOT_COVERED",
            "coverage_quality": "DIRECT/INDIRECT/TANGENTIAL",
            "coverage_notes": "Penjelasan bagaimana audit mencakup risiko ini"
        }
    ],
    "gap_analysis": {
        "uncovered_risks": [
            {
                "risk_id": "R-005",
                "risk_name": "Nama risiko",
                "risk_level": "HIGH/CRITICAL",
                "gap_severity": "CRITICAL/HIGH/MEDIUM/LOW",
                "reason": "Penjelasan mengapa risiko ini tidak tercakup",
                "potential_impact": "Dampak jika risiko tidak diaudit",
                "recommended_audit_response": "Rekomendasi program audit yang perlu ditambahkan"
            }
        ],
        "partially_covered_risks": [
            {
                "risk_id": "R-003",
                "risk_name": "Nama risiko",
                "risk_level": "HIGH",
                "current_coverage": "Penjelasan cakupan saat ini",
                "coverage_gap": "Aspek yang belum tercakup",
                "recommended_enhancement": "Rekomendasi peningkatan cakupan"
            }
        ],
        "over_audited_areas": [
            {
                "area": "Nama area/risiko",
                "audit_count": 0,
                "mapped_audits": ["A-001", "A-002"],
                "recommendation": "Rekomendasi optimasi"
            }
        ]
    },
    "recommendations": {
        "immediate_actions": [
            {
                "priority": 1,
                "action": "Deskripsi tindakan",
                "target_risk": "R-005",
                "estimated_resources": "X hari audit",
                "rationale": "Alasan prioritas"
            }
        ],
        "pkpt_adjustments": [
            "Rekomendasi penyesuaian PKPT"
        ],
        "resource_optimization": [
            "Rekomendasi optimasi sumber daya audit"
        ],
        "for_audit_committee": [
            "Rekomendasi spesifik untuk Komite Audit"
        ]
    },
    "data_quality_notes": {
        "risk_register_completeness": "HIGH/MEDIUM/LOW",
        "audit_plan_completeness": "HIGH/MEDIUM/LOW",
        "mapping_confidence": "HIGH/MEDIUM/LOW",
        "issues": ["Catatan tentang keterbatasan data"],
        "assumptions": ["Asumsi yang digunakan dalam analisis"]
    }
}

## Instruksi Penting:
1. Ekstrak SEMUA risiko dari Risk Register dan SEMUA program audit dari PKPT
2. Petakan setiap risiko terhadap program audit yang relevan
3. Identifikasi risiko yang tidak tercakup (terutama risiko HIGH dan CRITICAL)
4. Perhatikan kualitas cakupan: langsung (direct) vs tidak langsung (indirect)
5. Prioritaskan rekomendasi berdasarkan severity gap
6. Jika data tidak lengkap, catat di data_quality_notes
7. Gunakan bahasa Indonesia profesional
8. Output HARUS valid JSON"""


class RiskAuditMapper:
    """
    Strategic Risk-to-Audit Mapping Agent
    Maps risk register items against PKPT audit programs to identify coverage gaps
    """

    def __init__(self):
        self.persona = RISK_AUDIT_MAPPER_PERSONA
        self.system_prompt = RISK_MAPPING_SYSTEM_PROMPT
        logger.info("Risk Audit Mapper Agent initialized")

    async def analyze_mapping(
        self,
        risk_register_text: str,
        audit_plan_text: str,
        risk_register_metadata: Dict,
        audit_plan_metadata: Dict,
        mapping_type: str = "comprehensive"
    ) -> Tuple[Dict, int, int]:
        """
        Analyze risk register against audit plan and return gap analysis

        Args:
            risk_register_text: Full text of risk register document
            audit_plan_text: Full text of PKPT/audit plan document
            risk_register_metadata: Risk register document metadata
            audit_plan_metadata: Audit plan document metadata
            mapping_type: Type of mapping (comprehensive, quick, gap_only)

        Returns:
            Tuple of (mapping_result, execution_time_ms, tokens_used)
        """
        from backend.llm_client import llm_client

        start_time = time.time()

        try:
            analysis_prompt = self._build_mapping_prompt(
                risk_register_text,
                audit_plan_text,
                risk_register_metadata,
                audit_plan_metadata,
                mapping_type
            )

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": analysis_prompt}
            ]

            response = await llm_client.generate_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=4000,
                json_mode=True
            )

            mapping_result = json.loads(response)

            execution_time = int((time.time() - start_time) * 1000)
            tokens_used = llm_client.count_tokens(response)

            logger.info(f"Risk-audit mapping completed in {execution_time}ms")
            return mapping_result, execution_time, tokens_used

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in risk mapping: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

        except Exception as e:
            logger.error(f"Error in risk-audit mapping: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return self._generate_fallback_response(str(e)), execution_time, 0

    def _build_mapping_prompt(
        self,
        risk_register_text: str,
        audit_plan_text: str,
        risk_metadata: Dict,
        audit_metadata: Dict,
        mapping_type: str
    ) -> str:
        """Build the mapping analysis prompt with both document contexts"""

        max_chars_per_doc = 25000
        if len(risk_register_text) > max_chars_per_doc:
            risk_register_text = risk_register_text[:max_chars_per_doc] + \
                "\n\n[... dokumen terpotong karena keterbatasan panjang ...]"
        if len(audit_plan_text) > max_chars_per_doc:
            audit_plan_text = audit_plan_text[:max_chars_per_doc] + \
                "\n\n[... dokumen terpotong karena keterbatasan panjang ...]"

        mapping_instructions = {
            "comprehensive": "Lakukan pemetaan LENGKAP mencakup semua aspek: executive summary, "
                           "coverage matrix, gap analysis, dan rekomendasi detail.",
            "quick": "Lakukan pemetaan CEPAT dengan fokus pada risiko HIGH/CRITICAL yang tidak "
                   "tercakup. Summary dan rekomendasi boleh ringkas.",
            "gap_only": "Fokus pada IDENTIFIKASI GAP saja. Tampilkan hanya risiko yang "
                      "NOT_COVERED dan PARTIALLY_COVERED."
        }

        prompt = f"""## Dokumen 1: Risk Register
- Nama File: {risk_metadata.get('filename', 'Unknown')}
- Tipe: {risk_metadata.get('file_type', 'Unknown')}
- Kategori: {risk_metadata.get('category', 'Risk Register')}

### Konten Risk Register:
---
{risk_register_text}
---

## Dokumen 2: PKPT (Program Kerja Pengawasan Tahunan)
- Nama File: {audit_metadata.get('filename', 'Unknown')}
- Tipe: {audit_metadata.get('file_type', 'Unknown')}
- Kategori: {audit_metadata.get('category', 'Audit Plan')}

### Konten PKPT:
---
{audit_plan_text}
---

## Jenis Pemetaan: {mapping_type.upper()}
{mapping_instructions.get(mapping_type, mapping_instructions['comprehensive'])}

Lakukan pemetaan risiko terhadap program audit berdasarkan kedua dokumen di atas.
Berikan output dalam format JSON sesuai template yang telah ditentukan.
Pastikan output adalah valid JSON yang bisa di-parse."""

        return prompt

    def _generate_fallback_response(self, error: str) -> Dict:
        """Generate fallback response when mapping fails"""
        return {
            "executive_summary": {
                "overview": "Pemetaan tidak dapat diselesaikan karena error teknis. "
                          "Silakan coba lagi atau hubungi administrator.",
                "total_risks_identified": 0,
                "total_audit_programs": 0,
                "coverage_percentage": "N/A",
                "critical_gaps_count": 0,
                "overall_alignment": "UNKNOWN",
                "confidence_level": "LOW"
            },
            "risk_register_summary": [],
            "audit_plan_summary": [],
            "coverage_matrix": [],
            "gap_analysis": {
                "uncovered_risks": [],
                "partially_covered_risks": [],
                "over_audited_areas": []
            },
            "recommendations": {
                "immediate_actions": [],
                "pkpt_adjustments": ["Lakukan pemetaan ulang atau review manual"],
                "resource_optimization": [],
                "for_audit_committee": [
                    "Pertimbangkan review manual oleh tim internal audit"
                ]
            },
            "data_quality_notes": {
                "risk_register_completeness": "LOW",
                "audit_plan_completeness": "LOW",
                "mapping_confidence": "LOW",
                "issues": [f"Error teknis: {error}"],
                "assumptions": []
            },
            "error": error
        }


# Global instance
risk_audit_mapper = RiskAuditMapper()

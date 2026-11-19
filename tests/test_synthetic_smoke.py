"""
Synthetic Smoke & Data Integrity Tests for STEP-002 Verification.
Uses standard Python library constructs to verify tabular structures,
synthetic ECG waveform generation, and .gitignore exclusion patterns.
"""

import math
import os
import unittest


class TestSyntheticDataFixtures(unittest.TestCase):
    def test_tabular_fixture_structure(self):
        """Verify mock patient-level record containing all four proposal modalities."""
        mock_patient = {
            "patient_id": "PAT00000001",
            "encounter_id": "ENC00000001",
            "clinical": {
                "age": 55,
                "sex": 1,
                "systolic_bp": 135.0,
                "diastolic_bp": 85.0,
            },
            "ecg": {
                "heart_rate": 72.0,
                "pr_interval": 160.0,
                "qrs_duration": 90.0,
                "qt_interval": 400.0,
            },
            "laboratory": {
                "total_cholesterol": 210.0,
                "fasting_glucose": 105.0,
                "troponin_i": 0.01,
            },
            "lifestyle": {
                "smoking_status": 1,
                "physical_activity_hours": 2.5,
                "diet_score": 7.0,
            },
            "outcome_cvd": 1,
        }

        # Check required keys
        self.assertIn("clinical", mock_patient)
        self.assertIn("ecg", mock_patient)
        self.assertIn("laboratory", mock_patient)
        self.assertIn("lifestyle", mock_patient)
        self.assertEqual(mock_patient["outcome_cvd"], 1)

    def test_synthetic_ecg_sine_waveform(self):
        """Verify generation of synthetic 10-second 12-lead ECG sine-wave buffer at 500 Hz."""
        sampling_rate = 500  # Hz
        duration_sec = 10  # seconds
        num_samples = sampling_rate * duration_sec
        num_leads = 12

        # Generate synthetic sine-wave cardiac oscillation (fundamental freq 1.2 Hz ~ 72 bpm)
        freq = 1.2
        waveform = []
        for lead in range(num_leads):
            phase = (lead * math.pi) / 6.0
            lead_signal = [
                math.sin(2 * math.pi * freq * (t / sampling_rate) + phase)
                for t in range(num_samples)
            ]
            waveform.append(lead_signal)

        self.assertEqual(len(waveform), num_leads)
        self.assertEqual(len(waveform[0]), num_samples)
        # Check amplitude bounded in [-1.0, 1.0]
        self.assertTrue(all(-1.0 <= val <= 1.0 for val in waveform[0][:100]))

    def test_gitignore_contains_critical_phi_patterns(self):
        """Verify that .gitignore file exists and strictly excludes raw formats, PDFs, and weights."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        gitignore_path = os.path.join(repo_root, ".gitignore")
        self.assertTrue(os.path.isfile(gitignore_path), ".gitignore must exist in root")

        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()

        critical_patterns = [
            "raw/",
            "processed/",
            "*.edf",
            "*.xml",
            "*.dcm",
            "*.mat",
            "*.pt",
            "*.pth",
            "*.ckpt",
            "*.pdf",
            "fydp_title_proposal.pdf",
        ]
        for pattern in critical_patterns:
            self.assertIn(
                pattern,
                content,
                f"Missing critical exclusion pattern in .gitignore: {pattern}",
            )


if __name__ == "__main__":
    unittest.main()

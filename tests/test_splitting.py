"""
Unit tests verifying STEP-020 deterministic patient-grouped splitting and zero-leakage invariants.
"""

import unittest

from src.cvd_mm.splitting import (
    DEFAULT_SPLIT_SEED,
    assert_zero_patient_overlap,
    assign_patient_grouped_splits,
    compute_balance_summary,
)


class TestPatientGroupedSplitting(unittest.TestCase):
    def test_multi_visit_patients_never_cross_partitions_and_reproducible(self):
        rows = []
        # Create 60 patients: first 10 patients have 3 ED visits each!
        rec = 1
        for p_idx in range(60):
            n_visits = 3 if p_idx < 10 else 1
            y_val = "1" if p_idx % 2 == 0 else "0"
            sex_val = "F" if p_idx % 3 == 0 else "M"
            mod_val = "C+E_png+L" if p_idx % 5 != 0 else "C+L_[MISSING_ECG]"
            for _ in range(n_visits):
                rows.append({
                    "RecordID": f"R{rec:04d}",
                    "PatientGroupID": f"PAT_{p_idx:03d}",
                    "Target_y_ed_initial": y_val,
                    "sex": sex_val,
                    "age_years": str(40 + (p_idx % 30)),
                    "ModalitiesPresent": mod_val,
                })
                rec += 1

        m1 = assign_patient_grouped_splits(rows, ds_id="DS0002", target_col="Target_y_ed_initial", seed=DEFAULT_SPLIT_SEED)
        m2 = assign_patient_grouped_splits(rows, ds_id="DS0002", target_col="Target_y_ed_initial", seed=DEFAULT_SPLIT_SEED)
        self.assertEqual(m1, m2, "Splitting must be bit-for-bit deterministic for identical seed!")

        proof = assert_zero_patient_overlap(m1)
        self.assertEqual(proof["train_val_overlap"], 0)
        self.assertEqual(proof["train_test_overlap"], 0)
        self.assertEqual(proof["val_test_overlap"], 0)
        self.assertEqual(proof["cv_fold_overlap"], 0)

        # Verify each multi-visit patient sits wholly in one partition
        part_by_pat = {}
        for r in m1:
            part_by_pat.setdefault(r["PatientGroupID"], set()).add(r["Partition"])
        for pat, parts in part_by_pat.items():
            self.assertEqual(len(parts), 1, f"Patient {pat} leaked across partitions {parts}")

        bal = compute_balance_summary(m1)["DS0002"]
        total_enc = sum(bal[p]["encounters"] for p in ("train", "val", "test"))
        self.assertEqual(total_enc, len(rows))
        self.assertGreater(bal["train"]["encounters"], bal["val"]["encounters"])
        self.assertGreater(bal["train"]["encounters"], bal["test"]["encounters"])
        # Ensure 'MISSING_ECG' substring never falsely triggers HasLifestyle=1!
        self.assertEqual(sum(bal[p]["has_s"] for p in ("train", "val", "test")), 0)

    def test_large_scale_stratified_ratios_hold_at_70_15_15(self):
        rows = [
            {
                "RecordID": f"S{i}",
                "PatientGroupID": f"P{i}",
                "Target_y_sul_cardio": str(i % 2),
                "sex": "F" if i % 3 == 0 else "M",
                "age_years": "52.0",
                "ModalitiesPresent": "C+L_ord+S_[MISSING_ECG]",
            }
            for i in range(2000)
        ]
        m = assign_patient_grouped_splits(rows, ds_id="DS0004", target_col="Target_y_sul_cardio", seed=DEFAULT_SPLIT_SEED)
        bal = compute_balance_summary(m)["DS0004"]
        self.assertAlmostEqual(bal["train"]["encounters"] / 2000.0, 0.70, delta=0.015)
        self.assertAlmostEqual(bal["val"]["encounters"] / 2000.0, 0.15, delta=0.015)
        self.assertAlmostEqual(bal["test"]["encounters"] / 2000.0, 0.15, delta=0.015)
        self.assertAlmostEqual(bal["train"]["pos_pct"], 50.0, delta=1.5)
        self.assertAlmostEqual(bal["test"]["pos_pct"], 50.0, delta=1.5)

    def test_ptbxl_official_strat_fold_mapping_and_leak_detection(self):
        ptb_rows = [
            {"RecordID": "1", "PatientGroupID": "P1", "StratFold": "1", "Target_y_ptb_nonnorm": "0", "sex": "F", "age_years": "55", "ModalitiesPresent": "C_partial+E_wfdb"},
            {"RecordID": "2", "PatientGroupID": "P1", "StratFold": "1", "Target_y_ptb_nonnorm": "0", "sex": "F", "age_years": "55", "ModalitiesPresent": "C_partial+E_wfdb"},
            {"RecordID": "3", "PatientGroupID": "P2", "StratFold": "9", "Target_y_ptb_nonnorm": "1", "sex": "M", "age_years": "62", "ModalitiesPresent": "C_partial+E_wfdb"},
            {"RecordID": "4", "PatientGroupID": "P3", "StratFold": "10", "Target_y_ptb_nonnorm": "1", "sex": "M", "age_years": "70", "ModalitiesPresent": "C_partial+E_wfdb"},
        ]
        manifest = assign_patient_grouped_splits(ptb_rows, ds_id="DS0001", target_col="Target_y_ptb_nonnorm")
        by_id = {r["RecordID"]: r["Partition"] for r in manifest}
        self.assertEqual(by_id["1"], "train")
        self.assertEqual(by_id["2"], "train")
        self.assertEqual(by_id["3"], "val")
        self.assertEqual(by_id["4"], "test")

        # Cross-fold patient between fold 8 (train) and fold 10 (test) MUST raise AssertionError
        bad_ptb = [
            {"RecordID": "1", "PatientGroupID": "P_LEAK", "StratFold": "8", "Target_y_ptb_nonnorm": "0", "sex": "F", "age_years": "55", "ModalitiesPresent": "C_partial+E_wfdb"},
            {"RecordID": "2", "PatientGroupID": "P_LEAK", "StratFold": "10", "Target_y_ptb_nonnorm": "1", "sex": "F", "age_years": "55", "ModalitiesPresent": "C_partial+E_wfdb"},
        ]
        with self.assertRaises(AssertionError):
            assign_patient_grouped_splits(bad_ptb, ds_id="DS0001", target_col="Target_y_ptb_nonnorm")

    def test_assert_zero_patient_overlap_catches_injected_test_leak(self):
        manifest = [
            {"DS": "DS0003", "RecordID": "R1", "PatientGroupID": "P1", "GroupKey": "DS0003::P1", "Partition": "train", "CVFoldInTrain": "0"},
            {"DS": "DS0003", "RecordID": "R2", "PatientGroupID": "P1", "GroupKey": "DS0003::P1", "Partition": "test", "CVFoldInTrain": "-1"},
        ]
        with self.assertRaises(AssertionError):
            assert_zero_patient_overlap(manifest)


if __name__ == "__main__":
    unittest.main()

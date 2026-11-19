"""
Script to initialize all 22 Appendix B CSV registries across domain folders.
Ensures correct headers and common governance columns:
Owner,Version,Status,Created,Updated,EvidencePath
"""

import os

COMMON_COLS = ["Owner", "Version", "Status", "Created", "Updated", "EvidencePath"]

REGISTRIES = [
    {
        "path": "01_Project_Management/decisions.csv",
        "key": "DEC",
        "domain_cols": ["DEC", "UD", "Question", "Decision", "Approver", "ApprovalDate", "BlocksStep", "OptionsEvidence", "Supersedes", "AffectedGates"],
        "preserve_if_exists": True
    },
    {
        "path": "01_Project_Management/risk_register.csv",
        "key": "RISK",
        "domain_cols": ["RISK", "Description", "Category", "Trigger", "Probability", "Impact", "Mitigation", "Contingency", "ReviewDate"],
        "preserve_if_exists": False,
        "initial_rows": [
            ["RISK0001", "IRB/hospital approval delay or insufficient primary cohort enrollment", "Ethical/Cohort", "Delay exceeding 4 weeks post-S04", "Medium", "High", "Initiate early submission at STEP-011; screen external public cohorts (MIMIC-IV-ECG/PTB-XL) under UD06 as backup", "Adopt external validation cohort under UD06/UD26", "2026-11-20", "Mohammad Nafis Sadiq", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0002", "Cross-sectional vs longitudinal CVD endpoint and horizon mismatch", "Clinical/Schema", "Inconsistent follow-up timestamps", "Low", "Critical", "Formulate precise endpoint charter at STEP-014 with qualified cardiologist sign-off", "Bound claims to early risk detection rather than lifetime incidence", "2026-11-20", "Mohammad Nafis Sadiq", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0003", "Post-diagnosis feature leakage or pre-split transform leakage", "Methodology", "Preprocessing before train/test split", "Medium", "Critical", "Strict separation of record-local cleaning from training-fitted scalers/imputers (FitStateHash)", "Enforce automated leakage unit tests at G07-G08", "2026-11-20", "Rayan Ahmed", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0004", "Heterogeneous or noisy ECG signal formats and filter distortion of ST-T complexes", "Signal/Preprocessing", "ECG filter attenuates clinical waves", "Medium", "High", "Standardize lead specs; mandate cardiologist morphology check before release", "Adjust notch/bandpass cutoff and document filter frequency response", "2026-11-20", "Rayan Ahmed", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0005", "Small-N Transformer multimodal overfitting vs strong tabular GBDT baselines", "Modeling", "Transformer validation loss diverges", "High", "Medium", "Implement 4-tier baseline hierarchy (LR, RF, SVM, XGBoost, CNN, LSTM); pretraining/regularization", "Report findings honestly as rigorous Q1 comparative benchmarking even if baseline wins", "2026-11-20", "Rayan Ahmed", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0006", "Uncalibrated risk probabilities or spurious non-clinical shortcuts in SHAP", "Evaluation/XAI", "Attribution dominated by site ID or missingness", "Medium", "High", "Validation-only calibration (Brier/ECE/DCA); mandatory deletion/insertion faithfulness (AOPC) benchmarks", "Isolate shortcut variable and retrain; disclose limitations in PROBAST audit", "2026-11-20", "Rayan Ahmed", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0007", "Protected Health Information (PHI) exposure or artifact corruption", "Security/Governance", "Accidental staging of clinical CSVs/ECG headers", "Low", "Critical", "Enforce Four-Tier storage model; strict .gitignore; diff inspection before every commit", "Execute immediate history purge and security protocol under OS §11.4", "2026-11-20", "Mohammad Nafis Sadiq", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"],
            ["RISK0008", "Unsubstantiated novelty or missing TRIPOD+AI items causing Q1 peer-review desk rejection", "Literature/Writing", "Prior art refutes proposal gaps", "Medium", "High", "Zero-seed PRISMA systematic literature review; 100% verified citations; complete TRIPOD+AI checklist", "Refine gap statement to specific unimodal-vs-multimodal marginal value in South Asian cohort", "2026-11-20", "Rayan Ahmed", "v0.1.0", "Open", "2026-11-20T02:00:00+06:00", "2026-11-20T02:00:00+06:00", "01_Project_Management/risk_register.csv"]
        ]
    },
    {
        "path": "01_Project_Management/gates.csv",
        "key": "AssessmentID",
        "domain_cols": ["AssessmentID", "GateID", "DocumentOrEntityScope", "EntityVersions", "Outcome", "CriteriaReport", "Assessor", "HumanApprover", "AssessmentDate", "Supersedes", "Invalidates"],
        "preserve_if_exists": True
    },
    {
        "path": "02_Literature/papers.csv",
        "key": "P",
        "domain_cols": ["P", "Title", "Authors", "Year", "Venue", "DOI", "PMID", "SourceURL", "Access", "FullTextPath", "MetadataVerified", "ReadingStatus", "CohortCountry", "SampleSize", "Modalities", "ECGFormat", "EndpointHorizon", "FusionModel", "XAIUsed", "XAIEvaluated", "PROBASTRisk", "CitationKey"],
        "preserve_if_exists": False
    },
    {
        "path": "02_Literature/screening.csv",
        "key": "SCR",
        "domain_cols": ["SCR", "PaperID", "SearchRecord", "Stage", "RelevanceGroup", "Decision", "ExclusionReason", "Reviewer", "ConflictResolution", "DuplicateOf"],
        "preserve_if_exists": False
    },
    {
        "path": "02_Literature/gaps.csv",
        "key": "GAP",
        "domain_cols": ["GAP", "ProposalGap", "Statement", "SupportingPapers", "ContradictingPapers", "SearchCoverage", "SharpenedQ1Framing", "Feasibility", "ApprovedRQ", "DecisionRecord"],
        "preserve_if_exists": False
    },
    {
        "path": "02_Literature/claims.csv",
        "key": "CLAIM",
        "domain_cols": ["CLAIM", "Statement", "Scope", "PaperIDs", "SourceLocators", "ExperimentIDs", "EvaluationIDs", "XAIIDs", "AssetIDs", "Contradictions", "Uncertainty", "Verification", "WritingIDs"],
        "preserve_if_exists": False
    },
    {
        "path": "03_Datasets_Cohort/sites.csv",
        "key": "SITE",
        "domain_cols": ["SITE", "Name", "SourceType", "Country", "RecruitmentMode", "IRBApprovalID", "PermissionRecord", "ConsentOrWaiver", "ModalitiesAvailable", "ECGFormat", "EstimatedN", "SelectionDecision"],
        "preserve_if_exists": False
    },
    {
        "path": "03_Datasets_Cohort/datasets.csv",
        "key": "DS",
        "domain_cols": ["DS", "SiteIDs", "SourceVersion", "IRBRecord", "DUARecord", "ManifestHash", "PatientCount", "EncounterCount", "EventCount", "Prevalence", "Complete4ModalityCount", "ECGQualityPassCount", "CardPath", "RestrictedLocation"],
        "preserve_if_exists": False
    },
    {
        "path": "03_Datasets_Cohort/releases.csv",
        "key": "REL",
        "domain_cols": ["REL", "DatasetID", "AdjudicationID", "VariablesHash", "SplitID", "PreprocessingID", "FitStateHash", "ManifestHash", "PatientCount", "EncounterCount", "EventCount", "ModalitiesIncluded", "RestrictedLocation", "ParentRelease", "ChangeReason"],
        "preserve_if_exists": False
    },
    {
        "path": "04_Outcome_Schema_QA/variables.csv",
        "key": "VAR",
        "domain_cols": ["VAR", "Modality", "VariableName", "DataType", "Unit", "ValidRange", "CodingMap", "Instrument", "TimingRelativeToIndex", "IncorporationBiasRisk", "MissingPolicy", "PROBASTNotes", "Approver"],
        "preserve_if_exists": False
    },
    {
        "path": "04_Outcome_Schema_QA/adjudication_registry.csv",
        "key": "ADJ",
        "domain_cols": ["ADJ", "DatasetID", "EndpointCharterVersion", "VariablesHash", "ECGContractVersion", "BatchIDs", "Abstractors", "CardiologistReviewer", "PilotKappa", "PilotICC", "AdjudicatedCount", "UncertainExcludedCount", "NativeHash", "VerifiedHash", "QAReport", "ParentVersion"],
        "preserve_if_exists": False
    },
    {
        "path": "05_Preprocessing_Alignment/preprocessing_registry.csv",
        "key": "PP",
        "domain_cols": ["PP", "InputManifest", "RecordLocalOps", "TrainFittedOps", "ECGFilterSpec", "ECGMorphologyApprover", "ImputationRule", "MissingMaskPolicy", "ConfigPath", "ConfigHash", "FitPartition", "FitStateHash", "CodeRevision", "LeakageTestReport", "OutputManifest"],
        "preserve_if_exists": False
    },
    {
        "path": "06_Models_Fusion/candidates.csv",
        "key": "MC",
        "domain_cols": ["MC", "Tier", "ModelFamily", "Framework", "FrameworkVersion", "Architecture", "ModalityInputs", "PretrainedOrigin", "License", "ComputeFeasibility", "MissingModalitySupport", "Limitations", "SelectionDecision"],
        "preserve_if_exists": False
    },
    {
        "path": "06_Models_Fusion/model_registry.csv",
        "key": "MODEL",
        "domain_cols": ["MODEL", "CandidateID", "Tier", "ExperimentID", "RunID", "CheckpointID", "ReleaseID", "VariablesHash", "PreprocessingID", "FitStateHash", "ParamCount", "CalibratorHash", "ThresholdVal", "ArtifactLocation", "CardPath", "EvaluationIDs", "XAIIDs", "IntendedUse"],
        "preserve_if_exists": False
    },
    {
        "path": "07_Experiments/experiment_registry.csv",
        "key": "EXP",
        "domain_cols": ["EXP", "RQ", "ComparisonBlock", "Tier", "ParentBaselineEXP", "ActiveModalities", "ReleaseID", "ModelCandidate", "ConfigPath", "ConfigHash", "SourceCommit", "Seed", "RunIDs", "Start", "End", "StoppingReason", "ValROCAUC", "ValPRAUC", "ValBrier", "FailureReport", "Conclusion"],
        "preserve_if_exists": False
    },
    {
        "path": "08_Checkpoints/checkpoint_registry.csv",
        "key": "CKPT",
        "domain_cols": ["CKPT", "ExperimentID", "RunID", "EpochStep", "Role", "StateComponents", "ConfigHash", "ModelHash", "ArtifactPath", "SHA256", "Bytes", "BackupPath", "RestoreEvidence"],
        "preserve_if_exists": False
    },
    {
        "path": "09_Evaluation_Stats/evaluation_registry.csv",
        "key": "EVAL",
        "domain_cols": ["EVAL", "ExperimentID", "ModelID", "CheckpointID", "ReleaseID", "Partition", "ProtocolHash", "FreezeRecord", "CalibratorHash", "ThresholdUsed", "PredictionHash", "MetricPath", "CalibrationPath", "DCAPath", "StatsPath", "SubgroupPath", "ErrorPROBASTPath", "ReportPath", "Deviations", "ParentEvaluation"],
        "preserve_if_exists": False
    },
    {
        "path": "10_Explainability_XAI/xai_registry.csv",
        "key": "XAI",
        "domain_cols": ["XAI", "ModelID", "EvaluationID", "ReleaseID", "ExplainerType", "BackgroundPartition", "BackgroundHash", "AdditivityError", "DeletionAOPC", "InsertionAOPC", "RandomControlAOPC", "LOMOConcordance", "SeedStabilityRho", "ShortcutAuditOutcome", "ClinicianReviewPath", "ReportPath"],
        "preserve_if_exists": False
    },
    {
        "path": "11_Figures_Tables/assets.csv",
        "key": "AssetID",
        "domain_cols": ["AssetID", "Kind", "SourceIDs", "DataHash", "SpecPath", "GeneratorCommand", "CodeRevision", "OutputPath", "ResolutionFormat", "Caption", "Units", "PHICheck", "VisualReview", "WritingIDs"],
        "preserve_if_exists": False
    },
    {
        "path": "12_Writing/writing_registry.csv",
        "key": "WR",
        "domain_cols": ["WR", "Document", "Section", "Topic", "ClaimIDs", "PaperIDs", "EvaluationIDs", "XAIIDs", "AssetIDs", "TRIPODItems", "DraftPath", "Reviewer", "ReviewState", "Revision", "MissingEvidence"],
        "preserve_if_exists": False
    },
    {
        "path": "16_Archive/archive_manifest.csv",
        "key": "ArchiveItemID",
        "domain_cols": ["ArchiveItemID", "ArchiveID", "ReleaseTag", "ItemType", "SourcePath", "StoredLocation", "ArchiveVersion", "SHA256", "Bytes", "PHISensitivity", "License", "Retention", "RestoreEvidence", "SubmissionReceipt"],
        "preserve_if_exists": False
    }
]

import csv

def main():
    root = "e:/FYDP"
    for reg in REGISTRIES:
        full_path = os.path.join(root, reg["path"])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        if reg.get("preserve_if_exists") and os.path.exists(full_path):
            print(f"Preserving existing registry: {reg['path']}")
            continue
            
        columns = reg["domain_cols"] + COMMON_COLS
        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            
            if "initial_rows" in reg:
                for row in reg["initial_rows"]:
                    writer.writerow(row)
                    
        print(f"Initialized registry: {reg['path']}")

if __name__ == "__main__":
    main()

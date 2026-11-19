"""
Repository, CSV Registry, and Template Integrity Validator.
Enforces OS Appendix B schema contracts, template completeness, and PHI gitignore exclusion rules.
"""

import csv
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

COMMON_COLS = ["Owner", "Version", "Status", "Created", "Updated", "EvidencePath"]

REGISTRIES_SCHEMA = {
    "01_Project_Management/decisions.csv": ["DEC", "UD", "Question", "Decision", "Approver", "ApprovalDate", "BlocksStep", "OptionsEvidence", "Supersedes", "AffectedGates"],
    "01_Project_Management/risk_register.csv": ["RISK", "Description", "Category", "Trigger", "Probability", "Impact", "Mitigation", "Contingency", "ReviewDate"],
    "01_Project_Management/gates.csv": ["AssessmentID", "GateID", "DocumentOrEntityScope", "EntityVersions", "Outcome", "CriteriaReport", "Assessor", "HumanApprover", "AssessmentDate", "Supersedes", "Invalidates"],
    "02_Literature/papers.csv": ["P", "Title", "Authors", "Year", "Venue", "DOI", "PMID", "SourceURL", "Access", "FullTextPath", "MetadataVerified", "ReadingStatus", "CohortCountry", "SampleSize", "Modalities", "ECGFormat", "EndpointHorizon", "FusionModel", "XAIUsed", "XAIEvaluated", "PROBASTRisk", "CitationKey"],
    "02_Literature/screening.csv": ["SCR", "PaperID", "SearchRecord", "Stage", "RelevanceGroup", "Decision", "ExclusionReason", "Reviewer", "ConflictResolution", "DuplicateOf"],
    "02_Literature/gaps.csv": ["GAP", "ProposalGap", "Statement", "SupportingPapers", "ContradictingPapers", "SearchCoverage", "SharpenedQ1Framing", "Feasibility", "ApprovedRQ", "DecisionRecord"],
    "02_Literature/claims.csv": ["CLAIM", "Statement", "Scope", "PaperIDs", "SourceLocators", "ExperimentIDs", "EvaluationIDs", "XAIIDs", "AssetIDs", "Contradictions", "Uncertainty", "Verification", "WritingIDs"],
    "03_Datasets_Cohort/sites.csv": ["SITE", "Name", "SourceType", "Country", "RecruitmentMode", "IRBApprovalID", "PermissionRecord", "ConsentOrWaiver", "ModalitiesAvailable", "ECGFormat", "EstimatedN", "SelectionDecision"],
    "03_Datasets_Cohort/datasets.csv": ["DS", "SiteIDs", "SourceVersion", "IRBRecord", "DUARecord", "ManifestHash", "PatientCount", "EncounterCount", "EventCount", "Prevalence", "Complete4ModalityCount", "ECGQualityPassCount", "CardPath", "RestrictedLocation"],
    "03_Datasets_Cohort/releases.csv": ["REL", "DatasetID", "AdjudicationID", "VariablesHash", "SplitID", "PreprocessingID", "FitStateHash", "ManifestHash", "PatientCount", "EncounterCount", "EventCount", "ModalitiesIncluded", "RestrictedLocation", "ParentRelease", "ChangeReason"],
    "04_Outcome_Schema_QA/variables.csv": ["VAR", "Modality", "VariableName", "DataType", "Unit", "ValidRange", "CodingMap", "Instrument", "TimingRelativeToIndex", "IncorporationBiasRisk", "MissingPolicy", "PROBASTNotes", "Approver"],
    "04_Outcome_Schema_QA/adjudication_registry.csv": ["ADJ", "DatasetID", "EndpointCharterVersion", "VariablesHash", "ECGContractVersion", "BatchIDs", "Abstractors", "CardiologistReviewer", "PilotKappa", "PilotICC", "AdjudicatedCount", "UncertainExcludedCount", "NativeHash", "VerifiedHash", "QAReport", "ParentVersion"],
    "05_Preprocessing_Alignment/preprocessing_registry.csv": ["PP", "InputManifest", "RecordLocalOps", "TrainFittedOps", "ECGFilterSpec", "ECGMorphologyApprover", "ImputationRule", "MissingMaskPolicy", "ConfigPath", "ConfigHash", "FitPartition", "FitStateHash", "CodeRevision", "LeakageTestReport", "OutputManifest"],
    "06_Models_Fusion/candidates.csv": ["MC", "Tier", "ModelFamily", "Framework", "FrameworkVersion", "Architecture", "ModalityInputs", "PretrainedOrigin", "License", "ComputeFeasibility", "MissingModalitySupport", "Limitations", "SelectionDecision"],
    "06_Models_Fusion/model_registry.csv": ["MODEL", "CandidateID", "Tier", "ExperimentID", "RunID", "CheckpointID", "ReleaseID", "VariablesHash", "PreprocessingID", "FitStateHash", "ParamCount", "CalibratorHash", "ThresholdVal", "ArtifactLocation", "CardPath", "EvaluationIDs", "XAIIDs", "IntendedUse"],
    "07_Experiments/experiment_registry.csv": ["EXP", "RQ", "ComparisonBlock", "Tier", "ParentBaselineEXP", "ActiveModalities", "ReleaseID", "ModelCandidate", "ConfigPath", "ConfigHash", "SourceCommit", "Seed", "RunIDs", "Start", "End", "StoppingReason", "ValROCAUC", "ValPRAUC", "ValBrier", "FailureReport", "Conclusion"],
    "08_Checkpoints/checkpoint_registry.csv": ["CKPT", "ExperimentID", "RunID", "EpochStep", "Role", "StateComponents", "ConfigHash", "ModelHash", "ArtifactPath", "SHA256", "Bytes", "BackupPath", "RestoreEvidence"],
    "09_Evaluation_Stats/evaluation_registry.csv": ["EVAL", "ExperimentID", "ModelID", "CheckpointID", "ReleaseID", "Partition", "ProtocolHash", "FreezeRecord", "CalibratorHash", "ThresholdUsed", "PredictionHash", "MetricPath", "CalibrationPath", "DCAPath", "StatsPath", "SubgroupPath", "ErrorPROBASTPath", "ReportPath", "Deviations", "ParentEvaluation"],
    "10_Explainability_XAI/xai_registry.csv": ["XAI", "ModelID", "EvaluationID", "ReleaseID", "ExplainerType", "BackgroundPartition", "BackgroundHash", "AdditivityError", "DeletionAOPC", "InsertionAOPC", "RandomControlAOPC", "LOMOConcordance", "SeedStabilityRho", "ShortcutAuditOutcome", "ClinicianReviewPath", "ReportPath"],
    "11_Figures_Tables/assets.csv": ["AssetID", "Kind", "SourceIDs", "DataHash", "SpecPath", "GeneratorCommand", "CodeRevision", "OutputPath", "ResolutionFormat", "Caption", "Units", "PHICheck", "VisualReview", "WritingIDs"],
    "12_Writing/writing_registry.csv": ["WR", "Document", "Section", "Topic", "ClaimIDs", "PaperIDs", "EvaluationIDs", "XAIIDs", "AssetIDs", "TRIPODItems", "DraftPath", "Reviewer", "ReviewState", "Revision", "MissingEvidence"],
    "16_Archive/archive_manifest.csv": ["ArchiveItemID", "ArchiveID", "ReleaseTag", "ItemType", "SourcePath", "StoredLocation", "ArchiveVersion", "SHA256", "Bytes", "PHISensitivity", "License", "Retention", "RestoreEvidence", "SubmissionReceipt"]
}

EXPECTED_TEMPLATES = [
    f"T{i:02d}_{name}.{ext}" for i, name, ext in [
        (1, "readme", "md"), (2, "decision", "md"), (3, "session", "md"), (4, "search", "md"),
        (5, "paper_summary", "md"), (6, "gap", "md"), (7, "claim", "md"), (8, "site_irb", "md"),
        (9, "cohort_card", "md"), (10, "endpoint_charter", "md"), (11, "crf_ecg_protocol", "md"),
        (12, "adjudication_batch", "md"), (13, "preprocessing", "md"), (14, "split", "md"),
        (15, "failure", "md"), (16, "experiment", "md"), (17, "model_card", "md"),
        (18, "checkpoint", "md"), (19, "evaluation", "md"), (20, "error_probast", "md"),
        (21, "xai_audit", "md"), (22, "gate_audit", "md"), (23, "figure_table", "md"),
        (24, "reproduce", "md"), (25, "review_response", "md"), (26, "writing_unit", "md"),
        (27, "tripod_ai_checklist", "md"), (28, "submission", "md"), (29, "archive", "md"),
        (30, "risk_meeting", "md"), (31, "prompt", "md"), (32, "config", "yaml")
    ]
]


def validate_templates():
    print(">>> Validating Template Library (15_Templates_Prompts/)...")
    templates_dir = os.path.join(REPO_ROOT, "15_Templates_Prompts")
    if not os.path.isdir(templates_dir):
        print(f"FAIL: Missing directory {templates_dir}")
        return False

    missing = []
    for tmpl in EXPECTED_TEMPLATES:
        tmpl_path = os.path.join(templates_dir, tmpl)
        if not os.path.isfile(tmpl_path):
            missing.append(tmpl)

    if missing:
        print(f"FAIL: Missing {len(missing)} templates: {missing}")
        return False
    print(f"PASS: All {len(EXPECTED_TEMPLATES)} blank templates verified.")
    return True


def validate_registries():
    print(">>> Validating Appendix B CSV Registries...")
    errors = 0
    for rel_path, domain_cols in REGISTRIES_SCHEMA.items():
        full_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.isfile(full_path):
            print(f"FAIL: Registry file does not exist: {rel_path}")
            errors += 1
            continue

        expected_header = domain_cols + COMMON_COLS
        with open(full_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print(f"FAIL: Registry is empty: {rel_path}")
                errors += 1
                continue

            if header != expected_header:
                print(f"FAIL: Header mismatch in {rel_path}")
                print(f"  Expected: {expected_header}")
                print(f"  Got:      {header}")
                errors += 1
            else:
                pass

    if errors == 0:
        print(f"PASS: All {len(REGISTRIES_SCHEMA)} CSV registries verified with compliant schemas.")
        return True
    else:
        print(f"FAIL: Found {errors} registry schema errors.")
        return False


def validate_phi_ignore():
    print(">>> Validating .gitignore PHI & Safety Rules...")
    gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
    if not os.path.isfile(gitignore_path):
        print("FAIL: .gitignore missing")
        return False

    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_patterns = [
        "raw/", "processed/", "*.edf", "*.xml", "*.dcm", "*.mat",
        "*.pt", "*.ckpt", "*.pdf"
    ]
    missing = [p for p in required_patterns if p not in content]
    if missing:
        print(f"FAIL: Missing critical .gitignore patterns: {missing}")
        return False
    print("PASS: Critical PHI and binary .gitignore patterns verified.")
    return True


def main():
    print("=" * 60)
    print("  CVD MULTIMODAL REPOSITORY INTEGRITY VALIDATOR (STEP-003)")
    print("=" * 60)

    v1 = validate_templates()
    v2 = validate_registries()
    v3 = validate_phi_ignore()

    print("=" * 60)
    if v1 and v2 and v3:
        print("RESULT: ALL INTEGRITY AUDITS PASSED CLEANLY (G02 Ready)")
        print("=" * 60)
        sys.exit(0)
    else:
        print("RESULT: INTEGRITY AUDIT FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

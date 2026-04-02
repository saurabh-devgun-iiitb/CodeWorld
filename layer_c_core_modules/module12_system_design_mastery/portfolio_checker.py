"""Module 12: Validate architecture portfolio documents include required sections."""

from __future__ import annotations

from pathlib import Path

REQUIRED_SECTIONS = [
    "## Architecture Diagram",
    "## Capacity Estimates",
    "## Failure Analysis",
    "## Cost Analysis",
]

DOCS = [
    "docs/ml_inference_platform.md",
    "docs/log_analytics_system.md",
    "docs/feature_store.md",
    "docs/global_monitoring_system.md",
]


def validate_doc(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    return missing


def main() -> None:
    root = Path(__file__).parent
    print("=== Staff-level Architecture Portfolio Check ===")
    all_pass = True

    for relative in DOCS:
        path = root / relative
        missing = validate_doc(path)
        if missing:
            all_pass = False
            print(f"- {relative}: missing {missing}")
        else:
            print(f"- {relative}: OK")

    if all_pass:
        print("\nOutcome: four complete system design documents are ready for presentation.")


if __name__ == "__main__":
    main()

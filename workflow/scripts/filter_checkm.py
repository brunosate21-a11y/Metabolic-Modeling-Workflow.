__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Quality filter for CheckM results.
-----------------------------------
Reads CheckM quality.tsv files (one per MAG), applies completeness
and contamination thresholds from the workflow config, and produces:

  1. checkm_summary.tsv  — all MAGs with completeness, contamination,
                           and a PASS/FAIL column for downstream review.
  2. filtered_mags.txt   — names of MAGs that passed quality control,
                           one per line, ready for downstream filtering.

Thresholds are set in config/config.yaml under quality_filters.checkm:
  min_completeness  (default: 50.0)
  max_contamination (default: 10.0)
"""

import csv
import os

# ── Snakemake interface ──────────────────────────────────────────────
quality_files    = snakemake.input.quality
summary_out      = snakemake.output.summary
filtered_out     = snakemake.output.filtered
log_file         = snakemake.log[0]

min_completeness  = float(snakemake.params.min_completeness)
max_contamination = float(snakemake.params.max_contamination)

if isinstance(quality_files, str):
    quality_files = [quality_files]

# ── Main logic ───────────────────────────────────────────────────────
with open(log_file, "w") as logf:
    logf.write(
        f"CheckM quality filter\n"
        f"  min_completeness:  {min_completeness}\n"
        f"  max_contamination: {max_contamination}\n"
        f"  input files:       {len(quality_files)}\n\n"
    )

    rows = []

    for path in quality_files:
        mag = os.path.basename(os.path.dirname(path))
        logf.write(f"Reading {path} ...\n")

        try:
            with open(path) as f:
                reader = csv.DictReader(f, delimiter="\t")
                for record in reader:
                    completeness  = float(record.get("Completeness", 0))
                    contamination = float(record.get("Contamination", 100))

                    passed = (
                        completeness  >= min_completeness
                        and contamination <= max_contamination
                    )

                    rows.append({
                        "mag":            mag,
                        "completeness":   completeness,
                        "contamination":  contamination,
                        "status":         "PASS" if passed else "FAIL",
                    })

                    logf.write(
                        f"  {mag}: completeness={completeness:.1f}%, "
                        f"contamination={contamination:.1f}% "
                        f"-> {'PASS' if passed else 'FAIL'}\n"
                    )

        except Exception as e:
            logf.write(f"  ERROR reading {path}: {e}\n")
            rows.append({
                "mag":           mag,
                "completeness":  "NA",
                "contamination": "NA",
                "status":        "ERROR",
            })

    # ── Write summary TSV ────────────────────────────────────────────
    header = ["mag", "completeness", "contamination", "status"]

    with open(summary_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for row in rows:
            out.write("\t".join(str(row[h]) for h in header) + "\n")

    # ── Write filtered MAG list ──────────────────────────────────────
    passed_mags = [r["mag"] for r in rows if r["status"] == "PASS"]

    with open(filtered_out, "w") as out:
        for mag in passed_mags:
            out.write(mag + "\n")

    logf.write(
        f"\nSummary: {len(passed_mags)}/{len(rows)} MAGs passed quality filter\n"
        f"Results written to:\n"
        f"  {summary_out}\n"
        f"  {filtered_out}\n"
    )
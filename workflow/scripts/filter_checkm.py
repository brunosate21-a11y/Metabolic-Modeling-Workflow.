__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Quality filter for CheckM results.
-----------------------------------
Reads CheckM quality.tsv files, applies completeness and contamination
thresholds from the workflow config, and produces:

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


quality_files    = snakemake.input.quality
summary_out      = snakemake.output.summary
filtered_out     = snakemake.output.filtered
log_file         = snakemake.log[0]

min_completeness  = float(snakemake.params.min_completeness)
max_contamination = float(snakemake.params.max_contamination)

if isinstance(quality_files, str):
    quality_files = [quality_files]


with open(log_file, "w") as logf:
    logf.write(
        f"CheckM quality filter\n"
        f"  min_completeness:  {min_completeness}\n"
        f"  max_contamination: {max_contamination}\n"
        f"  input files:       {len(quality_files)}\n\n"
    )

    rows = []
    seen_mags = set()  

    for path in quality_files:
        path_mag = os.path.basename(os.path.dirname(path))
        logf.write(f"Reading {path} (target MAG: {path_mag}) ...\n")

        try:
            with open(path) as f:
                reader = csv.DictReader(f, delimiter="\t")
                matched = False
                for record in reader:
                    bin_id = record.get("Bin Id", "").strip()

                    
                    if bin_id != path_mag:
                        continue
                    if bin_id in seen_mags:
                        continue
                    seen_mags.add(bin_id)
                    matched = True

                    completeness  = float(record.get("Completeness", 0))
                    contamination = float(record.get("Contamination", 100))

                    passed = (
                        completeness  >= min_completeness
                        and contamination <= max_contamination
                    )

                    rows.append({
                        "mag":            bin_id,
                        "completeness":   completeness,
                        "contamination":  contamination,
                        "status":         "PASS" if passed else "FAIL",
                    })

                    logf.write(
                        f"  {bin_id}: completeness={completeness:.1f}%, "
                        f"contamination={contamination:.1f}% "
                        f"-> {'PASS' if passed else 'FAIL'}\n"
                    )

                if not matched:
                    logf.write(f"  WARNING: no row with Bin Id='{path_mag}' in {path}\n")
                    rows.append({
                        "mag":           path_mag,
                        "completeness":  "NA",
                        "contamination": "NA",
                        "status":        "MISSING",
                    })

        except Exception as e:
            logf.write(f"  ERROR reading {path}: {e}\n")
            rows.append({
                "mag":           path_mag,
                "completeness":  "NA",
                "contamination": "NA",
                "status":        "ERROR",
            })

     
    header = ["mag", "completeness", "contamination", "status"]

    with open(summary_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for row in rows:
            out.write("\t".join(str(row[h]) for h in header) + "\n")

     
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
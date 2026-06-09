__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Quality filter for Memote results.
------------------------------------
Reads Memote score.json files (one per metabolic model), applies a
minimum total score threshold from the workflow config, and produces:

  1. memote_quality.tsv    — all models with total score, sub-scores,
                             and a PASS/FAIL column for downstream review.
  2. filtered_models.txt   — names of models that passed quality control,
                             one per line, ready for downstream filtering.

Thresholds are set in config/config.yaml under quality_filters.memote:
  min_total_score  (default: 0.4)
"""

import json
import os

# ── Snakemake interface ──────────────────────────────────────────────
score_files     = snakemake.input.scores
quality_out     = snakemake.output.quality
filtered_out    = snakemake.output.filtered
log_file        = snakemake.log[0]

min_total_score = float(snakemake.params.min_total_score)

if isinstance(score_files, str):
    score_files = [score_files]

# ── Main logic ───────────────────────────────────────────────────────
with open(log_file, "w") as logf:
    logf.write(
        f"Memote quality filter\n"
        f"  min_total_score: {min_total_score}\n"
        f"  input files:     {len(score_files)}\n\n"
    )

    rows = []

    for path in score_files:
        mag = os.path.basename(os.path.dirname(path))
        logf.write(f"Reading {path} ...\n")

        try:
            with open(path) as f:
                data = json.load(f)

            score = data.get("score", {})
            total = score.get("total_score", 0)

            # Extract sub-scores when available
            scored = score.get("scored", {})
            consistency   = scored.get("Consistency", "NA")
            annotation    = scored.get("Annotation", "NA")
            biomass       = scored.get("Biomass", "NA")
            stoichiometry = scored.get("Stoichiometry", "NA")

            passed = float(total) >= min_total_score if total != "NA" else False

            rows.append({
                "mag":            mag,
                "total_score":    total,
                "consistency":    consistency,
                "annotation":     annotation,
                "biomass":        biomass,
                "stoichiometry":  stoichiometry,
                "status":         "PASS" if passed else "FAIL",
            })

            logf.write(
                f"  {mag}: total_score={total} "
                f"-> {'PASS' if passed else 'FAIL'}\n"
            )

        except Exception as e:
            logf.write(f"  ERROR reading {path}: {e}\n")
            rows.append({
                "mag":            mag,
                "total_score":    "NA",
                "consistency":    "NA",
                "annotation":     "NA",
                "biomass":        "NA",
                "stoichiometry":  "NA",
                "status":         "ERROR",
            })

    # ── Write quality TSV ────────────────────────────────────────────
    header = ["mag", "total_score", "consistency", "annotation",
              "biomass", "stoichiometry", "status"]

    with open(quality_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for row in rows:
            out.write("\t".join(str(row[h]) for h in header) + "\n")

    # ── Write filtered model list ────────────────────────────────────
    passed_models = [r["mag"] for r in rows if r["status"] == "PASS"]

    with open(filtered_out, "w") as out:
        for mag in passed_models:
            out.write(mag + "\n")

    logf.write(
        f"\nSummary: {len(passed_models)}/{len(rows)} models passed quality filter\n"
        f"Results written to:\n"
        f"  {quality_out}\n"
        f"  {filtered_out}\n"
    )
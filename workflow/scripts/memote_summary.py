__author__ = "Bruno Ferreira"
__license__ = "MIT"

import json
import os
import sys

score_files = snakemake.input.scores
summary_out = snakemake.output.summary
log_file    = snakemake.log[0]

if isinstance(score_files, str):
    score_files = [score_files]

with open(log_file, "w") as logf:
    rows = []

    for path in score_files:
        mag = os.path.basename(os.path.dirname(path))
        logf.write(f"Processing {mag} from {path}\n")

        try:
            with open(path) as f:
                data = json.load(f)

            score = data.get("score", {})
            total = score.get("total_score", "NA")

            # Extract sub-scores when available
            scored_sections = score.get("scored", {})
            consistency  = scored_sections.get("Consistency", "NA")
            annotation   = scored_sections.get("Annotation", "NA")
            biomass      = scored_sections.get("Biomass", "NA")
            stoichiometry = scored_sections.get("Stoichiometry", "NA")

            rows.append({
                "mag":            mag,
                "total_score":    total,
                "consistency":    consistency,
                "annotation":     annotation,
                "biomass":        biomass,
                "stoichiometry":  stoichiometry,
                "score_file":     path,
            })
        except Exception as e:
            logf.write(f"ERROR processing {path}: {e}\n")
            rows.append({
                "mag":            mag,
                "total_score":    "ERROR",
                "consistency":    "NA",
                "annotation":     "NA",
                "biomass":        "NA",
                "stoichiometry":  "NA",
                "score_file":     path,
            })

    # Write TSV
    header = ["mag", "total_score", "consistency", "annotation",
              "biomass", "stoichiometry", "score_file"]

    with open(summary_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for row in rows:
            out.write("\t".join(str(row[h]) for h in header) + "\n")

    logf.write(f"Summary written to {summary_out} ({len(rows)} models)\n")
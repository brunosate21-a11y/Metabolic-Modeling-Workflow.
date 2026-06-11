__author__ = "Bruno Ferreira"
__license__ = "MIT"

import json
import os

score_files = snakemake.input.scores
summary_out = snakemake.output.summary
log_file    = snakemake.log[0]

if isinstance(score_files, str):
    score_files = [score_files]


def extract_sections(sections):
    if not isinstance(sections, list):
        return {}
    return {
        s.get("section", ""): s.get("score", "NA")
        for s in sections if isinstance(s, dict)
    }


def average_annotation(section_scores):
    vals = [v for k, v in section_scores.items()
            if k.startswith("annotation_") and isinstance(v, (int, float))]
    return sum(vals) / len(vals) if vals else "NA"


with open(log_file, "w") as logf:
    rows = []
    for path in score_files:
        mag = os.path.basename(os.path.dirname(path))
        try:
            with open(path) as f:
                data = json.load(f)

            score = data.get("score", {})
            total = score.get("total_score", "NA")
            sec   = extract_sections(score.get("sections", []))

            rows.append({
                "mag": mag,
                "total_score": total,
                "consistency": sec.get("consistency", "NA"),
                "annotation":  average_annotation(sec),
                "score_file":  path,
            })
        except Exception as e:
            logf.write(f"ERROR processing {path}: {e}\n")
            rows.append({"mag": mag, "total_score": "ERROR",
                         "consistency": "NA", "annotation": "NA", "score_file": path})

    header = ["mag", "total_score", "consistency", "annotation", "score_file"]
    with open(summary_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for r in rows:
            out.write("\t".join(str(r[h]) for h in header) + "\n")

    logf.write(f"Summary written ({len(rows)} models)\n")
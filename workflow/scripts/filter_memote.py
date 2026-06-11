__author__ = "Bruno Ferreira"
__license__ = "MIT"

import json
import os

score_files     = snakemake.input.scores
quality_out     = snakemake.output.quality
filtered_out    = snakemake.output.filtered
log_file        = snakemake.log[0]

min_total_score = float(snakemake.params.min_total_score)

if isinstance(score_files, str):
    score_files = [score_files]


def extract_sections(sections):
    """Converte a lista de sections do memote em dict {nome: score}."""
    if not isinstance(sections, list):
        return {}
    return {
        s.get("section", ""): s.get("score", "NA")
        for s in sections if isinstance(s, dict)
    }


def average_annotation(section_scores):
    """Média de todas as sub-secções annotation_* numa única score."""
    vals = [v for k, v in section_scores.items()
            if k.startswith("annotation_") and isinstance(v, (int, float))]
    return sum(vals) / len(vals) if vals else "NA"


with open(log_file, "w") as logf:
    logf.write(f"Memote quality filter (min_total_score={min_total_score})\n\n")
    rows = []

    for path in score_files:
        mag = os.path.basename(os.path.dirname(path))
        try:
            with open(path) as f:
                data = json.load(f)

            score = data.get("score", {})
            total = score.get("total_score", "NA")
            sec   = extract_sections(score.get("sections", []))

            consistency = sec.get("consistency", "NA")
            annotation  = average_annotation(sec)

            passed = isinstance(total, (int, float)) and total >= min_total_score

            rows.append({
                "mag": mag,
                "total_score": total,
                "consistency": consistency,
                "annotation":  annotation,
                "status": "PASS" if passed else "FAIL",
            })
            logf.write(f"  {mag}: total={total} -> {'PASS' if passed else 'FAIL'}\n")
            logf.write(f"    sections: {list(sec.keys())}\n")

        except Exception as e:
            logf.write(f"  ERROR reading {path}: {e}\n")
            rows.append({"mag": mag, "total_score": "NA",
                         "consistency": "NA", "annotation": "NA", "status": "ERROR"})

    header = ["mag", "total_score", "consistency", "annotation", "status"]
    with open(quality_out, "w") as out:
        out.write("\t".join(header) + "\n")
        for r in rows:
            out.write("\t".join(str(r[h]) for h in header) + "\n")

    passed_models = [r["mag"] for r in rows if r["status"] == "PASS"]
    with open(filtered_out, "w") as out:
        for mag in passed_models:
            out.write(mag + "\n")

    logf.write(f"\nSummary: {len(passed_models)}/{len(rows)} models passed\n")
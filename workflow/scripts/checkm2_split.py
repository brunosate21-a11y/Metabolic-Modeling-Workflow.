__author__ = "Bruno Ferreira"
__license__ = "MIT"

import csv
import os

report = snakemake.input.report
out    = snakemake.output.quality
mag    = snakemake.params.mag
logf   = snakemake.log[0]

os.makedirs(os.path.dirname(out), exist_ok=True)


def pick(fieldnames, options):
    for o in options:
        if o in fieldnames:
            return o
    return None


with open(logf, "w") as log:
    log.write(f"CheckM2 split para bin '{mag}'\n")
    log.write(f"  fonte: {report}\n")

    with open(report) as f:
        reader = csv.DictReader(f, delimiter="\t")
        fn = reader.fieldnames or []
        name_col = pick(fn, ["sample", "Name", "Bin Id", "bin_id"])
        comp_col = pick(fn, ["completeness", "Completeness"])
        cont_col = pick(fn, ["contamination", "Contamination"])
        log.write(f"  colunas: name={name_col} comp={comp_col} cont={cont_col}\n")

        if not all([name_col, comp_col, cont_col]):
            raise ValueError(f"Colunas esperadas não encontradas em {report}. Cabeçalho: {fn}")

        target = None
        for row in reader:
            if row.get(name_col, "").strip() == mag:
                target = row
                break

    if target is None:
        raise ValueError(f"Bin '{mag}' não está no relatório CheckM2 {report}")

    completeness  = float(target.get(comp_col, 0))
    contamination = float(target.get(cont_col, 100))
    log.write(f"  completeness={completeness:.2f}%  contamination={contamination:.2f}%\n")

    with open(out, "w", newline="") as fout:
        w = csv.writer(fout, delimiter="\t")
        w.writerow(["Bin Id", "Completeness", "Contamination"])
        w.writerow([mag, completeness, contamination])

    log.write(f"  escrito: {out}\n")

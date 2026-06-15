__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Bypass do CheckM para o dataset real.
--------------------------------------
O orientador forneceu um relatório CheckM2 já calculado (um único TSV com
todos os bins). Em vez de re-correr o CheckM, esta regra extrai a linha do
bin alvo e escreve um quality.tsv individual no formato que o
filter_checkm.py espera (coluna 'Bin Id', 'Completeness', 'Contamination').

Assim o resto da pipeline (filter_checkm) funciona sem qualquer alteração,
quer os dados venham do CheckM (refs) quer do CheckM2 (reais).

CheckM2 usa a coluna 'Name'; CheckM1 usa 'Bin Id'. Esta conversão trata isso.
"""

import csv
import os

report = snakemake.input.report
out    = snakemake.output.quality
mag    = snakemake.params.mag
logf   = snakemake.log[0]

os.makedirs(os.path.dirname(out), exist_ok=True)

with open(logf, "w") as log:
    log.write(f"CheckM2 split para bin '{mag}'\n")
    log.write(f"  fonte: {report}\n")

    target = None
    with open(report) as f:
        reader = csv.DictReader(f, delimiter="\t")
        # CheckM2: 'Name'; tolera também 'Bin Id' caso o formato varie
        name_col = "Name" if "Name" in reader.fieldnames else "Bin Id"
        for row in reader:
            if row.get(name_col, "").strip() == mag:
                target = row
                break

    if target is None:
        log.write(f"  ERRO: bin '{mag}' não encontrado em {report}\n")
        raise ValueError(f"Bin '{mag}' não está no relatório CheckM2 {report}")

    completeness  = float(target.get("Completeness", 0))
    contamination = float(target.get("Contamination", 100))

    log.write(f"  completeness={completeness:.2f}%  contamination={contamination:.2f}%\n")

    # Escreve no formato CheckM1 que o filter_checkm.py consome.
    with open(out, "w", newline="") as fout:
        w = csv.writer(fout, delimiter="\t")
        w.writerow(["Bin Id", "Completeness", "Contamination"])
        w.writerow([mag, completeness, contamination])

    log.write(f"  escrito: {out}\n")

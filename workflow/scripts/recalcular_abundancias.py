__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Recalcular a qualidade das abundâncias após filtro de qualidade.
-----------------------------------------------------------------
As abundâncias de entrada (de mapeamento de reads) somam 1.0 sobre TODOS
os bins selecionados. Mas o filtro de qualidade (CheckM + Memote) pode
eliminar alguns bins. A comunidade que efetivamente entra na modelação
metabólica é só a dos bins APROVADOS — pelo que as abundâncias têm de ser
re-normalizadas para somar 1.0 apenas sobre esses.

Entradas:
  - abundances        : TSV (sample, abundance) original, soma 1.0 sobre todos
  - checkm_filtered   : filtered_mags.txt  (bins que passaram CheckM)
  - memote_filtered   : filtered_models.txt (bins que passaram Memote)

Saída:
  - abundances_filtered.tsv : (sample, abundance_raw, abundance_renorm, status)
    só os bins aprovados em AMBOS os filtros, com abundância re-normalizada.

Nota: a interseção (CheckM ∩ Memote) é a definição conservadora — um bin só
entra na comunidade final se passar nos dois critérios de qualidade.
"""

import csv
import os

abund_in   = snakemake.input.abundances
checkm_in  = snakemake.input.checkm_filtered
memote_in  = snakemake.input.memote_filtered
out        = snakemake.output.filtered
logf       = snakemake.log[0]

os.makedirs(os.path.dirname(out), exist_ok=True)


def read_list(path):
    with open(path) as f:
        return {line.strip() for line in f if line.strip()}


with open(logf, "w") as log:
    # Abundâncias originais
    raw = {}
    with open(abund_in) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            raw[row["sample"].strip()] = float(row["abundance"])

    checkm_pass = read_list(checkm_in)
    memote_pass = read_list(memote_in)
    approved = checkm_pass & memote_pass   # interseção: passa nos dois

    log.write("Recálculo de abundâncias pós-filtro\n")
    log.write(f"  bins totais (input):     {len(raw)}\n")
    log.write(f"  passaram CheckM:         {len(checkm_pass)}\n")
    log.write(f"  passaram Memote:         {len(memote_pass)}\n")
    log.write(f"  aprovados (interseção):  {len(approved)}\n\n")

    # Soma das abundâncias dos aprovados (para re-normalizar)
    approved_in_raw = [s for s in raw if s in approved]
    total_approved = sum(raw[s] for s in approved_in_raw)

    if total_approved == 0:
        log.write("  ERRO: soma das abundâncias aprovadas = 0\n")
        raise ValueError("Nenhum bin aprovado tem abundância > 0; impossível re-normalizar.")

    # Escrever saída (ordenada por abundância re-normalizada, desc)
    rows = []
    for s in raw:
        status = "APPROVED" if s in approved else "REMOVED"
        renorm = raw[s] / total_approved if s in approved else 0.0
        rows.append((s, raw[s], renorm, status))

    rows.sort(key=lambda r: -r[2])

    with open(out, "w", newline="") as fout:
        w = csv.writer(fout, delimiter="\t")
        w.writerow(["sample", "abundance_raw", "abundance_renorm", "status"])
        for s, raw_ab, renorm, status in rows:
            w.writerow([s, f"{raw_ab:.6f}", f"{renorm:.6f}", status])

    check = sum(r[2] for r in rows)
    log.write(f"  soma re-normalizada (deve ser 1.0): {check:.6f}\n")
    log.write(f"  escrito: {out}\n")

    # Log dos removidos, para rastreabilidade na tese
    removed = [s for s in raw if s not in approved]
    if removed:
        log.write(f"\n  Bins removidos pelo filtro ({len(removed)}):\n")
        for s in removed:
            log.write(f"    {s} (abund. original {raw[s]:.4f})\n")

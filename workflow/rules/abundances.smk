
rule recalcular_abundancias:
    input:
        abundances      = ABUNDANCES if ABUNDANCES else [],
        checkm_filtered = RESULTS + "/checkm/filtered_mags.txt",
        memote_filtered = RESULTS + "/memote/filtered_models.txt"
    output:
        filtered = RESULTS + "/abundances/abundances_filtered.tsv"
    log:
        LOGS + "/abundances/recalcular_abundancias.log"
    script:
        "../scripts/recalcular_abundancias.py"

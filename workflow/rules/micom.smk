rule micom:
    input:
        models     = expand(RESULTS + "/gems/{mag}.xml", mag=MAGS),
        abundances = (RESULTS + "/abundances/abundances_filtered.tsv") if ABUNDANCES else []
    output:
        exchange_fluxes = RESULTS + "/micom/exchange_fluxes.tsv"
    log:
        LOGS + "/micom/micom.log"
    conda:
        "../envs/micom.yaml"
    script:
        "../scripts/micom_script.py"

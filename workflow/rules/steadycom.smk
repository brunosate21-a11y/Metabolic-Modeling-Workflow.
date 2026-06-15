rule steadycom:
    input:
        models     = expand(RESULTS + "/gems/{mag}.xml", mag=MAGS),
        abundances = (RESULTS + "/abundances/abundances_filtered.tsv") if ABUNDANCES else []
    output:
        abundances = RESULTS + "/steadycom/abundances.tsv"
    log:
        LOGS + "/steadycom/steadycom.log"
    conda:
        "../envs/steadycom.yaml"
    script:
        "../scripts/steadycom.py"

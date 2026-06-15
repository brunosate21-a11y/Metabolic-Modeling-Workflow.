rule smetana:
    input:
        models = expand(RESULTS + "/gems/{mag}.xml", mag=MAGS)
    output:
        global_scores = RESULTS + "/smetana/global.tsv",
        detailed      = RESULTS + "/smetana/detailed.tsv"
    params:
        solver = config["solver"]
    log:
        LOGS + "/smetana/smetana.log"
    conda:
        "../envs/smetana.yaml"
    script:
        "../scripts/smetana.py"

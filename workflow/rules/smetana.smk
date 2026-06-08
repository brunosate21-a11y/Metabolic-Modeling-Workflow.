
rule smetana:
    input:
        models = expand("results/gems/{mag}.xml", mag=MAGS)
    output:
        global_scores = "results/smetana/global.tsv",
        detailed      = "results/smetana/detailed.tsv"
    params:
        solver = config["solver"]
    log:
        "logs/smetana/smetana.log"
    conda:
        "../envs/smetana.yaml"

    script:
        "../scripts/smetana.py"




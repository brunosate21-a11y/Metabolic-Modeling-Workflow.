rule carveme:
    input:
        genome  = "data/mags/{mag}.faa"
    output:
        model   = "results/gems/{mag}.xml"
    params:
        solver  = config["solver"],
        media   = config["media"]
    threads: 4
    log:
        "logs/carveme/{mag}.log"
    conda:
        "../envs/carveme.yaml"
    script:
        "../scripts/carveme.py"

        
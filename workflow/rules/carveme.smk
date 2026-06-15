rule carveme:
    input:
        genome  = mag_faa
    output:
        model   = RESULTS + "/gems/{mag}.xml"
    params:
        solver  = config["solver"],
        media   = config["media"]
    threads: 4
    log:
        LOGS + "/carveme/{mag}.log"
    conda:
        "../envs/carveme.yaml"
    script:
        "../scripts/carveme.py"

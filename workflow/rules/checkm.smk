rule checkm:
    input:
        genome = "data/mags/{mag}.faa"
    output:
        output_dir = directory("results/checkm/{mag}"),
        quality    = "results/checkm/{mag}/quality.tsv"
    threads: 4
    log:
        "logs/checkm/{mag}.log"
    conda:
        "../envs/checkm.yaml"
    script:
        "../scripts/checkm.py"



rule filter_checkm:
    input:
        quality = expand("results/checkm/{mag}/quality.tsv", mag=MAGS)
    output:
        summary  = "results/checkm/checkm_summary.tsv",
        filtered = "results/checkm/filtered_mags.txt"
    params:
        min_completeness  = config["quality_filters"]["checkm"]["min_completeness"],
        max_contamination = config["quality_filters"]["checkm"]["max_contamination"]
    log:
        "logs/checkm/filter_checkm.log"
    script:
        "../scripts/filter_checkm.py"
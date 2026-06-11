import os

CHECKM_DB = os.path.abspath(os.path.expanduser(config["checkm"]["data_path"]))


rule download_checkm_db:
    output:
        marker = os.path.join(CHECKM_DB, ".downloaded")
    params:
        url  = "https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz",
        dest = CHECKM_DB
    log:
        "logs/checkm/download_db.log"
    shell:
        """
        mkdir -p {params.dest}
        wget {params.url} -O {params.dest}/checkm_data.tar.gz 2> {log}
        tar -xzf {params.dest}/checkm_data.tar.gz -C {params.dest} 2>> {log}
        rm {params.dest}/checkm_data.tar.gz
        touch {output.marker}
        """


rule checkm:
    input:
        genome    = "data/mags/{mag}.faa",
        db_marker = ancient(os.path.join(CHECKM_DB, ".downloaded"))
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
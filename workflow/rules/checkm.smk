import os

CHECKM_DB = os.path.abspath(os.path.expanduser(config["checkm"]["data_path"]))




if USE_CHECKM2:

    # --- Bypass: divide o CheckM2 report em quality.tsv por bin ---
    rule checkm2_split:
        input:
            report = CHECKM_REPORT
        output:
            quality = RESULTS + "/checkm/{mag}/quality.tsv"
        params:
            mag = "{mag}"
        log:
            LOGS + "/checkm/{mag}.log"
        script:
            "../scripts/checkm2_split.py"

else:

    rule download_checkm_db:
        output:
            marker = os.path.join(CHECKM_DB, ".downloaded")
        params:
            url  = "https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz",
            dest = CHECKM_DB
        log:
            LOGS + "/checkm/download_db.log"
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
            genome    = mag_faa,
            db_marker = ancient(os.path.join(CHECKM_DB, ".downloaded"))
        output:
            output_dir = directory(RESULTS + "/checkm/{mag}"),
            quality    = RESULTS + "/checkm/{mag}/quality.tsv"
        threads: 4
        log:
            LOGS + "/checkm/{mag}.log"
        conda:
            "../envs/checkm.yaml"
        script:
            "../scripts/checkm.py"


# --- Filtro de qualidade (comum aos dois modos) ---
rule filter_checkm:
    input:
        quality = expand(RESULTS + "/checkm/{mag}/quality.tsv", mag=MAGS)
    output:
        summary  = RESULTS + "/checkm/checkm_summary.tsv",
        filtered = RESULTS + "/checkm/filtered_mags.txt"
    params:
        min_completeness  = config["quality_filters"]["checkm"]["min_completeness"],
        max_contamination = config["quality_filters"]["checkm"]["max_contamination"]
    log:
        LOGS + "/checkm/filter_checkm.log"
    script:
        "../scripts/filter_checkm.py"

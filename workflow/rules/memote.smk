rule memote:
    input:
        model  = RESULTS + "/gems/{mag}.xml"
    output:
        report = RESULTS + "/memote/{mag}/report.html",
        score  = RESULTS + "/memote/{mag}/score.json"
    log:
        LOGS + "/memote/{mag}.log"
    conda:
        "../envs/memote.yaml"
    script:
        "../scripts/memote.py"


rule memote_summary:
    input:
        scores = expand(RESULTS + "/memote/{mag}/score.json", mag=MAGS)
    output:
        summary = RESULTS + "/memote/memote_summary.tsv"
    log:
        LOGS + "/memote/memote_summary.log"
    script:
        "../scripts/memote_summary.py"


rule filter_memote:
    input:
        scores = expand(RESULTS + "/memote/{mag}/score.json", mag=MAGS)
    output:
        quality  = RESULTS + "/memote/memote_quality.tsv",
        filtered = RESULTS + "/memote/filtered_models.txt"
    params:
        min_total_score = config["quality_filters"]["memote"]["min_total_score"]
    log:
        LOGS + "/memote/filter_memote.log"
    script:
        "../scripts/filter_memote.py"

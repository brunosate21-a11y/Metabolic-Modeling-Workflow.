rule memote:
    input:
        model  = "results/gems/{mag}.xml"
    output:
        report = "results/memote/{mag}/report.html",
        score  = "results/memote/{mag}/score.json"
    log:
        "logs/memote/{mag}.log"
    conda:
        "../envs/memote.yaml"
    script:
        "../scripts/memote.py"


MAGS = config["MAGS"]

rule memote_summary:
    input:
        scores = expand("results/memote/{mag}/score.json", mag=MAGS)
    output:
        summary = "results/memote/memote_summary.tsv"
    log:
        "logs/memote/memote_summary.log"
    script:
        "../scripts/memote_summary.py"
rule sensitivity_analysis:
    input:
        checkm = "results/checkm/checkm_summary.tsv",
        memote = "results/memote/memote_summary.tsv"
    output:
        grid       = "results/sensitivity/threshold_grid.tsv",
        robustness = "results/sensitivity/mag_robustness.tsv",
        heatmap    = "results/sensitivity/heatmaps.png"
    params:
        checkm_completeness  = config["sensitivity_analysis"]["checkm"]["min_completeness"],
        checkm_contamination = config["sensitivity_analysis"]["checkm"]["max_contamination"],
        memote_score         = config["sensitivity_analysis"]["memote"]["min_total_score"]
    log:
        "logs/sensitivity/sensitivity_analysis.log"
    conda:
        "../envs/sensitivity.yaml"
    script:
        "../scripts/sensitivity_analysis.py"
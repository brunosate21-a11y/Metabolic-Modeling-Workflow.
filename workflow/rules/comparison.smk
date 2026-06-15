rule community_comparison:
    input:
        steadycom        = RESULTS + "/steadycom/abundances.tsv",
        micom            = RESULTS + "/micom/exchange_fluxes.tsv",
        smetana_global   = RESULTS + "/smetana/global.tsv",
        smetana_detailed = RESULTS + "/smetana/detailed.tsv"
    output:
        per_species = RESULTS + "/comparison/per_species.tsv",
        community   = RESULTS + "/comparison/community_summary.tsv",
        plot        = RESULTS + "/comparison/comparison.png"
    log:
        LOGS + "/comparison/community_comparison.log"
    conda:
        "../envs/sensitivity.yaml"
    script:
        "../scripts/community_comparison.py"

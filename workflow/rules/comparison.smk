rule community_comparison:
    input:
        steadycom        = "results/steadycom/abundances.tsv",
        micom            = "results/micom/exchange_fluxes.tsv",
        smetana_global   = "results/smetana/global.tsv",
        smetana_detailed = "results/smetana/detailed.tsv",
    output:
        per_species = "results/comparison/per_species.tsv",
        community   = "results/comparison/community_summary.tsv",
        plot        = "results/comparison/comparison.png",
    log:
        "logs/comparison/community_comparison.log"
    conda:
        "../envs/sensitivity.yaml"
    script:
        "../scripts/community_comparison.py"
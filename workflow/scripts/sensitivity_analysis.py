__author__ = "Bruno Ferreira"
__license__ = "MIT"



from itertools import product
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


checkm_file     = snakemake.input.checkm
memote_file     = snakemake.input.memote
grid_out        = snakemake.output.grid
robustness_out  = snakemake.output.robustness
heatmap_out     = snakemake.output.heatmap
log_file        = snakemake.log[0]

compl_grid    = list(snakemake.params.checkm_completeness)
contam_grid   = list(snakemake.params.checkm_contamination)
memote_grid   = list(snakemake.params.memote_score)

baseline_compl   = float(snakemake.config["quality_filters"]["checkm"]["min_completeness"])
baseline_contam  = float(snakemake.config["quality_filters"]["checkm"]["max_contamination"])
baseline_memote  = float(snakemake.config["quality_filters"]["memote"]["min_total_score"])


def find_col(df, candidates):
    """Find first matching column from candidates (case-insensitive)."""
    lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    return None


def closest(grid, value):
    """Return value from grid closest to baseline."""
    return min(grid, key=lambda x: abs(x - value))


with open(log_file, "w") as logf:
    logf.write("Sensitivity analysis\n")
    logf.write(f"  completeness grid:  {compl_grid}\n")
    logf.write(f"  contamination grid: {contam_grid}\n")
    logf.write(f"  memote score grid:  {memote_grid}\n\n")

    checkm = pd.read_csv(checkm_file, sep="\t")
    memote = pd.read_csv(memote_file, sep="\t")

    logf.write(f"checkm columns: {list(checkm.columns)}\n")
    logf.write(f"memote columns: {list(memote.columns)}\n")

    mag_col_c    = find_col(checkm, ["mag", "bin", "genome", "name"])
    compl_col    = find_col(checkm, ["completeness", "Completeness"])
    contam_col   = find_col(checkm, ["contamination", "Contamination"])
    mag_col_m    = find_col(memote, ["mag"])
    score_col    = find_col(memote, ["total_score", "score"])

    if not all([mag_col_c, compl_col, contam_col, mag_col_m, score_col]):
        raise RuntimeError(
            f"Missing required columns. Found checkm={list(checkm.columns)}, "
            f"memote={list(memote.columns)}"
        )

    checkm = checkm.rename(columns={
        mag_col_c: "mag",
        compl_col: "completeness",
        contam_col: "contamination",
    })[["mag", "completeness", "contamination"]]

    memote = memote.rename(columns={
        mag_col_m: "mag",
        score_col: "total_score",
    })[["mag", "total_score"]]

    quality = checkm.merge(memote, on="mag", how="inner")
    quality["completeness"]  = pd.to_numeric(quality["completeness"],  errors="coerce")
    quality["contamination"] = pd.to_numeric(quality["contamination"], errors="coerce")
    quality["total_score"]   = pd.to_numeric(quality["total_score"],   errors="coerce")

    logf.write(f"\nMerged quality table ({len(quality)} MAGs):\n")
    logf.write(quality.to_string(index=False) + "\n\n")

    rows = []
    mag_pass_counts = {mag: 0 for mag in quality["mag"]}

    for compl, contam, mscore in product(compl_grid, contam_grid, memote_grid):
        passed = quality[
            (quality["completeness"]  >= compl) &
            (quality["contamination"] <= contam) &
            (quality["total_score"]   >= mscore)
        ]["mag"].tolist()

        for mag in passed:
            mag_pass_counts[mag] += 1

        rows.append({
            "min_completeness":   compl,
            "max_contamination":  contam,
            "min_total_score":    mscore,
            "n_passed":           len(passed),
            "mags_passed":        ",".join(sorted(passed)),
        })

    grid_df = pd.DataFrame(rows)
    grid_df.to_csv(grid_out, sep="\t", index=False)
    logf.write(f"Grid table written ({len(grid_df)} combinations) -> {grid_out}\n")

    total_combos = len(grid_df)
    robustness = pd.DataFrame([
        {"mag": mag, "n_passes": c, "fraction": c / total_combos}
        for mag, c in mag_pass_counts.items()
    ]).sort_values("fraction", ascending=False)
    robustness.to_csv(robustness_out, sep="\t", index=False)
    logf.write(f"Robustness table written -> {robustness_out}\n")

    fixed_m  = closest(memote_grid,  baseline_memote)
    fixed_c  = closest(contam_grid,  baseline_contam)
    fixed_cp = closest(compl_grid,   baseline_compl)

    slice_a = grid_df[grid_df["min_total_score"]   == fixed_m].pivot_table(
        index="min_completeness", columns="max_contamination", values="n_passed"
    )
    slice_b = grid_df[grid_df["max_contamination"] == fixed_c].pivot_table(
        index="min_total_score",  columns="min_completeness", values="n_passed"
    )
    slice_c = grid_df[grid_df["min_completeness"]  == fixed_cp].pivot_table(
        index="min_total_score",  columns="max_contamination", values="n_passed"
    )

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.heatmap(slice_a, annot=True, fmt=".0f", cmap="YlGnBu",
                ax=axes[0], cbar_kws={"label": "MAGs passing"})
    axes[0].set_title(f"CheckM thresholds  (Memote = {fixed_m})")
    axes[0].set_xlabel("Max contamination")
    axes[0].set_ylabel("Min completeness")

    sns.heatmap(slice_b, annot=True, fmt=".0f", cmap="YlGnBu",
                ax=axes[1], cbar_kws={"label": "MAGs passing"})
    axes[1].set_title(f"Memote × Completeness  (Contamination = {fixed_c})")
    axes[1].set_xlabel("Min completeness")
    axes[1].set_ylabel("Min total_score (Memote)")

    sns.heatmap(slice_c, annot=True, fmt=".0f", cmap="YlGnBu",
                ax=axes[2], cbar_kws={"label": "MAGs passing"})
    axes[2].set_title(f"Memote × Contamination  (Completeness = {fixed_cp})")
    axes[2].set_xlabel("Max contamination")
    axes[2].set_ylabel("Min total_score (Memote)")

    plt.suptitle("Sensitivity to quality thresholds — number of MAGs passing", y=1.02)
    plt.tight_layout()
    plt.savefig(heatmap_out, dpi=150, bbox_inches="tight")
    plt.close()
    logf.write(f"Heatmap saved -> {heatmap_out}\n")

    logf.write("\nDone.\n")
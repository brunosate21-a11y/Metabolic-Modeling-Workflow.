__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Three-method comparison of community-level predictions.

Cross-references SteadyCom (per-species abundance & growth),
SMETANA detailed (pairwise metabolite cross-feeding) and SMETANA global
(community-level MIP/MRO) into a single per-species table and figure.

The MICOM output is also loaded but, depending on the upstream script,
may currently mirror SteadyCom — a warning is written to the log if so.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



steadycom_file        = snakemake.input.steadycom
micom_file            = snakemake.input.micom
smetana_global_file   = snakemake.input.smetana_global
smetana_detailed_file = snakemake.input.smetana_detailed

per_species_out = snakemake.output.per_species
community_out   = snakemake.output.community
plot_out        = snakemake.output.plot
log_file        = snakemake.log[0]


def load_members(path, suffix):
    """Load a 'members'-style TSV (SteadyCom or MICOM), drop the 'medium' row."""
    df = pd.read_csv(path, sep="\t")
    df = df[df["compartments"] != "medium"].copy()
    df = df.rename(columns={
        "compartments": "mag",
        "abundance":    f"abundance_{suffix}",
        "growth_rate":  f"growth_{suffix}",
    })
    return df[["mag", f"abundance_{suffix}", f"growth_{suffix}"]]


def load_smetana_per_species(path):
    """Per-species donor/receiver counts + unique compounds donated."""
    df = pd.read_csv(path, sep="\t")
    out = pd.DataFrame({"mag": sorted(set(df["donor"]) | set(df["receiver"]))})
    out["n_as_donor"]    = out["mag"].map(df.groupby("donor").size()).fillna(0).astype(int)
    out["n_as_receiver"] = out["mag"].map(df.groupby("receiver").size()).fillna(0).astype(int)
    out["unique_compounds_donated"] = (
        out["mag"].map(df.groupby("donor")["compound"].nunique()).fillna(0).astype(int)
    )
    return out


def load_smetana_community(path):
    return pd.read_csv(path, sep="\t").iloc[0].to_dict()


with open(log_file, "w") as logf:
    logf.write("Three-method community comparison\n\n")

    sc = load_members(steadycom_file, "steadycom")
    mc = load_members(micom_file, "micom")
    sm_sp = load_smetana_per_species(smetana_detailed_file)
    sm_com = load_smetana_community(smetana_global_file)

    # Detect the MICOM duplication bug
    micom_warning = False
    if sc.shape == mc.shape:
        sc_vals = sc[["abundance_steadycom", "growth_steadycom"]].to_numpy()
        mc_vals = mc[["abundance_micom",     "growth_micom"]].to_numpy()
        if np.allclose(sc_vals, mc_vals):
            micom_warning = True
            logf.write(
                "WARNING: MICOM output is identical to SteadyCom output — \n"
                "  micom_script.py is probably saving the wrong dataframe. \n"
                "  Comparison will rely on SteadyCom + SMETANA only. \n\n"
            )

    merged = sc.merge(mc, on="mag", how="outer").merge(sm_sp, on="mag", how="left").fillna(0)
    merged = merged.sort_values("growth_steadycom", ascending=False).reset_index(drop=True)
    merged.to_csv(per_species_out, sep="\t", index=False)

    n_pairs   = pd.read_csv(smetana_detailed_file, sep="\t").shape[0]
    n_unique  = pd.read_csv(smetana_detailed_file, sep="\t")["compound"].nunique()
    com_df = pd.DataFrame([{
        "n_species":              len(merged),
        "mip":                    sm_com.get("mip"),
        "mro":                    sm_com.get("mro"),
        "n_cross_feeding_pairs":  n_pairs,
        "n_unique_metabolites":   n_unique,
    }])
    com_df.to_csv(community_out, sep="\t", index=False)

    if len(merged) >= 3:
        corr = merged[["growth_steadycom", "n_as_donor"]].corr().iloc[0, 1]
    else:
        corr = float("nan")
    logf.write(f"Growth × N_as_donor correlation (Pearson): {corr:.3f}\n")
    logf.write(f"Per-species table written -> {per_species_out}\n")
    logf.write(f"Community summary written -> {community_out}\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    ax1.scatter(merged["growth_steadycom"], merged["n_as_donor"], s=120, alpha=0.8)
    for _, r in merged.iterrows():
        ax1.annotate(r["mag"], (r["growth_steadycom"], r["n_as_donor"]),
                     fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax1.set_xlabel("Growth rate (SteadyCom)")
    ax1.set_ylabel("N metabolites donated (SMETANA)")
    ax1.set_title(
        "Convergence: do fast growers donate more?\n"
        f"Pearson r = {corr:.2f}"
    )

    x = np.arange(len(merged))
    width = 0.35
    ax2.bar(x - width/2, merged["n_as_donor"],    width, label="As donor")
    ax2.bar(x + width/2, merged["n_as_receiver"], width, label="As receiver")
    ax2.set_xticks(x)
    ax2.set_xticklabels(merged["mag"], rotation=20, ha="right", fontsize=9)
    ax2.set_ylabel("N metabolite exchanges (SMETANA)")
    mip = sm_com.get("mip")
    mro = sm_com.get("mro")
    ax2.set_title(
        f"Cross-feeding pattern\nCommunity MIP = {mip}, MRO = {mro:.2f}"
    )
    ax2.legend()

    fig.suptitle(
        f"Three-method community comparison — {len(merged)} species" +
        ("  ⚠ MICOM output unusable, see log" if micom_warning else ""),
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(plot_out, dpi=150, bbox_inches="tight")
    plt.close()

    logf.write(f"Figure written -> {plot_out}\nDone.\n")
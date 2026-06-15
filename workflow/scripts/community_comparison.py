__author__ = "Bruno Ferreira"
__license__ = "MIT"

"""
Three-method comparison: SteadyCom (abundance/growth), MICOM (exchange fluxes),
SMETANA (predicted cross-feeding pairs).
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


def load_steadycom(path):
    df = pd.read_csv(path, sep="\t")
    df = df[df["compartments"] != "medium"]
    return df.rename(columns={
        "compartments": "mag",
        "abundance":   "abundance_steadycom",
        "growth_rate": "growth_steadycom",
    })[["mag", "abundance_steadycom", "growth_steadycom"]]


def load_micom_per_species(path):
    """Compute per-taxon metrics from MICOM exchange fluxes (long format)."""
    df = pd.read_csv(path, sep="\t")
    df = df[df["taxon"] != "medium"]

    grouped = df.groupby("taxon")
    out = pd.DataFrame({
        "n_produced_micom":  grouped["direction"].apply(lambda x: (x == "produced").sum()),
        "n_consumed_micom":  grouped["direction"].apply(lambda x: (x == "consumed").sum()),
        "total_flux_micom":  grouped["flux"].apply(lambda x: x.abs().sum()),
    }).reset_index().rename(columns={"taxon": "mag"})
    return out


def load_smetana_per_species(path):
    df = pd.read_csv(path, sep="\t")
    mags = sorted(set(df["donor"]) | set(df["receiver"]))
    out  = pd.DataFrame({"mag": mags})
    out["n_donor_smetana"]    = out["mag"].map(df.groupby("donor").size()).fillna(0).astype(int)
    out["n_receiver_smetana"] = out["mag"].map(df.groupby("receiver").size()).fillna(0).astype(int)
    return out


def load_smetana_community(path):
    return pd.read_csv(path, sep="\t").iloc[0].to_dict()


with open(log_file, "w") as logf:
    logf.write("Three-method community comparison\n\n")

    sc       = load_steadycom(steadycom_file)
    mc       = load_micom_per_species(micom_file)
    sm_sp    = load_smetana_per_species(smetana_detailed_file)
    sm_com   = load_smetana_community(smetana_global_file)

    merged = (sc.merge(mc, on="mag", how="outer")
                .merge(sm_sp, on="mag", how="outer")
                .fillna(0))
    merged = merged.sort_values("growth_steadycom", ascending=False).reset_index(drop=True)
    merged.to_csv(per_species_out, sep="\t", index=False)

    n_pairs  = pd.read_csv(smetana_detailed_file, sep="\t").shape[0]
    n_unique = pd.read_csv(smetana_detailed_file, sep="\t")["compound"].nunique()
    pd.DataFrame([{
        "n_species":             len(merged),
        "mip":                   sm_com.get("mip"),
        "mro":                   sm_com.get("mro"),
        "n_cross_feeding_pairs": n_pairs,
        "n_unique_metabolites":  n_unique,
    }]).to_csv(community_out, sep="\t", index=False)

    def corr(a, b):
        if merged[a].std() == 0 or merged[b].std() == 0:
            return float("nan")
        return merged[[a, b]].corr().iloc[0, 1]

    corr_growth_donor  = corr("growth_steadycom",  "n_donor_smetana")
    corr_produce_donate = corr("n_produced_micom", "n_donor_smetana")
    corr_consume_recv   = corr("n_consumed_micom", "n_receiver_smetana")

    logf.write(f"Pearson r(growth_SC, n_donor_SMETANA)        = {corr_growth_donor:.3f}\n")
    logf.write(f"Pearson r(n_produced_MICOM, n_donor_SMETANA)  = {corr_produce_donate:.3f}\n")
    logf.write(f"Pearson r(n_consumed_MICOM, n_receiver_SMETANA) = {corr_consume_recv:.3f}\n\n")

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))

    ax = axes[0]
    ax.scatter(merged["growth_steadycom"], merged["n_donor_smetana"], s=120, alpha=0.8)
    for _, r in merged.iterrows():
        ax.annotate(r["mag"], (r["growth_steadycom"], r["n_donor_smetana"]),
                    fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax.set_xlabel("Growth rate (SteadyCom)")
    ax.set_ylabel("N donated (SMETANA)")
    ax.set_title(f"SC × SMETANA\nPearson r = {corr_growth_donor:.2f}")

    ax = axes[1]
    ax.scatter(merged["n_produced_micom"], merged["n_donor_smetana"], s=120, alpha=0.8, c="darkorange")
    for _, r in merged.iterrows():
        ax.annotate(r["mag"], (r["n_produced_micom"], r["n_donor_smetana"]),
                    fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax.set_xlabel("N produced (MICOM)")
    ax.set_ylabel("N donated (SMETANA)")
    ax.set_title(f"MICOM × SMETANA (produção)\nPearson r = {corr_produce_donate:.2f}")

    ax = axes[2]
    x = np.arange(len(merged)); w = 0.2
    ax.bar(x - 1.5*w, merged["n_produced_micom"], w, label="Produced (MICOM)")
    ax.bar(x - 0.5*w, merged["n_donor_smetana"],  w, label="Donor (SMETANA)")
    ax.bar(x + 0.5*w, merged["n_consumed_micom"], w, label="Consumed (MICOM)")
    ax.bar(x + 1.5*w, merged["n_receiver_smetana"], w, label="Receiver (SMETANA)")
    ax.set_xticks(x)
    ax.set_xticklabels(merged["mag"], rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Contagem")
    ax.set_title(f"MICOM × SMETANA por espécie\nMIP={sm_com.get('mip')}, MRO={sm_com.get('mro'):.2f}")
    ax.legend(fontsize=8)

    fig.suptitle(f"Three-method community comparison — {len(merged)} species", y=1.02)
    plt.tight_layout()
    plt.savefig(plot_out, dpi=150, bbox_inches="tight")
    plt.close()

    logf.write(f"Figure -> {plot_out}\nDone.\n")
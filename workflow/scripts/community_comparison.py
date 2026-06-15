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

    corr_growth_donor   = corr("growth_steadycom",  "n_donor_smetana")
    corr_produce_donate = corr("n_produced_micom", "n_donor_smetana")
    corr_consume_recv   = corr("n_consumed_micom", "n_receiver_smetana")

    logf.write(f"Pearson r(growth_SC, n_donor_SMETANA)           = {corr_growth_donor:.3f}\n")
    logf.write(f"Pearson r(n_produced_MICOM, n_donor_SMETANA)    = {corr_produce_donate:.3f}\n")
    logf.write(f"Pearson r(n_consumed_MICOM, n_receiver_SMETANA) = {corr_consume_recv:.3f}\n\n")

 
    def short(name):
        return str(name).split("_")[-1]

    merged["label"] = merged["mag"].map(short)

    n = len(merged)
    bar_width_in = max(10, n * 0.9)

    fig = plt.figure(figsize=(max(16, bar_width_in), 11))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.32, wspace=0.22)

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.scatter(merged["growth_steadycom"], merged["n_donor_smetana"], s=130, alpha=0.8)
    for _, r in merged.iterrows():
        ax0.annotate(r["label"], (r["growth_steadycom"], r["n_donor_smetana"]),
                     fontsize=9, xytext=(5, 5), textcoords="offset points")
    ax0.set_xlabel("Taxa de crescimento (SteadyCom)")
    ax0.set_ylabel("Nº metabolitos doados (SMETANA)")
    ax0.set_title(f"SteadyCom × SMETANA   (r = {corr_growth_donor:.2f})")

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.scatter(merged["n_produced_micom"], merged["n_donor_smetana"],
                s=130, alpha=0.8, c="darkorange")
    for _, r in merged.iterrows():
        ax1.annotate(r["label"], (r["n_produced_micom"], r["n_donor_smetana"]),
                     fontsize=9, xytext=(5, 5), textcoords="offset points")
    ax1.set_xlabel("Nº metabolitos produzidos (MICOM)")
    ax1.set_ylabel("Nº metabolitos doados (SMETANA)")
    ax1.set_title(f"MICOM × SMETANA   (r = {corr_produce_donate:.2f})")

    ax2 = fig.add_subplot(gs[1, :])
    x = np.arange(n)
    w = 0.2
    ax2.bar(x - 1.5*w, merged["n_produced_micom"],   w, label="Produzidos (MICOM)")
    ax2.bar(x - 0.5*w, merged["n_donor_smetana"],    w, label="Doados (SMETANA)")
    ax2.bar(x + 0.5*w, merged["n_consumed_micom"],   w, label="Consumidos (MICOM)")
    ax2.bar(x + 1.5*w, merged["n_receiver_smetana"], w, label="Recebidos (SMETANA)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(merged["label"], rotation=90, fontsize=9)
    ax2.set_xlabel("Bin (sufixo)")
    ax2.set_ylabel("Contagem de metabolitos")
    mro_val = sm_com.get("mro")
    try:
        mro_str = f"{float(mro_val):.2f}"
    except (ValueError, TypeError):
        mro_str = str(mro_val)
    ax2.set_title(f"Papéis por espécie — MIP={sm_com.get('mip')}, MRO={mro_str}")
    ax2.legend(fontsize=9, ncol=4, loc="upper right")

    fig.suptitle(f"Comparação de três métodos — comunidade de {n} espécies",
                 y=0.995, fontsize=14)
    plt.savefig(plot_out, dpi=150, bbox_inches="tight")
    plt.close()

    logf.write(f"Figure -> {plot_out}\nDone.\n")

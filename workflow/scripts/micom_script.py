__author__ = "Bruno Ferreira"
__license__ = "MIT"

import os
import pandas as pd
from micom import Community


models       = snakemake.input.models
exchange_out = snakemake.output.exchange_fluxes
model_paths  = [models] if isinstance(models, str) else list(models)
os.makedirs(os.path.dirname(exchange_out), exist_ok=True)


abundances_file = None
if hasattr(snakemake.input, "abundances"):
    af = snakemake.input.abundances
    af = af[0] if isinstance(af, list) and af else (af if isinstance(af, str) else None)
    abundances_file = af or None


def build_taxonomy(model_paths, abundances_file):
    ids = [os.path.splitext(os.path.basename(p))[0] for p in model_paths]

    if abundances_file and os.path.exists(abundances_file):
        ab = pd.read_csv(abundances_file, sep="\t")
        col = "abundance_renorm" if "abundance_renorm" in ab.columns else "abundance"
        ab = ab[ab[col] > 0]
        amap = dict(zip(ab["sample"], ab[col]))

        keep = [(i, p) for i, p in zip(ids, model_paths) if i in amap]
        if not keep:
            raise ValueError("Nenhum modelo corresponde às abundâncias aprovadas.")
        ids_k  = [i for i, _ in keep]
        path_k = [p for _, p in keep]
        abund  = [amap[i] for i in ids_k]
        s = sum(abund)
        abund = [a / s for a in abund]
        print(f"Abundâncias REAIS: {len(ids_k)} modelos (de {len(ids)} fornecidos)")
        return pd.DataFrame({"id": ids_k, "file": path_k, "abundance": abund})

    print(f"Abundâncias UNIFORMES: 1/{len(ids)} para cada modelo")
    return pd.DataFrame({
        "id": ids, "file": model_paths,
        "abundance": [1.0 / len(model_paths)] * len(model_paths),
    })


taxonomy = build_taxonomy(model_paths, abundances_file)

print(f"A construir comunidade com {len(taxonomy)} modelo(s)...")
com = Community(taxonomy, solver="glpk")

print("A correr optimize (FBA)...")
sol = com.optimize(fluxes=True)

print("Members:")
print(sol.members)

print("A extrair exchange fluxes...")

exchange_cols = [c for c in sol.fluxes.columns if c.startswith("EX_")]
exchange_df   = sol.fluxes[exchange_cols].copy()
exchange_df.index.name = "taxon"

long_df = exchange_df.reset_index().melt(
    id_vars="taxon", var_name="reaction", value_name="flux"
)

long_df["direction"] = long_df["flux"].apply(
    lambda x: "produced" if x > 1e-9 else ("consumed" if x < -1e-9 else "zero")
)
long_df = long_df[long_df["direction"] != "zero"].copy()

long_df["metabolite"] = (
    long_df["reaction"]
      .str.replace(r"^EX_", "", regex=True)
      .str.replace(r"_e$",  "", regex=True)
)

long_df = (
    long_df[["taxon", "reaction", "metabolite", "direction", "flux"]]
    .sort_values(["taxon", "direction", "flux"], ascending=[True, True, False])
)

print(f"A guardar {len(long_df)} fluxos de troca não-zero em {exchange_out}")
long_df.to_csv(exchange_out, sep="\t", index=False)

__author__ = "Bruno Ferreira"
__license__ = "MIT"

import os
import pandas as pd
from micom import Community


models       = snakemake.input.models
exchange_out = snakemake.output.exchange_fluxes
model_paths  = [models] if isinstance(models, str) else list(models)
os.makedirs(os.path.dirname(exchange_out), exist_ok=True)

taxonomy = pd.DataFrame({
    "id":        [os.path.splitext(os.path.basename(p))[0] for p in model_paths],
    "file":      model_paths,
    "abundance": [1.0 / len(model_paths)] * len(model_paths),
})

print(f"A construir comunidade com {len(model_paths)} modelo(s)...")
com = Community(taxonomy, solver="glpk")

print("A correr optimize (FBA)...")
sol = com.optimize()

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

print("MICOM concluido.")
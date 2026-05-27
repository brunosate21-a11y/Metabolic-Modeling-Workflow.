__author__ = "Bruno Ferreira"
__license__ = "MIT"
import os
import pandas as pd
from micom import Community

models = snakemake.input.models
abundances_out = snakemake.output.abundances
model_paths = [models] if isinstance(models, str) else list(models)
os.makedirs(os.path.dirname(abundances_out), exist_ok=True)

taxonomy = pd.DataFrame({
    "id": [os.path.splitext(os.path.basename(p))[0] for p in model_paths],
    "file": model_paths,
    "abundance": [1.0 / len(model_paths)] * len(model_paths),
})

print(f"A construir comunidade com {len(model_paths)} modelo(s)...")
com = Community(taxonomy, solver="glpk")
print("A correr optimize (FBA)...")
sol = com.optimize()
print("Members:")
print(sol.members)
sol.members.to_csv(abundances_out, sep="\t")
print(f"SteadyCom concluido. Resultados guardados em {abundances_out}")
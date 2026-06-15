__author__ = "Bruno Ferreira"
__license__ = "MIT"

import sys
import os
import shutil
from pathlib import Path
from snakemake.shell import shell

models = snakemake.input.models
global_out = snakemake.output.global_scores
detailed_out = snakemake.output.detailed
solver = snakemake.params.get("solver", "scip")

if isinstance(models, str):
    models_str = models
else:
    models_str = " ".join(models)

smetana_path = str(Path(sys.executable).parent / "smetana")

log_str = snakemake.log_fmt_shell(stdout=True, stderr=True)
log_append_str = log_str.replace(">", ">>", 1) if ">" in log_str else log_str

os.makedirs(os.path.dirname(global_out), exist_ok=True)

prefix = os.path.join(os.path.dirname(global_out), "smetana").replace("\\", "/")

shell(f"python {smetana_path} {models_str} -g --solver {solver} -o {prefix} {log_str}")
shutil.move(f"{prefix}_global.tsv", global_out)

shell(f"python {smetana_path} {models_str} -d --solver {solver} -o {prefix} {log_append_str}")
shutil.move(f"{prefix}_detailed.tsv", detailed_out)
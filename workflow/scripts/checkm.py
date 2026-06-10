__author__ = "Bruno Ferreira"
__license__ = "MIT"

from snakemake.shell import shell

genome = snakemake.input.genome
output_dir = snakemake.output.output_dir
quality = snakemake.output.quality

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

shell(
    "checkm lineage_wf "
    "--genes "
    "-x faa "
    "--reduced_tree "                   
    "-t {snakemake.threads} "
    "--tab_table "
    "-f {quality} "
    "$(dirname {genome}) "
    "{output_dir} "
    "{log}"
)
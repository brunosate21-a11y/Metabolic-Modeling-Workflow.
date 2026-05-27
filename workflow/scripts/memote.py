__author__ = "Bruno Ferreira"
__license__ = "MIT"

from snakemake.shell import shell

model = snakemake.input.model
report = snakemake.output.report
score = snakemake.output.score

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

shell("memote report snapshot " "--filename {report} " "{model} " "{log}")
shell("memote run " "--ignore-git " "--filename {score} " "{model} " "{log}")
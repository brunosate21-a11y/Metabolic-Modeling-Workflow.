__author__ = "Bruno Ferreira"
__license__ = "MIT"

import cobra
from memote.suite.api import test_model
from memote.suite.reporting import SnapshotReport, ReportConfiguration

model_file  = snakemake.input.model
report_file = snakemake.output.report
score_file  = snakemake.output.score


model = cobra.io.read_sbml_model(model_file)

_, result = test_model(model, results=True)

config = ReportConfiguration.load()
report = SnapshotReport(result=result, configuration=config)

with open(report_file, "w", encoding="utf-8") as f:
    f.write(report.render_html())

with open(score_file, "w", encoding="utf-8") as f:
    f.write(report.render_json())
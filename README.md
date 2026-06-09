# Metabolic Modeling Workflow

> Automated genome-scale metabolic reconstruction and microbial community simulation from MAGs.

[![Snakemake](https://img.shields.io/badge/snakemake-≥8.0-brightgreen.svg)](https://snakemake.github.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Conda](https://img.shields.io/badge/conda-managed-44A833.svg)](https://docs.conda.io)

A reproducible Snakemake pipeline that reconstructs genome-scale metabolic models (GEMs) from metagenome-assembled genomes (MAGs) and simulates their interactions in microbial communities.

---

## ✨ Features

- 🧬 **Auto-detection of MAGs** — drop `.faa` files in `data/mags/` and the workflow picks them up automatically
- 🏗️ **Model reconstruction** with **CarveMe** (reference universe + gap-filling)
- ✅ **Quality assessment** via **Memote** with score-based filtering
- 🤝 **Three complementary community simulation approaches:**
  - **SMETANA** — metabolic interaction potential
  - **MICOM** — cooperative community FBA
  - **SteadyCom** — steady-state community abundances
- 📦 **Reproducible** — per-rule Conda environments
- ⚡ **Solver-agnostic** — works with SCIP (default), CPLEX, or Gurobi

---

## 📋 Requirements

- **OS:** Linux (native) or **Windows + WSL2** *(CarveMe is not supported on Windows native)*
- **Miniconda / Anaconda**
- **Snakemake** ≥ 8.0
- **LP solver:** SCIP (free, included) or CPLEX (recommended for community simulations)

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/brunosate21-a11y/Metabolic-Modeling-Workflow..git
cd Metabolic-Modeling-Workflow.
```

### 2. Set up the Snakemake environment

```bash
conda create -n snakemake -c bioconda -c conda-forge snakemake -y
conda activate snakemake
```

### 3. Add your MAGs

Place protein FASTA files (`.faa`) into `data/mags/`:

```
data/mags/
├── Ecoli_K12.faa
├── Bsubtilis_168.faa
└── ...
```

Or use the included NCBI download helper (Windows PowerShell):

```powershell
.\download_mags.ps1
```

### 4. (Optional) Tune the config

Edit `config/config.yaml`:

```yaml
solver: scip          # or cplex / gurobi
media: M9             # gap-fill medium

quality_filters:
  memote:
    min_total_score: 0.4
```

### 5. Run the pipeline

```bash
snakemake --use-conda --cores 12
```

That's it. The workflow handles dependency resolution, conda environments, and parallel execution.

---

## 📁 Project Structure

```
.
├── config/
│   └── config.yaml              # Pipeline configuration
├── data/
│   └── mags/                    # Input .faa files (drop here)
├── download_mags.ps1            # NCBI download helper
├── workflow/
│   ├── Snakefile                # Main entry point
│   ├── envs/                    # Conda environment definitions
│   ├── rules/                   # Snakemake rules (.smk)
│   └── scripts/                 # Python execution scripts
└── results/                     # Generated outputs (see below)
```

---

## 📤 Outputs

After a successful run, `results/` will contain:

```
results/
├── gems/
│   └── <MAG>.xml                # CarveMe-built GEMs (SBML format)
├── memote/
│   ├── <MAG>/report.html        # Interactive quality reports
│   ├── memote_summary.tsv       # Aggregated quality scores
│   └── filtered_models.txt      # Models that passed the threshold
├── micom/
│   └── exchange_fluxes.tsv      # Metabolite exchange fluxes
├── smetana/
│   ├── global.tsv               # MIP / MRO community-level scores
│   └── detailed.tsv             # Pairwise interaction predictions
└── steadycom/
    └── abundances.tsv           # Steady-state abundances
```

---

## 🔧 Scaling: Adding More MAGs

The pipeline scales automatically — **no code changes required**.

### Manual

1. Drop new `.faa` files into `data/mags/`
2. Re-run `snakemake --use-conda --cores 12`

### From NCBI

1. Edit the `$genomes` block in `download_mags.ps1`:

```powershell
   $genomes = @{
       "OrgName_strain" = "GCF_xxxxxxxxx.x"
   }
```

2. Run the script — files are downloaded, renamed, and placed in `data/mags/`
3. Run Snakemake — the new MAGs are detected and included

---

## ⚙️ Configuration Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `solver` | LP/MILP solver (`scip`, `cplex`, `gurobi`) | `scip` |
| `media` | Gap-fill culture medium | `M9` |
| `quality_filters.checkm.min_completeness` | Min CheckM completeness (%) | `50.0` |
| `quality_filters.checkm.max_contamination` | Max CheckM contamination (%) | `10.0` |
| `quality_filters.memote.min_total_score` | Min Memote total score | `0.4` |

---

## ⚡ Performance Tip: Use CPLEX

For community simulations (especially SMETANA), the LP solver dominates the runtime. With the same workflow:

| Solver | SMETANA runtime (4 organisms) |
|--------|-------------------------------|
| SCIP (default) | ~60–90 min |
| **CPLEX (academic)** | **~5–15 min** ⚡ |

To switch, install CPLEX Optimization Studio (free for academia via the [IBM Academic Initiative](https://academic.ibm.com)) and set `solver: cplex` in `config/config.yaml`.

---

## 🛠️ Tools

This workflow integrates several established open-source tools:

- **[CarveMe](https://github.com/cdanielmachado/carveme)** — GEM reconstruction
- **[Memote](https://github.com/opencobra/memote)** — Model quality assessment
- **[SMETANA](https://github.com/cdanielmachado/smetana)** — Metabolic interaction analysis
- **[MICOM](https://github.com/micom-dev/micom)** — Community modeling
- **[Snakemake](https://snakemake.readthedocs.io/)** — Workflow management

---

## 👤 Author

**Bruno Ferreira** ;
**Artur Gomes**

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

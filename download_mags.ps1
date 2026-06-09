# Lista de genomas: nome_genoma = accession_NCBI
$genomes = @{
    "Ecoli_K12"               = "GCF_000005845.2"
    "Btheta_VPI5482"          = "GCF_000011065.1"
    "Fprausnitzii_A2165"      = "GCF_902167865.1"
    "Akkermansia_muciniphila" = "GCF_000020225.1"
}


New-Item -ItemType Directory -Force -Path "data/mags" | Out-Null

foreach ($name in $genomes.Keys) {
    $acc = $genomes[$name]
    Write-Host "[$name] A descarregar $acc..." -ForegroundColor Cyan

    datasets download genome accession $acc --include protein
    Expand-Archive ncbi_dataset.zip -DestinationPath temp_extract -Force
    Move-Item "temp_extract/ncbi_dataset/data/$acc/protein.faa" "data/mags/$name.faa" -Force
    Remove-Item -Recurse -Force temp_extract, ncbi_dataset.zip

    Write-Host "[$name] Concluido -> data/mags/$name.faa" -ForegroundColor Green
}

Write-Host "`nTodos os MAGs descarregados!" -ForegroundColor Yellow
ls data/mags/*.faa
# Lista de genomas: nome_genoma = accession_NCBI
$genomes = @{
    "Ecoli_K12"                         = "GCF_000005845.2"
    "Pputida_NBRC14164"                 = "GCF_000412675.1"
    "Bsubtilis_168"                     = "GCF_000009045.1"   
    "Streptococcus_TIGR4"               = "GCF_000006885.1"
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
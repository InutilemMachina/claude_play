# 04_nlm_queries.ps1 -- mindmap-alapu NLM lekerdezesek
# Mindmap gyoker: "A Fourier-transzformacio es a digitalis jelfeldolgozas alapjai"
# Sablon: pipeline.md 3. szekcio

$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
$NB  = "92ecc692-3938-49a2-b616-279d6c77f450"
$OUT = "C:\Users\lasz\claude_play\test_outputs\DFT_teszt\1_het\3_raw_outputs"

# Q1 -- Gyoker csomopont: bevezeto
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q1 indul (gyoker: Fourier-transzformacio es digitalis jelfeldolgozas alapjai)..."
$r1 = nlm query notebook $NB "Beszeljen az ezekben a forrasokban targyalt Fourier-transzformacio es a digitalis jelfeldolgozas alapjai temakorrol." --json 2>&1
$r1 | Out-File "$OUT\nlm_q1_raw.txt" -Encoding utf8
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q1 kesz."

# Q2 -- 2. szint: DFT + Domainek
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q2 indul (DFT + Domainek)..."
$r2 = nlm query notebook $NB "Beszeljen az ezekben a forrasokban targyalt, a Fourier-transzformacio tagabb kontextusaba tartozo DFT (Diszkret Fourier Transzformacio) es a kapcsolodo domainek (idotartomany, frekvenciatartomany) temakorrol." --json 2>&1
$r2 | Out-File "$OUT\nlm_q2_raw.txt" -Encoding utf8
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q2 kesz."

# Q3 -- 2. szint: FFT
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q3 indul (FFT)..."
$r3 = nlm query notebook $NB "Beszeljen az ezekben a forrasokban targyalt, a Fourier-transzformacio tagabb kontextusaba tartozo FFT (Fast Fourier Transform) temakorrol." --json 2>&1
$r3 | Out-File "$OUT\nlm_q3_raw.txt" -Encoding utf8
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q3 kesz."

# Q4 -- 2. szint: Spektrum tipusok + Gyakorlati tenyezok
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q4 indul (Spektrum + Gyakorlati tenyezok)..."
$r4 = nlm query notebook $NB "Beszeljen az ezekben a forrasokban targyalt, a Fourier-transzformacio tagabb kontextusaba tartozo spektrum tipusok es skalazas, valamint a gyakorlati tenyezok temakorrol." --json 2>&1
$r4 | Out-File "$OUT\nlm_q4_raw.txt" -Encoding utf8
Write-Output "[$(Get-Date -Format HH:mm:ss)] Q4 kesz."

Write-Output "PIPELINE KESZ"

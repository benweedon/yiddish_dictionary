param(
    [String]$InputFile,
    [String]$OutputFile
)

$dict = @{}
$html = [xml](Get-Content (Resolve-Path $InputFile) -Encoding UTF8)
foreach ($tr in $html.ChildNodes[0].ChildNodes) {
    $english = $tr.ChildNodes[0].InnerText.Trim()
    $pronunciation = $tr.ChildNodes[2].InnerText.Trim()
    $pos = $tr.ChildNodes[3].InnerText.Trim()
    $yiddish = $tr.ChildNodes[4].InnerText.Trim()
    $dict[$yiddish] = @{english=$english; pronunciation=$pronunciation; pos=$pos}
}

Write-Output "" > $OutputFile
$outFile = Resolve-Path $OutputFile
[System.IO.File]::WriteAllLines($outFile, (ConvertTo-Json $dict))

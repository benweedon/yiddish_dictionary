param(
    [String]$InputFile,
    [String]$OutputFile
)

function Remove-Punctuation($s) {
    $punctuation_regex = '[`~!@#$%^&*()_+={}[\]\\|;:''"<>,./?\u2000-\u206F\u2E00-\u2E7F]+'
    $s = $s -replace $punctuation_regex,''
    return $s.Trim()
}

$dict = @{}
$html = [xml](Get-Content (Resolve-Path $InputFile) -Encoding UTF8)
foreach ($tr in $html.ChildNodes[0].ChildNodes) {
    $english = $tr.ChildNodes[0].InnerText.Trim()
    $pronunciation = $tr.ChildNodes[2].InnerText.Trim()
    $pos = $tr.ChildNodes[3].InnerText.Trim()
    $yiddish = $tr.ChildNodes[4].InnerText.Trim()

    $pronunciation = $pronunciation.Split('/')
    foreach ($i in 0..($pronunciation.Length-1)) {
        $pronunciation[$i] = $pronunciation[$i].Trim()
    }

    $yiddish = Remove-Punctuation $yiddish

    if (!$dict.ContainsKey($yiddish)) {
        $dict[$yiddish] = @{english=$english; pronunciation=$pronunciation; pos=$pos}
    }
}

Write-Output "" > $OutputFile
$outFile = Resolve-Path $OutputFile
[System.IO.File]::WriteAllLines($outFile, (ConvertTo-Json $dict))

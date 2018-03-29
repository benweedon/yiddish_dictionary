param(
    [String]$InputFile,
    [String]$OutputFile
)

function Remove-Punctuation($s) {
    $punctuation_regex = '[`~!@#$%^&*()_+={}[\]\\|;:''"<>,./?\u2000-\u206F\u2E00-\u2E7F]+'
    $s = $s -replace $punctuation_regex,''
    return $s.Trim()
}

function Combine-Entries($entry1, $entry2) {
    $newEntry = @{}
    $newEntry['eng'] = $entry1['eng'] + $entry2['eng'] | Select-Object -Unique
    $newEntry['_pro'] = $entry1['_pro'] + $entry2['_pro'] | Select-Object -Unique
    $newEntry['_pos'] = $entry1['_pos'] + $entry2['_pos'] | Select-Object -Unique
    return $newEntry
}

$dict = @{}
$html = [xml](Get-Content (Resolve-Path $InputFile) -Encoding UTF8)
foreach ($tr in $html.ChildNodes[0].ChildNodes) {
    $english = $tr.ChildNodes[0].InnerText.Trim()
    $pronunciation = $tr.ChildNodes[2].InnerText.Trim()
    $pos = $tr.ChildNodes[3].InnerText.Trim()
    $yiddish = $tr.ChildNodes[4].InnerText.Trim()

    $english = $english.Split(',;')
    foreach ($i in 0..($english.Length-1)) {
        $english[$i] = $english[$i].Trim()
    }

    $pronunciation = $pronunciation.Split('/')
    foreach ($i in 0..($pronunciation.Length-1)) {
        $pronunciation[$i] = $pronunciation[$i].Trim()
    }

    $pos = @($pos)

    $yiddish = Remove-Punctuation $yiddish

    $entry = @{eng=$english; _pro=$pronunciation; _pos=$pos}
    if (!$dict.ContainsKey($yiddish)) {
        $dict[$yiddish] = $entry
    } else {
        $dict[$yiddish] = Combine-Entries $entry $dict[$yiddish]
    }
}

Write-Output "" > $OutputFile
$outFile = Resolve-Path $OutputFile
[System.IO.File]::WriteAllLines($outFile, (ConvertTo-Json $dict))

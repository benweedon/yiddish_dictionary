﻿param(
    [String]$InputFile,
    [String]$OutputFile
)

function Combine-Entries($entry1, $entry2) {
    $newEntry = @{}
    $newEntry['eng'] = @($entry1['eng'] + $entry2['eng'] | Select-Object -Unique)
    $newEntry['_pro'] = @($entry1['_pro'] + $entry2['_pro'] | Select-Object -Unique)
    $newEntry['_pos'] = @($entry1['_pos'] + $entry2['_pos'] | Select-Object -Unique)
    return $newEntry
}

$dict = @{}
$html = [xml](Get-Content (Resolve-Path $InputFile) -Encoding UTF8)
foreach ($tr in $html.ChildNodes[0].ChildNodes) {
    $english = $tr.ChildNodes[0].InnerText.Trim()
    $pronunciation = $tr.ChildNodes[2].InnerText.Trim()
    $pos = $tr.ChildNodes[3].InnerText.Trim()
    $yiddish = $tr.ChildNodes[4].InnerText.Trim()

    if ($english -eq '') {
        $english = @()
    } else {
        $english = $english.Split(',;')
        foreach ($i in 0..($english.Length-1)) {
            $english[$i] = $english[$i].Trim()
        }
    }

    if ($pronunciation -eq '∙') {
        $pronunciation = ''
    }
    if ($pronunciation -eq '') {
        $pronunciation = @()
    } else {
        $pronunciation = $pronunciation.Split('/')
        foreach ($i in 0..($pronunciation.Length-1)) {
            $pronunciation[$i] = $pronunciation[$i].Trim()
        }
    }

    if ($pos -eq '') {
        $pos = @()
    } else {
        $pos = @($pos)
    }

    $entry = @{eng=$english; _pro=$pronunciation; _pos=$pos; _src=@('ydo')}
    if (!$dict.ContainsKey($yiddish)) {
        $dict[$yiddish] = $entry
    } else {
        $dict[$yiddish] = Combine-Entries $entry $dict[$yiddish]
    }
}

Write-Output '' > $OutputFile
$outFile = Resolve-Path $OutputFile
[System.IO.File]::WriteAllLines($outFile, (ConvertTo-Json $dict))

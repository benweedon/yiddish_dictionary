param(
    [String]$OutputFile
)

$r = Invoke-WebRequest 'http://verterbukh.org/vb?page=wdmin&tsu=en'

$entry = @{}

$yiddish = (($r.AllElements | where {$_.Class -eq 'lemma'} | select -ExpandProperty innerHTML) -split '<',2)[0].Trim()

$pronunciation = $r.AllElements | where {$_.Class -eq 'pron'} | select -ExpandProperty innerText
if ($pronunciation -ne $null) {
    $pronunciation = $pronunciation.Substring(2, $pronunciation.Length-4)
    $pronunciation = $pronunciation.Split('/') | % {$_.Trim()}
} else {
    $pronunciation = @()
}
$entry['_pro'] = @($pronunciation)

$pos = ($r.AllElements | where {$_.Class -eq 'help'} | select -ExpandProperty innerText).Trim()
$pos = @($pos) | % {
    if ($_ -eq 'masculine noun') {
        'm'
    } elseif ($_ -eq 'adjective') {
        'adj'
    } elseif ($_ -eq 'adverb') {
        'adv'
    } else {
        $_
    }
}
$entry['_pos'] = @($pos)

$entry['_src'] = @('ver')

$eng = ($r.AllElements | where {$_.Class -eq 'gloss'} | select -ExpandProperty innerText).Trim()
$entry['eng'] = @($eng)

$frenchR = Invoke-WebRequest 'http://verterbukh.org/vb?page=wdmin&tsu=fr'
$fra = ($frenchR.AllElements | where {$_.Class -eq 'gloss'} | select -ExpandProperty innerText).Trim()
$entry['fra'] = @($fra)

$dict = @{$yiddish=$entry}

$tempFile = '.\' + (New-Guid).Guid
Write-Output '' > $tempFile
try {
    [System.IO.File]::WriteAllLines((Resolve-Path $tempFile), (ConvertTo-Json $dict))
    python .\merge.py $OutputFile $tempFile $OutputFile
    python .\normalize.py $OutputFile
} finally {
    rm $tempFile
}

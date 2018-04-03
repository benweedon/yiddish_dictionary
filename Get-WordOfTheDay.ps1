param(
    [String]$OutputFile
)

$r = Invoke-WebRequest 'http://verterbukh.org/vb?page=wdmin'

$entry = @{}

$yiddish = (($r.AllElements | where {$_.Class -eq 'lemma'} | select -ExpandProperty innerHTML) -split '<',2)[0].Trim()

$pronunciation = $r.AllElements | where {$_.Class -eq 'pron'} | select -ExpandProperty innerText
$pronunciation = $pronunciation.Substring(2, $pronunciation.Length-4)
$pronunciation = $pronunciation.Split('/') | % {$_.Trim()}
$entry['_pro'] = $pronunciation

$pos = ($r.AllElements | where {$_.Class -eq 'help'} | select -ExpandProperty innerText).Trim()
if ($pos -eq 'masculine noun') {
    $pos = 'm'
}
$entry['_pos'] = $pos

$eng = ($r.AllElements | where {$_.Class -eq 'gloss'} | select -ExpandProperty innerText).Trim()
$entry['eng'] = @($eng)

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

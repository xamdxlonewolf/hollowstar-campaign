# Export vault to two book-like HTML/PDF outputs:
# 1) Player-safe world guide
# 2) GM reference guide
# Requires Pandoc: https://pandoc.org/install.html

param(
    [switch]$IncludeArchive
)

$ErrorActionPreference = "Stop"
$vaultRoot = (Resolve-Path ($PSScriptRoot + "\..")).Path
$outputDir = Join-Path $vaultRoot "export"
$timestamp = Get-Date -Format "yyyy-MM-dd"
$cssOut = Join-Path $outputDir "book-style.css"

$combinedPlayerMd = Join-Path $outputDir "combined_player_$timestamp.md"
$combinedGmMd = Join-Path $outputDir "combined_gm_$timestamp.md"
$playerHtmlOut = Join-Path $outputDir "World_of_Hollowstars_Player_$timestamp.html"
$playerPdfOut = Join-Path $outputDir "World_of_Hollowstars_Player_$timestamp.pdf"
$gmHtmlOut = Join-Path $outputDir "World_of_Hollowstars_GM_$timestamp.html"
$gmPdfOut = Join-Path $outputDir "World_of_Hollowstars_GM_$timestamp.pdf"
$validationReportOut = Join-Path $outputDir "validation_report_$timestamp.txt"

$excludePath = if ($IncludeArchive) { $null } else { "02_Geography_Archive" }

# ----- BOOK ORDER: defines how content is ordered for a readable campaign book -----
$partOrder = @(
    "00_Index",
    "02_Regions",
    "04_Factions",
    "05_Religion",
    "06_History",
    "07_Campaign",
    "08_GM_Notes",
    "09_NPCs"
)

$regionOrder = @(
    "Central_Heartlands",
    "Starfall_Basin",
    "Salt_Shore",
    "Silverbelt_Coast",
    "Desert_of_Glass",
    "Verdant_Crescent",
    "Frostwell_Tundra",
    "Northern_Expanse",
    "Glittering_Marshes",
    "Isle_Broken_Sphere"
)

$regionFileOrder = @(
    "Regional_Overview",
    "Central_Heartlands_Index", "Starfall_Basin_Index", "Salt_Shore_Index", "Silverbelt_Coast_Index",
    "Desert_of_Glass_Index", "Verdant_Crescent_Index", "Frostwell_Tundra_Index", "Northern_Expanse_Index",
    "Glittering_Marshes_Index", "Isle_Broken_Sphere_Index",
    "Geography", "Peoples_and_Culture", "Culture_and_Society", "Adventure_Hooks",
    "The_Simiah", "The_Shards", "The_Sleeper", "Outside_Factions",
    "Location_Index", "Locations"
)
$locationSubfolderOrder = @("Location_Index", "Cities", "Towns", "Landmarks", "Dungeons")
$religionOrder = @("Path of Spirits", "Six-Fold Faith", "First Flame Faith")
$historyOrder = @("Timeline", "Age Before", "The First Falls", "The Last Fall")
$indexOrder = @("README")

function Convert-ToDisplayText {
    param([string]$text)
    return ($text -replace "_", " ")
}

function Get-ObsidianLinkDisplayText {
    param(
        [string]$target,
        [string]$alias
    )

    if (-not [string]::IsNullOrWhiteSpace($alias)) {
        return $alias.Trim()
    }

    $cleanTarget = $target.Trim()
    if ($cleanTarget -match "#") {
        $anchorPart = ($cleanTarget -split "#", 2)[1]
        if (-not [string]::IsNullOrWhiteSpace($anchorPart)) {
            return (Convert-ToDisplayText ($anchorPart -replace "-", " ")).Trim()
        }
    }

    $pathOnly = ($cleanTarget -split "#", 2)[0]
    $pathParts = $pathOnly -split "[/\\]"
    $lastPart = $pathParts[-1]
    $base = [System.IO.Path]::GetFileNameWithoutExtension($lastPart)
    return (Convert-ToDisplayText $base).Trim()
}

function Normalize-RelPathKey {
    param([string]$pathLike)
    $key = $pathLike.Trim().Replace("/", "\").ToLowerInvariant()
    if ($key.EndsWith(".md")) { $key = $key.Substring(0, $key.Length - 3) }
    return $key
}

function Get-SectionAnchorId {
    param([string]$relPath)
    $safe = $relPath.ToLowerInvariant() -replace '[\\\/\. ]', '-' -replace '[^a-z0-9_-]', ''
    return "sec-" + $safe
}

function New-WikiLinkMap {
    param([System.Collections.IEnumerable]$files)

    $entries = @()
    $baseCounts = @{}
    foreach ($f in $files) {
        $rel = $f.RelPath
        $relNoExt = Normalize-RelPathKey -pathLike $rel
        $base = [System.IO.Path]::GetFileNameWithoutExtension($rel).ToLowerInvariant()
        $anchor = "#" + (Get-SectionAnchorId -relPath $rel)
        $entries += [PSCustomObject]@{
            RelNoExt = $relNoExt
            Base = $base
            Anchor = $anchor
        }
        if (-not $baseCounts.ContainsKey($base)) { $baseCounts[$base] = 0 }
        $baseCounts[$base] += 1
    }

    $map = @{
        Exact = @{}
        Base = @{}
    }
    foreach ($e in $entries) {
        $map.Exact[$e.RelNoExt] = $e.Anchor
        if ($baseCounts[$e.Base] -eq 1) {
            $map.Base[$e.Base] = $e.Anchor
        }
    }
    return $map
}

function Resolve-WikiLinkHref {
    param(
        [string]$target,
        [hashtable]$linkMap
    )
    if ([string]::IsNullOrWhiteSpace($target)) { return $null }
    if ($target.Trim().StartsWith("#")) { return $null }

    $pathOnly = ($target -split "#", 2)[0]
    if ([string]::IsNullOrWhiteSpace($pathOnly)) { return $null }

    $norm = Normalize-RelPathKey -pathLike $pathOnly
    if ($linkMap.Exact.ContainsKey($norm)) { return $linkMap.Exact[$norm] }
    $trimmed = $norm.TrimStart(".\")
    if ($linkMap.Exact.ContainsKey($trimmed)) { return $linkMap.Exact[$trimmed] }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($trimmed).ToLowerInvariant()
    if ($linkMap.Base.ContainsKey($base)) { return $linkMap.Base[$base] }
    return $null
}

function Get-WikiLinkMatches {
    param([string]$content)
    $pattern = '(!?)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    return [regex]::Matches($content, $pattern)
}

function Normalize-ObsidianWikiLinks {
    param(
        [string]$content,
        [hashtable]$linkMap
    )

    $pattern = '(!?)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    return [regex]::Replace(
        $content,
        $pattern,
        {
            param($match)
            $isEmbed = $match.Groups[1].Value -eq "!"
            $target = $match.Groups[2].Value
            $alias = $match.Groups[3].Value
            $display = Get-ObsidianLinkDisplayText -target $target -alias $alias
            if ($isEmbed) {
                return $display
            }
            $href = Resolve-WikiLinkHref -target $target -linkMap $linkMap
            if (-not [string]::IsNullOrWhiteSpace($href)) {
                return "[" + $display + "](" + $href + ")"
            }
            return $display
        }
    )
}

function Write-ValidationReport {
    param(
        [System.Collections.IEnumerable]$files,
        [hashtable]$linkMap,
        [string]$reportPath
    )

    $placeholderPattern = '\[TO BE DEVELOPED\]|\[TO BE DETERMINED\]|TODO'
    $missingLinks = [System.Collections.Generic.List[string]]::new()
    $placeholderHits = [System.Collections.Generic.List[string]]::new()

    foreach ($f in $files) {
        $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8
        $links = Get-WikiLinkMatches -content $content
        foreach ($m in $links) {
            $target = $m.Groups[2].Value
            $href = Resolve-WikiLinkHref -target $target -linkMap $linkMap
            if ([string]::IsNullOrWhiteSpace($href) -and -not $target.Trim().StartsWith("#")) {
                $missingLinks.Add("$($f.RelPath) -> [[${target}]]")
            }
        }

        $placeholderCount = ([regex]::Matches($content, $placeholderPattern)).Count
        if ($placeholderCount -gt 0) {
            $placeholderHits.Add("$($f.RelPath) -> $placeholderCount placeholder marker(s)")
        }
    }

    $report = [System.Text.StringBuilder]::new()
    [void]$report.AppendLine("Validation Report - $timestamp")
    [void]$report.AppendLine("")
    [void]$report.AppendLine("Missing wiki-link targets: $($missingLinks.Count)")
    if ($missingLinks.Count -gt 0) {
        [void]$report.AppendLine("")
        [void]$report.AppendLine("## Missing wiki-link targets")
        foreach ($entry in ($missingLinks | Sort-Object -Unique)) {
            [void]$report.AppendLine("- $entry")
        }
    }
    [void]$report.AppendLine("")
    [void]$report.AppendLine("Files with placeholders/TODO markers: $($placeholderHits.Count)")
    if ($placeholderHits.Count -gt 0) {
        [void]$report.AppendLine("")
        [void]$report.AppendLine("## Placeholder markers")
        foreach ($entry in ($placeholderHits | Sort-Object)) {
            [void]$report.AppendLine("- $entry")
        }
    }

    [System.IO.File]::WriteAllText($reportPath, $report.ToString(), [System.Text.UTF8Encoding]::new($false))
    Write-Host "Validation report: $reportPath" -ForegroundColor Cyan
    if ($missingLinks.Count -gt 0) {
        Write-Host "WARNING: Found $($missingLinks.Count) unresolved wiki-link target(s)." -ForegroundColor Yellow
    }
    if ($placeholderHits.Count -gt 0) {
        Write-Host "WARNING: Found placeholder/TODO markers in $($placeholderHits.Count) file(s)." -ForegroundColor Yellow
    }
}

function Get-BookSortKey {
    param([string]$relPath)
    $parts = $relPath -split "\\"
    $part = $parts[0]
    $partIdx = [array]::IndexOf($partOrder, $part)
    if ($partIdx -lt 0) { $partIdx = 999 }

    $key = [System.Text.StringBuilder]::new()
    [void]$key.AppendFormat("{0:D3}", $partIdx)

    switch ($part) {
        "00_Index" {
            $name = [System.IO.Path]::GetFileNameWithoutExtension($relPath)
            $idx = [array]::IndexOf($indexOrder, $name)
            $idxVal = if ($idx -ge 0) { $idx } else { 99 }
            [void]$key.AppendFormat(".{0:D2}", $idxVal)
            [void]$key.Append("." + $relPath.Replace("\", "_"))
            break
        }
        "02_Regions" {
            if ($relPath -eq "02_Regions\Regional_Overview.md") {
                [void]$key.Append(".00.00.Regional_Overview")
                break
            }
            $region = $parts[1]
            $regionIdx = [array]::IndexOf($regionOrder, $region)
            if ($regionIdx -lt 0) { $regionIdx = 99 }
            [void]$key.AppendFormat(".{0:D2}", $regionIdx)

            if ($parts.Length -eq 3) {
                $fname = [System.IO.Path]::GetFileNameWithoutExtension($parts[2])
                $fileIdx = [array]::IndexOf($regionFileOrder, $fname)
                $fileIdxVal = if ($fileIdx -ge 0) { $fileIdx } else { 99 }
                [void]$key.AppendFormat(".{0:D2}", $fileIdxVal)
                [void]$key.Append("." + $fname)
            } elseif ($parts.Length -ge 4 -and $parts[2] -eq "Locations") {
                $sub = $parts[3]
                $subName = if ($sub -match "\.md$") { [System.IO.Path]::GetFileNameWithoutExtension($sub) } else { $sub }
                $subIdx = [array]::IndexOf($locationSubfolderOrder, $subName)
                $subIdxVal = if ($subIdx -ge 0) { $subIdx + 20 } else { 99 }
                [void]$key.AppendFormat(".{0:D2}", $subIdxVal)
                [void]$key.Append("." + ($parts[3..($parts.Length - 1)] -join "_"))
            } else {
                [void]$key.Append(".99." + ($parts[2..($parts.Length - 1)] -join "_"))
            }
            break
        }
        "04_Factions" {
            $region = if ($parts.Length -gt 1) { $parts[1] } else { "" }
            $regionIdx = [array]::IndexOf($regionOrder, $region)
            $regionIdxVal = if ($regionIdx -ge 0) { $regionIdx } else { 99 }
            [void]$key.AppendFormat(".{0:D2}", $regionIdxVal)
            [void]$key.Append("." + ($relPath -replace "\\", "_"))
            break
        }
        "05_Religion" {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($parts[-1])
            $idx = [array]::IndexOf($religionOrder, $base)
            $idxVal = if ($idx -ge 0) { $idx } else { 99 }
            [void]$key.AppendFormat(".{0:D2}", $idxVal)
            [void]$key.Append("." + $base)
            break
        }
        "06_History" {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($parts[-1])
            $idx = [array]::IndexOf($historyOrder, $base)
            $idxVal = if ($idx -ge 0) { $idx } else { 99 }
            [void]$key.AppendFormat(".{0:D2}", $idxVal)
            [void]$key.Append("." + $base)
            break
        }
        "07_Campaign" { [void]$key.Append("." + $relPath.Replace("\", "_")); break }
        "08_GM_Notes" { [void]$key.Append("." + $relPath.Replace("\", "_")); break }
        "09_NPCs" {
            $region = if ($parts.Length -gt 1) { $parts[1] } else { "" }
            $regionIdx = [array]::IndexOf($regionOrder, $region)
            $regionIdxVal = if ($regionIdx -ge 0) { $regionIdx } else { 99 }
            [void]$key.AppendFormat(".{0:D2}", $regionIdxVal)
            [void]$key.Append("." + $relPath.Replace("\", "_"))
            break
        }
        default { [void]$key.Append("." + $relPath.Replace("\", "_")) }
    }
    return $key.ToString()
}

function Get-GmSortKey {
    param([string]$relPath)
    if ($relPath -like "08_GM_Notes\*") { return "000." + ($relPath -replace "\\", "_") }
    if ($relPath -like "07_Campaign\GM_Only\*") { return "001." + ($relPath -replace "\\", "_") }
    return "999." + ($relPath -replace "\\", "_")
}

function Get-DisplayTitle {
    param([string]$relPath)
    $base = [System.IO.Path]::GetFileNameWithoutExtension($relPath)
    return Convert-ToDisplayText $base
}

function Get-SectionContext {
    param([string]$relPath)
    $parts = $relPath -split "\\"
    if ($parts.Length -le 2) { return "" }

    $contextParts = @()
    for ($i = 1; $i -lt ($parts.Length - 1); $i++) {
        $segment = $parts[$i]
        if ($segment -eq "Locations") { continue }
        if ($segment -eq "GM_Only") { $segment = "GM Only" }
        $contextParts += (Convert-ToDisplayText $segment)
    }

    return ($contextParts -join " / ")
}

function Get-TitlePage {
    param(
        [string]$title,
        [string]$subtitle,
        [string]$stamp,
        [string]$note
    )
@"
# $title
## $subtitle

*Exported $stamp*

$note

<div style='page-break-after: always;'></div>
"@
}

function Build-CombinedMarkdown {
    param(
        [System.Collections.IEnumerable]$files,
        [string]$combinedPath,
        [hashtable]$partTitles,
        [string]$titlePage,
        [hashtable]$linkMap
    )

    $sb = [System.Text.StringBuilder]::new()
    [void]$sb.AppendLine($titlePage)

    $currentPart = ""
    foreach ($f in $files) {
        $rel = $f.RelPath
        $part = ($rel -split "\\")[0]
        if ($part -ne $currentPart -and $partTitles.ContainsKey($part)) {
            $currentPart = $part
            [void]$sb.AppendLine("")
            [void]$sb.AppendLine("# " + $partTitles[$part])
            [void]$sb.AppendLine("")
            [void]$sb.AppendLine("<div style='page-break-after: always;'></div>")
            [void]$sb.AppendLine("")
        }

        [void]$sb.AppendLine("---")
        [void]$sb.AppendLine("")
        $sectionAnchor = Get-SectionAnchorId -relPath $rel
        [void]$sb.AppendLine("<a id='" + $sectionAnchor + "'></a>")
        [void]$sb.AppendLine("")
        $displayTitle = Get-DisplayTitle -relPath $rel
        $contextLabel = Get-SectionContext -relPath $rel
        if ([string]::IsNullOrWhiteSpace($contextLabel)) {
            [void]$sb.AppendLine("## " + $displayTitle)
        } else {
            [void]$sb.AppendLine("## " + $displayTitle + " <span class='section-context'>" + $contextLabel + "</span>")
        }
        [void]$sb.AppendLine("")
        $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8
        $content = Normalize-ObsidianWikiLinks -content $content -linkMap $linkMap
        [void]$sb.AppendLine($content)
        [void]$sb.AppendLine("")
        [void]$sb.AppendLine("<div style='page-break-after: always;'></div>")
        [void]$sb.AppendLine("")
    }

    [System.IO.File]::WriteAllText($combinedPath, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
}

function Render-WithPandoc {
    param(
        [string]$inputMd,
        [string]$htmlOut,
        [string]$pdfOut,
        [string]$metadataTitle
    )

    $oldNativeErrPref = $null
    if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
        $oldNativeErrPref = $PSNativeCommandUseErrorActionPreference
        $PSNativeCommandUseErrorActionPreference = $false
    }

    $htmlOutput = & pandoc $inputMd -o $htmlOut --standalone --toc --toc-depth=3 -f markdown -t html5 --css=book-style.css --metadata title=$metadataTitle 2>&1
    $htmlExitCode = $LASTEXITCODE
    if ($null -ne $oldNativeErrPref) { $PSNativeCommandUseErrorActionPreference = $oldNativeErrPref }

    if ($htmlExitCode -ne 0) {
        Write-Host "HTML export failed for $metadataTitle." -ForegroundColor Red
        foreach ($line in $htmlOutput) {
            Write-Host "  $line" -ForegroundColor DarkYellow
        }
        exit 1
    }
    Write-Host "HTML: $htmlOut (linked table of contents)" -ForegroundColor Green

    $pdfEngine = "xelatex"
    $hasPdfEngine = Get-Command $pdfEngine -ErrorAction SilentlyContinue
    if (-not $hasPdfEngine) {
        Write-Host "PDF skipped for $metadataTitle ($pdfEngine not on PATH)." -ForegroundColor Yellow
        Write-Host "Restart terminal/Cursor and ensure MiKTeX adds xelatex to PATH." -ForegroundColor Yellow
        return
    }

    $pdfStdOut = Join-Path $outputDir ("pandoc_pdf_" + [System.Guid]::NewGuid().ToString("N") + ".out.log")
    $pdfStdErr = Join-Path $outputDir ("pandoc_pdf_" + [System.Guid]::NewGuid().ToString("N") + ".err.log")
    $pdfArgString = ('"{0}" -o "{1}" --standalone --toc --toc-depth=3 --pdf-engine={2}' -f $inputMd, $pdfOut, $pdfEngine)
    $pdfProc = Start-Process -FilePath "pandoc" -ArgumentList $pdfArgString -NoNewWindow -Wait -PassThru -RedirectStandardOutput $pdfStdOut -RedirectStandardError $pdfStdErr
    $pdfExitCode = $pdfProc.ExitCode
    $pdfOutput = @()
    if (Test-Path $pdfStdOut) { $pdfOutput += Get-Content -Path $pdfStdOut }
    if (Test-Path $pdfStdErr) { $pdfOutput += Get-Content -Path $pdfStdErr }

    if ($pdfExitCode -eq 0 -and (Test-Path $pdfOut)) {
        if (Test-Path $pdfStdOut) { Remove-Item $pdfStdOut -Force -ErrorAction SilentlyContinue }
        if (Test-Path $pdfStdErr) { Remove-Item $pdfStdErr -Force -ErrorAction SilentlyContinue }
        Write-Host "PDF:  $pdfOut" -ForegroundColor Green
        return
    }

    Write-Host "PDF export failed for $metadataTitle using $pdfEngine." -ForegroundColor Red
    if ($pdfOutput) {
        Write-Host "Pandoc/LaTeX output:" -ForegroundColor Yellow
        foreach ($line in $pdfOutput) {
            Write-Host "  $line" -ForegroundColor DarkYellow
        }
    } else {
        Write-Host "No diagnostic output was returned by pandoc." -ForegroundColor Yellow
    }
    if (Test-Path $pdfStdOut) { Remove-Item $pdfStdOut -Force -ErrorAction SilentlyContinue }
    if (Test-Path $pdfStdErr) { Remove-Item $pdfStdErr -Force -ErrorAction SilentlyContinue }
}

# ----- Collect all markdown files -----
$allFiles = Get-ChildItem -Path $vaultRoot -Filter "*.md" -Recurse -File |
    Where-Object {
        $_.FullName -notmatch "\\scripts\\" -and
        $_.FullName -notmatch "\\export\\" -and
        ($null -eq $excludePath -or $_.FullName -notmatch [regex]::Escape($excludePath))
    }

if ($allFiles.Count -eq 0) {
    Write-Host "No .md files found." -ForegroundColor Red
    exit 1
}

$allFileMeta = $allFiles | ForEach-Object {
    $rel = $_.FullName.Replace($vaultRoot, "").TrimStart("\")
    [PSCustomObject]@{
        FullName = $_.FullName
        RelPath = $rel
        BookSortKey = Get-BookSortKey -relPath $rel
        GmSortKey = Get-GmSortKey -relPath $rel
    }
}

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$playerParts = @("00_Index", "02_Regions", "04_Factions", "05_Religion", "06_History", "07_Campaign", "09_NPCs")
$playerFiles = $allFileMeta |
    Where-Object {
        $part = ($_.RelPath -split "\\")[0]
        $part -in $playerParts -and
        $_.RelPath -notlike "07_Campaign\GM_Only\*" -and
        $_.RelPath -notlike "08_GM_Notes\*"
    } |
    Sort-Object BookSortKey

$gmFiles = $allFileMeta |
    Where-Object {
        $_.RelPath -like "08_GM_Notes\*" -or $_.RelPath -like "07_Campaign\GM_Only\*"
    } |
    Sort-Object GmSortKey

if ($playerFiles.Count -eq 0) {
    Write-Host "No files selected for player guide." -ForegroundColor Red
    exit 1
}
if ($gmFiles.Count -eq 0) {
    Write-Host "No files selected for GM guide." -ForegroundColor Red
    exit 1
}

$vaultLinkMap = New-WikiLinkMap -files $allFileMeta
$playerLinkMap = New-WikiLinkMap -files $playerFiles
$gmLinkMap = New-WikiLinkMap -files $gmFiles
Write-ValidationReport -files $allFileMeta -linkMap $vaultLinkMap -reportPath $validationReportOut

$playerPartTitles = @{
    "00_Index" = "Part I - Introduction"
    "02_Regions" = "Part II - The World"
    "04_Factions" = "Part III - Factions"
    "05_Religion" = "Part IV - Religion"
    "06_History" = "Part V - History"
    "07_Campaign" = "Part VI - Campaign"
    "09_NPCs" = "Part VII - NPCs"
}

$gmPartTitles = @{
    "08_GM_Notes" = "Part I - GM Toolkit"
    "07_Campaign" = "Part II - Campaign Secrets"
}

$playerTitlePage = Get-TitlePage -title "World of Hollowstars" -subtitle "Player Guide" -stamp $timestamp -note "*Player-safe edition*"
$gmTitlePage = Get-TitlePage -title "World of Hollowstars" -subtitle "GM Reference Guide" -stamp $timestamp -note "**Spoiler Warning:** GM-only material."

Build-CombinedMarkdown -files $playerFiles -combinedPath $combinedPlayerMd -partTitles $playerPartTitles -titlePage $playerTitlePage -linkMap $playerLinkMap
Write-Host "Combined $($playerFiles.Count) files -> $combinedPlayerMd" -ForegroundColor Green

Build-CombinedMarkdown -files $gmFiles -combinedPath $combinedGmMd -partTitles $gmPartTitles -titlePage $gmTitlePage -linkMap $gmLinkMap
Write-Host "Combined $($gmFiles.Count) files -> $combinedGmMd" -ForegroundColor Green

# ----- Book-style CSS -----
$bookCss = @"
/* World of Hollowstars - book-style export */
:root { --text: #1a1a1a; --muted: #555; --border: #ddd; }

body {
  font-family: "Palatino Linotype", "Book Antiqua", Palatino, Georgia, serif;
  font-size: 11pt;
  line-height: 1.5;
  color: var(--text);
  max-width: 6.5in;
  margin: 0.75in auto;
}

h1 {
  font-size: 1.75em;
  font-weight: 600;
  margin-top: 1.25em;
  margin-bottom: 0.5em;
  padding-bottom: 0.2em;
  border-bottom: 1px solid var(--border);
  page-break-after: avoid;
}

h2 {
  font-size: 1.35em;
  margin-top: 1em;
  page-break-after: avoid;
}

h3 {
  font-size: 1.15em;
  margin-top: 0.75em;
  page-break-after: avoid;
}

.section-context {
  display: block;
  margin-top: 0.15em;
  font-size: 0.72em;
  color: var(--muted);
  font-weight: 400;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

body > h1 {
  font-size: 1.4em;
  color: var(--muted);
  border-bottom: 2px solid var(--border);
}

p { margin: 0.5em 0; text-align: justify; }
ul, ol { margin: 0.5em 0; padding-left: 1.5em; }
blockquote {
  margin: 1em 0;
  padding: 0.5em 1em;
  border-left: 4px solid var(--border);
  color: var(--muted);
  font-style: italic;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.75em 0;
  font-size: 0.95em;
  page-break-inside: avoid;
}
th, td { border: 1px solid var(--border); padding: 0.35em 0.5em; text-align: left; }
th { background: #f5f5f5; font-weight: 600; }

code { background: #f5f5f5; padding: 0.15em 0.35em; border-radius: 3px; font-size: 0.9em; }
pre {
  background: #f5f5f5;
  padding: 0.75em;
  overflow-x: auto;
  border-radius: 4px;
  font-size: 0.9em;
  page-break-inside: avoid;
}

hr { margin: 1.5em 0; border: none; border-top: 1px solid var(--border); }

@media print {
  body { max-width: none; margin: 0.6in; }
  a { color: var(--text); }
  div[style*="page-break-after"] { page-break-after: always !important; }
}
"@
[System.IO.File]::WriteAllText($cssOut, $bookCss, [System.Text.UTF8Encoding]::new($false))

# ----- Pandoc: HTML/PDF with TOC -----
$hasPandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $hasPandoc) {
    Write-Host "Pandoc not found. Install: winget install pandoc" -ForegroundColor Yellow
    Write-Host "Combined player markdown: $combinedPlayerMd" -ForegroundColor Cyan
    Write-Host "Combined GM markdown: $combinedGmMd" -ForegroundColor Cyan
    exit 0
}

Render-WithPandoc -inputMd $combinedPlayerMd -htmlOut $playerHtmlOut -pdfOut $playerPdfOut -metadataTitle "World of Hollowstars - Player Guide"
Render-WithPandoc -inputMd $combinedGmMd -htmlOut $gmHtmlOut -pdfOut $gmPdfOut -metadataTitle "World of Hollowstars - GM Reference Guide"

Write-Host "Open HTML files and Print to PDF if direct PDF export is unavailable." -ForegroundColor Cyan
Write-Host "`nDone. Output: $outputDir" -ForegroundColor Green

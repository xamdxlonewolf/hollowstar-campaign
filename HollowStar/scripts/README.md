# Scripts

## Export vault to PDF (or HTML)

**Script:** `export-to-pdf.ps1`

Builds a **single book-style document** with:

- **Logical order** — Content is ordered like a real campaign book:
  - **Part I — Introduction** (00_Index)
  - **Part II — The World** (02_Regions): Regional Overview first, then each region in a fixed order (Central Heartlands → Starfall Basin → Salt Shore → …). Within each region: Index → Geography → Culture → Adventure Hooks → Locations (Location Index, then Cities, Towns, Landmarks, Dungeons).
  - **Part III — Factions** (04_Factions), **Part IV — Religion** (05_Religion), **Part V — Campaign**, **Part VI — GM Notes**, **Part VII — NPCs** — each in a consistent order (e.g. religion: Path of Spirits → Six-Fold Faith → First Flame).
- **Part dividers** — Clear “Part I”, “Part II”, etc. headings and page breaks.
- **Title page** — First page: “World of Hollowstars — Campaign Setting” and export date.
- **Styling** — A `book-style.css` is generated so the HTML uses serif type, justified text, and print-friendly margins; the table of contents is included.

Exports as:

- **HTML** — open in a browser, then **Print (Ctrl+P) → Save as PDF**
- **PDF** — generated directly if you have Pandoc and a PDF engine (e.g. LaTeX)

### Run it

In PowerShell, from the **HollowStar** folder (or from anywhere, run the script by full path):

```powershell
cd "C:\Users\mikec\OneDrive\Documents\Daggerheart World\World_of_Hollowstars\World_of_Hollowstars\HollowStar"
.\scripts\export-to-pdf.ps1
```

**Options:**

- `-IncludeArchive` — include `02_Geography_Archive` in the export (default: exclude)
- Example: `.\scripts\export-to-pdf.ps1 -IncludeArchive`

### What you need

1. **Pandoc** (required for HTML and PDF)  
   - Install: [pandoc.org/install](https://pandoc.org/install.html) or `winget install pandoc`  
   - Without Pandoc, the script still builds a combined Markdown file in `export/`; you can use another tool to convert that to PDF.

2. **For direct PDF** (optional)  
   - A LaTeX engine (e.g. [MiKTeX](https://miktex.org/)) so Pandoc can produce PDF.  
   - If you don’t install LaTeX, use the generated **HTML** file: open it in Chrome or Edge and choose **Print → Save as PDF**.

### Output

Files are written to:

**`HollowStar/export/`**

- `combined_YYYY-MM-DD.md` — all content in one Markdown file  
- `World_of_Hollowstars_YYYY-MM-DD.html` — one HTML file (with table of contents)  
- `World_of_Hollowstars_YYYY-MM-DD.pdf` — one PDF (if Pandoc + PDF engine succeeded)

Open the HTML in your browser and use **Print → Save as PDF** to get a PDF from the HTML if the direct PDF step didn’t run or failed.

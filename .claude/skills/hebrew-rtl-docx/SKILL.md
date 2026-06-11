---
name: hebrew-rtl-docx
description: Use whenever the user asks to build, design, or polish a Word document (.docx) — especially for Hebrew RTL content, bilingual Hebrew+English specs, vendor briefs, formal PRDs, or any "make this properly readable as a document" request. Trigger phrases include "build a docx", "make this a Word document", "consolidate these MD files into a single doc", "design a polished doc", "vendor brief", "ספק אפיון", "תיצור לי מסמך מעוצב", "תבנה DOCX". Produces designed Word documents with proper RTL bidi, Heebo/Calibri font pairing, smart heading hierarchy, native Word TOC, and Hebrew-aware message blocks.
---

# Hebrew RTL DOCX Builder Skill

How to build polished, readable Word documents from markdown sources — handling Hebrew RTL, bilingual content, and English-only — using `python-docx`. This skill encodes the patterns proven out in the Road Protect bot-spec builds.

## When to use this skill

- User asks to convert markdown source(s) into a Word document
- User wants a "polished," "designed," or "properly formatted" doc
- User wants to consolidate multiple MD files into one document
- User asks for a vendor brief, PRD, or any handoff doc
- Content is Hebrew, mixed Hebrew+English, or pure English (auto-handled)

Do NOT use this skill for:
- Plain markdown deliverables (just write the MD)
- PDFs as primary output (build DOCX first, export via Word/LibreOffice)
- PPTX or XLSX (use those skills instead)

## Before starting — ask the user

Pick which of these are genuinely undecided. Skip questions where the answer is obvious from context.

1. **Source**: one MD file, or consolidating multiple? If multiple — what's the chapter/part structure?
2. **Audience tone**: technical reference (with SQL/JSON/tables OK) vs narrative prose (no code blocks, conversational)?
3. **Language**: Hebrew-first / English-first / auto-detect per paragraph (default if mixed)?
4. **TOC depth**: how deep into headings should the TOC go (`1-2` for executive, `1-3` for detailed)?
5. **Title page**: brand title needed, or skip straight to content?

Don't ask all of these. Ask the 1–2 that genuinely change the deliverable.

## The pattern — MD source, Python builder, single artifact

Always:

1. **Write or use existing markdown source(s).** Keep MD as source of truth. The DOCX is a derivative.
2. **Write a `build_<name>.py` script** that reads the MD and emits the DOCX. Save it next to the output.
3. **Run the script** to produce `<name>.docx`.
4. **Verify structure** by inspecting heading counts and a sample of content.

Never:
- Hand-edit the DOCX after building it. If something is wrong, fix the MD or the script and rebuild.
- Try to use Word's COM automation. Always python-docx.

## Setup

```bash
python -m pip install python-docx
```

On Windows: console encoding is cp1255 — use `PYTHONIOENCODING=utf-8` before any verification print statements, or avoid printing Hebrew/special chars. The DOCX itself is always UTF-8.

## Recipes — copy these into the build script

### Imports + brand palette

```python
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Road Protect brand (adapt per project)
NAVY_900 = RGBColor(0x0D, 0x18, 0x28)
NAVY_700 = RGBColor(0x22, 0x35, 0x5C)
NAVY_500 = RGBColor(0x3B, 0x5A, 0x9C)
TEAL_600 = RGBColor(0x0D, 0x94, 0x88)
TEAL_500 = RGBColor(0x14, 0xB8, 0xA6)
GRAY_500 = RGBColor(0x6B, 0x72, 0x80)
BODY_BLACK = RGBColor(0x1A, 0x1A, 0x1A)

FONT_HEBREW = "Heebo"   # for w:cs (complex-script)
FONT_LATIN = "Calibri"  # for w:ascii / w:hAnsi
FONT_MONO = "Consolas"
```

### Hebrew detection — threshold-based

```python
HEBREW_RANGE = re.compile(r"[֐-׿]")

def has_significant_hebrew(text: str, threshold: float = 0.20) -> bool:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    hebrew = [c for c in letters if HEBREW_RANGE.match(c)]
    return len(hebrew) / len(letters) >= threshold
```

Threshold of 0.20 (20%) catches Hebrew-dominant lines even when they contain English brand names, plan names, etc. Use 0.30 for stricter detection.

### Set paragraph RTL (the bidi attribute)

```python
def set_paragraph_rtl(paragraph, rtl: bool = True):
    pPr = paragraph._p.get_or_add_pPr()
    for existing in pPr.findall(qn("w:bidi")):
        pPr.remove(existing)
    bidi = OxmlElement("w:bidi")
    bidi.set(qn("w:val"), "1" if rtl else "0")
    pPr.append(bidi)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT if rtl else WD_ALIGN_PARAGRAPH.LEFT
```

**Critical**: alignment alone is NOT enough for RTL. The `w:bidi` element on the paragraph properties is what makes Word actually render right-to-left, mirroring punctuation and list bullets. Without it, Hebrew renders LTR even when aligned right.

### Run font — Latin + complex-script pair

```python
def set_run_font(run, size_pt=12, bold=False, italic=False,
                 color=BODY_BLACK, mono=False, hebrew=True):
    # AUTO-DETECT Hebrew at the RUN level. Any Hebrew character at all
    # triggers RTL markup — even one Hebrew word inside an English paragraph.
    # This catches mixed inline content (bold Hebrew phrase inside English
    # prose, Hebrew term in inline code, etc.) that explicit parameters miss.
    run_text = run.text or ""
    if any('֐' <= c <= '׿' for c in run_text):
        hebrew = True

    font = run.font
    font.size = Pt(size_pt)
    font.bold = bold
    font.italic = italic
    if color is not None:
        font.color.rgb = color

    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)

    if mono:
        rFonts.set(qn("w:ascii"), FONT_MONO)
        rFonts.set(qn("w:hAnsi"), FONT_MONO)
        rFonts.set(qn("w:cs"), FONT_MONO)
    else:
        rFonts.set(qn("w:ascii"), FONT_LATIN)
        rFonts.set(qn("w:hAnsi"), FONT_LATIN)
        rFonts.set(qn("w:cs"), FONT_HEBREW)

    if hebrew:
        # CRITICAL — without these two elements, Hebrew renders reversed
        # in Word even when the paragraph is bidi:
        #
        # 1. <w:rtl/> on rPr — marks the run itself as right-to-left.
        # 2. <w:lang w:bidi="he-IL"/> — sets the bidi locale to Hebrew.
        #
        # Without #1 specifically, Word applies the paragraph's RTL layout
        # but renders the run's characters in LTR order, producing the
        # classic "Hebrew letters appear reversed and unreadable" bug.
        if rPr.find(qn("w:rtl")) is None:
            rPr.append(OxmlElement("w:rtl"))
        lang = rPr.find(qn("w:lang"))
        if lang is None:
            lang = OxmlElement("w:lang")
            rPr.append(lang)
        lang.set(qn("w:bidi"), "he-IL")

        # Apply complex-script attributes for Hebrew bold/italic/size
        if bold:
            if rPr.find(qn("w:bCs")) is None:
                rPr.append(OxmlElement("w:bCs"))
        if italic:
            if rPr.find(qn("w:iCs")) is None:
                rPr.append(OxmlElement("w:iCs"))
        szCs = rPr.find(qn("w:szCs"))
        if szCs is None:
            szCs = OxmlElement("w:szCs")
            rPr.append(szCs)
        szCs.set(qn("w:val"), str(int(size_pt * 2)))
```

**Why both `w:ascii`/`w:hAnsi` AND `w:cs`**: Word uses `w:ascii`/`w:hAnsi` for Latin characters and `w:cs` ("complex script") for Hebrew/Arabic. Setting only `w:ascii` makes Hebrew render in a default fallback font. Setting `w:cs = "Heebo"` gives clean Hebrew typography.

**Why `w:szCs`, `w:bCs`, `w:iCs`**: complex-script size/bold/italic are separate attributes. Without them, Hebrew text won't honor your bold/size requests.

### Document setup — Hebrew-friendly defaults

```python
def setup_document():
    doc = Document()

    section = doc.sections[0]
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.4)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)

    # Normal style
    style = doc.styles["Normal"]
    style.font.name = FONT_LATIN
    style.font.size = Pt(12)
    style.paragraph_format.space_after = Pt(8)
    style.paragraph_format.line_spacing = 1.55  # generous for Hebrew readability

    # Force the complex-script font on the Normal style
    rPr = style.element.find(qn("w:rPr"))
    if rPr is None:
        rPr = OxmlElement("w:rPr")
        style.element.insert(0, rPr)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), FONT_LATIN)
    rFonts.set(qn("w:hAnsi"), FONT_LATIN)
    rFonts.set(qn("w:cs"), FONT_HEBREW)

    # Heading hierarchy — 4 levels usually enough
    heading_specs = {
        1: dict(size=24, color=NAVY_900, before=32, after=14),
        2: dict(size=17, color=NAVY_700, before=20, after=10),
        3: dict(size=13.5, color=NAVY_500, before=14, after=6),
        4: dict(size=12, color=NAVY_500, before=10, after=4),
    }
    for level, spec in heading_specs.items():
        s = doc.styles[f"Heading {level}"]
        s.font.name = FONT_LATIN
        s.font.size = Pt(spec["size"])
        s.font.bold = True
        s.font.color.rgb = spec["color"]
        s.paragraph_format.space_before = Pt(spec["before"])
        s.paragraph_format.space_after = Pt(spec["after"])
        s.paragraph_format.keep_with_next = True
        # Same complex-script font fix
        rPr = s.element.find(qn("w:rPr"))
        if rPr is None:
            rPr = OxmlElement("w:rPr")
            s.element.insert(0, rPr)
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.append(rFonts)
        rFonts.set(qn("w:ascii"), FONT_LATIN)
        rFonts.set(qn("w:hAnsi"), FONT_LATIN)
        rFonts.set(qn("w:cs"), FONT_HEBREW)

    return doc
```

### Title page

```python
def add_title_page(doc, brand="Road Protect", title_he="כותרת בעברית",
                   subtitle_en="English Subtitle", version="גרסה 1.0 · 2026"):
    for _ in range(7):
        doc.add_paragraph().paragraph_format.space_after = Pt(0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(p, True)
    run = p.add_run(brand)
    set_run_font(run, size_pt=40, bold=True, color=NAVY_900, hebrew=False)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(20)
    run = p.add_run("━━━━━━━━━━")
    set_run_font(run, size_pt=14, color=TEAL_500, hebrew=False)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(p, True)
    run = p.add_run(title_he)
    set_run_font(run, size_pt=28, bold=True, color=NAVY_700, hebrew=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle_en)
    set_run_font(run, size_pt=14, italic=True, color=GRAY_500, hebrew=False)

    for _ in range(10):
        doc.add_paragraph().paragraph_format.space_after = Pt(0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(p, True)
    run = p.add_run(version)
    set_run_font(run, size_pt=12, color=GRAY_500, hebrew=True)

    doc.add_page_break()
```

### Native Word TOC field (auto-populates on first open)

```python
def add_toc(doc, title_he="תוכן עניינים", depth="1-3"):
    p = doc.add_paragraph()
    set_paragraph_rtl(p, True)
    run = p.add_run(title_he)
    set_run_font(run, size_pt=22, bold=True, color=NAVY_900, hebrew=True)
    p.paragraph_format.space_after = Pt(16)

    p = doc.add_paragraph()
    set_paragraph_rtl(p, True)
    run = p.add_run()
    f_begin = OxmlElement("w:fldChar")
    f_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f'TOC \\o "{depth}" \\h \\z \\u'
    f_sep = OxmlElement("w:fldChar")
    f_sep.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "לחץ ימני → Update Field לאחר פתיחת המסמך"
    f_end = OxmlElement("w:fldChar")
    f_end.set(qn("w:fldCharType"), "end")
    run._r.append(f_begin)
    run._r.append(instr)
    run._r.append(f_sep)
    run._r.append(placeholder)
    run._r.append(f_end)
    set_run_font(run, size_pt=11, italic=True, color=GRAY_500, hebrew=True)

    doc.add_page_break()
```

The TOC is empty until the user opens the doc and right-clicks → "Update Field" (or hits F9). This is normal — there's no way to pre-populate a Word TOC from python-docx.

### Hebrew message block — for quotes / bot copy / featured content

```python
def add_message_block(doc, lines):
    """A blockquote-style container for Hebrew bot messages or featured quotes.
    Light teal bg, teal right-border (= RTL leading edge)."""
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.rows[0].cells[0]

    tcPr = cell._tc.get_or_add_tcPr()

    # Background
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F0FAF8")
    tcPr.append(shd)

    # Teal right-border + faint borders elsewhere
    tcBorders = OxmlElement("w:tcBorders")
    for side, weight, color in [
        ("right", "32", "14B8A6"),       # leading edge in RTL
        ("top", "4", "C8E8E2"),
        ("bottom", "4", "C8E8E2"),
        ("left", "4", "C8E8E2"),
    ]:
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), weight)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)

    # Cell padding
    tcMar = OxmlElement("w:tcMar")
    for side in ("top", "bottom", "left", "right"):
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), "180")
        m.set(qn("w:type"), "dxa")
        tcMar.append(m)
    tcPr.append(tcMar)

    cell.paragraphs[0].text = ""
    for idx, line in enumerate(lines):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.35
        set_paragraph_rtl(p, True)
        if line.strip():
            run = p.add_run(line)
            set_run_font(run, size_pt=12, color=NAVY_900, hebrew=True)
        else:
            p.add_run(" ")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
```

For English-only message blocks: change `set_paragraph_rtl(p, True)` to skip the call, and use the `left` side for the teal accent border instead of `right`.

### Code block — for technical SQL/JSON content

```python
def add_code_block(doc, code):
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.rows[0].cells[0]

    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F6F8FA")
    tcPr.append(shd)

    cell.paragraphs[0].text = ""
    for idx, line in enumerate(code.split("\n")):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(line if line else " ")
        # PER-LINE Hebrew detection: even inside a mostly-English code block
        # (like an ASCII funnel chart), individual lines may contain Hebrew.
        # Consolas has no Hebrew glyphs, so switch to Heebo on those lines.
        if any('֐' <= c <= '׿' for c in line):
            set_run_font(run, size_pt=10, mono=False,
                         color=RGBColor(0x24, 0x29, 0x2E), hebrew=True)
        else:
            set_run_font(run, size_pt=9.5, mono=True,
                         color=RGBColor(0x24, 0x29, 0x2E), hebrew=False)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
```

**Important**: detect whether a ``` block is Hebrew (message) or English (code). The same triple-backtick syntax in markdown can be either. Auto-detect:

```python
def render_fenced_block(doc, content):
    if has_significant_hebrew(content):
        add_message_block(doc, content.split("\n"))
    else:
        add_code_block(doc, content)
```

### RTL table with header shading

```python
def add_rtl_table(doc, header, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(header))
    table.style = "Light Grid Accent 1"
    table.autofit = True

    # Header row
    for col_idx, txt in enumerate(header):
        cell = table.rows[0].cells[col_idx]
        cell.text = ""
        p = cell.paragraphs[0]
        if has_significant_hebrew(txt):
            set_paragraph_rtl(p, True)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(txt)
        set_run_font(run, size_pt=10, bold=True,
                     color=RGBColor(0xFF, 0xFF, 0xFF),
                     hebrew=has_significant_hebrew(txt))

        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "16243E")
        tcPr.append(shd)

    # Data rows with zebra striping
    for row_idx, row_data in enumerate(rows, start=1):
        for col_idx, txt in enumerate(row_data):
            if col_idx >= len(header):
                continue
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            is_heb = has_significant_hebrew(txt)
            if is_heb:
                set_paragraph_rtl(p, True)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(txt)
            set_run_font(run, size_pt=10, hebrew=is_heb)

            if row_idx % 2 == 0:
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd")
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:color"), "auto")
                shd.set(qn("w:fill"), "F4F7FC")
                tcPr.append(shd)

    doc.add_paragraph()
```

### Inline markdown parser (bold, italic, inline code)

```python
INLINE_RE = re.compile(
    r"(\*\*([^*]+?)\*\*"   # bold
    r"|\*([^*\n]+?)\*"      # italic
    r"|`([^`]+?)`)"         # inline code
)

def add_inline_runs(paragraph, text, base_size=12, hebrew=True):
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            run = paragraph.add_run(text[pos:m.start()])
            set_run_font(run, size_pt=base_size, hebrew=hebrew)
        if m.group(2) is not None:
            run = paragraph.add_run(m.group(2))
            set_run_font(run, size_pt=base_size, bold=True,
                         color=NAVY_900, hebrew=hebrew)
        elif m.group(3) is not None:
            run = paragraph.add_run(m.group(3))
            set_run_font(run, size_pt=base_size, italic=True, hebrew=hebrew)
        elif m.group(4) is not None:
            code_text = m.group(4)
            run = paragraph.add_run(code_text)
            # Inline `code` chunks containing Hebrew (e.g. CRM column names
            # quoted in prose) must NOT use Consolas — no Hebrew glyphs.
            # Switch to italic+teal so the "term" feel is preserved while
            # Hebrew renders properly.
            if any('֐' <= c <= '׿' for c in code_text):
                set_run_font(run, size_pt=base_size, mono=False,
                             italic=True, color=TEAL_600, hebrew=True)
            else:
                set_run_font(run, size_pt=base_size - 0.5, mono=True,
                             color=TEAL_600, hebrew=False)
        pos = m.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_run_font(run, size_pt=base_size, hebrew=hebrew)
```

### Markdown driver loop

```python
def parse(doc, md_text, base_heading_offset=1):
    """Walk through the markdown and emit docx blocks."""
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Fenced code/message block
        if stripped.startswith("```"):
            i += 1
            content = []
            while i < len(lines) and not lines[i].rstrip().startswith("```"):
                content.append(lines[i])
                i += 1
            i += 1
            render_fenced_block(doc, "\n".join(content))
            continue

        # Heading
        h = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if h:
            level = len(h.group(1)) + base_heading_offset - 1
            level = max(1, min(level, 6))
            text = re.sub(r"^\d+(\.\d+)*\s+", "", h.group(2))
            # H1s start on new page (skip first H1 — title page already there)
            if level == 1 and i > 0:
                doc.add_page_break()
            p = doc.add_paragraph()
            p.style = doc.styles[f"Heading {level}"]
            is_heb = has_significant_hebrew(text)
            if is_heb:
                set_paragraph_rtl(p, True)
            size = int(doc.styles[f"Heading {level}"].font.size.pt)
            add_inline_runs(p, text, base_size=size, hebrew=is_heb)
            i += 1
            continue

        # Blockquote (Hebrew message)
        if stripped.startswith("> "):
            msg = []
            while i < len(lines) and lines[i].rstrip().startswith(">"):
                msg.append(re.sub(r"^>\s?", "", lines[i].rstrip()))
                i += 1
            add_message_block(doc, msg)
            continue

        # Bullet
        if re.match(r"^[-*]\s+", stripped):
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].rstrip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].rstrip())
                p = doc.add_paragraph(style="List Bullet")
                is_heb = has_significant_hebrew(item)
                if is_heb:
                    set_paragraph_rtl(p, True)
                p.paragraph_format.space_after = Pt(4)
                add_inline_runs(p, item, base_size=12, hebrew=is_heb)
                i += 1
            continue

        # Skip blank lines and horizontal rules
        if stripped == "" or re.match(r"^---+\s*$", stripped):
            i += 1
            continue

        # Paragraph (gather wrapped lines)
        para = [stripped]
        while (i + 1 < len(lines)
               and lines[i + 1].strip()
               and not lines[i + 1].rstrip().startswith(("#", "> ", "- ", "* ", "```", "---"))):
            para.append(lines[i + 1].rstrip())
            i += 1
        text = " ".join(para)
        p = doc.add_paragraph()
        is_heb = has_significant_hebrew(text)
        if is_heb:
            set_paragraph_rtl(p, True)
        add_inline_runs(p, text, base_size=12, hebrew=is_heb)
        i += 1
```

### Verification — after building, ALWAYS check structure

```python
def verify(output_path):
    from collections import Counter
    doc = Document(output_path)
    levels = Counter()
    for p in doc.paragraphs:
        if p.style and 'Heading' in p.style.name:
            levels[p.style.name] += 1
    print(f"Paragraphs: {len(doc.paragraphs)} | Tables: {len(doc.tables)}")
    for lvl in sorted(levels):
        print(f"  {lvl}: {levels[lvl]}")
```

Run this after building. Sanity-check that heading counts make sense (e.g., if you have 7 scenarios and each should be H1, you'd expect 7+ H1s).

## Common pitfalls — these will bite you

1. **Missing `<w:rtl/>` on runs**: The single most common bug producing "Hebrew letters appear reversed and unreadable." Paragraph bidi alone is NOT enough — each run containing Hebrew MUST have `<w:rtl/>` in its `rPr`. Without it, Word lays out the paragraph right-to-left but renders the characters within the run left-to-right, producing visual gibberish. Always add `<w:rtl/>` AND `<w:lang w:bidi="he-IL"/>` to runs containing Hebrew. The `set_run_font` recipe above does this when `hebrew=True`.

2. **RTL alignment without bidi**: Right-aligning a paragraph is NOT the same as RTL. Without `w:bidi="1"` on `pPr`, Hebrew text flows in LTR (punctuation in wrong place, bullets on wrong side). Always use `set_paragraph_rtl()`.

3. **Setting only `w:ascii` font**: Hebrew uses `w:cs` (complex-script). Set both `w:ascii` (for Latin) AND `w:cs` (for Hebrew), or Hebrew will render in a default fallback.

4. **Skipping `w:szCs` / `w:bCs`**: Hebrew bold/size are separate complex-script attrs. Without them, Hebrew text won't honor your sizing/bolding.

5. **Console encoding on Windows**: `print()` of Hebrew text fails with cp1255 error. Use `PYTHONIOENCODING=utf-8 python script.py` or `sys.stdout.reconfigure(encoding='utf-8')` at the top of verify scripts. The DOCX file itself is fine — only the console output errors.

6. **Mono font on Hebrew message blocks**: Don't use Consolas/monospace for Hebrew bot messages. Use Heebo (sans). Auto-detect Hebrew in fenced ``` blocks and choose font accordingly.

7. **Empty paragraph in a table cell**: `cell.text = ""` then add `cell.paragraphs[0]` is the right pattern. Don't add a new paragraph as the first — it leaves a blank above the content.

8. **Heading hierarchy gaps**: Don't skip levels (H1 → H3 with no H2). The TOC will look broken. If converting MD where `# Chapter` becomes a chapter, plan the offset so `##` becomes H2 not H3.

9. **TOC not populating**: Native Word TOC fields are placeholders until the doc is opened in Word and the field is updated (F9 / right-click → Update). This is a Word behavior, not a bug. Tell the user.

10. **Number prefixes in headings**: MD headings like `## 2.1 Section name` become "2.1 Section name" in TOC, duplicating the auto-numbering. Strip `\d+(\.\d+)*\s+` from heading text when parsing.

11. **`autofit = True` on tables**: Sometimes makes columns collapse oddly with Hebrew content. If a table looks wrong, set explicit column widths.

12. **Build script can't save — `PermissionError`**: The output DOCX is already open in Word. Word holds an exclusive lock on opened files. Close the file in Word before rebuilding. Tell the user to close it; don't try to force-overwrite.

## Verifying RTL is actually working

After building, **always** run this full sweep. Spot-checking one paragraph isn't enough — mixed inline content (bold Hebrew phrases inside English paragraphs, Hebrew terms in inline code) often slips through. This counts EVERY Hebrew run/paragraph and reports gaps:

```python
import sys, re, zipfile
sys.stdout.reconfigure(encoding='utf-8')

def verify_rtl(path, name=""):
    with zipfile.ZipFile(path) as z:
        xml = z.open('word/document.xml').read().decode('utf-8')

    # Check every run containing Hebrew
    runs = re.findall(r'<w:r[^>]*>.*?</w:r>', xml, re.DOTALL)
    h_total = h_rtl = h_lang = h_cs = 0
    for r in runs:
        m = re.search(r'<w:t[^>]*>([^<]*)</w:t>', r)
        if not m: continue
        if not any('֐' <= c <= '׿' for c in m.group(1)): continue
        h_total += 1
        if '<w:rtl/>' in r: h_rtl += 1
        if 'w:bidi="he-IL"' in r: h_lang += 1
        if 'w:cs="Heebo"' in r: h_cs += 1

    # Check every Hebrew-dominant paragraph
    pps = re.findall(r'<w:p[ >].*?</w:p>', xml, re.DOTALL)
    hp_total = hp_bidi = 0
    for p in pps:
        full = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
        heb = sum(1 for c in full if '֐' <= c <= '׿')
        letters = sum(1 for c in full if c.isalpha())
        if letters == 0 or heb == 0 or heb / letters < 0.2: continue
        hp_total += 1
        if 'w:bidi' in p: hp_bidi += 1

    ok = (h_rtl == h_total) and (h_lang == h_total) and (h_cs == h_total) and (hp_bidi == hp_total)
    print(f'{name}: runs={h_total} rtl={h_rtl} lang={h_lang} heebo={h_cs} | paras={hp_total} bidi={hp_bidi} | {"PASS" if ok else "FAIL"}')
    return ok

verify_rtl(output_path, "my-doc.docx")
```

The bar is 100% on every metric. **Anything less than 100% means some Hebrew text will render wrong in Word.** Common gaps and their fixes:

- `rtl < total` → `set_run_font` not auto-detecting Hebrew at run level (use the recipe above)
- `lang < total` → same fix
- `heebo < total` → some Hebrew text is in Consolas. Check inline-code chunks (backticks) and per-line content inside ``` blocks
- `bidi < total` → `set_paragraph_rtl` not called on Hebrew paragraphs. Check that `has_significant_hebrew()` threshold is low enough (0.20, not 0.30)

## Workflow

When the user asks for a designed DOCX:

1. **Check** if `python-docx` is installed: `python -c "import docx"`. Install if missing.
2. **Read the source MD** to understand structure and content.
3. **Ask** the 1–2 scoping questions that matter for this build (don't ask all).
4. **Write `build_<name>.py`** in the same folder as the output. Copy recipes from this skill.
5. **Run** the script: `cd <docs-dir> && PYTHONIOENCODING=utf-8 python build_<name>.py`.
6. **Verify** structure with the verification snippet above.
7. **Tell the user** the path to the output AND instructions to right-click → Update Field on the TOC the first time they open it.

If the user later edits the MD and wants a refresh — just run the build script again. The MD is source of truth; the DOCX is regenerated.

## Reference implementations in this workspace

Two working builders prove the patterns:

- `03_projects/active/2026-Q2_bot-spec-and-dashboard/docs/build_docx.py` — multi-file consolidator, technical spec style (SQL/JSON code blocks, data tables, parts/chapters)
- `03_projects/active/2026-Q2_bot-spec-and-dashboard/docs/build_vendor_brief.py` — single-file narrative style (Hebrew message blocks, no code, prose-focused)

Read one of these as a complete example before writing a new builder. They differ in scope but share the core helpers — same `set_paragraph_rtl`, `set_run_font`, `add_message_block`, etc.

## What this skill does NOT do

- **Doesn't build PDFs.** Build DOCX, let Word/LibreOffice export to PDF. Direct python → PDF (via reportlab/weasyprint) has worse Hebrew support.
- **Doesn't edit existing DOCX files.** Always rebuild from MD source. If the user has a DOCX with no MD source, convert it to MD first.
- **Doesn't generate PPTX / XLSX.** Use the dedicated skills for those.
- **Doesn't handle Arabic or other RTL scripts.** The patterns generalize, but the font (Heebo) is Hebrew-specific. Replace with `Cairo` or similar for Arabic.

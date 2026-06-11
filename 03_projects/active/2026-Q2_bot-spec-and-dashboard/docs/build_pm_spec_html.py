"""
Build an RTL-aware HTML version of the PM spec from PM_SPEC_full.md.

Mixed Hebrew/English: each block auto-detects direction. Hebrew bot-copy fenced
blocks render as teal "message" cards; English fenced blocks as code.

Run:
    PYTHONIOENCODING=utf-8 python build_pm_spec_html.py

Output:
    PM_SPEC_full.html (in this docs/ folder)
"""

import re
import html
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "PM_SPEC_full.md"
SRC_HE = Path(__file__).resolve().parent.parent / "PM_SPEC_full.he.md"
DASH = Path(__file__).resolve().parent.parent / "mockups" / "dashboard.html"
OUT = Path(__file__).resolve().parent / "PM_SPEC_full.html"

HEBREW = re.compile(r"[֐-׿]")


def heb_share(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if HEBREW.match(c)) / len(letters)


def is_heb(text):
    return heb_share(text) >= 0.20


def inline(text):
    """bold / italic / inline-code, then escape around them."""
    out = []
    pos = 0
    pat = re.compile(r"(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|\[([^\]]+)\]\(([^)]+)\))")
    for m in pat.finditer(text):
        if m.start() > pos:
            out.append(html.escape(text[pos:m.start()]))
        if m.group(2) is not None:
            out.append(f"<strong>{html.escape(m.group(2))}</strong>")
        elif m.group(3) is not None:
            out.append(f"<em>{html.escape(m.group(3))}</em>")
        elif m.group(4) is not None:
            out.append(f"<code>{html.escape(m.group(4))}</code>")
        elif m.group(5) is not None:
            out.append(f"<a href=\"{html.escape(m.group(6))}\">{html.escape(m.group(5))}</a>")
        pos = m.end()
    if pos < len(text):
        out.append(html.escape(text[pos:]))
    return "".join(out)


def dir_attr(text):
    return "rtl" if is_heb(text) else "ltr"


def render(md):
    lines = md.splitlines()
    i = 0
    html_parts = []
    while i < len(lines):
        line = lines[i]
        s = line.rstrip()

        # fenced block
        if s.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].rstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            content = "\n".join(buf)
            if is_heb(content):
                inner = "<br>".join(html.escape(l) if l.strip() else "&nbsp;" for l in buf)
                html_parts.append(f'<div class="msg" dir="rtl">{inner}</div>')
            else:
                html_parts.append(f'<pre class="code" dir="ltr">{html.escape(content)}</pre>')
            continue

        # heading
        h = re.match(r"^(#{1,6})\s+(.+?)\s*$", s)
        if h:
            lvl = len(h.group(1))
            txt = h.group(2)
            html_parts.append(f'<h{lvl} dir="{dir_attr(txt)}">{inline(txt)}</h{lvl}>')
            i += 1
            continue

        # hr
        if re.match(r"^---+\s*$", s):
            html_parts.append("<hr>")
            i += 1
            continue

        # table
        if "|" in s and i + 1 < len(lines) and re.match(r"^\s*\|?[\s\-:|]+\|?\s*$", lines[i + 1]):
            tbl = []
            while i < len(lines) and "|" in lines[i]:
                tbl.append(lines[i])
                i += 1
            header = [c.strip() for c in tbl[0].strip().strip("|").split("|")]
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in tbl[2:] if r.strip()]
            tdir = "rtl" if any(is_heb(c) for c in header) else "ltr"
            th = "".join(f'<th dir="{dir_attr(c)}">{inline(c)}</th>' for c in header)
            body = ""
            for r in rows:
                tds = "".join(f'<td dir="{dir_attr(c)}">{inline(c)}</td>' for c in r)
                body += f"<tr>{tds}</tr>"
            html_parts.append(f'<table dir="{tdir}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>')
            continue

        # bullet list
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].rstrip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].rstrip()))
                i += 1
            lis = "".join(f'<li dir="{dir_attr(it)}">{inline(it)}</li>' for it in items)
            html_parts.append(f"<ul>{lis}</ul>")
            continue

        # numbered list
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].rstrip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].rstrip()))
                i += 1
            lis = "".join(f'<li dir="{dir_attr(it)}">{inline(it)}</li>' for it in items)
            html_parts.append(f"<ol>{lis}</ol>")
            continue

        # blank
        if s == "":
            i += 1
            continue

        # paragraph (gather wrapped lines)
        para = [s]
        while (i + 1 < len(lines) and lines[i + 1].strip()
               and not re.match(r"^(#{1,6}\s|```|>|[-*]\s|\d+\.\s|---+\s*$)", lines[i + 1].rstrip())
               and "|" not in lines[i + 1]):
            para.append(lines[i + 1].rstrip())
            i += 1
        text = " ".join(para)
        html_parts.append(f'<p dir="{dir_attr(text)}">{inline(text)}</p>')
        i += 1

    return "\n".join(html_parts)


CSS = """
:root{
  --navy:#0e2540; --navy2:#13304f; --blue:#2563eb; --blue-d:#1d4ed8;
  --amber:#f59e0b; --ink:#0f172a; --muted:#475569; --line:#e2e8f0; --bg:#f1f5f9;
}
*{box-sizing:border-box}
body{
  font-family:'Rubik',system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
  color:var(--ink); line-height:1.7; margin:0; background-color:var(--bg);
}
.page{max-width:880px; margin:32px auto; background:#fff; padding:48px 56px;
  border:1px solid var(--line); border-radius:16px; box-shadow:0 20px 50px -30px rgba(14,37,64,.45);}
.cover{text-align:center; padding:38px 0 26px; border-bottom:3px solid var(--amber); margin-bottom:8px;}
.cover .brand{font-size:42px; font-weight:900; color:var(--navy); letter-spacing:-.02em;}
.cover .t-he{font-size:25px; font-weight:800; color:var(--navy); direction:rtl; margin-top:12px;}
.cover .t-en{font-size:15px; color:var(--muted); margin-top:4px;}
.cover .tag{display:inline-block; margin-top:16px; font-size:13px; font-weight:800;
  color:var(--navy); background-color:var(--amber); border-radius:999px; padding:.4em .9em;}
.cover .meta{font-size:12px; color:var(--muted); margin-top:12px;}
h1,h2,h3,h4,h5,h6{font-weight:800; color:var(--navy); letter-spacing:-.01em;}
h1{font-size:30px; margin:40px 0 14px; border-bottom:1px solid var(--line); padding-bottom:8px;}
h2{font-size:23px; margin:34px 0 12px;}
h3{font-size:17px; margin:24px 0 8px; border-inline-start:4px solid var(--blue); padding-inline-start:10px;}
p{margin:10px 0;}
ul,ol{margin:10px 0; padding-inline-start:26px;}
li{margin:5px 0;}
strong{color:var(--navy); font-weight:700;}
a{color:var(--blue); text-decoration:none;}
a:hover{text-decoration:underline;}
code{background:#eef4ff; color:var(--blue-d); font-family:ui-monospace,Consolas,monospace;
  font-size:.88em; padding:1px 6px; border-radius:6px; font-weight:600;}
hr{border:none; border-top:1px solid var(--line); margin:24px 0;}
/* tables */
table{width:100%; border-collapse:collapse; margin:14px 0 1rem; font-size:14px;}
th,td{padding:.75rem; border:1px solid var(--line); vertical-align:top;}
th{background-color:var(--navy); color:#fff; text-align:start; font-weight:700;}
tbody tr:nth-of-type(odd){background-color:#f8fafc;}
/* bot-copy callout — the actual WhatsApp message text */
.msg{background:#fffdf7; border:1px solid #fde8c4; border-inline-start:4px solid var(--amber);
  border-radius:12px; padding:14px 18px; margin:12px 0; color:var(--ink);
  font-size:15px; line-height:1.6;}
/* code block */
pre.code{background:#f8fafc; border:1px solid var(--line); border-radius:12px;
  padding:14px 16px; margin:12px 0; overflow-x:auto; font-family:ui-monospace,Consolas,monospace;
  font-size:13px; color:#1e293b;}
/* alert + badge helpers */
.alert{padding:.75rem 1.25rem; margin-bottom:1rem; border:1px solid transparent; border-radius:12px;}
.alert-warning{color:#7c4a03; background-color:#fff7ed; border-color:#fed7aa;}
.badge{display:inline-block; padding:.25em .5em; font-size:75%; font-weight:800; line-height:1;
  text-align:center; white-space:nowrap; vertical-align:baseline; border-radius:999px;}
.badge-primary{color:#fff; background-color:var(--blue);}
.badge-secondary{color:var(--navy); background-color:var(--amber);}
/* embedded dashboard mockup */
.dash-embed{margin:18px 0 8px; border:1px solid var(--line); border-radius:16px; overflow:hidden;
  box-shadow:0 18px 40px -28px rgba(14,37,64,.5);}
.dash-embed figcaption{background-color:var(--navy); color:#fff; font-size:13px; font-weight:700;
  padding:10px 14px; display:flex; justify-content:space-between; align-items:center; gap:12px;}
.dash-embed figcaption a{color:var(--amber); font-weight:800; text-decoration:none; white-space:nowrap;}
.dash-embed figcaption a:hover{text-decoration:underline;}
.dash-embed iframe{display:block; width:100%; height:780px; border:0; background:var(--bg);}
/* language toggle */
.langbar{position:sticky; top:0; z-index:50; display:flex; justify-content:center; gap:0;
  background:rgba(255,255,255,.95); backdrop-filter:blur(6px);
  border-bottom:1px solid var(--line); padding:8px; box-shadow:0 2px 12px rgba(14,37,64,.06);}
.langbar button{font-family:inherit; font-size:14px; font-weight:800; cursor:pointer;
  border:1.5px solid var(--navy); background:#fff; color:var(--navy); padding:7px 22px;}
.langbar button:first-child{border-radius:0 999px 999px 0; border-inline-start:none;}
.langbar button:last-child{border-radius:999px 0 0 999px; border-inline-end:none;}
.langbar button.active{background-color:var(--amber); border-color:var(--amber); color:var(--navy);}
body.he-mode #doc-en{display:none;}
body:not(.he-mode) #doc-he{display:none;}
@media print{body{background:#fff} .page{box-shadow:none; border:none; margin:0; max-width:none; border-radius:0}
  .langbar{display:none} body.he-mode #doc-en, body:not(.he-mode) #doc-he{display:none}}
"""


def strip_title(md):
    md = re.sub(r"^#\s+Road Protect.*?\n", "", md, count=1)
    md = re.sub(r"^##\s+(Full PM Spec|אפיון מוצר).*?\n", "", md, count=1)
    return md


def dashboard_embed(caption, link_label):
    """Self-contained dashboard mockup in an isolated iframe (srcdoc).
    Isolation keeps the mockup's Tailwind from touching the doc's styling."""
    dash = DASH.read_text(encoding="utf-8")
    srcdoc = html.escape(dash, quote=True)
    return (
        f'<figure class="dash-embed" dir="rtl">'
        f'<figcaption><span>{caption}</span>'
        f'<a href="../mockups/dashboard.html" target="_blank" rel="noopener">{link_label}</a></figcaption>'
        f'<iframe srcdoc="{srcdoc}" title="dashboard mockup" loading="lazy"></iframe>'
        f'</figure>'
    )


def build():
    body_en = render(strip_title(SRC.read_text(encoding="utf-8")))
    body_he = render(strip_title(SRC_HE.read_text(encoding="utf-8")))

    # Embed the live dashboard mockup right after the §9.3 "four screens" heading,
    # in each language body.
    embed_en = dashboard_embed("Live dashboard mockup — all four screens (Hebrew RTL)", "Open full screen ↗")
    embed_he = dashboard_embed("מוקאפ חי של לוח הבקרה — כל ארבעת המסכים", "פתח במסך מלא ↗")
    body_en = re.sub(r'(<h3[^>]*>9\.3 The four screens</h3>)',
                     lambda m: m.group(1) + embed_en, body_en, count=1)
    body_he = re.sub(r'(<h3[^>]*>9\.3 ארבעת המסכים</h3>)',
                     lambda m: m.group(1) + embed_he, body_he, count=1)

    doc = f"""<!DOCTYPE html>
<html lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Road Protect — בוט ולוח בקרה — אפיון מוצר</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="langbar">
  <button id="btn-en" class="active" onclick="setLang('en')">English</button>
  <button id="btn-he" onclick="setLang('he')">עברית</button>
</div>
<div class="page">
  <div class="cover">
    <div class="brand">Road Protect</div>
    <div class="t-he">בוט WhatsApp ולוח בקרה — אפיון מוצר</div>
    <div class="t-en">WhatsApp Bot &amp; Dashboard — Product Spec</div>
    <div class="tag" id="cover-tag">Non-technical · user journeys · full bot copy · UI · value prop</div>
    <div class="meta">Q2 2026 · Owner: Yossi · internal</div>
  </div>
  <div id="doc-en" dir="ltr">
{body_en}
  </div>
  <div id="doc-he" dir="rtl">
{body_he}
  </div>
</div>
<script>
function setLang(l){{
  var he = l === 'he';
  document.body.classList.toggle('he-mode', he);
  document.getElementById('btn-he').classList.toggle('active', he);
  document.getElementById('btn-en').classList.toggle('active', !he);
  document.getElementById('cover-tag').textContent = he
    ? 'לא-טכני · מסעות משתמש · נוסחי בוט מלאים · UI · הצעת ערך'
    : 'Non-technical · user journeys · full bot copy · UI · value prop';
  try {{ localStorage.setItem('rp_pm_lang', l); }} catch(e) {{}}
}}
(function(){{
  var saved = 'en';
  try {{ saved = localStorage.getItem('rp_pm_lang') || 'en'; }} catch(e) {{}}
  setLang(saved);
}})();
</script>
</body>
</html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"OK - built: {OUT}  ({len(doc):,} bytes)")


if __name__ == "__main__":
    build()

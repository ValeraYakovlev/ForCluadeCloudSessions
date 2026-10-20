"""Convert the Claude Docs XML export of the review into REPORT.md.
usage: python3 doc_xml_to_md.py doc.xml REPORT.md DOC_URL
"""
import sys, xml.etree.ElementTree as ET

BLOB_TO_FILE = {
    "blob/b1c8ed9b-86ea": "figures/fig1_burial_6X18.png",
    "blob/ca054f3f-2305": "figures/fig2_inactive_to_active.png",
    "blob/751e079c-a211": "figures/figA_inactive_to_active_3D.png",
    "blob/72429d98-1148": "figures/figB_two_ends_NAM.png",
    "blob/a8608290-28a3": "figures/figC_TMD_pocket_agonists.png",
    "blob/ad517678-7256": "figures/figD_Fab3F52_overlay.png",
    "blob/91d7ea1c-0f8b": "figures/figE_key_residues_6X18.png",
    "blob/ebb8bdd7-a8db": "figures/figF_ECD_groove_GLP1_Ex4.png",
    "blob/5f2e02fb-082d": "figures/figG_Baker_hotspot_L123.png",
}

def segments(e, bold=False, italic=False, href=None):
    """Flatten an inline element into (text, bold, italic, href) runs."""
    if e.tag == "bold": bold = True
    if e.tag == "italic": italic = True
    if e.tag == "link": href = e.get("href", "")
    if e.tag == "date": return [(e.get("value", ""), bold, italic, href)]
    if e.tag == "mention": return []
    segs = [(e.text, bold, italic, href)] if e.text else []
    for ch in e:
        segs += segments(ch, bold, italic, href)
        if ch.tail: segs.append((ch.tail, bold, italic, href))
    return segs

def render_segments(segs):
    merged = []
    for t, b, i, h in segs:
        if merged and merged[-1][1:] == (b, i, h):
            merged[-1] = (merged[-1][0] + t,) + merged[-1][1:]
        else:
            merged.append((t, b, i, h))
    out = ""
    for t, b, i, h in merged:
        core = t.strip()
        if not core:
            out += t
            continue
        lead, trail = t[:len(t) - len(t.lstrip())], t[len(t.rstrip()):]
        if b: core = "**" + core + "**"
        if i: core = "*" + core + "*"
        if h: core = "[" + core + "](" + h + ")"
        out += lead + core + trail
    return out

def para_text(p):
    parts = []
    run = []
    for ch in p:
        if ch.tag == "media":
            parts.append(render_segments(run)); run = []
            parts.append("![%s](%s)" % (ch.get("alt", ""), BLOB_TO_FILE.get(ch.get("blob"), ch.get("blob"))))
        else:
            run += segments(ch)
    parts.append(render_segments(run))
    return "".join(parts)

def cell_text(c):
    return "<br>".join(para_text(p) for p in c.findall("paragraph")).replace("|", "\\|").replace("\n", " ")

def render_table(t):
    rows = t.findall("row")
    lines = []
    for i, r in enumerate(rows):
        cells = [cell_text(c) for c in r.findall("cell")]
        lines.append("| " + " | ".join(cells) + " |")
        if i == 0:
            lines.append("|" + "---|" * len(cells))
    return "\n".join(lines)

def render_list(l, depth=0):
    kind = l.get("kind", "bullet")
    lines = []
    for n, it in enumerate(l.findall("listItem"), 1):
        mark = {"ordered": "%d." % n, "check": "- [ ]"}.get(kind, "-")
        if kind == "check":
            mark = "- [ ]"
        paras = it.findall("paragraph")
        first = para_text(paras[0]) if paras else ""
        lines.append("  " * depth + mark + " " + first)
        for p in paras[1:]:
            lines.append("  " * depth + "  " + para_text(p))
        for sub in it.findall("list"):
            lines.append(render_list(sub, depth + 1))
    return "\n".join(lines)

def main(src, dst, url):
    root = ET.fromstring(open(src, encoding="utf-8").read())
    out = []
    for b in root:
        if b.tag == "paragraph":
            txt = para_text(b).strip()
            lvl = b.get("heading")
            if lvl:
                out.append("#" * int(lvl) + " " + txt)
            elif b.find("date") is not None:
                out.append("%s · версия в Claude Docs: %s · таблица: GLP1R_agonist_vs_antagonist.xlsx" % (b.find("date").get("value"), url))
            elif txt:
                out.append(txt)
        elif b.tag == "table":
            out.append(render_table(b))
        elif b.tag == "list":
            out.append(render_list(b))
    open(dst, "w", encoding="utf-8").write("\n\n".join(out) + "\n")

if __name__ == "__main__":
    main(*sys.argv[1:4])

#!/usr/bin/env python3

import re
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path("resume_template.tex")
TEMPLATE = TEMPLATE_PATH.read_text()

def parse_sections(md_path: str) -> dict[str, list[str]]:
    sections = {}
    current = None

    for line in Path(md_path).read_text().splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line.rstrip())

    return sections

def md_to_tex(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*(.+?)\*", r"\\textit{\1}", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r"\\href{\2}{\1}", s)

    s = (
        s.replace("&", r"\&")
         .replace("%", r"\%")
         .replace("$", r"\$")
         .replace("#", r"\#")
    )
    return s

def render_section(title: str, lines: list[str]) -> str:
    out = [f"\\section*{{{title}}}"]
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.startswith("- "):
            out.append("\\begin{itemize}")
            while i < len(lines) and lines[i].strip().startswith("- "):
                out.append(f"  \\item {md_to_tex(lines[i][2:].strip())}")
                i += 1
            out.append("\\end{itemize}")
            continue

        out.append(md_to_tex(line))
        out.append("") # paragraph break
        i += 1

    return "\n".join(out)

def build():
    sections = parse_sections("resume.md")

    body = []
    for name in sections.keys():
        if name in sections:
            if name == "Projects":
                body.append("\\columnbreak") # start the right column here
            body.append(render_section(name, sections[name]))

    tex = TEMPLATE.replace("CONTENT", "\n\n".join(body))
    Path("resume.tex").write_text(tex)

    subprocess.run(
        ["tectonic", "resume.tex"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for ext in (".aux", ".log", ".out"):
        Path("resume" + ext).unlink(missing_ok=True)

if __name__ == "__main__":
    build()

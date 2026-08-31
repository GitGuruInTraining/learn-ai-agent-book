# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"D:\work\py\ai\learn-ai-agent-book") / "book" / "深入理解 AI Agent.md"
text = p.read_text(encoding="utf-8").replace("\r\n", "\n")

# Pandoc heading / image attributes
text = re.sub(r" \{\.unnumbered\}", "", text)
text = re.sub(r"\{height=[^}]+\}", "", text)
text = re.sub(r"\{width=[^}]+\}", "", text)
text = re.sub(r"\{#[^}]+\}", "", text)


def image_to_embed(m: re.Match) -> str:
    prefix = m.group(1) or ""
    alt = m.group(2).strip()
    path = m.group(3)
    embed = f"{prefix}![[{path}]]"
    if alt:
        embed += f"\n{prefix}*{alt}*"
    return embed


text = re.sub(
    r"^(> )?\!\[([^\]]*)\]\((images/[^)]+)\)",
    image_to_embed,
    text,
    flags=re.M,
)


def convert_line(line: str) -> str:
    m = re.match(r"^> \*\*(实验 \d+-\d+[^*]*)\*\*\s*$", line)
    if m:
        return f"> [!example] {m.group(1).rstrip()}"

    labeled = [
        (r"^> \*\*阅读提示\*\*：\s*(.*)$", "tip", "阅读提示"),
        (r"^> \*\*阅读指引\*\*：\s*(.*)$", "tip", "阅读指引"),
        (r"^> \*\*技术门槛提示\*\*：\s*(.*)$", "warning", "技术门槛提示"),
        (r"^> \*\*配套代码仓库\*\*：\s*(.*)$", "info", "配套代码仓库"),
    ]
    for pat, kind, title in labeled:
        m = re.match(pat, line)
        if m:
            rest = m.group(1).strip()
            if rest:
                return f"> [!{kind}] {title}\n> {rest}"
            return f"> [!{kind}] {title}"
    return line


text = "\n".join(convert_line(ln) for ln in text.split("\n"))

if not text.startswith("---\n"):
    fm = (
        "---\n"
        "title: 深入理解 AI Agent：设计原理与工程实践\n"
        "tags:\n"
        "  - AI-Agent\n"
        "  - book\n"
        "---\n\n"
    )
    text = fm + text.lstrip()

p.write_text(text, encoding="utf-8")
print("ok", p)
print("unnumbered left", text.count("{.unnumbered}"))
print("height attr left", len(re.findall(r"\{height=", text)))
print("md images left", len(re.findall(r"!\[.+\]\(images/", text)))
print("wikilink embeds", text.count("![[images/"))
print("example callouts", text.count("> [!example]"))
print("tip callouts", text.count("> [!tip]"))

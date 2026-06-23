#!/usr/bin/env python3
"""Render a minimalist PM thinking card as SVG from a JSON payload."""

from __future__ import annotations

import argparse
import html
import json
import re
import textwrap
from pathlib import Path
from typing import Any

WIDTH = 1080
HEIGHT = 1440
INK = "#17233f"
MUTED = "#60708a"
LINE = "#d8deea"
PAPER = "#fbfaf5"
ACCENT = "#b98236"
SOFT = "#f3efe4"
FOOTER_TEXT = "完整链接请见正文资料入口 | 产品表现 + 市场需求 = 产品价值"


def clean(text: Any) -> str:
    return " ".join(str(text or "").split())


def token_width(token: str) -> float:
    width = 0.0
    for ch in token:
        if "\u4e00" <= ch <= "\u9fff":
            width += 1.0
        elif ch.isspace():
            width += 0.35
        else:
            width += 0.55
    return width


def mixed_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./+-]+|\s+|[^A-Za-z0-9_./+-]", text)


def wrap(text: Any, width: int, max_lines: int | None = None) -> list[str]:
    text = clean(text)
    if not text:
        return []
    has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in text)
    if not has_cjk:
        lines = textwrap.wrap(text, width=width)
    else:
        lines: list[str] = []
        current = ""
        current_width = 0.0
        for token in mixed_tokens(text):
            w = token_width(token)
            if current and current_width + w > width:
                lines.append(current.strip())
                current = token
                current_width = w
            else:
                current += token
                current_width += w
        if current.strip():
            lines.append(current.strip())
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip("。,.，；;：: ") + "..."
    return lines


def text_lines(lines: list[str], x: int, y: int, size: int, fill: str = INK, weight: str = "400", line_height: float = 1.42) -> str:
    step = int(size * line_height)
    return "\n".join(
        f'<text x="{x}" y="{y + idx * step}" font-size="{size}" font-weight="{weight}" fill="{fill}">{html.escape(line)}</text>'
        for idx, line in enumerate(lines)
    )


def label(x: int, y: int, text: str) -> str:
    return f'<text x="{x}" y="{y}" font-size="22" font-weight="700" fill="{ACCENT}">{html.escape(text)}</text>'


def divider(y: int) -> str:
    return f'<line x1="72" y1="{y}" x2="1008" y2="{y}" stroke="{LINE}" stroke-width="2"/>'


def normalize_sources(payload: dict) -> list[dict]:
    fallback = [
        {"label": "OpenAI", "note": "官方发布"},
        {"label": "Anthropic", "note": "产品与工程博客"},
        {"label": "PM analysis", "note": "实践者视角"},
    ]
    value = payload.get("sources", fallback)
    out = []
    for item in value[:4]:
        if isinstance(item, dict):
            out.append({"label": clean(item.get("label", "Source")), "note": clean(item.get("note", ""))})
        else:
            out.append({"label": clean(item), "note": "资料入口"})
    return out


def render_sources(sources: list[dict]) -> str:
    svg = [label(72, 430, "资料入口")]
    for idx, source in enumerate(sources[:4]):
        x = 72 + idx * 234
        svg.append(f'<rect x="{x}" y="456" width="204" height="118" rx="8" fill="{SOFT}" stroke="{LINE}"/>')
        svg.append(text_lines(wrap(source["label"], 10, 1), x + 18, 495, 24, INK, "700"))
        svg.append(text_lines(wrap(source["note"], 12, 2), x + 18, 532, 21, MUTED))
    return "\n".join(svg)


def render_logic(logic: dict) -> str:
    blocks = [
        ("产品表现", logic.get("performance", "场景、路径、指标与团队贡献。")),
        ("市场需求", logic.get("demand", "用户需求、替代方案、竞品表现与时机。")),
        ("产品价值", logic.get("value", "用户价值、平台价值、商业化与壁垒。")),
    ]
    svg = [label(72, 642, "产品判断")]
    y = 676
    for idx, (title, body) in enumerate(blocks):
        x = 72 + idx * 312
        svg.append(f'<rect x="{x}" y="{y}" width="288" height="196" rx="8" fill="#ffffff" stroke="{LINE}"/>')
        svg.append(f'<text x="{x + 20}" y="{y + 42}" font-size="25" font-weight="700" fill="{INK}">{title}</text>')
        svg.append(text_lines(wrap(body, 13, 4), x + 20, y + 84, 22, MUTED, line_height=1.38))
    return "\n".join(svg)


def render_list(title: str, items: list, x: int, y: int, width_chars: int, max_items: int, item_size: int = 24) -> str:
    svg = [label(x, y, title)]
    current_y = y + 42
    for idx, item in enumerate(items[:max_items], 1):
        lines = wrap(item, width_chars, 2)
        svg.append(f'<text x="{x}" y="{current_y}" font-size="{item_size}" font-weight="700" fill="{ACCENT}">{idx}.</text>')
        svg.append(text_lines(lines, x + 34, current_y, item_size, INK, line_height=1.36))
        current_y += 34 * max(1, len(lines)) + 18
    return "\n".join(svg)


def render_prompts(prompts: list) -> str:
    svg = [f'<rect x="72" y="1190" width="936" height="134" rx="10" fill="{SOFT}" stroke="{LINE}"/>', label(102, 1230, "给自己的追问")]
    for idx, prompt in enumerate(prompts[:3], 1):
        x = 102 + (idx - 1) * 302
        svg.append(f'<text x="{x}" y="1284" font-size="24" font-weight="700" fill="{ACCENT}">{idx}.</text>')
        svg.append(text_lines(wrap(prompt, 12, 2), x + 34, 1284, 23, INK, line_height=1.35))
    return "\n".join(svg)


def render(payload: dict) -> str:
    title = clean(payload.get("title", "今日产品思考"))[:18]
    subtitle = clean(payload.get("subtitle", "Product Thinking Card"))[:42]
    question = payload.get("question", "")
    sources = normalize_sources(payload)
    logic = payload.get("logic", {}) if isinstance(payload.get("logic", {}), dict) else {}
    insights = payload.get("insights") or [payload.get("insight", "从用户行为、市场需求和商业闭环判断产品价值。")]
    prompts = payload.get("prompts", [])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>
  <rect x="40" y="40" width="1000" height="1360" rx="18" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>
  <circle cx="944" cy="104" r="18" fill="{ACCENT}" opacity="0.18"/>
  <circle cx="986" cy="126" r="6" fill="{ACCENT}" opacity="0.45"/>
  <line x1="72" y1="118" x2="176" y2="118" stroke="{ACCENT}" stroke-width="5" stroke-linecap="round"/>
  <text x="72" y="168" font-size="54" font-weight="800" fill="{INK}">{html.escape(title)}</text>
  <text x="72" y="212" font-size="24" fill="{MUTED}">{html.escape(subtitle)}</text>
  {divider(250)}
  {label(72, 300, "核心问题")}
  {text_lines(wrap(question, 25, 3), 72, 355, 43, INK, "800", 1.34)}
  {render_sources(sources)}
  {divider(602)}
  {render_logic(logic)}
  {divider(910)}
  {render_list("关键洞察", insights, 72, 966, 30, 3, 25)}
  {render_prompts(prompts)}
  <text x="72" y="1372" font-size="20" fill="{MUTED}">{html.escape(FOOTER_TEXT)}</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a minimalist PM thinking card SVG.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_svg", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8-sig"))
    args.output_svg.parent.mkdir(parents=True, exist_ok=True)
    args.output_svg.write_text(render(payload), encoding="utf-8")


if __name__ == "__main__":
    main()

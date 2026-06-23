#!/usr/bin/env python3
"""Render an interactive PM thinking HTML page from a JSON payload."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def esc(value: Any) -> str:
    return html.escape(clean(value), quote=True)


def as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def source_cards(sources: list[dict]) -> str:
    cards = []
    for idx, item in enumerate(sources, 1):
        label = esc(item.get("label", f"Source {idx}"))
        note = esc(item.get("note", ""))
        url = esc(item.get("url", "#"))
        kind = esc(item.get("kind", "资料"))
        cards.append(f'''
        <a class="source-card" href="{url}" target="_blank" rel="noreferrer">
          <span class="source-kind">{kind}</span>
          <strong>{label}</strong>
          <span>{note}</span>
        </a>''')
    return "\n".join(cards)


def fact_list(facts: list[str]) -> str:
    return "\n".join(f"<li>{esc(item)}</li>" for item in facts)


def judgment_column(title: str, subtitle: str, items: list[str]) -> str:
    bullets = "\n".join(f"<li>{esc(item)}</li>" for item in items)
    return f'''
      <article class="judgment-card">
        <p class="eyebrow">{esc(subtitle)}</p>
        <h3>{esc(title)}</h3>
        <ul>{bullets}</ul>
      </article>'''


def insight_cards(insights: list[dict]) -> str:
    html_cards = []
    for idx, item in enumerate(insights, 1):
        title = esc(item.get("title", f"洞察 {idx}"))
        detail = esc(item.get("detail", item if isinstance(item, str) else ""))
        evidence = esc(item.get("evidence", "")) if isinstance(item, dict) else ""
        action = esc(item.get("action", "")) if isinstance(item, dict) else ""
        html_cards.append(f'''
        <article class="insight-card">
          <div class="insight-index">{idx}</div>
          <div>
            <h3>{title}</h3>
            <p>{detail}</p>
            {f'<p class="support"><b>依据：</b>{evidence}</p>' if evidence else ''}
            {f'<p class="support"><b>联系实际：</b>{action}</p>' if action else ''}
          </div>
        </article>''')
    return "\n".join(html_cards)


def prompt_blocks(prompts: list[dict]) -> str:
    blocks = []
    for idx, item in enumerate(prompts, 1):
        question = esc(item.get("question", item if isinstance(item, str) else f"问题 {idx}"))
        hint = esc(item.get("hint", "")) if isinstance(item, dict) else ""
        blocks.append(f'''
        <label class="prompt-block">
          <span class="prompt-title">{idx}. {question}</span>
          {f'<span class="prompt-hint">{hint}</span>' if hint else ''}
          <textarea data-question="{question}" placeholder="写下你的判断、证据、反证和下一步验证..."></textarea>
        </label>''')
    return "\n".join(blocks)


def render(payload: dict) -> str:
    title = esc(payload.get("title", "产品思维训练"))
    subtitle = esc(payload.get("subtitle", "Product Thinking Coach"))
    question = esc(payload.get("question", "今天要拆解的产品问题是什么？"))
    date = esc(payload.get("date", "Daily Practice"))
    sources = as_list(payload.get("sources"))
    facts = as_list(payload.get("facts"))
    logic = payload.get("logic", {}) if isinstance(payload.get("logic"), dict) else {}
    insights = as_list(payload.get("insights"))
    prompts = as_list(payload.get("prompts"))
    writing_template = esc(payload.get("writing_template", "我观察到... 我判断... 关键证据是... 下一步验证..."))

    performance = as_list(logic.get("performance"))
    demand = as_list(logic.get("demand"))
    value = as_list(logic.get("value"))

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      --ink: #18233f;
      --muted: #667085;
      --paper: #fffaf0;
      --panel: rgba(255, 255, 255, 0.88);
      --line: #e7dcc7;
      --gold: #d7a84f;
      --rose: #c96062;
      --night: #263761;
      --teal: #668f8b;
      --shadow: 0 24px 70px rgba(34, 39, 62, 0.14);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      background:
        radial-gradient(circle at 88% 10%, rgba(38, 55, 97, 0.16), transparent 22rem),
        radial-gradient(circle at 12% 86%, rgba(215, 168, 79, 0.18), transparent 18rem),
        linear-gradient(135deg, #fff8e8 0%, #f8efe0 45%, #f6f1e7 100%);
      min-height: 100vh;
    }}
    .page {{ width: min(1180px, calc(100% - 40px)); margin: 0 auto; padding: 48px 0 64px; position: relative; }}
    .stars {{ position: fixed; inset: 0; pointer-events: none; overflow: hidden; }}
    .stars i {{ position: absolute; width: 4px; height: 4px; border-radius: 50%; background: var(--gold); opacity: .72; }}
    .stars i:nth-child(1) {{ left: 9%; top: 12%; }} .stars i:nth-child(2) {{ left: 82%; top: 16%; }} .stars i:nth-child(3) {{ left: 91%; top: 48%; }} .stars i:nth-child(4) {{ left: 18%; top: 76%; }} .stars i:nth-child(5) {{ left: 66%; top: 84%; }}
    header {{
      position: relative;
      padding: 44px 420px 42px 44px;
      border: 1px solid var(--line);
      border-radius: 26px;
      background: var(--panel);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .planet {{ position: absolute; right: 72px; top: 42px; width: 230px; height: 230px; border-radius: 50%; background: var(--night); box-shadow: inset -26px -22px 0 rgba(0,0,0,.08); }}
    .planet::before, .planet::after {{ content: ""; position: absolute; border-radius: 50%; background: #ffd86b; }}
    .planet::before {{ width: 18px; height: 18px; left: 60px; top: 72px; }}
    .planet::after {{ width: 8px; height: 8px; right: 58px; top: 104px; }}
    .orbit {{ position: absolute; right: 16px; top: 150px; width: 360px; height: 90px; border-top: 2px solid rgba(102,143,139,.42); transform: rotate(-8deg); border-radius: 50%; }}
    .rose {{ position: absolute; right: 310px; bottom: 42px; width: 52px; height: 86px; }}
    .rose::before {{ content: ""; position: absolute; left: 16px; top: 0; width: 24px; height: 24px; background: var(--rose); border-radius: 60% 40% 55% 45%; box-shadow: -9px 8px 0 #d87979, 9px 8px 0 #b94d54; }}
    .rose::after {{ content: ""; position: absolute; left: 26px; top: 28px; width: 2px; height: 58px; background: var(--teal); box-shadow: -14px 20px 0 -1px var(--teal), 14px 30px 0 -1px var(--teal); }}
    .kicker {{ color: var(--rose); font-weight: 800; letter-spacing: .08em; font-size: 14px; text-transform: uppercase; }}
    h1 {{ margin: 18px 0 16px; font-size: clamp(34px, 5vw, 64px); line-height: 1.08; letter-spacing: 0; }}
    .question {{ margin: 0; color: #2f3c5f; font-size: clamp(22px, 3vw, 32px); line-height: 1.45; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: 1fr; gap: 22px; margin-top: 24px; }}
    section {{ border: 1px solid var(--line); border-radius: 22px; background: var(--panel); box-shadow: 0 12px 40px rgba(34,39,62,.08); padding: 28px; }}
    .section-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 18px; }}
    h2 {{ margin: 0; font-size: 26px; }}
    .hint {{ color: var(--muted); font-size: 14px; }}
    .source-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }}
    .source-card {{ display: flex; min-height: 150px; flex-direction: column; gap: 10px; padding: 18px; border-radius: 18px; text-decoration: none; color: var(--ink); background: #fff8e8; border: 1px solid #eadbbd; transition: transform .18s ease, box-shadow .18s ease; }}
    .source-card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 30px rgba(34,39,62,.12); }}
    .source-kind {{ width: fit-content; border-radius: 999px; padding: 4px 9px; background: #263761; color: #fff; font-size: 12px; }}
    .source-card strong {{ font-size: 18px; }}
    .source-card span:last-child {{ color: var(--muted); line-height: 1.45; }}
    .facts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px 28px; padding-left: 20px; color: #34405f; line-height: 1.75; }}
    .judgment-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .judgment-card {{ padding: 22px; border-radius: 18px; background: #ffffff; border: 1px solid var(--line); }}
    .eyebrow {{ margin: 0 0 10px; color: var(--rose); font-weight: 800; font-size: 13px; }}
    .judgment-card h3 {{ margin: 0 0 14px; font-size: 22px; }}
    .judgment-card ul, .insight-card p {{ margin-bottom: 0; }}
    li {{ margin: 0 0 10px; }}
    .insight-list {{ display: grid; gap: 16px; }}
    .insight-card {{ display: grid; grid-template-columns: 42px 1fr; gap: 16px; padding: 20px; border: 1px solid var(--line); border-radius: 18px; background: #fff; }}
    .insight-index {{ width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; background: var(--gold); color: #fff; font-weight: 900; }}
    .insight-card h3 {{ margin: 0 0 8px; font-size: 21px; }}
    .insight-card p {{ color: #34405f; line-height: 1.7; }}
    .support {{ color: var(--muted) !important; font-size: 15px; }}
    .reflection-grid {{ display: grid; gap: 16px; }}
    .prompt-block {{ display: grid; gap: 10px; padding: 18px; border-radius: 18px; background: #fff8e8; border: 1px solid #eadbbd; }}
    .prompt-title {{ font-size: 18px; font-weight: 800; }}
    .prompt-hint {{ color: var(--muted); line-height: 1.55; }}
    textarea {{ width: 100%; min-height: 120px; resize: vertical; border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; font: inherit; line-height: 1.6; color: var(--ink); background: rgba(255,255,255,.86); }}
    textarea:focus {{ outline: 3px solid rgba(215,168,79,.24); border-color: var(--gold); }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-top: 16px; }}
    button {{ border: 0; border-radius: 999px; padding: 12px 18px; font-weight: 800; color: #fff; background: var(--night); cursor: pointer; }}
    button.secondary {{ background: var(--rose); }}
    .save-state {{ color: var(--muted); }}
    .template {{ margin-top: 14px; padding: 16px; border-radius: 16px; background: rgba(102,143,139,.12); color: #314e50; line-height: 1.65; }}
    @media (max-width: 900px) {{
      header {{ padding: 34px 28px 260px; }}
      .planet {{ right: 42px; top: auto; bottom: 32px; width: 170px; height: 170px; }}
      .orbit {{ right: 0; top: auto; bottom: 90px; }}
      .rose {{ right: 250px; bottom: 34px; }}
      .source-grid, .judgment-grid, .facts {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="stars"><i></i><i></i><i></i><i></i><i></i></div>
  <main class="page">
    <header>
      <div class="orbit"></div><div class="planet"></div><div class="rose"></div>
      <div class="kicker">{date} · PM Thinking Coach</div>
      <h1>{title}</h1>
      <p class="question">{question}</p>
      <p class="hint">{subtitle}</p>
    </header>

    <div class="grid">
      <section>
        <div class="section-head"><h2>资料入口</h2><span class="hint">点击卡片打开原始资料，便于回溯阅读</span></div>
        <div class="source-grid">{source_cards(sources)}</div>
      </section>

      <section>
        <div class="section-head"><h2>事实速写</h2><span class="hint">先看资料事实，再做产品推理</span></div>
        <ul class="facts">{fact_list(facts)}</ul>
      </section>

      <section>
        <div class="section-head"><h2>产品判断</h2><span class="hint">产品表现 + 市场需求 = 产品价值</span></div>
        <div class="judgment-grid">
          {judgment_column("产品表现", "场景 / 路径 / 指标", performance)}
          {judgment_column("市场需求", "用户 / 竞品 / 时机", demand)}
          {judgment_column("产品价值", "用户 / 平台 / 商业", value)}
        </div>
      </section>

      <section>
        <div class="section-head"><h2>关键洞察</h2><span class="hint">把抽象判断落到真实产品动作</span></div>
        <div class="insight-list">{insight_cards(insights)}</div>
      </section>

      <section>
        <div class="section-head"><h2>给自己的追问</h2><span class="hint">回答会保存在当前浏览器，可导出 JSON</span></div>
        <div class="reflection-grid">{prompt_blocks(prompts)}</div>
        <div class="template"><b>写作模板：</b>{writing_template}</div>
        <div class="actions">
          <button id="saveBtn">保存回答</button>
          <button id="exportBtn" class="secondary">导出 JSON</button>
          <span id="saveState" class="save-state">尚未保存</span>
        </div>
      </section>
    </div>
  </main>
  <script>
    const storageKey = 'pm-thinking-coach:' + document.title;
    const textareas = [...document.querySelectorAll('textarea')];
    function collectAnswers() {{
      return textareas.map((el, index) => ({{ index: index + 1, question: el.dataset.question, answer: el.value.trim() }}));
    }}
    function saveAnswers() {{
      localStorage.setItem(storageKey, JSON.stringify({{ savedAt: new Date().toISOString(), answers: collectAnswers() }}, null, 2));
      document.getElementById('saveState').textContent = '已保存：' + new Date().toLocaleString();
    }}
    function loadAnswers() {{
      const raw = localStorage.getItem(storageKey);
      if (!raw) return;
      try {{
        const data = JSON.parse(raw);
        (data.answers || []).forEach((item, idx) => {{ if (textareas[idx]) textareas[idx].value = item.answer || ''; }});
        if (data.savedAt) document.getElementById('saveState').textContent = '已恢复：' + new Date(data.savedAt).toLocaleString();
      }} catch (error) {{ console.warn(error); }}
    }}
    document.getElementById('saveBtn').addEventListener('click', saveAnswers);
    document.getElementById('exportBtn').addEventListener('click', () => {{
      const blob = new Blob([JSON.stringify({{ title: document.title, exportedAt: new Date().toISOString(), answers: collectAnswers() }}, null, 2)], {{ type: 'application/json' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = document.title.replace(/\s+/g, '-') + '-answers.json';
      link.click();
      URL.revokeObjectURL(link.href);
    }});
    textareas.forEach((el) => el.addEventListener('input', () => {{ document.getElementById('saveState').textContent = '有未保存修改'; }}));
    loadAnswers();
  </script>
</body>
</html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an interactive PM thinking HTML page.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8-sig"))
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(render(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Render an interactive PM thinking HTML page from a JSON payload."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from string import Template
from typing import Any


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def esc(value: Any) -> str:
    return html.escape(clean(value), quote=True)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def source_cards(sources: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for idx, item in enumerate(sources, 1):
        label = esc(item.get("label", f"Source {idx}"))
        note = esc(item.get("note", ""))
        url = esc(item.get("url", "#"))
        kind = esc(item.get("kind", "资料"))
        summary = esc(item.get("summary", ""))
        date = esc(item.get("date", ""))
        meta = f"<span class=\"source-date\">{date}</span>" if date else ""
        summary_block = f"<p class=\"source-summary\">{summary}</p>" if summary else ""
        cards.append(
            f"""
        <a class="source-card" href="{url}" target="_blank" rel="noreferrer">
          <div class="source-top">
            <div class="source-chip-row">
              <span class="source-kind">{kind}</span>
              {meta}
            </div>
            <strong>{label}</strong>
          </div>
          <span class="source-note">{note}</span>
          {summary_block}
        </a>"""
        )
    return "\n".join(cards)


def summary_blocks(items: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for idx, item in enumerate(items, 1):
        title = esc(item.get("title", f"总结 {idx}"))
        body = esc(item.get("body", ""))
        why = esc(item.get("why", ""))
        why_block = f"<p class=\"support\"><b>为什么重要：</b>{why}</p>" if why else ""
        blocks.append(
            f"""
        <article class="summary-card">
          <span class="summary-kicker">Summary {idx}</span>
          <h3>{title}</h3>
          <p>{body}</p>
          {why_block}
        </article>"""
        )
    return "\n".join(blocks)


def theme_cards(themes: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for idx, item in enumerate(themes, 1):
        title = esc(item.get("title", f"主题 {idx}"))
        why = esc(item.get("why", ""))
        training = esc(item.get("training_value", ""))
        why_block = f"<p><b>为什么入选：</b>{why}</p>" if why else ""
        training_block = f"<p><b>训练价值：</b>{training}</p>" if training else ""
        cards.append(
            f"""
        <article class="theme-card">
          <span class="theme-index">Theme {idx}</span>
          <h3>{title}</h3>
          {why_block}
          {training_block}
        </article>"""
        )
    return "\n".join(cards)


def question_cards(questions: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for item in questions[:1]:
        qtype = esc(item.get("type", "深度产品问题"))
        topic = esc(item.get("topic", ""))
        source = esc(item.get("source", ""))
        question = esc(item.get("question", ""))
        assumption = esc(item.get("assumption", ""))
        why = esc(item.get("why", ""))
        performance = esc(item.get("performance", item.get("judgment", "")))
        demand = esc(item.get("demand", ""))
        value = esc(item.get("value", ""))
        exercise = esc(item.get("exercise", ""))
        source_block = f"<p class=\"support\"><b>资料入口：</b>{source}</p>" if source else ""
        why_block = f"<p class=\"question-why\"><b>为什么值得思考：</b>{why}</p>" if why else ""
        cards.append(
            f"""
        <article class="question-card hero-question">
          <div class="question-heading">
            <span class="question-type">{qtype}</span>
            <h3>{topic}</h3>
          </div>
          {source_block}
          <p class="question-line">{question}</p>
          {why_block}
          <div class="question-meta">
            <p><b>隐藏假设</b><span>{assumption}</span></p>
            <p><b>产品表现</b><span>{performance}</span></p>
            <p><b>市场需求</b><span>{demand}</span></p>
            <p><b>产品价值</b><span>{value}</span></p>
            <p class="question-meta-wide"><b>10 分钟练习</b><span>{exercise}</span></p>
          </div>
        </article>"""
        )
    return "\n".join(cards)


def judgment_column(title: str, subtitle: str, items: list[Any]) -> str:
    bullets = "\n".join(f"<li>{esc(item)}</li>" for item in items)
    return f"""
      <article class="judgment-card">
        <p class="eyebrow">{esc(subtitle)}</p>
        <h3>{esc(title)}</h3>
        <ul>{bullets}</ul>
      </article>"""


def insight_cards(insights: list[Any]) -> str:
    html_cards: list[str] = []
    for idx, item in enumerate(insights, 1):
        if isinstance(item, dict):
            title = esc(item.get("title", f"洞察 {idx}"))
            detail = esc(item.get("detail", ""))
            evidence = esc(item.get("evidence", ""))
            action = esc(item.get("action", ""))
        else:
            title = esc(f"洞察 {idx}")
            detail = esc(item)
            evidence = ""
            action = ""
        evidence_block = f"<p class=\"support\"><b>依据：</b>{evidence}</p>" if evidence else ""
        action_block = f"<p class=\"support\"><b>联系实际：</b>{action}</p>" if action else ""
        html_cards.append(
            f"""
        <article class="insight-card">
          <div class="insight-index">{idx}</div>
          <div>
            <h3>{title}</h3>
            <p>{detail}</p>
            {evidence_block}
            {action_block}
          </div>
        </article>"""
        )
    return "\n".join(html_cards)


def prompt_blocks(prompts: list[Any]) -> str:
    blocks: list[str] = []
    for idx, item in enumerate(prompts, 1):
        if isinstance(item, dict):
            question = esc(item.get("question", f"问题 {idx}"))
            hint = esc(item.get("hint", ""))
        else:
            question = esc(item)
            hint = ""
        hint_block = f"<span class=\"prompt-hint\">{hint}</span>" if hint else ""
        blocks.append(
            f"""
        <label class="prompt-block">
          <span class="prompt-title">{idx}. {question}</span>
          {hint_block}
          <textarea data-question="{question}" placeholder="写下你的判断、证据、反证和下一步验证。"></textarea>
        </label>"""
        )
    return "\n".join(blocks)


PAGE_TEMPLATE = Template("""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>$title</title>
  <style>
    :root {
      --ink: #1f2947;
      --ink-soft: #40506f;
      --muted: #6e768c;
      --paper: #faf2e4;
      --panel: rgba(255, 251, 245, 0.88);
      --line: rgba(188, 161, 124, 0.30);
      --gold: #d6a652;
      --rose: #c86167;
      --night: #2b3f6f;
      --teal: #6c9389;
      --shadow: 0 26px 72px rgba(34, 39, 62, 0.15);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      font-family: Georgia, "Times New Roman", "Noto Serif SC", "Songti SC", serif;
      background:
        radial-gradient(circle at 14% 14%, rgba(255, 225, 174, 0.54), transparent 18rem),
        radial-gradient(circle at 88% 12%, rgba(43, 63, 111, 0.18), transparent 22rem),
        linear-gradient(180deg, #fdf6e8 0%, #f7ecd9 52%, #f5e7d3 100%);
      min-height: 100vh;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image: radial-gradient(rgba(255,255,255,0.16) 1px, transparent 1px);
      background-size: 18px 18px;
      opacity: .16;
      mix-blend-mode: multiply;
    }
    .page {
      width: min(1220px, calc(100% - 36px));
      margin: 0 auto;
      padding: 36px 0 68px;
      position: relative;
    }
    .stars {
      position: fixed;
      inset: 0;
      pointer-events: none;
      overflow: hidden;
    }
    .stars i {
      position: absolute;
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--gold);
      opacity: .8;
      box-shadow: 0 0 10px rgba(214,166,82,.34);
    }
    .stars i:nth-child(1) { left: 8%; top: 12%; }
    .stars i:nth-child(2) { left: 21%; top: 8%; }
    .stars i:nth-child(3) { left: 84%; top: 14%; }
    .stars i:nth-child(4) { left: 91%; top: 30%; }
    .stars i:nth-child(5) { left: 16%; top: 79%; }
    .stars i:nth-child(6) { left: 66%; top: 84%; }
    header {
      position: relative;
      padding: 54px 410px 54px 52px;
      border: 1px solid var(--line);
      border-radius: 34px;
      background: linear-gradient(180deg, rgba(255,252,247,.94), rgba(250,243,233,.88));
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .hero-wash {
      position: absolute;
      inset: auto -80px -120px auto;
      width: 420px;
      height: 420px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(108,147,137,.17), transparent 62%);
    }
    .planet {
      position: absolute;
      right: 86px;
      top: 56px;
      width: 238px;
      height: 238px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 32%, #334d83 0%, var(--night) 62%, #203056 100%);
      box-shadow: inset -30px -20px 0 rgba(0,0,0,.10);
    }
    .planet::before, .planet::after {
      content: "";
      position: absolute;
      border-radius: 50%;
      background: #f5cf7e;
    }
    .planet::before { width: 18px; height: 18px; left: 68px; top: 86px; }
    .planet::after { width: 8px; height: 8px; right: 58px; top: 110px; }
    .orbit {
      position: absolute;
      right: 6px;
      top: 166px;
      width: 384px;
      height: 94px;
      border-top: 2px solid rgba(108,147,137,.5);
      transform: rotate(-8deg);
      border-radius: 50%;
    }
    .rose {
      position: absolute;
      right: 306px;
      bottom: 48px;
      width: 62px;
      height: 104px;
    }
    .rose::before {
      content: "";
      position: absolute;
      left: 18px;
      top: 0;
      width: 28px;
      height: 28px;
      background: var(--rose);
      border-radius: 62% 38% 55% 45%;
      box-shadow: -11px 9px 0 #da7a7f, 11px 9px 0 #b64950;
    }
    .rose::after {
      content: "";
      position: absolute;
      left: 31px;
      top: 33px;
      width: 2px;
      height: 71px;
      background: var(--teal);
      box-shadow: -17px 22px 0 -1px var(--teal), 16px 34px 0 -1px var(--teal);
    }
    .kicker {
      color: var(--rose);
      font-weight: 700;
      letter-spacing: .12em;
      font-size: 13px;
      text-transform: uppercase;
    }
    h1 {
      margin: 18px 0 14px;
      font-size: clamp(38px, 4.8vw, 68px);
      line-height: 1.05;
      letter-spacing: 0;
      font-weight: 700;
    }
    .question {
      margin: 0;
      color: var(--ink-soft);
      font-size: clamp(22px, 2.9vw, 33px);
      line-height: 1.5;
      font-weight: 600;
      max-width: 12em;
    }
    .hero-note {
      margin-top: 18px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.75;
      max-width: 40rem;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 22px;
      margin-top: 24px;
    }
    section {
      border: 1px solid var(--line);
      border-radius: 26px;
      background: linear-gradient(180deg, rgba(255,252,246,.93), rgba(252,246,236,.86));
      box-shadow: 0 16px 38px rgba(34,39,62,.08);
      padding: 28px;
      position: relative;
      overflow: hidden;
    }
    section::after {
      content: "";
      position: absolute;
      right: -80px;
      top: -80px;
      width: 180px;
      height: 180px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(214,166,82,.08), transparent 70%);
    }
    .section-head {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
      position: relative;
      z-index: 1;
    }
    h2 {
      margin: 0;
      font-size: 27px;
      font-weight: 700;
    }
    .hint {
      color: var(--muted);
      font-size: 14px;
      max-width: 28rem;
      text-align: right;
      line-height: 1.6;
    }
    .source-grid,
    .summary-grid,
    .judgment-grid {
      display: grid;
      gap: 16px;
      position: relative;
      z-index: 1;
    }
    .source-grid,
    .summary-grid,
    .judgment-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .theme-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }
    .source-card,
    .summary-card,
    .theme-card,
    .question-card,
    .judgment-card,
    .insight-card,
    .prompt-block {
      position: relative;
      z-index: 1;
    }
    .source-card {
      display: flex;
      min-height: 216px;
      flex-direction: column;
      gap: 10px;
      padding: 20px;
      border-radius: 20px;
      text-decoration: none;
      color: var(--ink);
      background: rgba(255, 248, 236, 0.96);
      border: 1px solid rgba(214, 184, 133, 0.42);
      transition: transform .18s ease, box-shadow .18s ease;
      box-shadow: inset 0 1px 0 rgba(255,255,255,.6);
    }
    .source-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 16px 30px rgba(34,39,62,.12);
    }
    .source-top {
      display: grid;
      gap: 10px;
    }
    .source-chip-row {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }
    .source-kind,
    .source-date,
    .summary-kicker,
    .theme-index,
    .question-type {
      display: inline-flex;
      width: fit-content;
      border-radius: 999px;
      padding: 5px 10px;
      font-weight: 700;
      font-size: 12px;
      letter-spacing: .06em;
    }
    .source-kind {
      background: var(--night);
      color: #fff;
    }
    .source-date {
      background: rgba(107,118,140,.12);
      color: var(--ink-soft);
    }
    .summary-kicker,
    .theme-index,
    .question-type {
      background: rgba(200,97,103,.12);
      color: var(--rose);
      text-transform: uppercase;
    }
    .source-card strong,
    .summary-card h3,
    .theme-card h3,
    .question-card h3,
    .judgment-card h3,
    .insight-card h3 {
      font-size: 22px;
      line-height: 1.4;
      margin: 0;
    }
    .source-note {
      color: var(--ink-soft);
      line-height: 1.65;
      font-weight: 600;
    }
    .source-summary,
    .summary-card p,
    .theme-card p,
    .question-card p,
    .insight-card p,
    .judgment-card li {
      color: var(--ink-soft);
      line-height: 1.75;
      margin: 0;
    }
    .summary-card,
    .theme-card,
    .question-card,
    .judgment-card {
      padding: 22px;
      border-radius: 20px;
      background: rgba(255,255,255,.72);
      border: 1px solid rgba(214, 184, 133, 0.32);
    }
    .summary-card h3,
    .theme-card h3,
    .question-card h3,
    .judgment-card h3 {
      margin: 14px 0 10px;
    }
    .hero-question {
      background: linear-gradient(180deg, rgba(255,250,240,.94), rgba(255,244,228,.88));
    }
    .question-heading {
      display: grid;
      gap: 8px;
    }
    .question-line {
      font-size: 20px;
      font-weight: 700;
      color: var(--ink) !important;
      line-height: 1.8 !important;
      margin: 14px 0;
    }
    .question-why {
      font-size: 16px;
      margin-bottom: 0;
    }
    .question-meta {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 16px;
    }
    .question-meta p {
      margin: 0;
      padding: 15px 16px;
      border-radius: 16px;
      background: rgba(255, 248, 236, 0.92);
      border: 1px solid rgba(214, 184, 133, 0.42);
      display: grid;
      gap: 8px;
    }
    .question-meta b {
      color: var(--rose);
    }
    .question-meta-wide {
      grid-column: 1 / -1;
    }
    .eyebrow {
      margin: 0 0 10px;
      color: var(--rose);
      font-weight: 700;
      font-size: 13px;
      letter-spacing: .05em;
    }
    .judgment-card ul {
      margin: 0;
      padding-left: 18px;
    }
    .insight-list,
    .reflection-grid {
      display: grid;
      gap: 16px;
    }
    .insight-card {
      display: grid;
      grid-template-columns: 46px 1fr;
      gap: 18px;
      padding: 22px;
      border: 1px solid rgba(214, 184, 133, 0.32);
      border-radius: 20px;
      background: rgba(255,255,255,.74);
    }
    .insight-index {
      width: 46px;
      height: 46px;
      display: grid;
      place-items: center;
      border-radius: 50%;
      background: var(--gold);
      color: #fff;
      font-weight: 700;
    }
    .support {
      color: var(--muted) !important;
      font-size: 15px;
    }
    .prompt-block {
      display: grid;
      gap: 12px;
      padding: 20px;
      border-radius: 20px;
      background: rgba(255, 248, 236, 0.92);
      border: 1px solid rgba(214, 184, 133, 0.42);
    }
    .prompt-title {
      font-size: 18px;
      font-weight: 700;
      line-height: 1.6;
    }
    .prompt-hint {
      color: var(--muted);
      line-height: 1.65;
    }
    textarea {
      width: 100%;
      min-height: 132px;
      resize: vertical;
      border: 1px solid rgba(188, 161, 124, 0.36);
      border-radius: 16px;
      padding: 16px 18px;
      font: inherit;
      line-height: 1.7;
      color: var(--ink);
      background: rgba(255,255,255,.9);
    }
    textarea:focus {
      outline: 3px solid rgba(214,166,82,.22);
      border-color: var(--gold);
    }
    .template {
      margin-top: 16px;
      padding: 18px;
      border-radius: 16px;
      background: rgba(108,147,137,0.12);
      color: #385655;
      line-height: 1.75;
    }
    .html-link-card {
      padding: 20px 22px;
      border-radius: 20px;
      background: rgba(43, 63, 111, 0.94);
      color: #fff7ea;
      display: grid;
      gap: 10px;
    }
    .html-link-card a {
      color: #fff7ea;
      text-decoration: underline;
      word-break: break-all;
    }
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      margin-top: 16px;
    }
    button {
      border: 0;
      border-radius: 999px;
      padding: 12px 18px;
      font-weight: 700;
      color: #fff;
      background: var(--night);
      cursor: pointer;
      font-family: inherit;
    }
    button.secondary {
      background: var(--rose);
    }
    .save-state {
      color: var(--muted);
    }
    @media (max-width: 980px) {
      header {
        padding: 36px 30px 280px;
      }
      .planet {
        right: 42px;
        top: auto;
        bottom: 36px;
        width: 184px;
        height: 184px;
      }
      .orbit {
        right: -10px;
        top: auto;
        bottom: 86px;
        width: 300px;
      }
      .rose {
        right: 238px;
        bottom: 38px;
      }
      .source-grid,
      .summary-grid,
      .theme-grid,
      .judgment-grid,
      .question-meta {
        grid-template-columns: 1fr;
      }
      .question-meta-wide {
        grid-column: auto;
      }
      .section-head {
        flex-direction: column;
        align-items: flex-start;
      }
      .hint {
        text-align: left;
      }
    }
  </style>
</head>
<body>
  <div class="stars"><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <main class="page">
    <header>
      <div class="hero-wash"></div>
      <div class="orbit"></div>
      <div class="planet"></div>
      <div class="rose"></div>
      <div class="kicker">$date · PM Thinking Coach</div>
      <h1>$title</h1>
      <p class="question">$question</p>
      <p class="hero-note">$subtitle</p>
    </header>

    <div class="grid">
      <section>
        <div class="section-head"><h2>AI 前沿资料入口</h2><span class="hint">保留链接，也保留为什么值得关注。</span></div>
        <div class="source-grid">$source_cards</div>
      </section>

      <section>
        <div class="section-head"><h2>前沿资料总结</h2><span class="hint">把“发生了什么”和“为什么重要”拆开讲清楚。</span></div>
        <div class="summary-grid">$summary_blocks</div>
      </section>

      <section>
        <div class="section-head"><h2>主题过滤</h2><span class="hint">从信号里收敛到真正值得想的问题。</span></div>
        <div class="theme-grid">$theme_cards</div>
      </section>

      <section>
        <div class="section-head"><h2>今日深度产品问题</h2><span class="hint">一题走深，兼顾设计、战略、成熟产品与新成功产品视角。</span></div>
        $question_cards
      </section>

      <section>
        <div class="section-head"><h2>产品问题分析</h2><span class="hint">产品表现 + 市场需求 = 产品价值</span></div>
        <div class="judgment-grid">
          $performance_column
          $demand_column
          $value_column
        </div>
      </section>

      <section>
        <div class="section-head"><h2>关键洞察</h2><span class="hint">把前沿变化翻译成能落到真实产品动作的判断。</span></div>
        <div class="insight-list">$insight_cards</div>
      </section>

      <section>
        <div class="section-head"><h2>给自己的追问</h2><span class="hint">先做自己的判断，再回看参考答案，训练价值更高。</span></div>
        <div class="reflection-grid">$prompt_blocks</div>
        <div class="template"><b>写作模板：</b>$writing_template</div>
        <div class="actions">
          <button id="saveBtn">保存回答</button>
          <button id="exportBtn" class="secondary">导出 JSON</button>
          <span id="saveState" class="save-state">尚未保存</span>
        </div>
      </section>

      <section>
        <div class="section-head"><h2>HTML 页面链接</h2><span class="hint">这个链接也应回写到 Notion 的自动推送页面里。</span></div>
        <div class="html-link-card">
          <strong>今日可视化输出</strong>
          <a href="$html_href">$html_link</a>
        </div>
      </section>
    </div>
  </main>
  <script>
    const storageKey = 'pm-thinking-coach:' + document.title;
    const textareas = Array.from(document.querySelectorAll('textarea'));

    function collectAnswers() {
      return textareas.map((el, index) => ({
        index: index + 1,
        question: el.dataset.question,
        answer: el.value.trim()
      }));
    }

    function saveAnswers() {
      const payload = {
        savedAt: new Date().toISOString(),
        answers: collectAnswers()
      };
      localStorage.setItem(storageKey, JSON.stringify(payload, null, 2));
      document.getElementById('saveState').textContent = '已保存：' + new Date().toLocaleString();
    }

    function loadAnswers() {
      const raw = localStorage.getItem(storageKey);
      if (!raw) return;
      try {
        const data = JSON.parse(raw);
        (data.answers || []).forEach((item, idx) => {
          if (textareas[idx]) {
            textareas[idx].value = item.answer || '';
          }
        });
        if (data.savedAt) {
          document.getElementById('saveState').textContent = '已恢复：' + new Date(data.savedAt).toLocaleString();
        }
      } catch (error) {
        console.warn(error);
      }
    }

    document.getElementById('saveBtn').addEventListener('click', saveAnswers);
    document.getElementById('exportBtn').addEventListener('click', () => {
      const blob = new Blob([
        JSON.stringify({
          title: document.title,
          exportedAt: new Date().toISOString(),
          answers: collectAnswers()
        }, null, 2)
      ], { type: 'application/json' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = document.title.replace(/\s+/g, '-') + '-answers.json';
      link.click();
      URL.revokeObjectURL(link.href);
    });

    textareas.forEach((el) => {
      el.addEventListener('input', () => {
        document.getElementById('saveState').textContent = '有未保存修改';
      });
    });

    loadAnswers();
  </script>
</body>
</html>
""")


def render(payload: dict[str, Any]) -> str:
    title = esc(payload.get("title", "产品思维训练"))
    subtitle = esc(payload.get("subtitle", "Product Thinking Coach"))
    question = esc(payload.get("question", "今天要拆解的产品问题是什么？"))
    date = esc(payload.get("date", "Daily Practice"))
    sources = as_list(payload.get("sources"))
    source_summaries = as_list(payload.get("source_summaries"))
    logic = payload.get("logic", {}) if isinstance(payload.get("logic"), dict) else {}
    themes = as_list(payload.get("themes"))
    questions = as_list(payload.get("questions"))
    insights = as_list(payload.get("insights"))
    prompts = as_list(payload.get("prompts"))
    writing_template = esc(payload.get("writing_template", "我观察到…… 我判断…… 关键证据是…… 下一步验证……"))
    html_link = clean(payload.get("html_link", "本页面即为今日 HTML 输出"))
    html_link_safe = esc(html_link)
    html_href = esc(html_link if html_link.startswith(("http://", "https://", "file://")) else html_link)

    performance = as_list(logic.get("performance"))
    demand = as_list(logic.get("demand"))
    value = as_list(logic.get("value"))

    return PAGE_TEMPLATE.substitute(
        title=title,
        subtitle=subtitle,
        question=question,
        date=date,
        source_cards=source_cards(sources),
        summary_blocks=summary_blocks(source_summaries),
        theme_cards=theme_cards(themes),
        question_cards=question_cards(questions),
        performance_column=judgment_column("产品表现", "场景 / 路径 / 设计 / 指标", performance),
        demand_column=judgment_column("市场需求", "用户 / 竞品 / 时机 / 证据", demand),
        value_column=judgment_column("产品价值", "用户 / 平台 / 商业 / 壁垒", value),
        insight_cards=insight_cards(insights),
        prompt_blocks=prompt_blocks(prompts),
        writing_template=writing_template,
        html_link=html_link_safe,
        html_href=html_href,
    )


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

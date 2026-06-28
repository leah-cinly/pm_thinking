# Notion Daily Push

Use this reference when publishing daily AI-frontier product-thinking practice to Notion `产品思维训练营`.

## Destination

- Target name: `产品思维训练营`.
- Prefer an existing Notion database/page with this exact name.
- If multiple matches exist, choose the most recently edited training/workspace page or ask the user.
- If Notion tools are unavailable, provide the complete Markdown page content and explicitly say the push was not completed.

## Core Collaboration Logic

Notion is the storage and collaboration surface for:

- AI frontier material
- frontier summaries
- selected product themes
- one deep product question
- product-question analysis
- key insights
- personal reflection prompts
- HTML page link

The second function is not mere storage. It should build a richer, structured product analysis around the chosen question and include source links so the user can backtrack and read.

The third function is reflection guidance, plus a beautiful HTML page that visualizes the daily question, insight reference, and reflection prompts. The HTML link should also be written into the Notion daily page.

## Daily Pipeline

1. Run at 9:00 daily through Codex automation.
2. Collect 6-10 AI frontier sources with links.
3. For each source, include:
   - label
   - type
   - date when visible
   - short summary
   - why it matters for PMs
4. Filter the sources into 1-2 product themes.
5. Generate one deep product design or strategy question.
6. Build a structured product analysis for that question.
7. Generate an HTML page and include its path/link.
8. Write the daily page into Notion.
9. Let the user answer in Notion.
10. Run weekly review on the accumulated answers.

## Daily Page Structure

Use this structure for every daily page:

```markdown
# 产品思维训练｜YYYY-MM-DD｜主题关键词

## 今日主线
One sentence connecting today's selected theme and question.

## AI 前沿资料入口（6-10 条）
- [Source label](url)｜type｜date：why it matters.

## 前沿资料总结
- What changed?
- Why now?
- Why product managers should care?

## 主题过滤
### 主题 1：Theme name
- 为什么入选：
- 对产品人的训练价值：

### 主题 2：Theme name, optional
- 为什么入选：
- 对产品人的训练价值：

## 今日深度产品问题
- 关联主题：
- 产品/场景：
- 资料入口：
- 主问题：
- 隐藏假设：
- 为什么值得思考：
- 10 分钟练习：

## 产品问题分析
### 产品表现
- Scenario / user path / design details / metrics / OKR contribution.
### 市场需求
- Target users / real need / substitutes / competitor behavior / timing / demand proof.
### 产品价值
- User value / platform value / commercialization / moat.

## 关键洞察
- Insight + evidence + practical implication.

## 给自己的追问（在 Notion 中回答）
1. Question
2. Question
3. Question

## HTML 页面链接
- Local deliverable path or shareable output reference.

## 今日输出模板
我观察到：...
我判断核心问题是：...
关键证据是：...
我的产品假设是：...
下一步验证：...
```

## Notion Styling Rules

Even when created through text blocks, the page should feel modular and readable:

- Use clear H1/H2/H3 hierarchy.
- Keep section titles consistent.
- Group source links separately from source summaries.
- Keep the question and product analysis visually distinct.
- Make the HTML link a dedicated section near the bottom.
- Prefer short, high-density sections over long wall-of-text paragraphs.

## Weekly Review Structure

Create one weekly Notion review page after reading the last 7 daily pages and user answers:

```markdown
# 产品思维周复盘｜YYYY-MM-DD 至 YYYY-MM-DD

## 本周输入概览
- Themes covered:
- Strongest frontier signals:
- Most repeated product pattern:

## 回答质量评估
- 证据使用：
- 因果推理：
- 取舍判断：
- 指标清晰度：
- 反证意识：

## 最好的 3 个回答
1. Answer summary + why strong.
2. ...
3. ...

## 3 个思维盲点
1. Blind spot + example.
2. ...
3. ...

## 下周训练重点
1. Drill
2. Drill
3. Drill

## PM 风格改写示范
A rewritten model answer based on one of the user's answers.
```

## Quality Bar

- The daily question should force judgment, tradeoff, and evidence, not recall.
- Product analysis should be structured, not slogan-like.
- Use source links with dates when available.
- Separate source facts from inference.
- Do not cite inaccessible social posts as evidence.
- Keep daily focus to 1-2 themes.
- Always include the HTML page reference in the Notion page.

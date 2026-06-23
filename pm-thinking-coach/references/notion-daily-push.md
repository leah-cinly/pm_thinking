# Notion Daily Push

Use this reference when publishing daily AI-frontier product-thinking practice to Notion `产品思维训练营`.

## Destination

- Target name: `产品思维训练营`.
- Prefer an existing Notion database/page with this exact name.
- If multiple matches exist, choose the most recently edited training/workspace page or ask the user.
- If Notion tools are unavailable, provide the complete Markdown page content and explicitly say the push was not completed.

## Daily Pipeline

1. **Run at 9:00 daily** through Codex automation.
2. **Collect 6-10 AI frontier sources** with links.
3. **Filter into 1-2 product themes** worth thinking about.
4. **Generate 1 deep product question**. Do not force five categories. Use mature product, new successful product, creative design detail, strategic layout, and personal reflection only as optional lenses.
5. **For the question**, include source entries, hidden assumption, product performance angles, market demand angles, product value angles, and a 10-minute exercise.
6. **Generate optional HTML** using `scripts/render_thinking_html.py` for a beautiful interactive page.
7. **Write the Notion page** in `产品思维训练营`.
8. **User answers in Notion**.
9. **Weekly review** evaluates answer quality and product judgment progress.

## Source Collection Rules

Collect 6-10 sources across these buckets:

- Official AI/product sources: OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft AI, GitHub, product docs, release notes, engineering blogs.
- Research/model sources: official papers, labs, technical reports, benchmark discussions from primary sources.
- Operator/expert sources: credible product leaders, AI founders, researchers, YC/a16z/Lenny/Stratechery-style analysis.
- Chinese PM/practitioner sources: 人人都是产品经理 and similar product-analysis sources when relevant.
- Social/video sources: X or YouTube only when directly accessible and useful; use as weak signals, not proof.

For every source, record:

- Source label
- URL
- Type: official / research / expert / practitioner / social-video
- Date if visible
- One sentence: why this matters for product thinking

## Theme Filter

Filter the sources into 1-2 themes using this scorecard:

- Product impact: changes user behavior, workflow entry, pricing, trust, distribution, or moat.
- Freshness: new release, new capability, new adoption signal, or newly important market shift.
- Learnability: can produce judgment questions, not just trivia.
- Evidence quality: has official or credible sources.
- Breadth: can connect mature product systems, new products, design details, strategy, and personal reflection.

Do not select more than 2 themes. The value is focus.

## Daily Page Structure

Use this structure for every daily page:

```markdown
# 产品思维训练｜YYYY-MM-DD｜主题关键词

## 今日主线
One sentence connecting today's 1-2 selected themes.

## AI 前沿资料入口（6-10 条）
- [Source label](url)｜type｜date if visible：why it matters.

## 主题过滤
### 主题 1：Theme name
- 为什么入选：product impact / freshness / learnability / evidence.
- 对产品人的训练价值：what kind of judgment it exercises.

### 主题 2：Theme name, optional
same structure

## 今日深度产品问题
- 关联主题：
- 产品/场景：
- 资料入口：
- 主问题：
- 隐藏假设：
- 为什么值得思考：
- 产品表现思考角度：场景 / 用户路径 / 功能表现 / 指标 / OKR 贡献 / 设计细节
- 市场需求思考角度：目标用户 / 真实需求 / 竞品或替代方案 / 时机 / 需求证据
- 产品价值思考角度：用户价值 / 平台价值 / 商业化 / 长期壁垒
- 10 分钟练习：
- 可选延展：成熟产品 / 新成功产品 / 创意细节 / 战略布局 / 个人复盘

## 产品判断训练
### 产品表现
- Scenario / user path / metric / OKR contribution.
### 市场需求
- Target user / real need / competitor or substitute / timing.
### 产品价值
- User value / platform value / commercialization / moat.

## 关键洞察
- Insight + evidence + practical implication.

## 给自己的追问（在 Notion 中回答）
1. Question
2. Question
3. Question

## 今日输出模板
我观察到：...
我判断核心问题是：...
关键证据是：...
我的产品假设是：...
下一步验证：...
```

## HTML Payload Shape

Use these fields when creating a local interactive HTML page:

- `sources`: 6-10 source objects with `kind`, `label`, `note`, `url`.
- `themes`: 1-2 theme objects with `title`, `why`, `training_value`.
- `questions`: 1 primary question object, or a small list when useful, with `type`, `topic`, `source`, `question`, `assumption`, `performance`, `demand`, `value`, `exercise`.
- `logic`: product performance / demand / value bullets.
- `insights`: each with title, detail, evidence, action.
- `prompts`: answer prompts for the user.

## Weekly Review Structure

Create one weekly Notion review page after reading the last 7 daily pages and user answers:

```markdown
# 产品思维周复盘｜YYYY-MM-DD 至 YYYY-MM-DD

## 本周输入概览
- Themes covered:
- Strongest sources:
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

- The daily question should force judgment, tradeoff, and evidence, not recall. One excellent deep question is better than five shallow questions.
- Product judgment must be concrete enough that the user can write a PM-style answer.
- Use source links with dates when available.
- Separate source facts from inference.
- Do not cite inaccessible social posts as evidence.
- Do not overwhelm the user with too many themes; keep daily focus to 1-2 themes.

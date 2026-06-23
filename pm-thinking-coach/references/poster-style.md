# HTML/Card Style

Goal: create a beautiful, interactive product-thinking page that feels like a polished strategy memo placed in a romantic storybook world. The visual language can be inspired by small planets, stars, roses, orbit lines, desert paper, and quiet night-blue skies, but do not copy exact copyrighted Little Prince characters, scenes, costumes, or illustrations.

## Layout

- Prefer a self-contained HTML page for rich output.
- Use clear full-width sections: header, 资料入口, 事实速写, 产品判断, 关键洞察, 给自己的追问.
- Keep sources clickable and visually grouped as cards.
- Product judgment must be concrete and information-rich, not slogan-like.
- Reflection prompts need visible textarea answer windows plus save/export actions.
- Use responsive grids; on mobile, stack columns into one column.
- Decorative planets, stars, roses, and orbit lines must stay outside text flow and never overlap readable content.

## Visual Style

- Romantic but clean: warm paper background, night-blue planet, muted gold stars, soft rose accent, subtle teal orbit lines.
- Use panels with translucent white backgrounds and thin warm borders.
- Keep illustration elements restrained and intentional.
- Avoid clutter, heavy gradients, bokeh, large busy illustrations behind text, or purely decorative cards that reduce readability.

## Typography

- Use readable system sans-serif fonts for Chinese and English.
- Hero title may be large; section headings should stay compact and scannable.
- Body text should use generous line height.
- No negative letter spacing.

## Interaction Rules

- Source cards should open links in a new tab.
- Textareas should be large enough for real answers.
- Save answers to localStorage with a stable page-specific key.
- Export answers as JSON.
- Status text should show unsaved/saved/restored state.

## Content Density Rules

- Source cards: 4-6 entries when available.
- Facts: 3-6 concise facts.
- Product judgment: 3 bullets each for 产品表现, 市场需求, 产品价值 when possible.
- Insights: each insight should include detail, evidence, and practical action.
- Reflection prompts: include a hint that pushes the user toward evidence, tradeoffs, metrics, or next validation.

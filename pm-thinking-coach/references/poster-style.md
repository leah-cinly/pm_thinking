# HTML/Card Style

Goal: create a beautiful interactive product-thinking page that feels like a crafted storybook research sheet. The visual language can be inspired by small planets, stars, roses, orbit lines, desert paper, and quiet night-blue skies, but do not copy exact copyrighted Little Prince characters, scenes, costumes, or illustrations.

## Layout

- Prefer a self-contained HTML page for rich output.
- Use clear full-width sections: hero, AI frontier sources, source summaries, selected themes, deep product question, product analysis, insights, reflection prompts.
- Keep links clickable and visually grouped as cards.
- Product analysis must be concrete and information-rich, not slogan-like.
- Reflection prompts need visible textarea answer windows plus save/export actions.
- Use responsive grids; on mobile, stack columns into one column.
- Decorative planets, stars, roses, orbit lines, and paper shapes must stay outside text flow and never overlap readable content.

## Visual Style

- Romantic editorial atmosphere rather than plain dashboard style.
- Warm paper background with layered gradients and soft texture feeling.
- Night-blue hero planet, muted gold stars, rose-red accents, subtle teal orbit lines.
- Use translucent panels with clear borders and depth.
- Favor composition and rhythm over decorative clutter.
- Avoid generic purple tech gradients, bokeh blobs, and flat white cards.

## Typography

- Use readable system sans-serif fonts for body copy.
- Hero title may be expressive and large; section headings should stay compact and polished.
- Body text should use generous line height and clean spacing.
- No negative letter spacing.

## Interaction Rules

- Source cards open links in a new tab.
- Textareas should be large enough for real answers.
- Save answers to localStorage with a stable page-specific key.
- Export answers as JSON.
- Status text should show unsaved, saved, or restored state.

## Content Density Rules

- Sources: 6-10 entries when available.
- Summaries: each source cluster should include concise synthesis.
- Themes: 1-2 only.
- Deep question: one main question with strong support text.
- Product analysis: concrete modules for 产品表现 / 市场需求 / 产品价值.
- Insights: each insight includes detail, evidence, and practical action.
- Reflection prompts: each includes a hint that pushes evidence, tradeoffs, metrics, or next validation.

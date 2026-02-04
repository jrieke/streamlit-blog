# AGENTS.md

Guidance for writing Streamlit blog posts with AI.

## Core principles (non-negotiable)

- Be brief, concrete, and to the point. Cut fluff.
- Keep it fun and a little whimsical. Light emojis are ok.
- Match Streamlit blog tone: friendly, practical, optimistic.
- Foster community and collaboration. Invite readers to share.
- Avoid salesy/corporate marketing language.

## What top posts do well

- Open with a crisp hook and a clear promise.
- Provide a concrete example or story early.
- Use tight sections and skimmable headings.
- Show real code and explain _why_ it works.
- Emphasize iteration, speed, and forward progress.
- Celebrate the community and real apps.

## Mandatory pre-write step (do not skip)

- **First: read this `AGENTS.md` file.**  
  This is required. Do not write anything until this file has been read.
- **Then: find related posts via `article_index.jsonl`.**  
  Use it to identify related topics and check ratings to prioritize the best
  examples. Prefer higher-rated posts, but read all clearly related ones.
- **Then: read those articles from `articles/` as input.**  
  Always read the full Markdown files of the related posts before drafting.
  Err on the side of reading _more_ related posts rather than too few.

## Structure template (recommended)

1. **Hook (1–3 sentences)**  
   State the problem and the payoff. Be human.
2. **What you’ll build / learn (bullets)**  
   3–5 items, action verbs.
3. **Quick context**  
   One short paragraph to align on the “why.”
4. **Steps / sections**  
   Each section answers one question. Use code + visuals.
5. **Outro**  
   Invite community input + CTA + "Happy Streamlit-ing!" sign off (see variations below).

## Writing style

- Short paragraphs (2–4 lines).
- Prefer active voice.
- Use bold for key takeaways sparingly.
- Use emojis for warmth, not decoration.
- Prefer “you” and “we” over “users” and “customers.”
- Avoid hype words: “revolutionary,” “game-changing,” “enterprise-grade.”

## Technical depth

- Give enough detail to reproduce the build.
- Use minimal, focused code blocks.
- Explain tradeoffs and edge cases briefly.
- Include performance or reliability tips when relevant.

## Streamlit-specific guidance

- Lead with interactivity and iteration speed.
- Use Streamlit-native APIs first.
- Favor readable, declarative examples.
- Show patterns that scale: `st.session_state`, caching, modular code.
- If charts are needed: prefer `st.line_chart`, `st.bar_chart`, `st.scatter_chart`; use Altair when necessary.
- When using tables: show `st.dataframe` with proper `column_config`, `hide_index=True`, and `use_container_width=True` if wide.
- Use `st.divider()` for section breaks (not markdown `---`).
- If multi-page: mention `st.navigation`, `app_pages/`, and shared state in `st.session_state`.

## Community tone cues

- Include a “try the app / repo” link near the top.
- Call out community work and credit collaborators.
- Invite readers to share builds, ideas, or feedback.

## Brand voice and style (from guidelines)

- Lean into **useful + toy-like**: solve real problems, but feel playful.
- Aim for **superpower** energy: frictionless, magical, no waiting.
- Focus on **clarity, minimalism, polish**; prefer typography over visuals.
- Avoid borders, shadows, and boxed layouts; use whitespace.
- Use emojis sparingly and with purpose (joy in otherwise annoying moments).
- Use magic metaphors lightly: spellbook, sorcerer, wizard-in-training.
- Keep tone craftsperson-like: precise, elegant, high standards.
- Emphasize empowering others and community momentum.

## Brand language and phrases (optional sprinkle)

- Useful and toy-like
- Superpower
- Spellbook / spells
- Streamlit Creator / Streamlit Sorcerer
- You can BUILD and you can SHARE

## Greetings and sign-offs (optional)

- Hey Streamlit fam! 👋
- Hey Community! 👋
- Happy Streamlit-ing! ❤️
- We can't wait to see what you build and share! 🎈
- Tada! It's just that easy.
- In a snap you have an app!
- That's how you streamline it with Streamlit!

## Punctuation and title rules (strict)

- Titles/subtitles must not end with a period.
- If a sentence ends with an emoji, put punctuation before the emoji.

## SEO and content hygiene (practical only)

- Make the article SEO-friendly by default (clear intent, scannable structure).
- Use active voice.
- Keep copy concise and skimmable; focus on clarity over word count.
- Use clear header structure: one H1, then H2/H3 as needed.
- Place target keywords naturally in the H1 and key headers; avoid keyword stuffing.
- Write an SEO title tag (55–68 chars) and meta description (155–165 chars) when asked.
- Include a short 40–60 word synopsis early when it fits (featured snippet friendly).
- Always include a clear CTA (demo link, repo link, “see it in action,” etc.).
- Use short, descriptive, keyword-forward URLs (3–5 words, hyphens, lowercase).
- Only use imagery if it serves a purpose; if used, include descriptive alt text.
- Add an internal link if there’s a clearly relevant Streamlit resource or prior post.

## Common pitfalls to avoid

- Overlong background or history.
- Giant code dumps without explanation.
- Corporate/product announcements disguised as tutorials.
- Overpromising without concrete steps.
- Ignoring limitations, costs, or failure modes.

## Final checklist

- Hook is crisp and specific.
- Steps are skimmable and actionable.
- Tone is friendly and lightly playful.
- Community invite is present.
- No salesy phrasing.
- CTA is clear.

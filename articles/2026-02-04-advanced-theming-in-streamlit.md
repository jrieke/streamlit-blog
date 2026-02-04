---
title: "Advanced theming is here"
subtitle: "More control over your app’s look and feel (still zero CSS required)"
date: 2026-02-04
authors:
  - "Johannes Rieke"
category: "Product"
---

If you’ve ever thought “I love Streamlit, but I want *my* app’s vibe,” this one’s for you. **Streamlit 1.44** ships **advanced theming**: a bigger, more expressive set of theming options in `.streamlit/config.toml`.

👉 Fastest way to try it: add a `.streamlit/config.toml`, tweak a few keys, and rerun your app.

For examples + the full option list: [Theming overview](https://docs.streamlit.io/develop/concepts/configuration/theming)

## What’s new in advanced theming

You can now:

- **Define separate light + dark themes** (`[theme.light]` and `[theme.dark]`) and let viewers switch in the Settings menu.
- **Theme the sidebar independently** (nearly everything has a `[theme.sidebar]` equivalent — plus light/dark variants).
- **Go beyond the “big 4” colors** with link/code text, code backgrounds, borders, and dataframe header colors.
- **Tune typography** with heading + code fonts, per-heading sizes/weights, and base font size/weight.
- **Set shape + structure** with border radius and widget borders.
- **Align charts with your brand** via categorical and sequential color scales for Plotly, Altair, and Vega-Lite.
- **Customize the basic palette** (red/orange/yellow/green/blue/violet/gray) used in places like colored Markdown text and sparklines.

If you want the full matrix (including what can/can’t be overridden per light/dark/sidebar), the docs have you covered:
[`config.toml` theme options](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#theme)

## A tiny example to get you started

Here’s a minimal “advanced” theme that shows the new shape/typography/sidebar split without turning this post into a novella:

```toml
# .streamlit/config.toml

[theme]
base = "dark"
primaryColor = "#7C3AED"
linkUnderline = false
baseRadius = "large"
baseFontSize = 16
baseFontWeight = 400

[theme.dark.sidebar]
backgroundColor = "#0B0F19"
secondaryBackgroundColor = "#111827"
borderColor = "#1F2937"
```

Want to inherit from Streamlit’s light/dark themes *or* pull a theme from a local file/URL and then override just a few keys? That’s supported too — see `theme.base` in the docs.

## Demos you can steal (politely)

The theming docs include a couple of fun, polished examples you can use as starting points:

- Anthropic-inspired light theme: `https://doc-theming-overview-anthropic-light-inspired.streamlit.app/`
- Spotify-inspired dark theme: `https://doc-theming-overview-spotify-inspired.streamlit.app/`

## One pro tip for faster iteration

Most theming changes show up as soon as you save `config.toml` and rerun. A few options (like custom `fontFaces`) may require a full server restart — if something looks “stuck,” stop `streamlit run` and start it again.

---

If you build a great theme (or a small “theme pack” your team uses across apps), share it on the [Streamlit forum](https://discuss.streamlit.io). We’d love to see what you make.

Happy Streamlit-ing! 🎨

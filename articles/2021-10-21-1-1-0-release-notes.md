---
title: "1.1.0 release notes"
subtitle: "This release launches memory improvements and semantic versioning"
date: 2021-10-21
authors:
  - "Johannes Rieke"
category: "Release Notes"
---

![1.1.0 release notes](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--12-.svg)


Hey, Streamlit community! 👋

Say hello to some sweet improvements around memory usage and the introduction of semantic versioning!

## 🧠 **Memory improvements**

Ever had a Streamlit app use too much memory? Rejoice! We made [some important changes](https://github.com/streamlit/streamlit/pull/3879?ref=streamlit.ghost.io) to shrink memory usage. This affects **all Streamlit apps**, especially the ones that have run for long periods of time and have many viewers. This change also prevents many resource-limit errors on Streamlit Cloud (the "Argh" error page you might've seen here and there) and builds on top of other memory improvements from [version 0.82.0](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io#version-0820).

For example, here is one of our internal Streamlit app's memory usage. The colored lines on the left are using older Streamlit versions. The blue line on the right is using the 1.1.0 release.

![memory-usage-4](https://streamlit.ghost.io/content/images/2021/10/memory-usage-4.png#browser)

Update the Streamlit version of all your apps on [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io#plans-table) to 1.1.0 to enjoy these improvements!

## 🧬 **Semantic versioning**

With the recent release of Streamlit 1.0, we’re also committing to following a loose variant of [semantic versioning](https://semver.org/?ref=streamlit.ghost.io). This fulfills our promise to keep the API stable so you can confidently build production-quality apps.

* All changes introduced in minor versions will be additive. Breaking changes will only be introduced in major versions, while patch releases will be for bug fixes.
* Whenever possible, a deprecation path will be provided rather than an outright breaking change. We’ll introduce deprecations in minor versions.

There are a few caveats, though:

* Features released with the `experimental_` prefix are excluded from semantic versioning because they’re prototype features that need community input and iteration.
* `st.session_state` has a few minor issues left. While we're working on resolving them, this feature might see some updates outside semantic versioning in the next quarter.
* UI changes are not considered breaking changes as long as apps still work.
* Changes to CSS class names are not considered breaking changes.

## 🎒 **Other notable updates**

* ♻️ Apps now automatically rerun when the content of `secrets.toml` changes. Before this, you had to refresh the page manually.
* 🔗 We redirected documentation links (e.g., in exceptions) to our [brand-new docs site](https://docs.streamlit.io/?ref=streamlit.ghost.io).
* 🐛 Bug fix: Range slider can now be initialized with the session state API ([#3586](https://github.com/streamlit/streamlit/issues/3586?ref=streamlit.ghost.io))
* 🐞 Bug fix: Charts now automatically refresh when using `add_rows` with `datetime` index ([#3653](https://github.com/streamlit/streamlit/issues/3653?ref=streamlit.ghost.io))

## 🏁 **Wrapping up**

Thanks for checking out the release notes for 1.1.0. You can always see the most recent updates on our [changelog](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io) or via [this tag on the forum](https://discuss.streamlit.io/tag/release-notes?ref=streamlit.ghost.io).

Let us know in the comments below if you have any questions. We're looking forward to hearing what you think about this release!

Happy Streamlit-ing. 🎈

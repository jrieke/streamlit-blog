---
title: "Announcing the Figma-to-Streamlit plugin \ud83c\udfa8"
subtitle: "Go from prototype to code as easy as 1-2-3 with our new community resource!"
date: 2022-11-01
authors:
  - "Krista Muir"
category: "Product"
---

![Announcing the Figma-to-Streamlit plugin 🎨](https://streamlit.ghost.io/content/images/size/w2000/2022/10/Announcement-2.svg)


Hi Streamlit and Figma lovers! 👋🏻

My name is Juan, and I’m a designer and developer here at Streamlit. Remember last week we shared with you our [Streamlit Design System in Figma](https://www.figma.com/community/file/1166786573904778097?ref=streamlit.ghost.io)? Today, I want to unveil…

Our complementary [Figma plugin](https://www.figma.com/community/plugin/1167469184805790690/Figma-to-Streamlit?ref=streamlit.ghost.io)!

Prototype *and* code your apps easier than ever by turning components into code automatically, without leaving Figma. Pretty awesome, right?

In this post, you’ll learn:

* How to install the plugin
* How to use it
* How to contribute to the plugin’s development

Want to check it out right away? Head on to [our community profile](https://www.figma.com/@streamlit?ref=streamlit.ghost.io) and give it a try. Or strap yourself in and follow along with me!

**NOTE:** This is an experiment from our design team. We’re releasing it early to get your feedback, so there’s [still stuff missing](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#roadmap). If you find it useful, please [contribute!](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#contributing)

## How to install the plugin

Installing the plugin is super easy. Just follow these steps:

1. Go to our [Figma community profile](https://www.figma.com/@streamlit?ref=streamlit.ghost.io), open the plugin, and hit `Try it out`.
2. Go to Figma and run it from the `Plugins` tab.

## How to use it

As mentioned above, this plugin is complementary to our [Streamlit Design System](https://www.figma.com/community/file/1166786573904778097?ref=streamlit.ghost.io). Drag and drop a component, tweak its props and values, hit `See my code`, and get a code snippet to use in your app!

Need help creating an app to test the code? Check out our docs on [Getting started](https://docs.streamlit.io/library/get-started?ref=streamlit.ghost.io) or use Yuichiro Tachibana’s amazing [stlite sharing template](https://edit.share.stlite.net/?sampleAppId=template&ref=streamlit.ghost.io). Just copy the plugin’s snippet, paste it into the code editor on the left, and click `💾 Save`. The app on the right will update and show the generated output automagically!

Here is what it’ll look like:

[![](https://img.spacergif.org/v1/2558x1054/0a/spacer.png)](https://streamlit.ghost.io/content/media/2022/10/Intro.mp4)

0:00

/

1×

Last but not least, if you need a refresher on how to use our Design System library to prototype your app, make sure to check out [last week’s post](https://streamlit.ghost.io/prototype-your-app-in-figma/)! And if you have any issues, check out our [troubleshooting section](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#troubleshooting) on GitHub.

**NOTE:** If you need a refresher on how to use our Design System to prototype your app, check out [this post](https://streamlit.ghost.io/prototype-your-app-in-figma/). And if you have any issues, read our [troubleshooting section](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#troubleshooting) on GitHub.

## How to contribute to the plugin’s development

This plugin is an experiment, which means we’re still developing it.

As of this writing, it supports:

* [Text elements](https://docs.streamlit.io/library/api-reference/text?ref=streamlit.ghost.io) (except for `st.latex` and `st.markdown`)
* [Input widgets](https://docs.streamlit.io/library/api-reference/widgets?ref=streamlit.ghost.io) (except for `st.select_slider`)
* [Native Chart elements](https://docs.streamlit.io/library/api-reference/charts?ref=streamlit.ghost.io) (`st.line_chart`, `st.bar_chart`, and `st.area_chart`)

In the future, we plan to have it support:

* More widgets: [Media elements](https://docs.streamlit.io/library/api-reference/media?ref=streamlit.ghost.io), [Progress and Status](https://docs.streamlit.io/library/api-reference/status?ref=streamlit.ghost.io), [Data display elements](https://docs.streamlit.io/library/api-reference/data?ref=streamlit.ghost.io), [Layout and Containers](https://docs.streamlit.io/library/api-reference/layout?ref=streamlit.ghost.io), and [Control flow](https://docs.streamlit.io/library/api-reference/control-flow?ref=streamlit.ghost.io).
* More variants/features: recognizing **bold**, *italic* and ~~strikethrough~~ formatting; `label_visibility` on input widgets; optional properties and global page configuration; plugin settings to tweak the code output to better suit your needs.
* Internal improvements: code refactoring, type annotations, automatic data import, example callbacks, and more!

Want to help us out with the plugin’s development? See the [instructions](https://github.com/streamlit/figma-to-streamlit/blob/main/README.md?ref=streamlit.ghost.io#contributing) on how to contribute to the codebase. Thank you! 🙏

### **Wrapping up**

That’s pretty much it, folks.

We hope you enjoy playing with this [new plugin](https://www.figma.com/community/plugin/1167469184805790690/Figma-to-Streamlit?ref=streamlit.ghost.io). If you find any errors or have any ideas on how to improve it, please [file an issue](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#submitting-an-issue), and we’ll get back to you as soon as we can. Better yet, help us build those features yourself by [contributing to the codebase](https://github.com/streamlit/figma-to-streamlit?ref=streamlit.ghost.io#contributing).

Happy Figma-to-Streamlit-ing! 🎈

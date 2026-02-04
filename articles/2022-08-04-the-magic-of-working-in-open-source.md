---
title: "The magic of working in open source"
subtitle: "How we build our open-source library and release new features"
date: 2022-08-04
authors:
  - "Ken McGrady"
category: "Tutorials"
---

![The magic of working in open source](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image.svg)


Wondering what it’s like to work on the Streamlit open-source project? There are many reasons why we all love it. But the most exciting one is our focus on becoming *the best tool* in every data scientist’s toolchain.

Open source involves lots of stakeholders yet offers limited resources. So our biggest challenge is to prioritize and implement the most useful features.

In this post, you’ll learn:

* How we prioritize new features
* What goes into implementing new features
* How we keep in touch with the community
* How you can contribute to the open-source community

### How we prioritize new features

We prioritize new features every quarter:

* Our product team decides which features will evolve the product and its audience.
* Our engineering team builds solutions to GitHub issues.
* Our community team monitors our social channels and advocates for the community’s needs.

For example, these features took countless hours of brainstorming, prototyping, and testing: [multipage apps](https://streamlit.ghost.io/introducing-multipage-apps/), [new caching primitives](https://streamlit.ghost.io/new-experimental-primitives-for-caching/), [camera input](https://docs.streamlit.io/library/api-reference/widgets/st.camera_input?ref=streamlit.ghost.io), and [updated dataframes](https://discuss.streamlit.io/t/new-st-dataframe-based-on-glide-data-grid/26660?ref=streamlit.ghost.io).

In between the larger features, we tackle small delightful experiences, fix bugs, improve built-in charts, and add parameters to our APIs (tooltips, gap sizes, disabled widgets, etc.).

### What goes into implementing new features

Before we start working on a new feature, we talk to our Data Science team and [Streamlit Creators](https://streamlit.io/creators?ref=streamlit.ghost.io). Together, we decide which feature has the right amount of complexity and the most intuitive API (though there’s rarely a single solution for everyone’s use case).

A feature typically starts out as a simple “couple-of-lines change” that grows into a discussion on how it’ll impact the users, how it could be misused, and if it’ll keep our software resilient. We sort through lots of community feedback before finally pulling the trigger.

Once we build and release the feature, we move forward *super-fast* by:

* Unit-testing it to narrow down bugs in code;
* End-to-end testing to test the full functionality of a feature;
* And screenshot-testing it to make the visuals pixel-perfect.

From an engineering standpoint, we try to not break our API while [keeping a semantic versioning promise](https://streamlit.ghost.io/announcing-streamlit-1-0/). We work with our product and design teams to give our users the best experience by looking at the common data use cases and designing solutions that have room for change. Plus, all external contributors' code gets assigned a code reviewer. Often we assign *two* code reviewers because we’re not familiar with the context!

If you’re curious to learn more about how we implement new features, check out these posts:

* [How to enhance Google Search Console data exports with Streamlit](https://streamlit.ghost.io/how-to-enhance-google-search-console-data-exports-with-streamlit/)
* [How Streamlit uses Streamlit: sharing contextual apps](https://streamlit.ghost.io/how-streamlit-uses-streamlit-sharing-contextual-apps/)
* [New experimental primitives for caching](https://streamlit.ghost.io/new-experimental-primitives-for-caching/)
* [Announcing theming for Streamlit apps!](https://streamlit.ghost.io/introducing-theming/)

### How we keep in touch with the community

It can be a challenge for engineers to balance delivering features and talking to the community. We want to deliver our code on time, so our community conversations have a “context switching” tax. Our focus tends to be more on *the quality* of our product and less on the use cases, so our attention goes to the [GitHub issues](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io) and [bugs](https://github.com/streamlit/streamlit/issues?q=is%3Aopen+is%3Aissue+label%3Abug&ref=streamlit.ghost.io). We try to understand the issue, reliably reproduce it, and guesstimate its impact. Often, due to timing, we can’t fix the bug, but we get enough knowledge to help an external contributor solve the problem.

But we’re out there:

* Our Engineering team posts release notes and responds to many posts on the forum.
* Our Data Science team always has new ideas based on their Streamlit dogfooding.
* Our Developer Relations team works with the community to produce rich content like [30 days of Streamlit](https://streamlit.ghost.io/30-days-of-streamlit/).

We’re now part of Snowflake, and Snowflake’s mission is to mobilize the world’s data. Our community plays a big role in it. We believe in the [full-employment theorem](https://en.wikipedia.org/wiki/Full-employment_theorem?ref=streamlit.ghost.io) so we can *always* make Streamlit a better product for data scientists!

### How you can contribute to the open-source community

Contributing to the open-source community is very rewarding. The software is free. And you can improve a single function or a whole discipline! But getting involved may seem daunting as most conversations are asynchronous. It takes time, patience, and fortitude.

If you want to get involved and help us make a stronger product, we’d love for you to do so! Here is how to get started:

* [Use Streamlit](https://docs.streamlit.io/library/get-started?ref=streamlit.ghost.io)! Building software requires domain experience. Read more about [Streamlit’s main concepts](https://docs.streamlit.io/library/get-started/main-concepts?ref=streamlit.ghost.io).
* [File bugs if you see them](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io). Implement small, reliable, reproducible cases, and include as many details as possible. Many issues take time to understand because messages get lost in translation.
* [Help the community](https://discuss.streamlit.io/?ref=streamlit.ghost.io). Simple explanations help people understand Streamlit better. Better yet, turn it into content (for example, a [YouTube channel](https://www.youtube.com/c/FaniloAndrianasolo?ref=streamlit.ghost.io) or a [Medium blog](https://giswqs.medium.com/?ref=streamlit.ghost.io).)
* [Improve our documentation](https://docs.streamlit.io/?ref=streamlit.ghost.io). We have amazing documentation and we value your input!
* [Share your apps](https://discuss.streamlit.io/c/streamlit-examples/9?ref=streamlit.ghost.io) on the forum and social!

Spend a month or two focused on the above—it’ll clarify for you how to help out in code. When ready, [follow our contributing guidelines](https://github.com/streamlit/streamlit/wiki/Contributing?ref=streamlit.ghost.io) and take on a [bug from our GitHub issues](https://github.com/streamlit/streamlit/issues?q=is%3Aopen+is%3Aissue+label%3Abug&ref=streamlit.ghost.io). Bugs are understandable, reproducible, and have a desired outcome. We identified some [good first issues](https://github.com/streamlit/streamlit/issues?q=is%3Aopen+is%3Aissue+label%3Abug+label%3A%22good+first+issue%22&ref=streamlit.ghost.io), but there are many more to choose from.

And finally, follow good software engineering practices in designing your solution and write tests (it saves the first comment in a code review). 🧑‍💻

### Does this make you excited?

Want to work on open source as a job? Join our team! Our jobs require a unique skill set because Streamlit’s main value is delivering a clean and interactive user interface for developers, so we rely on strong frontend skills with TypeScript/React. And our developers interface with Streamlit using a simple Python API and server.

Here are our current job openings:

* [Senior Software Engineer](https://careers.snowflake.com/us/en/job/6262618002/Software-Engineer-Streamlit?ref=streamlit.ghost.io) and [Senior Product Manager](https://careers.snowflake.com/us/en/job/6276477002?gh_jid=6276477002&ref=streamlit.ghost.io) on our Open Source team.
* [Software Engineer](https://careers.snowflake.com/us/en/job/6192257002/Software-Engineer-Streamlit-Community-Cloud?ref=streamlit.ghost.io) on our Community Cloud team (if you have experience building full-stack services in the cloud).

Thank you for being part of our community. If you have questions, please post them in the comments below, and you may see them answered in future blog posts. 😉

Happy coding! 🎈

---
title: "AppTest: test & build interactive Python data apps faster"
subtitle: "A native framework for automated app testing"
date: 2023-10-31
authors:
  - "Joshua Carroll"
category: "Product"
---

![Introducing AppTest: a faster way to build quality Streamlit apps](https://streamlit.ghost.io/content/images/size/w2000/2023/10/Announcement-2.svg)


Every data app builder wants to build a flawless app in record time, but speed and quality may feel at odds with each other. Imagine pouring your heart into coding a beautiful new Python app, eager to share it with the world. However, before you can deploy, you can’t rush testing, else you’ll risk a code error tarnishing your app experience.

We've heard your pain and felt this ourselves. In practice, you probably do some manual sanity tests of your app changes and hope for the best. Yesterday’s automated test options are usually complex and hard to maintain:

* Conduct unit tests on the backend logic by factoring it out from the UI
* Set up a heavyweight browser testing framework like Selenium, Playwright, or Cypress for end-to-end testing

Luckily, you don’t have to live in this reality anymore. You can develop faster and ensure high quality!

![A diagram demonstrating how with automated testing you can enjoy faster development and a high quality result](https://streamlit.ghost.io/content/images/2023/10/horse-meme.png)

## Introducing: AppTest

AppTest is a new automated way to write and execute tests natively in Streamlit. Developers can use this API to confirm that all aspects of their app are working correctly.

With this automated testing framework you can:

**Code with confidence:** Run all your tests with a single command with Pytest. You no longer need to factor out your unit testable code or do extensive manual testing. Dealing with heavy end-to-end testing frameworks can be a thing of the past.

**Collaborate seamlessly**: Build apps with your team without worrying about breaking existing workflows. By connecting Streamlit to tools like GitHub Actions you can build a continuous integration pipeline that automatically runs tests after each commit.

**Feel more comfortable with complexity.** Go beyond prototypes and build more powerful apps to take your data apps to the next level.

Simple, powerful, and all in Python. 💪

### How AppTest works

Now you can test each feature, interaction, or app logic headlessly via API. By headlessly, we mean that you can test the result without having to preview in the browser.  You can use the API reference [docs](https://docs.streamlit.io/library/api-reference/app-testing?ref=streamlit.ghost.io) to build out different scenarios you want to test.

When you are ready, test everything with Pytest, locally and/or with GitHub Actions. View the results that will confirm that your features are all working correctly (or not).

![An example of the App test API running a test and showing the results](https://streamlit.ghost.io/content/images/2023/10/Screenshot-2023-10-25-at-2.59.51-PM-1.png)

## AppTest in action

Watch the video below to take a tour of AppTest. In the demo video we will cover:

* Simple example - writing tests as you build your app
* [Reference API overview](https://docs.streamlit.io/library/api-reference/app-testing?ref=streamlit.ghost.io)
* Examples from [Sophisticated Palette](https://sophisticated-palette.streamlit.app/?ref=streamlit.ghost.io) and [LLM-Examples](https://llm-examples.streamlit.app/?ref=streamlit.ghost.io) apps
* Integrating with GitHub Actions

## Ready, set, test!

Start building and executing tests faster with AppTest to have more control over your app experiences. Check out the [docs](https://docs.streamlit.io/library/api-reference/app-testing?ref=streamlit.ghost.io) to get started.

### Show off what you have built!

Share a link to tests you built for your Community Cloud app and show them successfully running in GitHub Actions.

You can share an example by posting a link to your test file like [this](https://github.com/streamlit/llm-examples/blob/main/app_test.py?ref=streamlit.ghost.io), and then share a successful run in a link like [this](https://github.com/streamlit/llm-examples/actions/runs/6695654403/job/18191691777?ref=streamlit.ghost.io). To get started setting up GitHub Actions, take a look at [GitHub’s tutorial](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python?ref=streamlit.ghost.io) or use our [sample workflow file](https://github.com/streamlit/llm-examples/blob/main/.github/workflows/python-app.yml?ref=streamlit.ghost.io).

If you provide your email in the comment with the two links, we will send the first 10 examples a Streamlit t-shirt!

Happy Streamlit-ing 🎈

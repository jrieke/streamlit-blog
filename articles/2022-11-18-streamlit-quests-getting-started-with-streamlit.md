---
title: "Streamlit Quests: Getting started with Streamlit"
subtitle: "The guided path for learning Streamlit"
date: 2022-11-18
authors:
  - "Chanin Nantasenamat"
category: "Tutorials"
---

![Streamlit Quests: Getting started with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/11/streamlit-quests-1.svg)


Streamlit is a Python library that makes building beautiful, interactive apps in a few lines of code easy. But every new library has its quirks and conventions, and it takes time to learn. You might be wondering where to start and if there are any resources. No worries. I got you covered!

Let’s learn Streamlit with this guide called **Streamlit Quests**. It’s inspired by role-playing games where players navigate the landscape by completing a sequential set of tasks—*quests*.

## Two quests

Your learning journey will have two quests:

1. **👨‍💻 Expert Quest.** This is a sequential track. Learning starts as easy and gradually becomes more complex.
2. **🎈 Community Quest.** This is a non-sequential track. You can refer to these resources at any point in your journey.

The topics checklist below serves a dual purpose: a table of contents and a to-do checklist that you can refer to at any time (think of it as your compass in your learning journey of Streamlit):

|  |  |  |
| --- | --- | --- |
| ▢ |  | Install Streamlit **👨‍💻** |
| ▢ |  | Run the demo app via `streamlit hello` **👨‍💻** |
| ▢ |  | Create a [single-page app](https://docs.streamlit.io/library/get-started/create-an-app?ref=streamlit.ghost.io) **👨‍💻** |
| ▢ |  | Use the [Streamlit App Starter Kit](github.com/streamlit/app-starter-kit) to quickly build a single-page app **🎈** |
| ▢ |  | Read the Documentation for specific information on Streamlit commands at `https://docs.streamlit.io` **🎈** |
| ▢ |  | Complete the `#30DaysOfStreamlit` challenge at `https://30days.streamlit.app` (the first three weeks are beginner-friendly, while the last week is more advanced) **👨‍💻** |
| ▢ |  | Get inspiration by exploring Streamlit apps in the Gallery at `https://streamlit.io/gallery` **🎈** |
| ▢ |  | Use or create Streamlit Components (third-party modules that extend Streamlit functionality) at `https://streamlit.io/components` **👨‍💻** |
| ▢ |  | Explore hundreds of components from the [Streamlit Components Hub](https://components.streamlit.app/?ref=streamlit.ghost.io) **🎈** |
| ▢ |  | Create a [multipage app](https://docs.streamlit.io/library/get-started/multipage-apps?ref=streamlit.ghost.io) **👨‍💻** |
| ▢ |  | Use the [Streamlit Multipage App Starter Kit](https://github.com/dataprofessor/multipage-app-starter-kit?ref=streamlit.ghost.io) to quickly build a multipage app **🎈** |
| ▢ |  | Deploy a Streamlit app on Streamlit Community Cloud at `https://streamlit.io/cloud` **👨‍💻** |
| ▢ |  | Share your Streamlit app on Twitter/LinkedIn and tag us `@streamlit` **🎈** |
| ▢ |  | Get unstuck by asking the forum at `https://discuss.streamlit.io` **🎈** |
| ▢ |  | Read our blog to stay updated on the latest developments and use cases at `https://blog.streamlit.io` **🎈** |

👉

NOTE: Emojis at the end of each task mark tasks as part of the Expert or the Community Quest.

Let’s get started!

## Install Streamlit

The simplest way to install Streamlit is by using `pip`. Just type the following into the command line:

```
pip install streamlit
```

## Run the demo app

After installing Streamlit, run the demo app by typing the following into the command line:

```
streamlit hello
```

In a few moments, a new browser should launch, displaying the following demo app:

![streamlit-demo-app-1](https://streamlit.ghost.io/content/images/2022/11/streamlit-demo-app-1.gif#browser)

It showcases a wide range of Streamlit functionalities to show you what you can build.

## Create a single-page app

In most cases, a basic app that performs a new task could be performed by a [single-page app](https://docs.streamlit.io/library/get-started/create-an-app?ref=streamlit.ghost.io). Conceptually, the app has a single page that’s sitting in the `streamlit_app.py` file.

Learn how to build a [single-page app](https://docs.streamlit.io/library/get-started/create-an-app?ref=streamlit.ghost.io) in [this article](https://docs.streamlit.io/library/get-started/create-an-app?ref=streamlit.ghost.io).

Or better yet…

## Use the Streamlit App Starter Kit

Use the starter code from the [Streamlit App Starter Kit](https://github.com/streamlit/app-starter-kit?ref=streamlit.ghost.io) to get a template app up and running in just a few minutes (learn how in [this article](https://streamlit.ghost.io/streamlit-app-starter-kit-how-to-build-apps-faster/)).

## Read the Documentation

In-depth coverage of every Streamlit command, along with code examples, is provided in the Streamlit Documentation at `https://docs.streamlit.io`. There are also Getting Started articles, cheat sheets, tutorials, and knowledge base articles. In addition to coverage of the Streamlit library, there’s also content on the Streamlit Community Cloud.

When building Streamlit apps, I keep the Documentation handy for quick and easy reference. I can always find a suitable Streamlit command or code examples to repurpose for my apps.

## Complete the `#30DaysOfStreamlit` challenge

30 Days of Streamlit helps new users learn the Streamlit library. We launched it on April 1, 2022, releasing a new challenge daily (with three difficulty levels). Then we compiled them all into a public app `https://30days.streamlitapp.com`.

The app encourages you to share your progress with the community by posting it on Twitter or LinkedIn with the hashtag `#30DaysOfStreamlit` or by tagging `@streamlit` (so we can retweet it). It’s now available in Portuguese, French, Spanish, and Russian.

Want to help translate it into your language? Go to `https://github.com/streamlit/30days` to get started.

## Get inspiration by exploring Streamlit apps in the Gallery

The Streamlit Gallery (available at `https://streamlit.io/gallery`) is a collection of the best apps built with our framework. Here you can find inspiration for your next app by browsing through the apps or learning how to build a particular type of app by looking at their code. The apps are categorized by topic: science and technology, finance and business, data visualization, etc.

## Use or create Streamlit Components

Streamlit components are third-party modules that extend Streamlit’s functionality of Streamlit. A curated collection is provided at `https://streamlit.io/components`.

To use a Streamlit component such as AgGrid:

1.  Install via `pip` as follows:

```
pip install streamlit-aggrid
```

2.  Use in a Streamlit app by simply importing the component and using its function:

```
from st_aggrid import AgGrid

AgGrid(my_dataframe)
```

To create your own Streamlit component, refer to some of these excellent articles:

* [How to build your own Streamlit component: Learn how to make a component from scratch!](https://streamlit.ghost.io/how-to-build-your-own-streamlit-component/)
* [Introducing Streamlit Components: A new way to add and share custom functionality for Streamlit apps](https://streamlit.ghost.io/introducing-streamlit-components/)
* Documentation on [Custom Components](https://docs.streamlit.io/library/components?ref=streamlit.ghost.io) (contains additional information on creating and publishing components as well as the components API)
* [Streamlit Components, security, and a five-month quest to ship a single line of code](https://streamlit.ghost.io/streamlit-components-security-and-a-five-month-quest-to-ship-a-single-line-of-code/)

And check out this 2-part tutorial video series:

1. [How to build a Streamlit component - Part 1: Setup and architecture](https://youtu.be/BuD3gILJW-Q?ref=streamlit.ghost.io)
2. [How to build a Streamlit component - Part 2: Make a slider widget](https://youtu.be/QjccJl_7Jco?ref=streamlit.ghost.io)

## Create a multipage app

A more complex app may require several pages. As a result, you might want to look into building a [multipage app](https://docs.streamlit.io/library/get-started/multipage-apps?ref=streamlit.ghost.io). The app consists of two major components:

1. The main page that serves as the entry point of the multipage app.
2. One of several pages that reside inside a `pages` folder is called upon when users click on the page of interest from the left sidebar panel.

Learn how to build a multipage app in [this article](https://docs.streamlit.io/library/get-started/multipage-apps?ref=streamlit.ghost.io).

## Use the Streamlit Multipage App Starter Kit

Just like with the Streamlit App Starter Kit for single-page apps, check out the fully functional early version of the [Streamlit Multipage App Starter](https://github.com/dataprofessor/multipage-app-starter-kit?ref=streamlit.ghost.io) (an article about this coming soon) to make a multipage app in no time.

## Deploy a Streamlit app on Streamlit Community Cloud

Let’s say you’ve already built your Streamlit app and want to share it with the community. You can share it by using Streamlit Community Cloud at `https://streamlit.io/cloud`.

To deploy to the Community Cloud:

1. Upload or Git-push app files to a GitHub repository
2. From within Community Cloud, click on “New app,” then select repo, branch, and app file.

That’s it! Once the app is up and running, share its uniquely generated URL with the community.

## Share your Streamlit app

Ready to share your Streamlit app creation with the community? Hop on [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io) or [LinkedIn](https://www.linkedin.com/company/streamlit?ref=streamlit.ghost.io) and tag us with `@streamlit`. It’s a great way to contribute to the community and receive helpful and constructive feedback for improving your app.

## Get unstuck by asking the forum

Are you encountering errors when creating Streamlit apps? To get unstuck, try the following:

1. Read the error logs displayed in the command line as apps load. These errors will tell you exactly why certain aspects of the app may fail to load or display. They will also hint at which dependent libraries may be the root of the problem.
2. Search Google, Stack Overflow, or the Streamlit Forum ( `https://discuss.streamlit.io`) to see if there are related posts that may already have a solution.
3. If you’ve done the above and are still stuck, post your question on the Streamlit Forum. See this article [How to post a question in the Streamlit forum](https://discuss.streamlit.io/t/how-to-post-a-question-in-the-streamlit-forum/30960?ref=streamlit.ghost.io) to craft a thoughtful and practical question.

## Read our blog to stay updated on the latest developments

Blog posts are a great way to stay updated on the latest developments and use cases, especially regarding the Streamlit web framework.

The Streamlit Blog (available at `https://blog.streamlit.io`) is home to 106 articles (as of this writing) that provide timely information on new features, product releases, and other news that can help you stay ahead of the curve. It also features guest posts from experts in the field, which can provide valuable insights into best practices and real-world applications as they share their first-hand experiences.

## Wrapping up

Congratulations! You’ve been acquainted with all the essential resources for building Streamlit apps. It’s time to take what you’ve learned and create something extraordinary!

If you have any questions, please leave them in the comments below or contact me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=streamlit.ghost.io) or on [LinkedIn](https://www.linkedin.com/in/chanin-nantasenamat/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

---
title: "pip vs. uv: How Streamlit Cloud sped up app load times by 55%"
subtitle: "After discovering a dependency installation bottleneck, we decided to try out Astral uv \u2013 the new pip drop-in replacement written in Rust."
date: 2024-07-11
authors:
  - "Antoni Kedracki"
category: "Product"
---

![pip vs. uv: How Streamlit Cloud sped up app load times by 55%](https://streamlit.ghost.io/content/images/size/w2000/2024/07/_Users_lacosta_Downloads_Announcement-20-3-.svg.png)


In engineering, faster is better. The faster you can set up your dependencies and test your code, the faster you can improve it. This tight iteration loop is the ultimate productivity goal, and speed is one of the core tenets of Streamlit.

The more sophisticated an app is, the more dependencies it will likely require. Manually installing dependencies wastes valuable engineering resources. This is why package managers exist.

The most popular package manager in Python is the “Preferred Installer Program” – otherwise known as “pip.” However, while pip may be the most popular package manager, it’s not always the fastest. That tool turned out to be uv.

When we switched from pip to uv package manager, **we sped up Streamlit Cloud app deployment time by 55%!**

In this blog, you’ll learn how we discovered the need for faster app load times, and ultimately why we chose uv vs. pip as Streamlit’s preferred package manager.

## Discovering the need for faster app load times

While working on Streamlit Community Cloud, we do quite a number of test deployments. Which means we spend a lot of time looking at the pastry loading animation. That’s when we realized: If *we* have to wait over 10 seconds, so do our users. 😨

So why was this lag happening? It all comes down to “cold deployments.”

During local development, you can use Streamlit’s ability to hot-reload which allows you to see changes in your code right away so you can iterate faster on your code. Streamlit uses a similar mechanism when updating apps running on Community Cloud. In both scenarios, all the app’s dependencies are already installed via pip and no additional package work is required. This allows the app to load changes quickly.

However, a lag occurs when a Streamlit app has “gone to sleep” and needs to be “woken up.” Waking a sleeping app requires a cold deployment. In a cold deployment, Streamlit Community Cloud performs additional work to provision an execution environment and perform an initial setup so the app can run. The result was long loading times.

A production ready app needs to be quick and reliable, so we knew we had to make cold deployments faster. What we *didn’t* know was where exactly the deployment bottlenecks were occurring. So – we started collecting metrics.

That’s when we discovered deployment slowed down significantly during dependency installation and – more importantly – that most of our users are using pip for Python dependencies.

In the beginning of April 2024:

* The average daily deployment time was about 90 seconds
* Installing dependencies took up the bulk of this time at an average of 60 seconds
* pip was used by 97% of all deployments

So we asked ourselves, “How can we make this faster?”

## What makes pip so slow? The tradeoff between stability and speed

Since its inception in 2008, pip has become the official and primary package manager for Python. It comes bundled with CPython and is relatively easy to use, making it the go-to-no-hassle solution.

Due to its popularity, pip needs to provide exceptional stability. As a result, speed is a secondary thought. In fact, since 2013, one of the oldest open issues for pip on GitHub centers around the need to download packages in parallel. Over the years, the main concern of pip has been how to make this deterministic without impacting the user experience.

Why does pip take so long to install required packages? The process can be divided into two main steps:

1. **pip determines which packages to download and install.** This means resolving the user provided dependency list to figure out what to download. (In the case of Streamlit, this leads to about 200 network calls of various sizes – including multi-megabyte downloads!)
2. **pip installs the necessary packages.** This involves unpacking them, placing them in the right location, and pre-compiling modules.

All of this is performed sequentially, on a single thread. You can probably already imagine how all these round-trip times (RTT), transfer times, and IO stack up – before you know it, minutes have passed and your app is still nowhere near ready!

This is the tradeoff between stability and speed. For Streamlit, speed is paramount, so we looked for an alternative.

## uv to the rescue

In April of 2024, we discovered the uv Python package manager by Astral. 💥

**What is the** [**uv package manager**](https://github.com/astral-sh/uv?ref=streamlit.ghost.io)**?** From their GitHub page, uv is “An extremely fast Python package installer and resolver, written in Rust. Designed as a drop-in replacement for common pip and pip-tools workflows.”

uv is so fast because it makes heavy use of parallelization, caching, and a number of other clever tricks.

For example, when deciding which packages to download and install, pip first downloads the dependency list for each package. For Python wheel packages, this list is in the metadata file. To access this metadata, pip has to download the *entire* wheel, even though only the metadata is needed.

uv approaches this differently. Because wheels are zip archives, uv queries **only** the index (also called the Central Directory) and uses file offsets contained within it to download just the metadata file. uv removes the unnecessary step of downloading entire Python wheels just to access the metadata file.

**So just how fast is uv?** [According to Astral](https://astral.sh/blog/uv?ref=streamlit.ghost.io), uv is 8-10 times faster than pip.

In mid-April 2024, we switched all users of pip on Streamlit Community Cloud to uv, resulting in the average dependency install time dropping from 60 to 20 seconds.

![A bar graph illustrating how both total deployment and dependency install times decreased once uv was introduced.](https://streamlit.ghost.io/content/images/2024/07/2024-04----Blog----uv-vs.-pip-install--3-.png)

A bar graph illustrating how both total deployment and dependency install times decreased once uv was introduced.

This meant that total average spin up times dropped 55% – from 90 to 40 seconds. Not bad I would say!

A video comparing a Streamlit app loading using pip on the left and uv on the right.

## Open source makes things faster

Improvements like the expedited package management uv provides are made possible by open source development. When everything's out in the open, everyone has the opportunity to contribute and help solve problems. We’re grateful for the developers of uv so we can offer our community faster app spin-up times!

If you are already a Streamlit Community Cloud user, no additional action is required to use uv.

For local development, you can start using uv today with the following:

1. Install uv according to the [uv documentation](https://pypi.org/project/uv/?ref=streamlit.ghost.io)
2. Use `uv pip install` instead of `pip install`

This is just the beginning when it comes to improving faster load times on Streamlit Community Cloud. Expect to see more improvements soon!

To learn more about using uv in your other Python projects, check out the [documentation](https://github.com/astral-sh/uv?ref=streamlit.ghost.io) and let us know what your experience is. You can always find out about what's new with Streamlit in the [release notes](https://docs.streamlit.io/develop/quick-reference/release-notes?ref=streamlit.ghost.io).

Happy (faster!) Streamlit-ing!

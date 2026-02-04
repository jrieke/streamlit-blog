---
title: "Introducing two new caching commands to replace st.cache!"
subtitle: "st.cache_data and st.cache_resource are here to make caching less complex and more performant"
date: 2023-02-14
authors:
  - "Tim Conkling"
category: "Product"
---

![Introducing two new caching commands to replace st.cache!](https://streamlit.ghost.io/content/images/size/w2000/2023/02/two-new-caching-commands.svg)


Caching is one of the most beloved *and* dreaded features of Streamlit. We understand why! `@st.cache` makes apps run faster—just slap it on top of a function, and its output will be cached for subsequent runs. But it comes with a lot of baggage: complicated exceptions, slow execution, and a [host of edge cases](https://github.com/streamlit/streamlit/issues?q=is%3Aopen+is%3Aissue+label%3Afeature%3Acache&ref=streamlit.ghost.io) that make it tricky to use. 😔

Today, we're excited to announce two new caching commands…

`st.cache_data` and `st.cache_resource`!

They're simpler and faster, and they will replace `st.cache` going forward! 👣

## What's the problem with `st.cache`?

We spent a lot of time investigating it and talking to users. Our verdict: `st.cache` tries to solve too many use cases!

The two main use cases are:

1. Caching data computations, e.g. when you transform a dataframe, compute NumPy arrays, or run an ML model.
2. Caching the initialization of shared resources, such as database connections or ML models.

These use cases require **very** different optimizations. One example:

* For (1), you want your cached object to be safe against mutations. Every time the function is used, the cache should return the same value, regardless of what your app does with it. That's why `st.cache` constantly checks if the cached object has changed. Cool! But also…slow.
* For (2), you definitely don't want these mutation checks. If you access a cached database connection many times throughout your app, checking for mutations will only slow it down without any benefit.

There are many more examples where `st.cache` tries to solve both scenarios but gets slow or throws exceptions. So in 2021, we decided to separate these use cases. We released two experimental caching commands, `st.experimental_memo` and `st.experimental_singleton`. They work similarly to `st.cache` and are optimized for (1) and (2), respectively. Their behavior worked great, but the names confused users (especially if they didn't know the underlying CS concepts of [memoization](https://en.wikipedia.org/wiki/Memoization?ref=streamlit.ghost.io) and [singleton](https://en.wikipedia.org/wiki/Singleton_pattern?ref=streamlit.ghost.io)).

## The solution: `st.cache_data` and `st.cache_resource`

Today, we're releasing our new solution for caching: `st.cache_data` and `st.cache_resource`. These commands have the same behavior as `st.experimental_memo` and `st.experimental_singleton` (with a few additions described below) but should be much easier to understand.

Using these new commands is super easy. Just add them as a decorator on top of the function you want to cache:

```
@st.cache_data
def long_running_function():
    return ...
```

Here's how to use them:

* `st.cache_data` is the recommended way to cache computations that return data: loading a DataFrame from CSV, transforming a NumPy array, querying an API, or any other function that returns a serializable data object (str, int, float, DataFrame, array, list, and so on). It creates a new copy of the return object at each function call, protecting it from [mutation and concurrency issues](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io#mutation-and-concurrency-issues). The behavior of `st.cache_data` is what you want in most cases—so if you're unsure, start with `st.cache_data` and see if it works!
* `st.cache_resource` is the recommended way to cache global resources such as ML models or database connections—unserializable objects that you don't want to load multiple times. By using it, you can share these resources across all reruns and sessions of an app without copying or duplication. Note that any mutations to the cached return value directly mutate the object in the cache.

## New documentation

Along with this release, we're launching a [brand new docs page](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io) for caching. 🚀 It explains in detail how to use both commands, what their parameters are, and how they work under the hood. We've included many examples to make it as close to real life as possible. If anything is unclear, please let us know in the comments. ❤️

## Additional features ✨

The behavior of the new commands is mostly the same as `st.experimental_memo` and `st.experimental_singleton`, but we also implemented some highly requested features:

* `st.cache_resource` now has a `ttl`—to expire cached objects.
* `st.cache_resource` got a `validate` parameter—to run a function that checks whether cached objects should be reused. Great for recreating expired database connections!
* `ttl` can now accept `timedelta` objects—instead of `ttl=604800` you can now write `ttl=timedelta(days=7)`.
* Last but not least: cached functions can now contain most Streamlit commands! This powerful feature allows you to cache entire parts of your UI. See details [here](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io#using-streamlit-commands-in-cached-functions).

## What will happen to `st.cache`?

Starting with 1.18.0, you'll get a deprecation warning if you use `st.cache`. We recommend you try the new commands the next time you build an app. They'll make your life easier and your apps faster. In most cases, it's as simple as changing a few words in your code. But we also know that many existing apps use `st.cache`, so we'll keep `st.cache` around, for now, to preserve backward compatibility. Read more in our [migration guide in the docs](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io#migrating-from-stcache).

We'll also be deprecating `st.experimental_memo` and `st.experimental_singleton`—as they were experimental. The good news is: their behavior is the same as the new commands, so you'll only need to replace *one name*.

## The future of caching

We'll continue to improve caching! The new commands will make it easier to use and understand. Plus, we have more features on our roadmap, such as limiting the amount of memory the cache can use or adding a cache visualizer right into your app.

Track our progress at [roadmap.streamlit.app](https://roadmap.streamlit.app/?ref=streamlit.ghost.io) and send us [feature requests on GitHub](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io). And if you have any questions or feedback, please leave them in the comments below.

Happy Streamlit-ing! 🎈

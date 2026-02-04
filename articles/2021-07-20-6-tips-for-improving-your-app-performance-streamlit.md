---
title: "6 Tips for Improving Your App Performance | Streamlit"
subtitle: "Moving your Streamlit app from analysis to production"
date: 2021-07-20
authors:
  - "Randy Zwitch"
category: "Tutorials"
---

![6 tips for improving your Streamlit app performance](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--13-.svg)


In the first two parts of this blog series ([part 1](https://streamlit.ghost.io/designing-streamlit-apps/), [part 2](https://streamlit.ghost.io/designing-streamlit-apps-for-the-user-part-ii/)), my colleague Abhi outlined principles for designing Streamlit apps from the perspective of the end user. From using wireframes before you start coding to adding contextual help, layout and theming features, designing for the intended user can take your app from being seldom used to being a key tool in your organization.

In this final part of the series, I’ll discuss some subtle *unseen-but-definitely-felt* user experience improvements that tune the performance of your Streamlit apps. And for most of this post we'll be focusing on apps that, at least in part, operate on static data (data that doesn't change). The tips are listed in order from easiest-to-implement to hardest-to-implement, and depending on the use case not all of them will apply to every Streamlit app.

## 1. Do you really need a million-value slider?

![screen-shot-2021-07-16-at-3.47.33-pm--1-](https://streamlit.ghost.io/content/images/2021/10/screen-shot-2021-07-16-at-3.47.33-pm--1-.png#border)

In the same way a line chart with 10,000 lines is visual overload, having a [slider](https://docs.streamlit.io/en/stable/api.html?ref=streamlit.ghost.io#streamlit.slider), [selectbox](https://docs.streamlit.io/en/stable/api.html?ref=streamlit.ghost.io#streamlit.selectbox), [multiselect](https://docs.streamlit.io/en/stable/api.html?ref=streamlit.ghost.io#streamlit.multiselect), or [select\_slider](https://docs.streamlit.io/en/stable/api.html?ref=streamlit.ghost.io#streamlit.select_slider) widget with 10,000 options is granularity overload: it would be nigh impossible to use, not to mention to understand each option.

But even worse, for most of those widgets, the more options you pass as input the more data needs to be sent from the Streamlit server to the Streamlit JavaScript frontend. This means more data needs to be serialized, sent over the network, and stored in the browser's memory. Take the following line of code:

```
price = st.selectbox("House Price", range(10000000))
```

In this toy example, all 10⁷ values will be converted to `str` and almost 100 megabytes sent over to the user's browser.

A less silly example would be a slider:

```
price = st.slider("House Price", 1, 10000000)
```

Due to implementation details, high-cardinality sliders don't suffer from the serialization and network transfer delays mentioned earlier, but they will still lead to a poor user experience (who needs to specify house prices up to the dollar?) and high memory usage. In my testing, the example above increased RAM usage by gigabytes until the web browser eventually gave up (though this is something that should be solvable on our end. We'll look into it!)

Suffice to say, performance *and* user experience will be much improved if you consider alternative means of interacting with apps of this kind, such as a using `st.number_input` or `st.text_input` to allow the user to enter arbitrary or high-granularity inputs. If you absolutely must use widgets that enumerate every value, choose a `step` size that gives the end user *at most* dozens of choices to pick from. Your users will thank you!

```
price = st.slider("House Price", 100000, 10000000, step=100000)
```

## 2. Pre-calculate inputs and cache whenever possible

When moving a Streamlit app to production, consider whether there are parts of the app that can be pre-calculated. If your app aggregates a 10-million-row dataframe by U.S. State, you can improve performance by [caching](https://docs.streamlit.io/en/stable/caching.html?ref=streamlit.ghost.io) that computation and only re-running it when needed:

```
@st.cache(ttl=24*60*60)  # Don't forget to add a TTL!
def get_data_by_state():
	return huge_df['US state'].unique()
```

Going further, if the data in question never changes, you can do this calculation beforehand outside of the app and save it as a file which you then load and [cache](https://docs.streamlit.io/en/stable/caching.html?ref=streamlit.ghost.io) when your app first starts:

```
@st.cache  # No need for TTL this time. It's static data :)
def get_data_by_state():
	return pd.read_csv(PRECALCULATED_DATA_PATH)
```

Creating a list on-the-fly by taking the unique value across a 10-million-row dataframe is always going to be reading the list directly from memory. So, for dynamic datasets, wrap your computation in an `@st.cache`  and set a large TTL. And for static datasets you should always consider offloading computations to a file, to constants, or to a separate Python modules.

## 3. Avoid downloading large, static models

![Screen-Shot-2021-07-16-at-4.14.55-PM](https://streamlit.ghost.io/content/images/2021/10/Screen-Shot-2021-07-16-at-4.14.55-PM.png#border)

In the [Streamlit Self-Driving Car demo](https://github.com/streamlit/demo-self-driving?ref=streamlit.ghost.io), we show a code pattern where we download the YOLOv3 object detection model from S3 all while using `st.progress` to keep the user informed while the download takes place. While this is a great pattern when sharing a model across multiple repos, it does put the app at the mercy of internet bandwidth when running in production: the YOLOv3 model is approximately 240MB, which can take several minutes to download before a user even has a chance to get started.

The solution is simple: when pushing your Streamlit app to production, bring your model and other assets to the production machine, and you can get orders-of-magnitude better startup time. For [Streamlit sharing](https://share.streamlit.io/?ref=streamlit.ghost.io) specifically, [Git LFS (Large File Storage)](https://git-lfs.github.com/?ref=streamlit.ghost.io) is supported, so you can use it to store your model in your GitHub repository and make it available to your app automatically. Couple that with reading a file from disk with `@st.cache` and app users may not even realize a model is being loaded in the background!

## 4. Remove unused data

When starting a data project, a common task is pulling data from a database or CSV file and exploring it interactively. If you haven't use Streamlit for this exploratory data analysis phase yet (EDA), you should give it a try — just use Streamlit's "[magic commands](https://docs.streamlit.io/en/stable/api.html?ref=streamlit.ghost.io#magic-commands)" and press Ctrl-S or Cmd-S to save the source file, and Streamlit shows updates live. This makes it easy to try numerous combinations of inputs and (hopefully!) find meaningful information in the data.

However, when moving the app to production, you are often *telling a story*, not searching for one. At this point, you usually know that your analysis only needs a handful of columns among the dozens in your dataset. In some cases, a dataset may have columns that can’t even be shared (personally-identifying information), that don't change (version numbers) or simply aren’t being used (user-agent strings).

So go ahead and remove those unnecessary columns and rows you aren’t using. Your data will get read in faster, use less RAM, and overall be more efficient when calculations are performed. To paraphrase a [computer-science saying](https://news.ycombinator.com/item?id=10979240&ref=streamlit.ghost.io#:~:text=Robert%20Galanakis%3A%20%E2%80%9CThe%20fastest%20code,code%20that%20was%20never%20written.%E2%80%9D), the fastest-loading data is the one you don't have to load!

## 5. Optimize data storage formats

If you’ve made it this far into the post, you probably have a pretty svelte app! Your input widgets are optimized to provide meaningful choices, these choices are coded as constants in your app, you’re not downloading large amounts of data over the internet unnecessarily and what data you are reading are only the rows and columns you need. But what if that’s not *fast enough?*

If you’re reading large amounts of data via CSV or JSON, consider using a binary-serialized format such as [Apache Parquet](https://www.upsolver.com/blog/apache-parquet-why-use?ref=streamlit.ghost.io) or [Apache Arrow IPC](https://arrow.apache.org/docs/python/ipc.html?ref=streamlit.ghost.io#ipc). While CSV and JSON are convenient formats for data transport, ultimately they are optimized for humans, not computers! By using an optimized data storage format, your production app won’t spend time parsing text into data types such as integers, floats and strings, which, incredibly, can consume quite a bit of time. Additionally, binary formats often have metadata and logical partitioning such that Python can read the metadata to find exactly where the data are located, skipping entire data partitions from loading.

## 6.  Use the right tool for the job!

While many of the common libraries in the PyData ecosystem have C or FORTRAN underpinnings, in the end, some problems are larger than a single computer can reasonably handle. For tabular data, there have been decades of research into performance optimization of relational databases. From indexing to multi-core query processing, moving your computation workflow from Python to a relational database could give considerable speed improvements.

Taking it a step further, for heavy workloads consider separating the Streamlit app from the computation portion, so that your computation can scale independently of the web app.  Specialized hardware such as GPUs, [Dask](https://dask.org/?ref=streamlit.ghost.io) or [Spark](https://spark.apache.org/?ref=streamlit.ghost.io) clusters and other higher-performance options are all ways to solve the largest data problems while still staying in the larger PyData ecosystem.

## Wrapping Up

How are you optimizing your Streamlit apps? This blog post highlights six ways to improve Streamlit app performance, but there are definitely dozens of other tips and tricks that aren’t covered here. What are your favorite optimization tricks? Are you using [Streamlit with databases](https://docs.streamlit.io/en/stable/tutorial/databases.html?ref=streamlit.ghost.io)? Stop by the [Streamlit Community forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io) and let us know what you’ve done to optimize your apps, and what else could be working better within Streamlit!

## Resources

* [Github](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)
* [Design Series Part 1](https://streamlit.ghost.io/designing-streamlit-apps/)
* [Design Series Part 2](https://streamlit.ghost.io/designing-streamlit-apps-for-the-user-part-ii/)

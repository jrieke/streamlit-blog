---
title: "New experimental primitives for caching (that make your app 10x faster!)"
subtitle: "Help us test the latest evolution of st.cache"
date: 2021-09-22
authors:
  - "Abhi Saini"
category: "Product"
---

![New experimental primitives for caching (that make your app 10x faster!)](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--6--2.svg)


Having trouble with `@st.cache`? You're not alone.

We've found that `@st.cache` is hard to use. You're either faced with cryptic errors like `InternalHashError` or `UnhashableTypeError`. Or you need to understand concepts like `hash_funcs` and `allow_output_mutation`.

Ouch.

But don't fret. We've got two new solutions for you: **st.experimental\_memo** and **st.experimental\_singleton**. It's conceptually simpler! And much, ***much*** faster. In some of our internal tests on caching large dataframes, `@st.experimental_memo` has outperformed `@st.cache` by an order of magnitude. That's over 10X faster! 🚀

Here is the summary of the post (TL;DR! 😉):

**Problem:** `@st.cache` tries to solve two different problems:

1. caching data
2. storing global objects (TensorFlow sessions, database connections, etc)

* As a result of `@st.cache` doing both those things, it's both slower *and* more complex (see: `hash_funcs`)

**Solution:** We have *two* experimental APIs, each of which solves a single problem:

* As a result, they are simpler and faster.
* If you're interested in trying this out, we recommend that you replace all uses of `@st.cache` with `@st.experimental_memo` and `@st.experimental_singleton`, as appropriate (see how below!).

**Which to use,** **memo or singleton?**

* `@st.experimental_memo` is the primary replacement for `@st.cache` and is for storing ***data***. If you're computing a value and you want to cache it, you almost always want memo. We expect it to be used more frequently. It's used for caching expensive computation that you don't want to run multiple times.
* `@st.experimental_singleton` is for storing *non-data objects*. If you have an object that is not the result of computation but is instead used to *implement* computation or other program logic, you probably want singleton.
* Another way of thinking about this: `@st.memo` is for stuff you might put in a database. `@st.singleton` is for stuff that doesn't make sense to put in a database.

Want to learn more details? Let's dive even deeper.

## **Problem**

First, we wanted to understand how `@st.cache` was being used in the wild. A detailed analysis of open-source Streamlit apps indicated that `@st.cache` was serving the following use-cases:

1. Storing computation results given different kinds of inputs. In Computer Science literature, this is called **memoization**.
2. Initializing an object exactly once, and reusing that same instance on each rerun for the Streamlit server's lifetime. This is called the **singleton pattern**.
3. Storing global state to be shared and modified across multiple Streamlit sessions (and, since Streamlit is threaded, you need to pay special attention to thread-safety).

This led us to wonder whether `@st.cache`'s complexity could be a product of it trying to cover too many use-cases under a single unified API.

To test out this hypothesis, today we are introducing two specialized Streamlit commands covering the most common use-cases above (singletons and memoization). We have used those commands ourselves to replace `@st.cache` in several Streamlit apps, and we're finding them truly amazing.

**We'd like to share them with all of you in our amazing community to try out these two commands and tell us what you think.** ❤️

## **Solution**

While `@st.cache` tries to solve two very different problems simultaneously (caching data and sharing global singleton objects), these new primitives simplify things by dividing the problem across two different APIs.

## **`@st.experimental_memo`**

Use this to store expensive computation which can be "cached" or "memoized" in the traditional sense. It has almost the exact same API as the existing `@st.cache`, so you can often blindly replace one for the other:

```
@st.experimental_memo
def factorial(n):
	if n < 1:
		return 1
	return n * factorial(n - 1)

f10 = factorial(10)
f9 = factorial(9)  # Returns instantly!
```

**Properties**

* Unlike `@st.cache`, this returns cached items by value, not by reference. This means that you no longer have to worry about accidentally mutating the items stored in the cache. Behind the scenes, this is done by using Python's `pickle()` function to serialize/deserialize cached values.
* Although this uses a custom hashing solution for generating cache keys (like `@st.cache`), it does ***not*** use `hash_funcs` as an escape hatch for unhashable parameters. Instead, we allow you to ignore unhashable parameters (e.g. database connections) by prefixing them with an underscore.

For example:

```
@st.experimental_memo
def get_page(_sessionmaker, page_size, page):
	"""Retrieve rows from the RNA database, and cache them.
	
	Parameters
	----------
	_sessionmaker : a SQLAlchemy session factory. Because this arg name is
	                prefixed with "_", it won't be hashed.
	page_size : the number of rows in a page of result
	page : the page number to retrieve
	
	Returns
	-------
	pandas.DataFrame
	A DataFrame containing the retrieved rows. Mutating it won't affect
	the cache.
	"""
	with _sessionmaker() as session:
		query = (
			session
				.query(RNA.id, RNA.seq_short, RNA.seq_long, RNA.len, RNA.upi)
				.order_by(RNA.id)
				.offset(page_size * page)
				.limit(page_size)
		)
		
		return pd.read_sql(query.statement, query.session.bind)
```

## **`@st.experimental_singleton`**

This is a key-value store that's shared across all sessions of a Streamlit app. It's great for storing heavyweight singleton objects across sessions (like TensorFlow/Torch/Keras sessions and/or database connections).

```
from sqlalchemy.orm import sessionmaker

@st.singleton
def get_db_sessionmaker():
	# This is for illustration purposes only
	DB_URL = "your-db-url"
	engine = create_engine(DB_URL)
	return sessionmaker(engine)

dbsm = get_db_sessionmaker()
```

How this compares to `@st.cache`:

* Like `@st.cache`, **this returns items by reference.**
* You can return any object type, including objects that are not serializable.
* Unlike `@st.cache`, this decorator does not have additional logic to check whether you are unexpectedly mutating the cached object. That logic was slow and produced confusing error messages. So, instead, we're hoping that by calling this decorator "singleton," we're nudging you to the correct behavior.
* This does not follow the computation graph.
* You don't have to worry about `hash_funcs`! Just prefix your arguments with an underscore to ignore them.

**WARNING:** Singleton objects can be used concurrently by every user connected to your app, and *you are responsible for ensuring that `@st.singleton` objects are thread-safe*. (Most objects you'd want to stick inside an `@st.singleton` annotation are probably already safe—but you should verify this.)

## **Which to use:** memo or singleton?

Decide between `@st.experimental_memo` and `@st.experimental_singleton` based on your \*\*function's *return type*. Functions that return *data* should use `memo`. Functions that return *non-data objects* should use `singleton`.

For example:

* Dataframe computation (pandas, numpy, etc): this is \*data—\*use `memo`
* Storing downloaded data: `memo`
* Calculating pi to n digits: `memo`
* Tensorflow session: this is a \*non-data object—\*use `singleton`
* Database connection: `singleton`

**NOTE:** The commands we're introducing today are **experimental**, so they're governed by our [experimental API process](https://docs.streamlit.io/en/stable/api.html?highlight=experimental&ref=streamlit.ghost.io#beta-and-experimental-features). This means:

1. We can change these APIs at any time. That's the whole point of the experiment! 😉
2. To make this clear, the names of these new commands start with "experimental\_".
3. If/when these commands graduate to our stable API, the "experimental\_" prefix will be removed.

## **Wrapping up**

These specialized **memoization** and **singleton** commands represent a big step in Streamlit's evolution, with the potential to *entirely replace* `@st.cache` at some point in 2022.

Yes, today you may use `@st.cache` for storing data you pulled in from a database connection (for a Tensorflow session, for caching the results of a long computation like changing the datetime values on a pandas dataframe, etc.). But these are very different things, so we made two new functions that will make it much faster! 💨

As usual, you can upgrade by using the following command:

```
pip install --upgrade streamlit
```

Please help us out by testing these commands in real apps and leaving comments in [the Streamlit forums](https://discuss.streamlit.io/?ref=streamlit.ghost.io). And come by the forum or [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io) to share all the cool things you make! 🎈

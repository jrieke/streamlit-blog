---
title: "What is Apache Arrow, How it Works & More| Streamlit"
subtitle: "How we improved performance by deleting over 1k lines of code"
date: 2021-07-23
authors:
  - "Henrikh Kantuni"
category: "Product"
---

![All in on Apache Arrow](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--14-.svg)


A long time ago in a galaxy far, far away, among the first few lines of code ever committed to Streamlit was a painstakingly crafted module that serialized Pandas [DataFrames](https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html?ref=streamlit.ghost.io#dataframe) (read "fancy tables") into a complex set of custom [Protobufs](https://developers.google.com/protocol-buffers?ref=streamlit.ghost.io) (read "fancy JSON") — plus the inverse of that module to deserialize them back into arrays in the browser.

Let's backtrack for a second. Why is this even needed? As you know, a great portion of Streamlit commands receive DataFrames as input arguments. It makes sense: DataFrames are efficient, versatile, and easy to work with. We all love them. They were a complete game-changer when they first appeared in the Python ecosystem. And while your DataFrames hung out in Python land, everything was hunky-dory. But as soon as we had to send them to the JavaScript territories, [there be dragons](https://en.wikipedia.org/wiki/Here_be_dragons?ref=streamlit.ghost.io): DataFrames were just not traditionally suited to be sent over-the-wire, and there was no standard JavaScript library to handle them on the browser side anyway. Hence, all the custom code.

And this came with a cost...

Our custom format grew considerably slower as users pushed for larger and larger DataFrames. Furthermore, every time Pandas released new features, adding support for them in Streamlit meant undertaking a considerable amount of work. Finally, we weren't big fans of our old custom module, to begin with!

So the search for a better format began. We spent months researching different solutions, trying out serialization formats, embarking on false starts, and going right back to where we started. Our old code still checked more boxes than all the options out there.

Until finally, we found it!

![](https://streamlit.ghost.io/content/images/2021/07/arrow.gif)

Yes, this blog post is about the TV show.

Meet [Arrow](https://arrow.apache.org/?ref=streamlit.ghost.io), an efficient memory format and set of libraries that will handle Streamlit's DataFrame serialization from now on. We love it, and we think you will too.

## What is Arrow, and how does it work

Arrow is a memory format for DataFrames, as well as a set of libraries for manipulating DataFrames in that format from all sorts of programming languages. From the Arrow [website](https://arrow.apache.org/?ref=streamlit.ghost.io):

> "A critical component of Apache Arrow is its in-memory columnar format, a standardized, language-agnostic specification for representing structured, table-like datasets in-memory. This data format has a rich data type system (including nested and user-defined data types) designed to support the needs of analytic database systems, data frame libraries, and more."

Let's break that down:

* It's column-oriented: so doing things like computing the sum of a column of your DataFrame is lightning fast.
* It's designed to be memory-mapped: so serialization/deserialization are basically free. Just send the bytes over the wire as they are.
* It's language-agnostic: so it's well-supported both in Python and JavaScript.
* Plus it supports all those DataFrame features that our custom module never got around to. This means that adding support to new DataFrame features into Streamlit is a much, much smaller undertaking.

![legacy-vs-arrow-2-1](https://streamlit.ghost.io/content/images/2021/07/legacy-vs-arrow-2-1.png#shadow)

## What this means for your Streamlit apps

### Faster and more efficient DataFrames

In our legacy serialization format, as DataFrame size grew, the time to serialize also increased significantly. Iterating through the DataFrame, converting all its data into formats we could use, packing them into a whole hierarchy of Protobufs, that's a whole lot of work that Arrow's memory-mapped format just throws out the window. Just compare the performance of our legacy format vs Arrow. It's not even funny!

![arrow-vs-legacy-chart-1](https://streamlit.ghost.io/content/images/2021/07/arrow-vs-legacy-chart-1.png#shadow)

### Other benefits to using Arrow

* As new features are introduced to Arrow, Streamlit can support them with much less work. Remember those features we never got around to supporting? Well, we just added a bunch of them now: table captions, categorical indices, interval indices, multi-index Styler objects, and more!
* If your app uses Arrow Tables, Streamlit will now accept them anywhere a Pandas DataFrame is accepted. Except it's, you guessed it, much faster.
* This one is mostly a benefit for us, Streamlit devs: **we get to delete over 1k lines of code from our codebase.** You can't believe how good this feels 😃

## How do I use it

Just upgrade to the latest version of Streamlit! Arrow is the default serialization format starting with version `0.85`:

```
pip install --upgrade streamlit
```

In the vast majority of cases, **no updates to your code are needed!** You can still give Streamlit your Pandas DataFrames just as before, and we'll convert it to Arrow behind the scenes for you.

## Sharp edges

* Arrow is a bit more strict than Pandas about keeping your DataFrames organized. For example, elements in the same column of a DataFrame must all have the same data type. But we find that this is an overall benefit to your data model, and valid reasons for breaking this rule are rare.
* Some features such as `PeriodIndex` and `TimedeltaIndex` are not yet fully supported. But, as mentioned earlier, adding them is easier than ever.
* Styler concatenation is no longer supported when using `add_rows()`. This is not really an Arrow-specific issue, but more that when you concatenate Styler objects it may not do what you wanted: if the Styler is configured to draw the `max` of a column in red, for example, then a correct concatenation would require recomputing the `max` for the entire column. Which is... suboptimal.
* This is a big change, and even though we tested it thoroughly, there may still be bugs lurking around.

If you encounter a bug (or the caveats above are blocking for you), you can revert to the previous implementation by setting the `dataFrameSerialization` config option to `"legacy"` in your `config.toml` as shown below:

```
[global]
dataFrameSerialization = "legacy"
```

And if you do that, **please file an issue on [GitHub](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)** so we can work on fixing whatever issue you found ASAP.

## Wrapping it up

Arrow is the new hotness, and it's where we believe the ecosystem is moving. So we're super excited to finally jump on that rocketship and help propel it forward with all of you.

Have fun with the updates, and looking forward to hearing what you think! As usual, come share what you create on the [forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io) or [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io). If you have any questions about Arrow or Streamlit, or just want to say hi, leave a comment below or on the forum. 🎈

## **Resources**

* [Documentation](https://docs.streamlit.io/en/stable/?ref=streamlit.ghost.io)
* [GitHub](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)

*Thanks to Abhi Saini, Alex Reece, Amanda Kelly, Jon Roes, Marisa Smith, and Tim Conkling for their input on this article.  
Massive shout-out to Thiago Teixeira and TC Ricks for the enormous work they did to create this beauty!*

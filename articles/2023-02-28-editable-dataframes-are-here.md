---
title: "Editable dataframes are here! \u270d\ufe0f"
subtitle: "Take interactivity to the next level with st.experimental_data_editor"
date: 2023-02-28
authors:
  - "Lukas Masuch"
category: "Product"
---

![Editable dataframes are here! ✍️](https://streamlit.ghost.io/content/images/size/w2000/2023/02/Announcement--5--2.svg)


Working with dataframes is at the heart of data science. If you’re like us, you probably load data from a CSV or a database, transform it in Pandas, fix it, transform it again, fix it again…and so on, until you’re happy. `st.dataframe` lets you visualize data instantly, but sometimes it’s not enough. You want to *interact* with it, not just look at a table!

Hence, we plan to release some major improvements for working with dataframes in the next few months. Today, we’re excited to launch…

**Editable dataframes!** 🎉

## How to use it

Editable dataframes are supported via a new command, `st.experimental_data_editor`. It shows the dataframe in a table, similar to `st.dataframe`. But in contrast to `st.dataframe`, this table isn’t static. The user can click on cells and edit them. The edited data is then returned on the Python side.

Here’s an example:

```
edited_df = st.experimental_data_editor(df)
favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
```

Try it out by double-clicking on a cell. 👆

⚠️

This feature is experimental, i.e. it might change at any time. We plan to de-experimentalize it in the next few months. See [here](https://docs.streamlit.io/library/advanced-features/prerelease?ref=streamlit.ghost.io#experimental-features) for details.

## Advanced features

* Adding and deleting rows. Just set the parameter `num_rows=”dynamic”`, and users can add rows to the table or delete existing rows:

![data-editor-add-delete-10.44.28-AM-1](https://streamlit.ghost.io/content/images/2023/02/data-editor-add-delete-10.44.28-AM-1.gif#browser)

* Copy-and-paste support that’s compatible with Google Sheets, Excel, and others:

![data-editor-clipboard-10.44.28-AM](https://streamlit.ghost.io/content/images/2023/02/data-editor-clipboard-10.44.28-AM.gif#browser)

* Bulk-editing by dragging the handle on a cell (similar to Excel):

![data-editor-bulk-editing-10.44.28-AM](https://streamlit.ghost.io/content/images/2023/02/data-editor-bulk-editing-10.44.28-AM.gif#browser)

* Easy access to edited data. No need to compare the old and new dataframe to get the difference. Just use `st.experimental_data_editor` together with session state to access all edits, additions, and deletions.
* Support for additional data types. Let your users edit lists, tuples, sets, dictionaries, NumPy arrays, or Snowpark and PySpark dataframes. Most types are returned in their original format.
* Automatic input validation, e.g., number cells don’t allow characters.
* Rich editing experience, e.g., checkboxes for booleans and dropdowns for categorical data. The date picker for datetime cells is coming soon!

## New docs page

To support this release, we created a [brand-new docs page on dataframes](https://docs.streamlit.io/library/advanced-features/dataframes?ref=streamlit.ghost.io). It explains everything you need to know about `st.dataframe` and the new `st.experimental_data_editor`, including all of the sweet features you saw above. The best part is, it comes with lots of interactive examples! 🕹️

And of course, we also added `st.experimental_data_editor` to our API reference. Check out all of its parameters [here](https://docs.streamlit.io/library/api-reference/widgets/st.experimental_data_editor?ref=streamlit.ghost.io).

## Examples

Excited to jump in? Check out our [demo app](https://data-editor.streamlit.app/?ref=streamlit.ghost.io). It shows examples of using the data editor in practice. From guessing idioms to matrix operations over custom convolution filters, you can do a lot with this new feature.

## Next up

Editable dataframes are only the beginning! 🌱

We have a bunch of new features for `st.dataframe` and `st.experimental_data_editor` in the pipeline for the next few months: showing images, clickable URLs in tables, letting the users select rows, and more. You can always follow our progress on [roadmap.streamlit.app](https://roadmap.streamlit.app/?ref=streamlit.ghost.io)!

We’re excited to see what you build. Let us know your feedback in the comments below.

Happy Streamlit-ing! 🎈

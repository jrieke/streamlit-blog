---
title: "Introducing column config \u2699\ufe0f"
subtitle: "Take st.dataframe and st.data_editor to the next level!"
date: 2023-06-22
authors:
  - "Lukas Masuch"
category: "Product"
---

![Introducing column config ⚙️](https://streamlit.ghost.io/content/images/size/w2000/2023/06/Announcement--5-.svg)


One of the biggest pain points you've told us about repeatedly is **dataframe customization**.

Data wrangling is at the core of your work, and you've long needed more capabilities than those offered by `st.dataframe` and `st.data_editor`.

Here are some of the things you told us you need to do:

* [Hide the index column](https://github.com/streamlit/streamlit/issues/641?ref=streamlit.ghost.io)
* Show [images](https://github.com/streamlit/streamlit/issues/1873?ref=streamlit.ghost.io) or [clickable links](https://github.com/streamlit/streamlit/issues/983?ref=streamlit.ghost.io) in table cells
* [Disable editing for specific columns](https://github.com/streamlit/streamlit/issues/6221?ref=streamlit.ghost.io) of the new data editor

We heard you! That's why in Streamlit 1.23, we're excited to introduce…

**Column configuration! 🎉**

Now you can customize all columns in `st.dataframe` and `st.data_editor`, so your tables look and feel exactly the way you need. Want to see it? Check out [our demo app](https://column-config.streamlit.app/?ref=streamlit.ghost.io) or read below.

Plus, we've moved `st.data_editor` out of experimental! 🎈

## A small example

The main star of the show is the new `column_config` parameter. We added it to both `st.dataframe` and `st.data_editor`.

It's a dictionary that maps column types to their configuration:

```
st.data_editor(
    df,
    column_config={
        "column 1": "Name",  # change the title
        "column 3": st.column_config.ImageColumn("Avatar"),
        "column 4": st.column_config.NumberColumn(
            "Age", min_value=0, max_value=120, format="%d years"
        ),
        "column 8": st.column_config.LineChartColumn(
            "Activity (1 year)", y_min=0, y_max=100
        ),
    },
)
```

Taking this [a bit further](https://github.com/streamlit/release-demos/blob/master/1.23/column_config_profiles_standalone/streamlit_app.py?ref=streamlit.ghost.io), you can create powerful tables like this:

Try playing with it:

* Scroll to the right to see some beautiful charts ✨📈
* Double-click on links to open them 🔗
* Double-click on a cell to edit it and see input validation features in action ✍️

As you can see in the code, we also introduced new classes for different column types under the `st.column_config` namespace. In fact, there are 14 different column types that cover everything from text over images to sparkline charts! Each of these classes lets you set additional parameters to configure the display and editing behavior of the column.

Have a look at them [on our new docs page](https://docs.streamlit.io/library/api-reference/data/st.column_config?ref=streamlit.ghost.io)! 🎈

![column-configuration-page](https://streamlit.ghost.io/content/images/2023/06/column-configuration-page.png#browser)

To learn more about the `column_config` parameter itself, check out the API references for  [`st.dataframe`](https://docs.streamlit.io/library/api-reference/data/st.dataframe?ref=streamlit.ghost.io) and [`st.data_editor`](https://docs.streamlit.io/library/api-reference/data/st.data_editor?ref=streamlit.ghost.io).

## More parameters

Want to hide the index column without delving into column configuration? We've got you covered!

In addition to the `column_config` parameter, we added a few more parameters that allow you to perform common operations more quickly:

* `hide_index=True` lets you hide the index column
* `column_order=["col 3", "col2"]` lets you set the order in which columns show up
* `disabled=["col1", "col2"]` lets you turn off editing for individual columns on `st.data_editor`

Read more about these parameters on the API docs for [`st.dataframe`](https://docs.streamlit.io/library/api-reference/data/st.dataframe?ref=streamlit.ghost.io) and [`st.data_editor`](https://docs.streamlit.io/library/api-reference/data/st.data_editor?ref=streamlit.ghost.io).

## Wrapping up

We're excited to see what you'll build with this new feature. Please share your examples on Twitter and the forum! Head over to our [example app](https://column-config.streamlit.app/?ref=streamlit.ghost.io) to get some inspiration. And if you have more feature requests for dataframes (and beyond), [let us know on GitHub](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

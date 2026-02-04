---
title: "Introducing multipage apps! \ud83d\udcc4"
subtitle: "Quickly and easily add more pages to your Streamlit apps"
date: 2022-06-02
authors:
  - "Vincent Donato"
category: "Product"
---

![Introducing multipage apps! 📄](https://streamlit.ghost.io/content/images/size/w2000/2022/11/multipage-apps-1.svg)


💡

To learn more about the latest in multipage apps, check out the documentation [here](https://docs.streamlit.io/develop/concepts/multipage-apps/overview?ref=streamlit.ghost.io).

So, you built a Streamlit app that became super useful, but then you got overloaded with feature requests. You kept adding more and more features until it felt too cluttered. You tried splitting the content across several pages by using `st.radio` or `st.selectbox` to choose which “page” to run.

It worked! But maintaining the code got harder. You were limited by the `st.selectbox` UI and couldn’t customize page titles with `st.set_page_config` or navigate between them via URLs. 🤯

Sound familiar?

We wanted to find a simple solution for this, so today, we’re excited to introduce…

**Native support for multipage apps!**

![multipage-apps](https://streamlit.ghost.io/content/images/2022/11/multipage-apps.gif#browser)

In this post, we’ll show you how to use this new feature and share tips and tricks on getting the most out of it.

Want to jump right in? Update Streamlit to the newest version and see the `streamlit hello` demo [app](https://doc-mpa-hello.streamlitapp.com/?ref=streamlit.ghost.io) and [repo](https://github.com/streamlit/hello?ref=streamlit.ghost.io) for inspiration. Read more on how to get started in [our docs](https://docs.streamlit.io/library/get-started/multipage-apps?ref=streamlit.ghost.io).

## Using multipage apps

Building a multipage app is easy! Just follow these steps:

1. Create a main script named `streamlit_app.py`.

2. In the same folder, create a new `pages` folder.

3. Add new `.py` files in the `pages` folder. Your filesystem will look like this:

```
my_app
├── streamlit_app.py    <-- Your main script
└── pages
    ├── page_2.py       <-- New page 2!
    └── page_3.py       <-- New page 3!
```

4. Run `streamlit run streamlit_app.py` as usual.

That’s it!

The `streamlit_app.py` script will now correspond to your app's main page. You’ll see the other scripts from the `pages` folder in the sidebar page selector.

## Converting an existing app into a multipage app

Let’s say you built a multipage app by using `st.selectbox` and want to convert it to the multipage app functionality. In your current app, the selectbox picks which page to display, and each “page” is written as a function.

If your folder name is `~/my_app` , your code will look like this:

```
# Contents of ~/my_app/streamlit_app.py
import streamlit as st

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
```

![](https://streamlit.ghost.io/content/images/2022/06/mpa-1.gif)

To convert your app to a multipage app, follow these steps:

1. Upgrade Streamlit to the newest version: `pip install --upgrade` `streamlit`

2. Add a new `pages` folder inside of `~/my_app`.

3. Create three new files inside of `~/my_app` :

* `main_page.py`
* `pages/page_2.py`
* `pages/page_3.py`

4. Move the contents of the `main_page`, `page2`, and `page3` functions into their corresponding new files:

```
# Contents of ~/my_app/main_page.py
import streamlit as st

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

# Contents of ~/my_app/pages/page_2.py
import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

# Contents of ~/my_app/pages/page_3.py
import streamlit as st

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")
```

5. Remove the original `streamlit_app.py` file.

6. Run `streamlit run main_page.py` and view your shiny new multipage app!

![](https://streamlit.ghost.io/content/images/2022/06/mpa-2.gif)

## Tips and tricks

We didn’t specify an order for pages 2 and 3, but they displayed correctly anyway. Why? 🤔 Because they’re ordered alphabetically by default.

But what if you wanted to make this more clear?

Just add numerical prefixes in front of the files in the `pages/` folder and rename them `pages/02_page_2.py` and `pages/03_page_3.py`. The names won’t include these prefixes—they’re used only for sorting.

You can also add emojis! 🥳 Try renaming the script files to:

* `01_🎈_main_page.py`
* `pages/02_❄️_page2.py`
* `pages/03_🎉_page3.py`

## Bonus features: new dataframe UI, horizontal radio buttons, and more!

Want to make your multipage apps look even cooler? 😎

Good news!

We launched more new features in Streamlit’s 1.10 release. Among them are the redesigned [st.dataframe](https://docs.streamlit.io/library/api-reference/data/st.dataframe?ref=streamlit.ghost.io) (based on [glide-data-grid](https://github.com/glideapps/glide-data-grid?ref=streamlit.ghost.io)) and horizontal radio buttons. Check out [the release notes](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io#version-1100) for more info.

![MPA-1](https://streamlit.ghost.io/content/images/2022/06/MPA-1.png#browser)

## Wrapping up

And that’s it for the intro to multipage apps! Adding more pages to your apps is now easier than ever. To start using multipage apps today, upgrade to the latest version of Streamlit:

```
pip install --upgrade streamlit
```

Have any questions or want to share a cool app you made? Join us on the [forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io), tag us on [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io), or let us know in the comments below. 🎈

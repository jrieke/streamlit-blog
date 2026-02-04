---
title: "Discover and share useful bits of code with the\u00a0\ud83e\udea2\u00a0streamlit-extras library"
subtitle: "How to extend the native capabilities of Streamlit apps"
date: 2022-10-25
authors:
  - "Arnaud Miribel"
category: "Tutorials"
---

![Discover and share useful bits of code with the 🪢 streamlit-extras library](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image-3.svg)


Hey, community! 👋

My name is Arnaud Miribel, and I’m a data scientist at Streamlit.

Every day I work on making or improving our internal apps. That means developing new reusable functions that improve the apps’ appearance or functionality. I also collect useful bits of code on our [forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io) or in the GitHub [issues](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io) that I can incorporate into my work. Essentially, those bits are mini [Streamlit components](https://docs.streamlit.io/library/components?ref=streamlit.ghost.io). Creating a new project for each would be a pain. So I bundled them all into one project—an experimental library where you can easily discover, try, install, and share these components.

Say hello to…

…`streamlit-extras`!

In this post, I’ll go over the following:

* What are streamlit-extras?
* How to discover extras
* How to try extras
* How to install extras
* How to contribute your own extras

Let’s get going!

## What are streamlit-extras?

`streamlit-extras` (extras for short) is just a collection of small custom Streamlit components. Most of them have a minimal of code, and most are Python-only (with some CSS/HTML hacks via `st.markdown`). Think of extras as an installable `utils.py` full of small, handy Streamlit components. 🙂

![ezgif.com-gif-maker](https://streamlit.ghost.io/content/images/2022/08/ezgif.com-gif-maker.gif#browser)

## How to discover extras

Head over to [extras.streamlitapp.com](http://extras.streamlitapp.com/?ref=streamlit.ghost.io) to discover extras in their natural habitat. Even the library’s gallery is a multipage app (why not make another app, right? 😉).

Let’s look at some of them:

### Badges

An easy way to add social badges to your apps:

![1](https://streamlit.ghost.io/content/images/2022/08/1.png#browser)

### App logo

A small function to add a logo to your navigation bar (sweet!):

![2](https://streamlit.ghost.io/content/images/2022/08/2.png#browser)

### Dataframe explorer UI

Recognize this? The now *famous* [filter\_dataframe](https://streamlit.ghost.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/) function that creates a UI on top of dataframes:

![3](https://streamlit.ghost.io/content/images/2022/08/3.png#browser)

### Toggle button

A simple lightweight alternative to st.expander—a toggle button:

![4](https://streamlit.ghost.io/content/images/2022/08/4.png#browser)

Browse the pages in the left navigation bar to see more!

## How to try extras

Some extras feature a “Playground” section. Try passing your own parameters to the extra and see how it works.

For example, try playing with `streamlit_extras.stoggle`:

![Untitled](https://streamlit.ghost.io/content/images/2022/08/Untitled.gif#browser)

Just for fun, try it within the [colored headers](https://extras.streamlitapp.com/Color%20ya%20Headers?ref=streamlit.ghost.io) or the [keyboard text](https://extras.streamlitapp.com/Keyboard%20text?ref=streamlit.ghost.io) extra. And guess what…“Playgrounds” are powered by *yet* *another extra*: the [function explorer](https://extras.streamlitapp.com/Function%20explorer?ref=streamlit.ghost.io). 😉

## How to install extras

You can easily use extras in your apps. Simply open your terminal and run:

```
pip install streamlit-extras
```

Extras are accessible as modules within the library itself, and you can use *all of them*.

For example, if you want to use `streamlit_extras.stoggle`, just create a new script:

```
# streamlit_app.py

import streamlit as st 
from streamlit_extras.stoggle import stoggle

stoggle("Here's a little secret", "Streamlit-extras is so cooool")
```

Go ahead and run `streamlit run streamlit_app.py`, and you’ll see this in your app:

![](https://streamlit.ghost.io/content/images/2022/08/Untitled--4-.png)

Congrats! You have used your first Streamlit extra. 🎊

## How to contribute your own extras

As part of this project, I populated the library with 20+ extras. But there is room for more. And it’s open-source, so you’re welcome to contribute!

For example, if you want to share an extra `strike` that strikes ~~a text~~, you can do it with HTML (let’s forget `st.markdown("~Hey~")` for a moment):

```
 def strike(text: str):
    """Strikes input text

    Args:
        text (str): Input text
    """
    return st.write(f"<del>{text}</del>", unsafe_allow_html=True)
```

Here is an example usage of `strike()`:

```
strike("Some outdated statement")
```

This will output:

![](https://streamlit.ghost.io/content/images/2022/08/Untitled--5-.png)

Take a look at the code. All extras have their own directory within `streamlit_extras` and a `__init__.py` in it:

```
.
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── gallery
│   ├── requirements.txt
│   ├── streamlit_app.py
│   └── streamlit_patches.py
├── poetry.lock
├── pyproject.toml
├── src
│   └── streamlit_extras       # <-- This is where extras live!
│       ├── __init__.py
│       ├── altex              # <-- Every extra has its directory...
│       │   └── __init__.py    # <-- ... and an __init__.py
│       ├── annotated_text
│       │   └── __init__.py
│   ├── ...
└── tests
    ├── __init__.py
    └── test_extras.py
```

To add a new extra:

1. Create a new directory in `src/streamlit_extras` called `strike_text`.
2. Create a new file `__init__.py` in this new directory.
3. Put the `strike()` function, for example, and some metadata:

```
# strike_text/__init__.py
import streamlit as st

def strike(text: str):
    """Strikes input text

    Args:
        text (str): Input text
    """
    return st.write(f"<del>{text}</del>", unsafe_allow_html=True)

def example():
    strike("Some outdated statement")

# Metadata that's useful to add your extra to the gallery
__func__ = strike
__title__ = "Strike text"
__desc__ = "A simple function to strike text"
__icon__ = "⚡"
__examples__ = [example]
__author__ = "Dark Vador"
__experimental_playground__ = True
```

That’s it!

Now create a pull request with these additions. Upon approval, I’ll feature your extra and make it accessible in the `streamlit-extras` library. Easy, right?

## Wrapping up

Hopefully you’ll find extras useful and contribute your own. If you have questions or thoughts, drop them in our [Github repo](https://github.com/arnaudmiribel/streamlit-extras?ref=streamlit.ghost.io). Remember—extras are just a little bit more of what you can do with Streamlit. The Streamlit community regularly makes awesome new [components](https://streamlit.io/components?ref=streamlit.ghost.io) that extend your apps in big ways.

If you want to learn about how to make your own advanced component with HTML and JavaScript, check out [this post](https://streamlit.ghost.io/how-to-build-your-own-streamlit-component/).

Happy Streamlit-ing! 🎈

P.S.: Learn more about `streamlit-extras` and the Streamlit Data Product team at [Snowflake BUILD](https://www.snowflake.com/build/?ref=streamlit.ghost.io), a free virtual developer conference. My colleague [Tyler](https://twitter.com/tylerjrichards?ref=streamlit.ghost.io) will be there, talking about the library along with the product feedback loops we’ve set up!

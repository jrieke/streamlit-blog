---
title: "Tips to Improve App Usability | Designing Apps for the User"
subtitle: "Designing an app your users will love"
date: 2021-06-02
authors:
  - "Abhi Saini"
category: "Tutorials"
---

![How to make a great Streamlit app](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--4--1.svg)


# Part 1: Building an app for the user

When you're building an app it's easy to focus on just getting it to work for your data and models, but it's equally important to think about your viewer. We've all had times when an app we created was shared with teammates and we were told it was hard to use, or it was slow, or that it could look nicer.

Never fear - Streamlit is here to help! Not only is it super easy to stand up web apps as a Data Scientist, but with a few easy tricks it’s also possible to have them look great and be performant! We're doing a 3 part series of blog posts on usability, aesthetics and performance.

In **Part 1**, we’ll go over tips on how to design for the user. In **[Part 2](https://streamlit.ghost.io/designing-streamlit-apps-for-the-user-part-ii/)**, we'll cover how Streamlit features like Layout, Theming can help make your app look great and finally in **[Part 3](https://streamlit.ghost.io/six-tips-for-improving-your-streamlit-app-performance/)**, we'll focus on how to make the apps even more performant.

Kicking off **Part 1: Designing for the user**, the main things to keep in mind are:

1. Put yourself in the user's shoes
2. Show users how your app works and have instructions
3. Have examples
4. Hide excess information

Let's jump in!

## Start with the user

A good place to begin before starting to write Streamlit code is to think how your users will actually use the app. Imagine what they might do when opening the app or better yet, talk to some of your users and discuss:

* What is the problem that the user is facing?
* What objectives are users trying to achieve?
* How will users use this app?

Writing down your users goals and matching that to specific widgets, text, and visuals to add (or even [doing some quick wireframing](https://www.figma.com/blog/how-to-wireframe/?ref=streamlit.ghost.io)!) can help structure your app into something both easy-to-use and effective for your user's needs.

## Show users how it works

Using an app can sometimes be confusing, especially for first time users. To help them navigate the app, add some explainer text in the app or a separate document that tells them how to use it. And because showing is always better than telling, it can be helpful to consider creating a video that navigates through the various inputs. You can do this with a feature Streamlit natively ships with called [Record a screencast](https://docs.streamlit.io/en/stable/advanced_concepts.html?highlight=record&ref=streamlit.ghost.io#record-a-screencast).

At Streamlit, we use this feature to record demos of our new features as seen in some of our previous blog posts (See [Theming](https://streamlit.ghost.io/introducing-theming/) and [Forms](https://streamlit.ghost.io/introducing-submit-button-and-forms/) blog posts)

![Record_Screencast-1](https://streamlit.ghost.io/content/images/2021/08/Record_Screencast-1.gif#border)

It is also super easy to embed videos in Streamlit apps. All it takes is two lines of code!

```
import streamlit as st

st.video('recorded_screencast.mp4')
```

## Have examples of input data

With multiple input fields or file formats, first time users can be confused by what goes into each box and how the app will respond. Having default input data helps users get started on using the app right away.

In your streamlit app, default input data can be pre-filled into widgets by using the `value` argument, for eg.

```
txt = st.text_area('Text to analyze', value='It was the best of times')
```

For other apps, where the input type can be something more complex, app developers can provide a default input. For eg. the [Goodreads Reading Habits](https://share.streamlit.io/tylerjrichards/streamlit_goodreads_app/books.py?ref=streamlit.ghost.io) app developed by Tyler Richards is a great example of how having default inputs allows the user to visualize the app's expected output.

## Show information only when it is needed

To reduce visual clutter, sometimes it's best to hide information and let the user access it when needed. This frees up valuable screen real estate for the developer to help focus the user's attention. In this section, we describe 2 ways of achieving this: 1) Tooltips and 2) Expanders.

### Using Tooltips

Starting with version `0.79.0`, Streamlit introduced Tooltips which can be associated with **input** widgets like `st.text_input`, `st.selectbox` etc. Tooltips can help reduce visual clutter as well as act as a source of helpful information for app users.

Tooltips can be conveniently added to supported widgets using the `help` keyword.

```
import streamlit as st

st.title('Tooltips in Streamlit')
st.radio("Pick a number", [1, 2, 3], help='Select a number out of 3 choices')

# Tooltips also support markdown
radio_markdown = '''
Select a number, you have **3** choices!
'''.strip()

st.header('Tooltips with Markdown')
st.radio("Pick a number", [1, 2, 3], help=radio_markdown)
```

This results in a `(?)` being added to the widget. Upon hovering on the tooltip, the help message appears as shown below:

![ToolTips](https://streamlit.ghost.io/content/images/2021/08/ToolTips.gif#browser)

All **input widgets** like `st.number_input`, `st.slider`, `st.radio`, `st.text_area` etc support tooltips via the `help` keyword.

### Using Expanders

Expanders can also be used to reduce visual clutter and hide text that may only be relevant to users looking for additional details.

![1-1](https://streamlit.ghost.io/content/images/2021/08/1-1.png#border)

![2-2](https://streamlit.ghost.io/content/images/2021/08/2-2.png#border)

See our previous [blog post](https://streamlit.ghost.io/introducing-new-layout-options-for-streamlit/) on Layouts for more details on how to use expanders.

## **Wrapping up**

We hope that by using these features, your Streamlit apps will be cleaner and more usable for your users. To use the features discussed above in your apps, go ahead and upgrade to the latest version of Streamlit

```
pip install --upgrade streamlit
```

In **[Part 2](https://streamlit.ghost.io/designing-streamlit-apps-for-the-user-part-ii/)**, of this blog series, we'll cover more on how Streamlit features like Layout, Theming, and Anchors can help make your app look even better 🎈

If you have any questions let us know on the forum!

### Resources

* [Github](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)

---
title: "Store Information Across App Interactions | Session State"
subtitle: "You can now store information across app interactions and reruns!"
date: 2021-07-01
authors:
  - "Abhi Saini"
category: "Product"
---

![Session State for Streamlit 🎈](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--10--1.svg)


Soon after Streamlit launched in 2019, the community started asking for ways to add statefulness to their apps. Hacks for [Session State](https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92?ref=streamlit.ghost.io) have been around since October 2019, but we wanted to build an elegant solution that you could intuitively weave into apps in a few lines of code. Today we're excited to release it!

You can now use Session State to store variables across reruns, create events on input widgets and use callback functions to handle events. This powerful functionality helps create apps which can:

* Perform data/image annotation
* Support Pagination
* Add widgets that depend on other widgets
* Build simple stateful games like Battleship, Tic Tac Toe, etc.
* And much more - all of this with the simplicity of writing apps that are Python scripts!

💡 If you want to jump right in, check out our [demo](https://share.streamlit.io/streamlit/release-demos/0.84/0.84/streamlit_app.py?page=headliner&ref=streamlit.ghost.io) to see some of the above apps in action or head to the [docs](https://docs.streamlit.io/en/stable/add_state_app.html?ref=streamlit.ghost.io) for more detailed info on getting started.

## Add State to your App

In Streamlit, interacting with a widget triggers a rerun and variables defined in the code get reinitialized after each rerun. But with Session State, it's possible to have values persist across reruns for those instances when you *don't* want your variables reinitialized.

For example, here's a simple counter that maintains a count value across multiple presses of an increment button. Each button press triggers a rerun but the count value is preserved and incremented (or decremented) across the rerun:

![Session_State_GIF_1-edited](https://streamlit.ghost.io/content/images/2021/08/Session_State_GIF_1-edited.gif#browser)

```
import streamlit as st

st.title('Counter Example')

# Streamlit runs from top to bottom on every iteraction so
# we check if `count` has already been initialized in st.session_state.

# If no, then initialize count to 0
# If count is already initialized, don't do anything
if 'count' not in st.session_state:
	st.session_state.count = 0

# Create a button which will increment the counter
increment = st.button('Increment')
if increment:
    st.session_state.count += 1

# A button to decrement the counter
decrement = st.button('Decrement')
if decrement:
    st.session_state.count -= 1

st.write('Count = ', st.session_state.count)
```

💡 To continue building on this example, follow along in our [Topic Guide: Add State to your App](https://docs.streamlit.io/en/stable/add_state_app.html?ref=streamlit.ghost.io) 🤓

The above shows a basic example of how values can persist over reruns, but let's move on to something a little more complex!

## Callback functions and Session State API

As part of this release, we're launching Callbacks in Streamlit. Callbacks can be passed as arguments to widgets like `st.button` or `st.slider` using the `on_change` argument.

💡 Curious what a callback is? Wikipedia phrases it well: "*a callback, also known as a "call-after" function, is any executable code that is passed as an argument to other code; that other code is expected to call back (execute) the argument at a given time.* " [Here's a link](https://en.wikipedia.org/wiki/Callback_(computer_programming)?ref=streamlit.ghost.io) if you'd like to read more.

With Session State, events associated with changes to a widget or click events associated with button presses can be handled by callback functions. It's important to remember the following order of execution:

![Quick-Image-2--2-](https://streamlit.ghost.io/content/images/2021/08/Quick-Image-2--2-.png#border)

**Order of Execution:** If a callback function is associated with a widget then a change in the widget triggers the following sequence: First the callback function is executed and then the app executes from top to bottom.

Here's an example:

![Session_State_GIF_2-1-edited](https://streamlit.ghost.io/content/images/2021/08/Session_State_GIF_2-1-edited.gif#border)

```
import streamlit as st

def update_first():
    st.session_state.second = st.session_state.first

def update_second():
    st.session_state.first = st.session_state.second

st.title('🪞 Mirrored Widgets using Session State')

st.text_input(label='Textbox 1', key='first', on_change=update_first)
st.text_input(label='Textbox 2', key='second', on_change=update_second)
```

In the above, we showcase the use of callbacks and session state.  We also showcase an advanced concept, where session state can be associated with widget state using the `key` parameter.

To read more on this, check out the [Advanced Concepts section](https://docs.streamlit.io/en/stable/add_state_app.html?ref=streamlit.ghost.io#advanced-concepts) in the Session State docs and to check out the API in detail visit the [State API documentation](https://docs.streamlit.io/en/stable/session_state_api.html?ref=streamlit.ghost.io).

## Wrapping up

That's it for the intro to Session State, but we hope this isn't the end of the conversation! We're excited to see how you'll use these new capabilities, and all the new functionalities state will unlock for the community.

To get started, upgrade to the latest release to use `st.session_state` and `callbacks` in your apps:

```
pip install --upgrade streamlit
```

If you have any questions about these (or about Streamlit in general) let us know below in the comments or [on the forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io). And make sure to come by the forum or [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io) to share all the cool things you make! 🎈

## **Resources**

* [Session State Topic Guide](https://docs.streamlit.io/en/stable/add_state_app.html?ref=streamlit.ghost.io)
* [Session State API Reference](https://docs.streamlit.io/en/stable/session_state_api.html?ref=streamlit.ghost.io)
* [Session State Demo App](https://share.streamlit.io/streamlit/release-demos/0.84/0.84/streamlit_app.py?page=headliner&ref=streamlit.ghost.io)
* [Github](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)

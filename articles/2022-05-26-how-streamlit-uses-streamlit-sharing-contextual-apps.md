---
title: "How Streamlit uses Streamlit: Sharing contextual apps"
subtitle: "Learn about session state and query parameters!"
date: 2022-05-26
authors:
  - "Tyler Richards"
category: "Tutorials"
---

![How Streamlit uses Streamlit: Sharing contextual apps](https://streamlit.ghost.io/content/images/size/w2000/2022/05/light-border.gif)


All of us on the Streamlit Data Science team are massive Streamlit fans (obviously!). In our day jobs, we produce internal Streamlit apps. These apps do everything from helping our partners discover useful tables in our data warehouse, to graphing [Streamlit Community Cloud’s](https://streamlit.io/cloud?ref=streamlit.ghost.io) monthly active developers over time, to seeing what Streamlit features are rising and falling in use. This means we produce a *ton* of apps and keep them all in one large, multi-page app.

But as we traveled down this path, we found ourselves in a bit of a pickle. We’d create a new app, find a widget combination that sheds light on something *super useful*, and would want to share it in that exact state. For example, what if we worked for Uber and wanted to share how [NYC rideshare traffic looked at 2 am](https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main?ref=streamlit.ghost.io)? Or how the 2 am traffic differed from the 2 pm traffic?

To do this, we could:

1. Set the app's widgets' default values so that the user could find them *on screen load*. We'd share the app in this exact initial state, but the users can still interact with it and explore other configurations.
2. Take app screenshots and send them via Slack, Notion, or email.
3. Write instructions for rediscovering the finding, either in the app itself or in the message to users, “Hi! We made a new change in our NYC rideshare app. Here is the link. Go ahead and change the slider bar to 2am. We noticed an interesting concentration of rides in the Chelsea area during that time, especially relative to the 2pm time period.”

But these options aren’t all that great.

* Option 1 doesn’t take into consideration that we often have many cool findings per app! It also doesn’t work for our multi-page app setup, so it’s out of the picture.
* Option 2 defeats the purpose of an app. Why create an interactive app when users will see only a static photo?
* Option 3 puts in friction between the user and the insight. This creates a bad user experience.

We solved this by combining session state with passing the URL query parameters to Streamlit apps. In this post, I’ll walk you through a minimum viable app. You’ll learn:

* How to get URL query parameters into Streamlit
* How to use those parameters in Streamlit widgets
* How to sync widgets and your app’s URLs

## How to get URL query parameters into Streamlit

This part is the easiest!

Streamlit has a feature called `st.experimental_get_query_parameters` (read more about it in [our docs](https://docs.streamlit.io/library/api-reference/utilities/st.experimental_get_query_params?ref=streamlit.ghost.io)). It returns a list of parameters that are already in the URL. For example, here is the URL of a locally deployed app [http://localhost:8501/?my\_name=tyler&month=may.](http://localhost:8501/?my_name=tyler&month=may.&ref=streamlit.ghost.io)

This URL has two parameters (`my_name`, `month`) with values (`tyler`, `may`). Or for an app deployed on Streamlit Community Cloud, the link [https://share.streamlit.io/tylerjrichards/streamlit\_goodreads\_app/books.py/?is\_checked=True](https://share.streamlit.io/tylerjrichards/streamlit_goodreads_app/books.py/?is_checked=True&ref=streamlit.ghost.io) has the parameter `is_checked` with the value `True`.

This code pulls the parameters from the URL and prints them out:

```
import streamlit as st

my_query_params = st.experimental_get_query_params()
st.write("My Query Params:")
st.write(my_query_params)
```

Now you can save this code in a Python file (mine is `streamlit_example_app.py`), run it with `streamlit run streamlit_example_app.py` , and get the URL parameters programmatically!

![2-new-new-1](https://streamlit.ghost.io/content/images/2022/05/2-new-new-1.png#browser)

See how query parameters can be “passed” to your Streamlit app. 👆

**NOTE:** You probably noticed the `experimental_` prefix in our function call. That means it's a feature we're still working on or trying to understand, and it'll go through many iterations as we get feedback from the community. You can find more information about experimental features in our [docs](https://docs.streamlit.io/library/advanced-features/prerelease?ref=streamlit.ghost.io)!

## How to use those parameters in Streamlit widgets

Now that you have the Streamlit URL parameters, you can use them to influence the Streamlit widgets we use in building apps.

For example, let’s create a URL parameter called `is_checked` *and* pass it to the value of a Streamlit checkbox. We return the query parameters as lists inside a dictionary, so you can use the `get` function to pull the parameter (if it exists), and use `== "true"` to make it a boolean that is passed into your checkbox value parameter:

```
import streamlit as st

query_params = st.experimental_get_query_params()
my_checkbox = st.checkbox(
    "Example Checkbox",
    value=query_params.get("is_checked", ["False"])[0].lower() == "true",
)
st.write(query_params)
```

Now if you go to [http://localhost:8501/is\_checked=True](http://localhost:8501/is_checked=True?ref=streamlit.ghost.io), you’ll see that the checkbox is checked:

![3-new-new](https://streamlit.ghost.io/content/images/2022/05/3-new-new.png#browser)

See how the checkbox value equals the query parameter. 👆

This is a great V0!

But what if you want the URL to change when you change widget inputs? Typing out URL parameters is annoying. Instead, take advantage of `st.session_state` and `st.experimental_set_query_params()`.

## How to sync widgets and your app’s URLs

We have lots of great [documentation](https://docs.streamlit.io/library/api-reference/session-state?ref=streamlit.ghost.io) on `st.session_state`. Check it out if this is your first rodeo!

As a super basic introduction, `st.session_state` is a magic dictionary that doesn’t get reset every time the page updates. Use it to see how users interact with your app across all reruns. And if you want to change your URL parameters, use `st.experimental_set_query_params()`!

For this to work, you’ll need to ‘reset’ your URL parameter at the end of your app with `st.experimental_set_query_params` *and* ensure you’re only reading from `st.experimental_get_query_params` on the first app run.

To do this, check if the `is_check` parameter is inside `st.session_state`. If it’s not, add it to `st.session_state` as we did above 👆  to get the current query parameters from your URL:

```
import streamlit as st

query_params = st.experimental_get_query_params()
if "is_checked" not in st.session_state:
    st.session_state["is_checked"] = (
        query_params.get("is_checked", ["False"])[0].lower() == "true"
    )
my_checkbox = st.checkbox("Example Checkbox", key="is_checked")
st.experimental_set_query_params(is_checked=my_checkbox)
st.write(st.session_state)
```

You’ll notice another change in the code.

Before, you had to assign the default value of the checkbox. Now you can use the key parameter to keep the checkbox synced with `is_checked` from inside `st.session_state`! Adding a key to a widget automatically creates a corresponding entry in `st.session_state`.

The final change is with the `st.experimental_set_query_params` function. Overwrite the `is_checked` variable with whatever was last in your checkbox. Query parameters and your Streamlit checkbox are now synchronized! 🎉

![4-new-1](https://streamlit.ghost.io/content/images/2022/05/4-new-1.gif#browser)

## Wrapping up

Now you can share your Streamlit apps in the right context and help users play with them!

Massive thanks to [Zachary Blackwood](https://www.linkedin.com/in/blackary/?ref=streamlit.ghost.io) for teaching me much of what I know about `st.session_state` and for helping with the code. Also thanks to the folks [in this Twitter thread](https://twitter.com/MarkusOdenthal/status/1525142434342215682?ref=streamlit.ghost.io) who gave me the idea to write about how to use the suggested methods.

I’d love to hear how you solve this problem and your ideas for the future of Streamlit. Find me on Twitter as [@tylerjrichards](https://twitter.com/tylerjrichards?ref=streamlit.ghost.io) and check out the [forums](https://discuss.streamlit.io/?ref=streamlit.ghost.io) to see what our vibrant community is creating.

Happy Streamlit-ing! 🎈

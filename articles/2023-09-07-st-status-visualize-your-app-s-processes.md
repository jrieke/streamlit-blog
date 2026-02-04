---
title: "st.status: Visualize your app\u2019s processes"
subtitle: "Rich context for users and more control for developers"
date: 2023-09-07
authors:
  - "Joshua Carroll"
category: "Product"
---

![st.status: Visualize your app’s processes](https://streamlit.ghost.io/content/images/size/w2000/2023/09/st-status-blog-image.png)


✅

**TL;DR:** Replace long app wait times and shed light on the “black box” of data processing with [st.status](https://docs.streamlit.io/library/api-reference/status/st.status?ref=streamlit.ghost.io). Play with our [demo app](https://release126.streamlit.app/st.status_demo?ref=streamlit.ghost.io) to see how it works.

Long-running apps like LLM agents rarely show you their inner workings out of the box. On top of that, if a response takes too long to generate, users get impatient and leave. Not ideal!

**Introducing: `st.status`**

If you're not always confident in your model's output, how do you inspect the intermediate steps and chain of thought to verify results?  A few months ago, we provided a targeted solution by integrating with [LangChain, using their callback system](https://streamlit.ghost.io/langchain-streamlit/#rendering-llm-thoughts-and-actions).

Now you can add `st.status` to ***any*** interactive or API-powered app to:

* Animate its "under-the-hood" processes such as API calls or data retrieval.
* See step-by-step logic to understand what went wrong (or validate what went right).
* Allow users to engage with your app, rather than experiencing a blank page.

See how it works in our [demo app](https://release126.streamlit.app/st.status_demo?ref=streamlit.ghost.io)! Choose any of the 8 different animations below to pair with your app operations. Check out the [docs](https://docs.streamlit.io/library/api-reference/status/st.status?ref=streamlit.ghost.io) for more detail.

Let's look at two examples to see it in action.

## Step-by-step transparency, in real-time

With `st.status`, every process step is defined, broken out, and animated. The app viewer can expand the status to check the details or leave it collapsed to focus on the final output.

Unlike `st.spinner`, the intermediate steps remain available to inspect even after the process completes.

![](https://streamlit.ghost.io/content/images/2023/09/st-status-transparency.gif)

https://release126.streamlit.app/st.status\_demo

## Flexible interaction to validate results

This can be particularly helpful to validate results from LLM-based apps.

LLMs aren't perfect. Their intelligence relies on the data sets they are trained on, which could be incomplete or contain misinformation. The LLM attempts to generate a plausible response to a user's prompt, but if it reaches the boundaries of its knowledge base, it can take liberties. This phenomenon causes an LLM to "hallucinate." If the user can't quite tell if the model is correct, or is embellishing a result, they quickly lose trust.

With `st.status`, the context and intermediate steps are available so users can validate the output logic:

![](https://streamlit.ghost.io/content/images/2023/09/st-status-expand-output.gif)

https://release126.streamlit.app/LangChain\_demo

## What's next

This flexible framework gives you a higher degree of control to up-level your app’s user experience, and easily integrate custom components. It’s worth the extra lines of code!

Help us raise the bar with new (and refined) UI improvements. What [additional transparency features](https://docs.streamlit.io/library/api-reference/status?ref=streamlit.ghost.io) would you like to see next?

Let us know in the comments below or on [Discord](https://discord.gg/bTz5EDYh9Z?ref=blog.streamlit.io).

Happy Streamlit-ing! 🎈

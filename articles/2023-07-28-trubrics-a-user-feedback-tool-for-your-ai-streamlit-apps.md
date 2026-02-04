---
title: "Trubrics: A user feedback tool for your AI Streamlit apps"
subtitle: "A 3-step guide on collecting, analyzing, and managing AI model feedback"
date: 2023-07-28
authors:
  - "Jeff Kayne"
category: "Advocate Posts"
---

![Trubrics: A user feedback tool for your AI Streamlit apps](https://streamlit.ghost.io/content/images/size/w2000/2023/07/user-feedback-trubrics.svg)


🚀

Update: Streamlit now has a built-in element `st.feedback`, which may be an alternative to the component below. Read more [in our docs](https://docs.streamlit.io/develop/api-reference/widgets/st.feedback?ref=streamlit.ghost.io).

Hey, community! 👋

My name is Jeff, and I’m a co-founder of [Trubrics](https://trubrics.com/?ref=streamlit.ghost.io). As a data scientist and Machine Learning engineer, I have experienced firsthand the challenges of deploying new ML models without understanding how users interact with them. This can lead to reduced model performance and, ultimately, misaligned models and users.

More specifically, here is why you should start listening to your users:

* **🚨 Identify bugs:** Users constantly run inference on your models and may be more likely to find bugs than your ML monitoring system.
* **🧑‍💻️ Fine-tune:** Users often have domain knowledge that can be useful in fine-tuning models.
* **👥 Align:** Identifying user preferences can help align models with users.

If you want to generate user insights on your AI models, we've built Trubrics, the first user insights platform for AI models.

In this post, we'll cover:

1. How to create a free account with Trubrics
2. How to collect user feedback from your AI Streamlit app
3. How to analyze and manage your user feedback in Trubrics

🚨

TLDR: Here is the [app](https://trubrics.streamlit.app/?ref=streamlit.ghost.io) and the [repo](https://github.com/trubrics/trubrics-sdk?ref=streamlit.ghost.io), and here is the [video](https://www.youtube.com/watch?v=2Qt54qGwIdQ&ref=streamlit.ghost.io) (watch it above).

## 1. How to create a free account with Trubrics

Create an account directly in the Trubrics [app](https://trubrics.streamlit.app/?ref=streamlit.ghost.io):




After logging in, you'll find a pre-existing `default` component.

Click on it to access code snippets and start collecting feedback. You can create different feedback components to collect and organize feedback across multiple projects or apps.

![trubrics-component](https://streamlit.ghost.io/content/images/2023/07/trubrics-component.png#browser)

Now, to save your first piece of feedback to the default component, head over to our example user feedback LLM [app](https://trubrics-llm-example-chatbot.streamlit.app/?ref=streamlit.ghost.io):




## 2. How to collect user feedback from your AI Streamlit app

Let's explore various code snippets to see how you can embed Trubrics feedback components directly into your app.

First, install our SDK with the `streamlit` dependency (if it's not already installed):

```
pip install "trubrics[streamlit]"
```

Then copy and paste this snippet into your app:

```
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector(
    email=st.secrets.TRUBRICS_EMAIL,
    password=st.secrets.TRUBRICS_PASSWORD,
    project="default"
)

user_feedback = collector.st_feedback(
    component="default",
    feedback_type="thumbs",
    open_feedback_label="[Optional] Provide additional feedback",
    model="gpt-3.5-turbo",
    prompt_id=None,  # checkout collector.log_prompt() to log your user prompts
)

if user_feedback:
    st.write(user_feedback)
```

What's going on here? Let's break it down:

1. **The `FeedbackCollector` object.** Store your Trubrics credentials in [st.secrets](https://streamlit.ghost.io/secrets-in-sharing-apps/), and specify the project to which you want to save. In this case, use the `default`.
2. **Its `st_feedback()` method.** Calling this method allows users to embed UI widgets in their apps. These widgets can be added throughout your app to collect feedback on different predictions.

And that's it!

Now you'll see a thumbs up / down feedback widget in your application, like this:

![additional-feedback](https://streamlit.ghost.io/content/images/2023/09/Screenshot-2023-09-11-at-09.55.49.png)

🚨

To learn more about customizing your feedback component, read our [docs](https://trubrics.github.io/trubrics-sdk/integrations/streamlit/?ref=streamlit.ghost.io).

## **3.** How to analyze and manage your user feedback in Trubrics

After you've saved the feedback to Trubrics, consult the [👍 Feedback](https://trubrics.streamlit.app/Feedback?ref=streamlit.ghost.io) page for quantitative and qualitative analysis. This enables AI teams to understand whether users are satisfied with predictions and compare results between different models.

![trubrics-insights](https://streamlit.ghost.io/content/images/2023/07/trubrics-insights.png#browser)

Various filters on the `User feedback` tab allow AI teams to:

* Aggregate responses by frequency (hourly, daily, weekly, monthly)
* View all responses for a specific score, model, or user
* Compare responses for all scores, models, or users

For qualitative feedback, user comments are collected in the `text` field of the `Feedback` response. All comments are listed in the `Comments` tab and may be grouped to create an [issue](https://trubrics.github.io/trubrics-sdk/platform/issues/?ref=streamlit.ghost.io). AI model issues can also be opened or closed on the [issues](https://trubrics.streamlit.app/Issues?ref=streamlit.ghost.io) page.

## Wrapping up

Thank you for reading! You've learned how to collect app user feedback and view it in [Trubrics](https://trubrics.streamlit.app/?ref=streamlit.ghost.io). If you have any questions, please post them in the comments below or contact me directly on my [LinkedIn](https://www.linkedin.com/in/jeffrey-kayne/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

---
title: "Collecting user feedback on ML in Streamlit"
subtitle: "Improve user engagement and model quality with the new Trubrics feedback component"
date: 2023-05-04
authors:
  - "Jeff Kayne"
category: "Advocate Posts"
---

![Collecting user feedback on ML in Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/04/trubrics-feedback-compontent.svg)


Hey, community! 👋

I'm Jeff, co-founder of [Trubrics](https://trubrics.com/?ref=streamlit.ghost.io). We build tools to help data scientists collect user feedback on machine learning (ML). We've developed a new component that enables you to do just that with a few lines of code in your Streamlit app!

Why collect user feedback on ML?

1. **Improving model performance.** User feedback provides insights into the strengths and weaknesses of the model from the user's perspective. This information enables fixes and fine-tuning of the ML model, ultimately improving its performance.
2. **Enhancing user experience.** User feedback can help identify user preferences and pain points. This information can be used to design better user interfaces, improve model usability, and ultimately enhance the user experience.
3. **Increasing user engagement.** Collecting user feedback shows that you care about your users' opinions and are committed to providing the best possible experience. This can increase user engagement, satisfaction, adoption, and loyalty.
4. **Growing responsibility of the ML group.** Adding diversity and cross-functional teams to the ML review process helps us strive towards building #responsibleAI and #ethicalAI.
5. **Continuous model improvement and monitoring.** Collecting user feedback in production can help you improve your ML model by incorporating bug fixes, user needs, and preferences.

⚠️

This blog post refers to a previous version of our component `trubrics-sdk==1.3.6` . For an updated blog, please see [here](https://streamlit.ghost.io/trubrics-a-user-feedback-tool-for-your-ai-streamlit-apps/).

In this post, you'll learn:

* How to `pip install` the FeedbackCollector from the [trubrics-sdk](https://github.com/trubrics/trubrics-sdk/?ref=streamlit.ghost.io)
* How to get started with just 3 lines of code [Beginner]
* How to collect complex feedback [Advanced]
* How to manage your feedback in the Trubrics platform [Optional]

👉

Can't wait to try it? Here are the links to our [demo app](https://trubrics-titanic-example.streamlit.app/?ref=streamlit.ghost.io), [repo](https://github.com/trubrics/trubrics-sdk/?ref=streamlit.ghost.io), and [docs](https://trubrics.github.io/trubrics-sdk/streamlit/?ref=streamlit.ghost.io).

## How to pip install the FeedbackCollector from the [trubrics-sdk](https://github.com/trubrics/trubrics-sdk/?ref=streamlit.ghost.io)

Trubrics embeds some Streamlit components, so you'll need to install both libraries:

```
pip install "trubrics[streamlit]"==1.3.6
```

By the way, Trubrics is tested for Python versions 3.7, 3.8, and 3.9.

## How to get started with just 3 lines of code [Beginner]

Add these three lines of code to your Streamlit app/a blank Python script (if you're just getting started):

```
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()
collector.st_feedback(feedback_type="issue")
```

What's going on here? Let's break it down:

1. The [FeedbackCollector](https://trubrics.github.io/trubrics-sdk/streamlit/?ref=streamlit.ghost.io#feedbackcollector) object provides feedback functionality and static metadata about your app (e.g., model version). Create an instance of this object once at the top of your app.
2. The [st\_feedback()](https://trubrics.github.io/trubrics-sdk/streamlit/?ref=streamlit.ghost.io#st_feedback) method allows you to embed feedback components in your app and save different types of feedback to .json files. Use multiple instances of this method to add different feedback collection points around your app.

Now you can launch your app with `streamlit run basic_app.py` !

You'll see a feedback component in your app that will let you start collecting *qualitative* *feedback* from your users:

![trubrics_ml_feedback_type_issue](https://streamlit.ghost.io/content/images/2023/04/trubrics_ml_feedback_type_issue.png#browser)

Try other types of *quantitative feedback* collection, such as:

```
collector.st_feedback(feedback_type="faces")
```

![trubrics_ml_feedback_type_faces](https://streamlit.ghost.io/content/images/2023/04/trubrics_ml_feedback_type_faces.png#browser)

```
feedback = collector.st_feedback(
	feedback_type="thumbs",
	path="thumbs_feedback.json"
)

# print out the feedback object as a dictionary in your app
feedback.dict() if feedback else None
```

![trubrics_ml_feedback_type_thumbs](https://streamlit.ghost.io/content/images/2023/04/trubrics_ml_feedback_type_thumbs.png#browser)

The `st_feedback()` method returns a feedback object that can be manipulated (in this case, we're printing it out in the app). And it saves a feedback .json to a specified path, such as `path="thumbs_feedback.json"`. To save multiple files, use a dynamic path, such as `path=f"thumbs_{timestamp}.json"` with a time stamp.

To learn more about the different feedback types and their available options, read our [docs](https://trubrics.github.io/trubrics-sdk/streamlit/?ref=streamlit.ghost.io#feedback-types).

## How to collect complex feedback [Advanced]

You can use the Trubrics FeedbackCollector to collect more complex feedback with `type="custom"`. This is super useful for collecting forms or survey responses with multiple questions:

```
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector
collector = FeedbackCollector()
q1 = st.text_input("Q 1")
q2 = st.text_input("Q 2")
q3 = st.text_input("Q 3")
if q1 and q2 and q3:
    button = st.button(label="submit")
    if button:
        feedback = collector.st_feedback(
            "custom",
            user_response={
                "Q 1": q1,
                "Q 2": q2,
                "Q 3": q3,
            },
            path="./feedback.json",
        )
        feedback.dict() if feedback else None
```

This lets you use any Streamlit components to create the feedback form of your choice.

👉

TIP: For creating more robust forms in Streamlit, check out [st.form](https://docs.streamlit.io/library/api-reference/control-flow/st.form?ref=streamlit.ghost.io).

![trubrics_ml_feedback_type_custom-1](https://streamlit.ghost.io/content/images/2023/04/trubrics_ml_feedback_type_custom-1.png#browser)

You can use Trubrics' "faces" and "thumbs" feedback UI components in your custom feedback forms, as shown [here](https://trubrics.github.io/trubrics-sdk/streamlit/?ref=streamlit.ghost.io#trubrics-ui-components).

## How to manage your feedback in the Trubrics platform [Optional]

To manage and collaborate on feedback issues more effectively, we offer functionality that enables you to save feedback directly to our platform from your Streamlit app. This also allows users to authenticate within the apps and track who has recorded what feedback:

![trubrics_ml_feedback_platform](https://streamlit.ghost.io/content/images/2023/04/trubrics_ml_feedback_platform.png#browser)

## Wrapping up

And...here is the final app!

Thank you for reading our story. We hope that you're now armed and ready to start collecting feedback on your ML projects. Please try out our component and let us know any feedback. And if you have any questions or ideas, we'd be very happy to hear from you. Drop us a message in the comments below, or contact us on [GitHub,](https://github.com/trubrics/trubrics-sdk/issues?ref=streamlit.ghost.io) [LinkedIn](https://www.linkedin.com/in/jeffrey-kayne/?ref=streamlit.ghost.io), or via [email](mailto:jeff.kayne@trubrics.com).

Happy Streamlit-ing! 🎈

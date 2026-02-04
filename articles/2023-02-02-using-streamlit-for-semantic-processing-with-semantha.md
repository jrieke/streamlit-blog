---
title: "Using Streamlit for semantic processing with semantha"
subtitle: "Learn how to integrate a semantic AI into Snowflake with Streamlit"
date: 2023-02-02
authors:
  - "Sven Koerner"
category: "Advocate Posts"
---

![Using Streamlit for semantic processing with semantha](https://streamlit.ghost.io/content/images/size/w2000/2023/01/semantic-processing.svg)


Hey, community! 👋

My name is Sven and I work as an AI researcher at thingsTHINKING.

We integrated our semantic platform with large-scale (data) customers. They use Snowflake to combine hundreds of data sinks. Connecting with Snowflake’s API and using Streamlit gave the users a super-efficient UI while preserving our platform capabilities. The integration was only 3 lines of code—and the UI setup was only 46!

In this post, I’ll show you:

* How to integrate semantic AI processing into your apps and use cases
* How to give your app “common sense” with a 3-liner
* How to get inspired!

Want to jump right in? Here's a [sample app](https://semantha.streamlit.app/?ref=streamlit.ghost.io) and a [repo code](https://github.com/thingsTHINKING/semantha-streamlit?ref=streamlit.ghost.io).

## How to integrate semantic AI processing into your apps and use cases

Follow these simple steps:

**Step 1.** Install the corresponding semantha package for your use case with `pip install semantha-streamlit-compare`.

You can find the latest version of this demo on [pypi](https://pypi.org/project/semantha-streamlit-compare/?ref=streamlit.ghost.io). We also provide a [pip-based SDK](https://pypi.org/project/semantha-sdk/?ref=streamlit.ghost.io) so that you can use all our semantic processing features (more on this in future posts).

Here is an example:

```
from semantha_streamlit_compare.components.compare import SemanticCompare

compare = SemanticCompare()
compare.build_input(sentences=("First sentence", "Second sentence"))
```

**Step 2.** Create your Streamlit UI and add the semantha endpoint.

Here is a sample UI with only 30 lines of code on [GitHub](https://github.com/thingsTHINKING/semantha-streamlit?ref=streamlit.ghost.io):

![sample-code-github](https://streamlit.ghost.io/content/images/2023/01/sample-code-github.png#browser)

**Step 3 (optional).** Import the semantha (Python) package into your code and use it in whatever form you’d like.

**Step 4.** Request an API code from semantha and run your prototype.

For example, to use a component, request a `secrets.toml` file from [support@thingsthinking.atlassian.net](mailto:support@thingsthinking.atlassian.net). After you are authenticated, copy it into the `.streamlit/secrets.toml` folder as documented [here](https://streamlit.ghost.io/secrets-in-sharing-apps/). You may need to create it in the root of your Streamlit app.

Here is the file structure of the `secrets.toml` file:

```
[semantha]
server_url="URL_TO_SERVER"
api_key="YOUR_API_KEY_ISSUED"
domain="USAGE_DOMAIN_PROVIDED_TO_YOU"
documenttype="document_with_contradiction_enabled"
```

## How to give your app “common sense” with a 3-liner

If you’ve done the above, you’ve built “common sense” into your app, which can now automatically understand when things are similar, different, or of opposite meanings. Extend this idea to documents and all the unstructured information you process every day. You know where this could lead to…a trusty sidekick in your daily knowledge work!

## How to get inspired!

Check out this video to see what people have built based on Streamlit:

You know your use cases best—and you know where a coworker (in this case, not a human but an AI) could be very helpful!

## Wrapping up

We’ll provide more use cases in future posts, including:

* Movie Quote Search
* ESG Document Comparison Using semantha’s MagicSort
* RFI/RFP/Tender processing with semantic platforms on Streamlit/Snowflake

![visualization-1](https://streamlit.ghost.io/content/images/2023/01/visualization-1.png#border)

If you have any questions, please post them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/svenjkoerner/?ref=streamlit.ghost.io), [Twitter](https://twitter.com/SvenJKoerner?ref=streamlit.ghost.io), or via [email](mailto:sven@thingsthinking.net).

Happy coding! 🧑‍💻

---
title: "Streamlit App Starter Kit: How to build apps faster"
subtitle: "Save 10 minutes every time you build an app"
date: 2022-09-27
authors:
  - "Chanin Nantasenamat"
category: "Tutorials"
---

![Streamlit App Starter Kit: How to build apps faster](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--20--1.svg)


To build a Streamlit app you’d typically follow these steps:

* Install prerequisite libraries by specifying library names in `requirements.txt`
* Customize the theme via `.streamlit/config.toml` (optional)
* Create an app file `streamlit_app.py`
* Inside the app file, call `import streamlit as st`
* Specify the app tasks (e.g. read a CSV, perform data wrangling, display a scatter plot, train an ML model, etc.)

Every step takes only minutes, but over time it can amount to hours—or even days! 😅

In this article, you’ll learn how to save 10 minutes every time you build an app:

* What is the Streamlit App Starter Kit?
* How to use the Streamlit App Starter Kit

👉

**NOTE:** We recommend having a basic knowledge of [Python](https://www.python.org/?ref=streamlit.ghost.io) and Streamlit (learn it by completing the [#30DaysOfStreamlit](https://30days.streamlitapp.com/?ref=streamlit.ghost.io) challenge), plus a [GitHub](https://github.com/?ref=streamlit.ghost.io) and a [Streamlit Community Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io) accounts.

Let’s dive right in!

### What is the Streamlit App Starter Kit?

The [Streamlit App Starter Kit](https://github.com/streamlit/app-starter-kit?ref=streamlit.ghost.io) has the following files:

```
app-starter-kit/
├─ .streamlit/
│  ├─ config.toml
├─ README.md
├─ packages.txt (optional)
├─ requirements.txt
├─ streamlit_app.py
```

This is what it looks like in a GitHub repository:

![app-starter-kit-1-2](https://streamlit.ghost.io/content/images/2022/09/app-starter-kit-1-2.png#border)

It contains:

`.streamlit/config.toml`—a configuration file with parameters for customizing your app’s theme:

```
[theme]
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
```

`README.md`—a README file with a project description:

```
# Name of Streamlit App

Description of the app ...

## Demo App

[![Streamlit App](<https://static.streamlit.io/badges/streamlit_badge_black_white.svg>)](<https://share.streamlit.io/dataprofessor/st-app/>)

## Section Heading

This is filler text. Please replace this with the text for this section.

## Further Reading

This is filler text. Please replace this with explanatory text about further relevant resources for this repo.
- Resource 1
- Resource 2
- Resource 3
```

`packages.txt`—a list of Linux tools and packages to install (blank by default). Go ahead and populate it with the package names you want to install—one name per line.

`requirements.txt`—a list of Python libraries to install. By default, the Streamlit App Starter Kit lists only `streamlit`. It’ll install the latest version:

```
streamlit
```

If you want a specific version—like `1.13.0`—do the following:

```
streamlit==1.13.0
```

Add some Python libraries:

```
streamlit==1.13.0
pandas==1.3.5
scikit-learn==1.1.0
```

`streamlit_app.py`—the Streamlit app:

```
import streamlit as st

st.title('🎈 App Name')

st.write('Hello world!')
```

### How to use the Streamlit App Starter Kit

The Streamlit App Starter Kit is available as a GitHub template. Clone it to your repo and use it to make your own Streamlit app:

![streamlit-app-starter-kit-22Sep2022](https://streamlit.ghost.io/content/images/2022/09/streamlit-app-starter-kit-22Sep2022.gif#browser)

Want to customize the contents of the app files? Use widgets to accept user input and display the output results (read more about widgets in [our docs](https://docs.streamlit.io/?ref=streamlit.ghost.io)).

Finally, deploy your app with the [Streamlit Community Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io) or some other [cloud service provider](https://docs.streamlit.io/knowledge-base/tutorials/deploy?ref=streamlit.ghost.io)! 🎉

### Wrapping up

Congratulations! You’ve used the Streamlit App Starter Kit to make your app-making process faster. 💨

If you like to work with command line interfaces, check out the [streamlit-kickoff-cli](https://github.com/arnaudmiribel/streamlit-kickoff-cli?ref=streamlit.ghost.io) developed by our very own [Arnaud Miribel](https://twitter.com/arnaudmiribel?ref=streamlit.ghost.io). And if you have any questions, please leave them in the comments below or contact me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=streamlit.ghost.io) or on [LinkedIn](https://www.linkedin.com/in/chanin-nantasenamat/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

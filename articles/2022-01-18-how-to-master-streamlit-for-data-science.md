---
title: "How to master Streamlit for data\u00a0science"
subtitle: "The essential Streamlit for all your data\u00a0science needs"
date: 2022-01-18
authors:
  - "Chanin Nantasenamat"
category: "Tutorials"
---

![How to master Streamlit for data science](https://streamlit.ghost.io/content/images/size/w2000/2022/11/how-to-master-streamlit.svg)


## The essential Streamlit for all your data science needs

To build a web app you’d typically use such Python web frameworks as Django and Flask. But the steep learning curve and the big time investment for implementing these apps present a major hurdle.

Streamlit makes the app creation process as simple as writing Python scripts!

In this article, you’ll learn how to master Streamlit when getting started with data science.

Let’s dive in!

## 1. Getting up to speed

### 1.1. Why deploy models?

The data science process boils down to converting data to knowledge/insights while summarizing the conversion with the [CRISP-DM](https://www.ibm.com/docs/en/spss-modeler/SaaS?topic=dm-crisp-help-overview&ref=streamlit.ghost.io) and [OSEMN](https://web.archive.org/web/20211219192027/http://www.dataists.com/2010/09/a-taxonomy-of-data-science/) data frameworks. Aside from knowledge/insights, a data project can make a greater impact if you deploy your machine learning models as web apps.

Why? Because deployed models can be accessed by stakeholders who can play with them and figure out what works and what doesn't.

### 1.2. Types of model deployment

Model deployment is the endpoint of a data science workflow. Models can be deployed as:

* Jupyter notebooks
* API
* Web apps

**Jupyter notebooks.** Jupyter notebooks are commonly used for prototyping the data science workflow and they can be:

* Uploaded to [GitHub](https://github.com/?ref=streamlit.ghost.io)
* Shared as a link via [Google Colab](https://colab.research.google.com/?ref=streamlit.ghost.io)
* Shared via [Binder](https://mybinder.org/?ref=streamlit.ghost.io)

**API.** Models can also be deployed as a REST API using tools such as [FastAPI](https://fastapi.tiangolo.com/?ref=streamlit.ghost.io). This approach does not have a frontend for displaying it graphically for ease of use.

**Web apps.** This brings us to deploying machine learning models as web applications. The traditional approach is to wrap the API via the use of web frameworks such as Django and Flask. A much simpler approach is to use a low-code solution such as Streamlit to create a web app.

Let’s explore this in more depth in the following section.

### 1.3. Traditional vs. low-code web frameworks

Though Django and Flask may be the gold standard for developing web apps, the technical barriers limit their usage by the wider data community. Low-code solutions such as Streamlit have lowered the barrier to entry by enabling data enthusiasts (e.g. data scientists, analysts, and hobbyists) to easily convert machine learning models into interactive data-driven web apps.

Here are the low-code solutions:

![](https://streamlit.ghost.io/content/images/2022/01/model-building.jpeg)

## 2. Streamlit 101

Streamlit is a Python library you can use to build interactive data-driven web apps.

### 2.1. What you need to use Streamlit

To use Streamlit, you need to:

* Have basic Python knowledge.
* Write scripts to perform specific tasks (like taking several Excel files as input and combining them into one).
* Build and grow the Streamlit app line by line instead of starting with a predefined layout (it takes only a few lines of code).

If you can do all this, congratulations! You're ready to plunge into the world of Streamlit.

### 2.2. Four Streamlit design principles

According to Adrien Treuille, co-founder and CEO of Streamlit, Streamlit was originally based on three principles (as mentioned in the [2019 PyData LA talk](https://youtu.be/0It8phQ1gkQ?ref=streamlit.ghost.io) and the [Medium launch post](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace?ref=streamlit.ghost.io)). The fourth principle was introduced at the launch of [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io):

1. **Embrace Python scripting.** Build and grow Streamlit apps line by line.
2. **Treat widgets as variables.** Widgets are input elements that let users interact with Streamlit apps. They’re presented as basic input text boxes, checkboxes, slider bars, etc.
3. **Reuse data and computation.** Historically, data and computations had been cached with the `@st.cache` decorator. This saves computational time for app changes. It can be *hundreds of times* if you actively revise the app! In 0.89.0 release Streamlit launched two new primitives ([st.experimental\_memo](https://docs.streamlit.io/library/api-reference/performance/st.experimental_memo?ref=streamlit.ghost.io) and [st.experimental\_singleton](https://docs.streamlit.io/library/api-reference/performance/st.experimental_singleton?ref=streamlit.ghost.io)) to afford a significant speed improvement to that of `@st.cache`.
4. **Deploy instantly.** Easily and instantly deploy apps with [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io).

## 3. How to set up your Streamlit workspace

### 3.1. Install Streamlit

Install the Streamlit library by using `pip`:

```
pip install streamlit
```

### 3.2. Code a Streamlit app

After doing so, you can start to code an app by creating a Python script file (e.g. `app.py`). Inside this file, you can import the Streamlit library via `import streamlit as st` and use any of the available Streamlit functions.

### 3.3. Launch your Streamlit apps

Once the app has been coded, launching it is as easy as running `streamlit run app.py`.

For first time users, you can also type  `streamlit hello`  into the command line to see Streamlit in action.

Go ahead and give it a try!

### 3.4. Create a conda environment

As I show on my [YouTube channel](https://youtube.com/dataprofessor?ref=streamlit.ghost.io), I like to house my Streamlit apps in a dedicated conda environment. This way the library dependencies don’t get entangled with my other Python libraries. I recommend you do the same.

Begin by building an EDA app. Read how I created a dedicated conda environment in the [GitHub repo’s](https://github.com/dataprofessor/eda-app?ref=streamlit.ghost.io) `readme.md` file, then watch this tutorial video on [How to Build an EDA app using Pandas Profiling](https://youtu.be/p4uohebPuCg?ref=streamlit.ghost.io) and follow these steps:

**Step 1.** Create a conda environment called `eda`:

```
conda create -n eda python=3.7.9
```

**Step 2.** Activate the `eda` environment:

```
conda activate eda
```

**Step 3.** Install prerequisite libraries by downloading the `requirements.txt` file (it contains the library version numbers):

```
wget https://raw.githubusercontent.com/dataprofessor/eda-app/main/requirements.txt
```

**Step 4.** Install libraries via `pip`:

```
pip install -r requirements.txt
```

**Step 5.** Download and unzip contents from the GitHub repo: [https://github.com/dataprofessor/eda-app/archive/main.zip](https://github.com/dataprofessor/eda-app/archive/main.zip?ref=streamlit.ghost.io)

**Step 6.** Launch the app:

```
streamlit run app.py
```

You’ll see the web app browser pop up:

![](https://streamlit.ghost.io/content/images/2022/01/EDA-app.png)

The functionality of this EDA app leverages the capabilities of `pandas-profiling`:

![](https://streamlit.ghost.io/content/images/2022/01/EDA_app.gif)

Congratulations! You now know how to clone a Streamlit app from a GitHub repo, setup a dedicated conda environment, and successfully launch the app!

Next, customize the app to your own liking.

## 4. Practice by building the “Hello, World!” app

Now that you know Streamlit principles, let’s build some apps. It’s not as hard as you may think. A typical rite of passage for learning any new programming language is to start with printing `Hello World!`.

Here is how to do it in Streamlit in four easy steps:

**Step 1.** Launch your favorite code editor ([Atom.io](http://atom.io/?ref=streamlit.ghost.io), VS Code, etc.).

**Step 2.** Create a file and name it `app.py`.

**Step 3.** Add this code into the `app.py` file:

```
import streamlit as st

st.write('Hello world!')
```

**Step 4.** Launch the app by typing this into the command line:

```
streamlit run app.py
```

## 5. Build your Own Streamlit App

I like to start my Streamlit projects by coding the “brains” of the app on Google Colab.

At a high level, a web app is comprised of three key elements:

1. **Input.** Widgets make it possible to take in user input. They can be sliders, text/number boxes, file upload widgets, etc.
2. **The “brains” of the app.** The brains or the inner workings of the app is what differentiates one app from another. It performs the function of transforming user inputs into outputs.
3. **Output.** This can be anything: DataFrame printouts, images, plots, numerical values, text, or embeddings of audio, videos, and tweets.

Because web apps adopt a similar structure, some of the elements used in one project can be repurposed and reused in the next project.

### 5.1. Elements of a Streamlit app

* Contents (text, images, embedded videos, audio, tweets, etc.)
* Widgets
* Auxillaries (balloons, code box, etc.)

### 5.2. The “Brains” of the Streamlit app

* Use Streamlit components
* Make use of existing functions from Python libraries of interest
* Code your own custom function

### 5.3. Lay out the app

I like to put widgets on the left-hand sidebars of the app. Use `st.sidebar.` in front of any widget functions of interest (instead of `st.`). For example, to place the text input box in the sidebar, use `st.sidebar.text_input(‘Name’)` instead of `st.text_input(‘Name’)` (which would place the text input box into the main panel).

## 6. Deploy your Streamlit app

Now that you’ve built a Streamlit app, deploy it to the cloud for general public access. The easiest way to do this is with [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io):

1. Create a GitHub repo of the app files (`app.py`, `requirements.txt`, and dependency files)
2. In [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io), link your GitHub account and select the app’s repo to deploy.

You can also watch [this video](https://youtu.be/kXvmqg8hc70?ref=streamlit.ghost.io) on how to deploy Streamlit apps.

## 7. Resources

### 7.1. Documentation

Streamlit’s [documentation website](https://docs.streamlit.io/?ref=streamlit.ghost.io) is the best place to get you started:

* **Streamlit library.** A guide on how to build Streamlit apps with various Streamlit functions (the API reference), “Get started” tutorials, and a cheat sheet.
* **Streamlit Cloud.** Everything you need to know on how to deploy apps to Streamlit Cloud.
* **Knowledge base.** A growing collection of tutorial articles and FAQs about using Streamlit and troubleshooting problems.

### 7.2. Discussion forum

Can’t find the information on the documentation website? Check out the [Streamlit discussion forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io) and read the [troubleshooting guide](https://docs.streamlit.io/en/stable/troubleshooting/index.html?ref=streamlit.ghost.io) for tips on resolving problems.

### 7.3. YouTube tutorials

Here’s a list of these YouTube channels about Streamlit:

* **[Streamlit](https://www.youtube.com/channel/UC3LD42rjj-Owtxsa6PwGU5Q?ref=streamlit.ghost.io)**. The official Streamlit YouTube channel with official announcements of the latest features.
* **[Data Professor](https://www.youtube.com/c/DataProfessor?ref=streamlit.ghost.io)**. My YouTube channel with videos on data science and bioinformatics and a growing [playlist of 30 videos on Streamlit](https://www.youtube.com/watch?v=ZZ4B0QUHuNc&list=PLtqF5YXg7GLmCvTswG32NqQypOuYkPRUE&ref=streamlit.ghost.io).
* **[JCharisTech](https://www.youtube.com/channel/UC2wMHF4HBkTMGLsvZAIWzRg?ref=streamlit.ghost.io)**. Jesse’s YouTube channel with tutorial videos on Python and Streamlit and with a [playlist of almost 70 videos on Streamlit](https://www.youtube.com/watch?v=_9WiB2PDO7k&list=PLJ39kWiJXSixyRMcn3lrbv8xI8ZZoYNZU&ref=streamlit.ghost.io).
* **[1littlecoder](https://www.youtube.com/c/1littlecoder?ref=streamlit.ghost.io)**. AbdulMajed’s YouTube channel with tutorial videos on Python and Streamlit and with a [playlist of almost 20 videos on Streamlit](https://www.youtube.com/watch?v=Iv2vt-7AYNQ&list=PLpdmBGJ6ELUI6Tws8BqVVNadsYOQlWGtw&ref=streamlit.ghost.io).

### 7.4. Books

Tyler Richards wrote a book titled [Getting Started with Streamlit for Data Science: Create and Deploy Streamlit Web Applications from Scratch in Python](https://amzn.to/3ypOTWY?ref=streamlit.ghost.io). It takes readers on a journey of how they can build interactive data-driven apps. The last chapter was super-fun to read as Tyler interviewed Streamlit power users.

I also interviewed Tyler in the hour-long podcast [Data Science Podcast with Tyler Richards - Facebook Data Scientist](https://youtu.be/uPg7PEdx7WA?ref=streamlit.ghost.io). We talked about his journey into data science, his experience as a data scientist, and his thoughts and inspiration for writing a book about Streamlit.

## Wrapping up

You’ve learned Streamlit essentials that will start you on building your own interactive data-driven Python apps. Well done! Of course, there’s always more to learn. Feel free to drop a comment or a suggestion below on the topics that you'd like to learn more about.

Happy Streamlit-ing! 🎈

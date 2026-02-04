---
title: "LangChain tutorial #2: Build a blog outline generator app in 25 lines of code"
subtitle: "A guide on conquering writer\u2019s block with a Streamlit app"
date: 2023-06-07
authors:
  - "Chanin Nantasenamat"
category: "LLMs"
---

![LangChain tutorial #2: Build a blog outline generator app in 25 lines of code](https://streamlit.ghost.io/content/images/size/w2000/2023/06/Langchain-Tutorial-2.svg)


In [LangChain tutorial #1](https://streamlit.ghost.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/), you learned about LangChain modules and built a simple LLM-powered app. The app took input from a text box and passed it to the LLM (from OpenAI) to generate a response. But it didn’t leverage other LangChain modules.

In this post, I’ll show you how to use LangChain’s prompt template and build a blog outline generator app in four simple steps:

1. Get an OpenAI API key
2. Set up the coding environment
3. Build the app
4. Deploy the app

  

🦜

Want to skip reading? Here's the [demo app](https://langchain-outline-generator.streamlit.app/?ref=streamlit.ghost.io) and the [repo code](https://github.com/dataprofessor/langchain-blog-outline-generator?ref=streamlit.ghost.io).

Before we get to building the app, let's talk about…

## What's a prompt template?

A prompt is an instruction given to an LLM. You can use a prompt template to generate prompts on-the-fly. It has two parts:

1. A static descriptive text part (hard-coded in the code).
2. A dynamically generated part (determined by the user).

Use it to pre-define the app's scope so it performs a specific task as a function of user instructions (e.g. generates prompts in a reproducible manner).

Here is an example of a prompt template:

```
'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
```

The text `As an experienced data scientist and technical writer, generate an outline for a blog about` is the static component, and the `{topic}` is the dynamic component determined by the user (e.g. a blog topic they're interested in).

### Prompt template in action

To implement the prompt template, use LangChain's `PromptTemplate()` function.

It accepts the following input arguments:

* `input_variables` allows you to accept user-provided values comprising the prompt template's dynamic component.
* `template` is the static component of the prompt template.

Here is what it'll look like:

```
template = 'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
prompt = PromptTemplate(input_variables=['topic'], template=template)
```

  

📖

Check out the LangChain documentation on [prompt template](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/?ref=streamlit.ghost.io) for further information.

### App overview

The app solves one of the most time-consuming problems for technical writers...

**Writer's block!** ✍️

It works like this:

![](https://streamlit.ghost.io/content/images/2023/06/blog-outline-generation-diagram.jpg)

Its workflow consists of three simple steps:

1. Use Streamlit's `st.text_input()` function to accept the user-provided "Topic" as input.
2. Combine the "topic" and the prompt instructions using `PromptTemplate()` to create the final prompt.
3. Use the final prompt to generate a response.

Go ahead and try it:

Here is what it should look like:

![blog-outline-app_scaling-0.3_fps-20_speed-10.0_duration-0-44](https://streamlit.ghost.io/content/images/2023/06/blog-outline-app_scaling-0.3_fps-20_speed-10.0_duration-0-44.gif)

Now, let's build the app!

## Step 1. Get an OpenAI API key

Hop over to the [LangChain tutorial #1](https://streamlit.ghost.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/) for instructions on how to get an OpenAI API key.

## Step 2. Set up the coding environment

### Local development

To set up a programming workspace on your own system, install Python version 3.7 or higher. Then install these Python libraries:

```
pip install streamlit openai langchain
```

### Cloud development

You can also create the app on the Streamlit Community Cloud. To get started, use the [Streamlit app template](https://github.com/streamlit/app-starter-kit?ref=streamlit.ghost.io) (read more [here](https://streamlit.ghost.io/streamlit-app-starter-kit-how-to-build-apps-faster/)).

Next, include the three prerequisite Python libraries in the `requirements.txt` file:

```
streamlit
openai
langchain
```

## Step 3. Build the app

The code for building the app is only 25 lines long (23 without the two comments):

```
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate

st.set_page_config(page_title="🦜🔗 Blog Outline Generator App")
st.title('🦜🔗 Blog Outline Generator App')
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(topic):
  llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)
  # Prompt
  template = 'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
  prompt = PromptTemplate(input_variables=['topic'], template=template)
  prompt_query = prompt.format(topic=topic)
  # Run LLM model and print out response
  response = llm(prompt_query)
  return st.info(response)

with st.form('myform'):
  topic_text = st.text_input('Enter keyword:', '')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(topic_text)
```

First, create the `streamlit_app.py` file to house the full code snippet above. Or follow along and add the code block by block.

In the first few lines, import the necessary Python libraries, such as Streamlit and specific Langchain methods `OpenAI` and `PromptTemplate`:

```
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
```

Next, give the app a page title for display on the browser window and in-app:

```
st.set_page_config(page_title="🦜🔗 Blog Outline Generator App")
st.title('🦜🔗 Blog Outline Generator App')
```

A text box is created to accept OpenAI credentials:

```
openai_api_key = st.sidebar.text_input('OpenAI API Key')
```

A custom function generates an LLM response based on the user's provided "topic" of interest. An instance of the LLM model is created using `OpenAI()`. This is followed by creating a dynamically created prompt stored in the `prompt_query` variable. This prompt combines static and dynamic components.

The LLM model accepts the prompt as input for generating a response—the blog outline. It's displayed in a blue box using `st.info()`:

```
def generate_response(topic):
  llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)
  # Prompt
  template = 'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
  prompt = PromptTemplate(input_variables=['topic'], template=template)
  prompt_query = prompt.format(topic=topic)
  # Run LLM model
  response = llm(prompt_query)
  return st.info(response)
```

Finally, `st.form()` is used as an app logic to generate the blog outline only after correctly entering the OpenAI API key, filling the text box with the blog topic, and clicking the `Submit` button:

```
with st.form('myform'):
  topic_text = st.text_input('Enter keyword:', '')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(topic_text)
```

## Step 4. Deploy the app

After creating your app, you can deploy it in three steps:

1. Create a GitHub repository for your app.
2. Go to the Community Cloud, click the `New app` button, and select the repository, branch, and app file.
3. Click the `Deploy!` button.

And voilà! You're done.

## Wrapping up

In this post, you've learned how to use the LLM model with the LangChain prompt template to build a blog outline generator. You can customize your app by adjusting the prompt. Check out the [LLM gallery](https://streamlit.io/gallery?category=llms&ref=streamlit.ghost.io) for more ideas and inspiration.

If you have any questions, please post them in the comments below or contact me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=blog.streamlit.io) or on [LinkedIn](https://www.linkedin.com/in/chanin-nantasenamat/?ref=blog.streamlit.io).

Happy app-building! 🦜🔗

P.S. This post was made possible thanks to the technical review by Tim Conkling and editing by Ksenia Anske.

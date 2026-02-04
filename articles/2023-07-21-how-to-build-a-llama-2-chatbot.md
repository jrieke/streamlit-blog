---
title: "How to build a Llama 2 chatbot"
subtitle: "Experiment with this open-source LLM from Meta"
date: 2023-07-21
authors:
  - "Chanin Nantasenamat"
category: "LLMs"
---

![How to build a Llama 2 chatbot](https://streamlit.ghost.io/content/images/size/w2000/2023/07/Announcement-1.svg)


Generative AI has been widely adopted, and the development of new, larger, and improved LLMs is advancing rapidly, making it an exciting time for developers.

You may have heard of the recent release of [Llama 2](https://ai.meta.com/llama/?ref=streamlit.ghost.io), an open source large language model (LLM) by Meta. This means that you can build on, modify, deploy, and use a local copy of the model, or host it on cloud servers (e.g., [Replicate](https://replicate.com/?ref=streamlit.ghost.io)).

While it’s free to download and use, it’s worth noting that self-hosting the Llama 2 model requires a powerful computer with high-end GPUs to perform computations in a timely manner. An alternative is to host the models on a cloud platform like Replicate and use the LLM via API calls. In particular, the three Llama 2 models (`llama-7b-v2-chat`, `llama-13b-v2-chat`, and `llama-70b-v2-chat`) are hosted on Replicate.

In this post, we’ll build a Llama 2 chatbot in Python using Streamlit for the frontend, while the LLM backend is handled through API calls to the Llama 2 model hosted on Replicate. You’ll learn how to:

1. Get a Replicate API token
2. Set up the coding environment
3. Build the app
4. Set the API token
5. Deploy the app



🦙

Want to jump right in? Here's the [demo app](https://llama2.streamlit.app/?ref=streamlit.ghost.io) and the [GitHub repo](https://github.com/dataprofessor/llama2?ref=streamlit.ghost.io).

## What is Llama 2?

Meta released the second version of their open-source Llama language model on July 18, 2023. They’re democratizing access to this model by making it free to the community for both research and commercial use. They also prioritize the transparent and responsible use of AI, as evidenced by their [Responsible Use Guide](https://ai.meta.com/llama/responsible-use-guide?ref=streamlit.ghost.io).

Here are the five key features of Llama 2:

1. Llama 2 outperforms other open-source LLMs in benchmarks for reasoning, coding proficiency, and knowledge tests.
2. The model was trained on almost twice the data of version 1, totaling 2 trillion tokens. Additionally, the training included over 1 million new human annotations and fine-tuning for chat completions.
3. The model comes in three sizes, each trained with 7, 13, and 70 billion parameters.
4. Llama 2 supports longer context lengths, up to 4096 tokens.
5. Version 2 has a more permissive license than version 1, allowing for commercial use.

## App overview

Here is a high-level overview of the Llama2 chatbot app:

1. The user provides two inputs: (1) a Replicate API token (if requested) and (2) a prompt input (i.e. ask a question).
2. An API call is made to the Replicate server, where the prompt input is submitted and the resulting LLM-generated response is obtained and displayed in the app.

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-schematic-diagram.JPG.jpg)

Let's take a look at the app in action:






1. Go to [https://llama2.streamlit.app/](https://llama2.streamlit.app/?ref=streamlit.ghost.io)
2. Enter your Replicate API token if prompted by the app.
3. Enter your message prompt in the chat box, as shown in the screencast below.

![Llama2-chatbot-screencast_scaling-0.5_fps-15_speed-10.0_duration-0-48](https://streamlit.ghost.io/content/images/2023/07/Llama2-chatbot-screencast_scaling-0.5_fps-15_speed-10.0_duration-0-48.gif)

## 1. Get a Replicate API token

Getting your Replicate API token is a simple 3-step process:

1. Go to [https://replicate.com/signin/](https://replicate.com/signin/?ref=streamlit.ghost.io).
2. Sign in with your GitHub account.
3. Proceed to the API tokens page and copy your API token.

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-Replicate-API-token.png)

## 2. Set up the coding environment

### Local development

To set up a local coding environment, enter the following command into a command line prompt:

```
pip install streamlit replicate
```



🦙

NOTE: Make sure to have Python version 3.8 or higher pre-installed.

### Cloud development

To set up a cloud environment, deploy using the Streamlit Community Cloud with the help of the [Streamlit app template](https://github.com/streamlit/app-starter-kit?ref=blog.streamlit.io) (read more [here](https://streamlit.ghost.io/streamlit-app-starter-kit-how-to-build-apps-faster/)).

Add a `requirements.txt` file to your GitHub repo and include the following prerequisite libraries:

```
streamlit
replicate
```

## 3. Build the app

The Llama 2 chatbot app uses a total of 77 lines of code to build:

```
import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
```

### Import necessary libraries

First, import the necessary libraries:

* `streamlit` - a low-code web framework used for creating the web frontend.
* `replicate` - an ML model hosting platform that allows interfacing with the model via an API call.
* `os` - the operating system module to load the API key into the environment variable.

```
import streamlit as st
import replicate
import os
```

### Define the app title

The title of the app displayed on the browser can be specified using the `page_title` parameter, which is defined in the `st.set_page_config()` method:

```
# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")
```

### Define the web app frontend for accepting the API token

When designing the chatbot app, divide the app elements by placing the app title and text input box for accepting the Replicate API token in the sidebar and the chat input text in the main panel. To do this, place all subsequent statements under `with st.sidebar:`, followed by the following steps:

1. Define the app title using the `st.title()` method.

2. Use if-else statements to conditionally display either:

* A success message in a green box that reads `API key already provided!` for the `if` statement.
* A warning message in a yellow box along with a text input box asking for the API token, as none were detected in the Secrets, for the `else` statement.

Use nested if-else statement to detect whether the API key was entered into the text box, and if so, display a success message:

```
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
```

### Adjustment of model parameters

In continuation from the above code snippet and inside the same `with st.sidebar:` statement, we're adding the following code block to allow users to select the Llama 2 model variant to use (namely `llama2-7B` or `Llama2-13B`) as well as adjust model parameters (namely `temperature`, `top_p` and `max_length`).

```
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')
```

### Store, display, and clear chat messages

1. The first code block creates an initial session state to store the LLM generated response as part of the chat message history.
2. The next code block displays messages (via `st.chat_message()`) from the chat history by iterating through the `messages` variable in the session state.
3. The last code block creates a `Clear Chat History` button in the sidebar, allowing users to clear the chat history by leveraging the callback function defined on the preceding line.

```
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
```

### Create the LLM response generation function

Next, create the `generate_llama2_response()` custom function to generate the LLM’s response. It takes a user prompt as input, builds a dialog string based on the existing chat history, and calls the model using the `replicate.run()` function.

The model returns a generated response:

```
# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output
```

### Accept prompt input

The chat input box is displayed, allowing the user to enter a prompt. Any prompt entered by the user is added to the session state messages:

```
# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
```

### Generate a new LLM response

If the last message wasn’t from the assistant, the assistant will generate a new response. While it’s formulating a response, a spinner widget will be displayed. Finally, the assistant's response will be displayed in the chat and added to the session state messages:

```
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
```

## 4. Set the API token

### Option 1. Set the API token in Secrets

If you want to provide your users with free access to your chatbot, you'll need to cover the costs as your credit card is tied to your account.

To set the API token in the Secrets management on Streamlit Community Cloud, click on the expandable menu at the far right, then click on **Settings**:

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-Community-Cloud-settings.png)

To define the `REPLICATE_API_TOKEN` environment variable, click on the **Secrets** tab and paste your Replicate API token:

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-Community-Cloud-st-secrets.png)

Once the API token is defined in Secrets, users should be able to use the app without needing to use their own API key:

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-API-via-st-secrets-1.png)

### Option 2. Set the API token in the app

An alternative to setting the API token in Secrets is to prompt users to specify it in the app. This way, users will be notified to provide their own Replicate API token to proceed with using the app:

![](https://streamlit.ghost.io/content/images/2023/07/Llama2-API-in-app.png)

## 5. Deploy the app

Once the app is created, deploy it to the cloud in three steps:

1. Create a GitHub repository for the app.
2. In Streamlit Community Cloud, click on the `New app` button, then choose the repository, branch, and app file.
3. Click `Deploy!` and the app will be live!

## Wrapping up

Congratulations! You’ve learned how to build your own Llama 2 chatbot app using the LLM model hosted on Replicate.

It’s worth noting that the LLM was set to the 7B version and that model parameters (such as `temperature` and `top_p`) were initialized with a set of arbitrary values. This post also includes the Pro version, which allows users to specify the model and parameters. I encourage you to experiment with this setup, adjust these parameters, and explore your own variations. This can be a great opportunity to see how these modifications might affect the LLM-generated response.

For additional ideas and inspiration, check out the [LLM gallery](https://streamlit.io/gallery?category=llms&ref=blog.streamlit.io). If you have any questions, let me know in the comments below or find me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=blog.streamlit.io) or on LinkedIn at [Chanin Nantasenamat](https://www.linkedin.com/in/chanin-nantasenamat/?ref=blog.streamlit.io). You can also check out the Streamlit YouTube channel or my personal YouTube channel, [Data Professor](https://youtube.com/dataprofessor?ref=blog.streamlit.io).

Happy chatbot-building! 🦙

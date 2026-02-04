---
title: "LangChain \ud83e\udd1d Streamlit"
subtitle: "The initial integration of Streamlit with LangChain and our future plans"
date: 2023-07-11
authors:
  - "Joshua Carroll"
category: "LLMs"
---

![LangChain 🤝 Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/07/langchain-streamlit.svg)


🤝

This post was written in collaboration with the LangChain team.

Today, we're excited to announce the initial integration of Streamlit with LangChain and share our plans and ideas for future integrations.

The LangChain and Streamlit teams had previously [used](https://blog.langchain.dev/auto-eval-of-question-answering-tasks/?ref=streamlit.ghost.io) and [explored](https://streamlit.ghost.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/) each other's libraries and found that they worked incredibly well together.

* [Streamlit](https://streamlit.io/generative-ai?ref=streamlit.ghost.io) is a faster way to build and share data apps. It turns data scripts into shareable web apps in minutes, all in pure Python.
* [LangChain](https://blog.langchain.dev/?ref=streamlit.ghost.io) helps developers build powerful applications that combine LLMs with other sources of computation or knowledge.

Both libraries have a strong open-source community ethic, and a "batteries included" approach to quickly delivering a working app and iterating rapidly.

## Rendering LLM thoughts and actions

Our first goal was to create a simpler method for rendering and examining the thoughts and actions of an LLM agent. We wanted to show what takes place before the agent's final response. It's useful for both the final application (to notify the user about the process) and the development stage (to troubleshoot any problems).

The [Streamlit Callback Handler](https://python.langchain.com/docs/modules/callbacks/integrations/streamlit?ref=streamlit.ghost.io) does precisely that. Passing the callback handler to an agent running in Streamlit displays its thoughts and tool input/outputs in a compact expander format.

Try it out with this MRKL example, a popular Streamlit app:

What are we seeing here?

* An expander is rendered for each thought and tool call from the agent
* The tool name, input, and status (running or complete) are shown in the expander title
* LLM output is streamed token by token into the expander, providing constant feedback to the user
* Once finished, the tool return value is also written out inside the expander

We added this to our app with just one extra line of code:

```
# initialize the callback handler with a container to write to

st_callback = StreamlitCallbackHandler(st.container())

# pass it to the agent in the call to run()

answer = agent.run(user_input, callbacks=[st_callback])
```

For a complete walkthrough on how to get started, please refer to our [docs](https://python.langchain.com/docs/modules/callbacks/integrations/streamlit?ref=streamlit.ghost.io#installation-and-setup).

## Advanced usage

You can configure the behavior of the callback handler with advanced options available [here](https://api.python.langchain.com/en/latest/callbacks/langchain.callbacks.streamlit.streamlit_callback_handler.StreamlitCallbackHandler.html?ref=streamlit.ghost.io):

* Choose whether to expand or collapse each step when it first loads and completes
* Determine how many steps will render before they start collapsing into a "History" step
* Define custom labels for expanders based on the tool name and input

The callback handler also works seamlessly with the new [Streamlit Chat UI](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps?ref=streamlit.ghost.io), as you can see in this "chat with search" app (requires an OpenAI API Key to run):

  

🤝

View more example apps and a 1-click GitHub Codespaces setup to start hacking from our [shared repo](https://github.com/langchain-ai/streamlit-agent?ref=streamlit.ghost.io).

## Where are we going from here?

We have a few improvements in progress:

* Extend StreamlitCallbackHandler to support additional chain types like VectorStore, SQLChain, and simple streaming (and improve the default UI/UX and ease of customization).
* Make it even easier to use LangChain primitives like Memory and Messages with Streamlit chat and session\_state.
* Add more app examples and templates to [langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent?ref=streamlit.ghost.io).

We're also exploring some deeper integrations for connecting data to your apps and visualizing chain/agent state to improve the developer experience. And we're excited to collaborate and see how you use these features!

If you have ideas, example apps, or want to contribute, please reach out on the [LangChain](https://discord.gg/6adMQxSpJS?ref=streamlit.ghost.io) or [Streamlit](https://discord.gg/bTz5EDYh9Z?ref=streamlit.ghost.io) Discord servers.

Happy coding! 🎈🦜🔗

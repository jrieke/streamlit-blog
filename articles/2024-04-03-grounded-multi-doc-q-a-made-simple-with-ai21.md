---
title: "Grounded multi-doc Q&A made simple with AI21"
subtitle: "In just a few steps, build a context-based question-answering app based on your own documents and powered by AI21\u2019s RAG Engine and task-specific models"
date: 2024-04-03
authors:
  - "Robbin Jang"
category: "LLMs"
---

![Grounded multi-doc Q&A made simple with AI21](https://streamlit.ghost.io/content/images/size/w2000/2024/03/202403_blog-title-image_ai21-rag-streamlit-q-a.png)


At AI21, we’re working with developers across industries to power their question-answering apps with our task-specific models and [RAG Engine](https://www.ai21.com/blog/the-promise-of-rag-bringing-enterprise-generative-ai-to-life?ref=streamlit.ghost.io). Most developers want to build apps that provide answers grounded in a specific body of knowledge, such as their company’s documentation. This approach is called Retrieval Augmented Generation (RAG). RAG reduces hallucinations by keeping answers context-specific.

Building a RAG-based Q&A app can be complicated. Developers need to complete multiple steps to stitch together a RAG pipeline, including:

1. Connecting to a knowledge base of your documents
2. Segmenting and embed those documents into a vector store
3. Setting up semantic search capabilities for sending queries to the vector store
4. Retrieving the relevant context from the vector store and pass it to an LLM for augmented response generation

AI21’s RAG Engine and Contextual Answers task-specific model (TSM) takes care of these steps. The RAG Engine allows developers to quickly deploy a performant, scalable RAG pipeline with no manual setup. Thanks to the Contextual Answers TSM, responses are grounded and accurate, and the cost is significantly lower than leading foundation models.

🏂

Ready to jump right in? Here’s the [app](https://ai21-studio-demos.streamlit.app/?ref=streamlit.ghost.io) and [GitHub repo](https://github.com/AI21Labs/studio-demos/tree/main?ref=streamlit.ghost.io).

![A diagram of an example RAG solution package.](https://streamlit.ghost.io/content/images/2024/03/202403_blog-image_diagram_ai21-streamlit-rag-engine_001-1.png)

For developers looking to build production-ready RAG, this post will walk you through creating your own Q&A app powered by AI21’s RAG Engine and Contextual Answers TSM. A sandbox version of the app is available [here](https://ai21-studio-demos.streamlit.app/?ref=streamlit.ghost.io).

[![](https://img.spacergif.org/v1/1920x1080/0a/spacer.png)](https://streamlit.ghost.io/content/media/2024/03/streamlit_ai21.mp4)

0:00

/0:17

1×

In this post, we will:

1. Introduce the concept of a Task-Specific Model (TSM) and evaluate how AI21’s Contextual Answers TSM compares to other models for RAG-based Q&A
2. Explain how our RAG Engine provides a simple but powerful solution for deploying a RAG pipeline
3. Give you step-by-step instructions to build and run your own Q&A application powered by AI21

### **What is a TSM?**

AI21’s Task-Specific Models (TSMs) are highly specialized small language models trained to excel in specific use cases. TSMs focus on common use cases like grounded Q&A, summarization, and text editing.

The Contextual Answers TSM offers multiple advantages for RAG Q&A apps:

1. **Higher accuracy in specialized Q&A**

The Contextual Answers TSM has a very low hallucination rate, especially compared to other foundation models. It is very good at spotting irrelevancy between the context and the question, and returning “Answers are not in the documents” instead of hallucinating an answer. Less prompt engineering is needed, which results in a better user experience.

![A chart illustrating how the Contextual Answers TSM resulted in a 68% rate of “good” answers.](https://streamlit.ghost.io/content/images/2024/03/202403_blog-image_chart_ai21-rag-streamlit_TSMPerformance-1.png)

The Contextual Answers TSM resulted in a 68% rate of “good” answers.

The Contextual Answers TSM resulted in a 68% rate of “good” answers.

In fact, the Contextual Answers TSM outperformed Claude 2.1 in testing, with a 12% higher rate of “Good” answers. “Good” answers were defined as factually correct, fluent, and comprehensive.

2. **Increased safety**

Since the Contextual Answers TSM is trained for generating grounded responses, it’s more secure against prompt injection and other abuse from bad actors.

3. **Lower latency and cost** **compared to other foundation models**

Using foundation models like GPT-4 at scale can be extremely expensive. The Contextual Answers TSM is significantly cheaper to use and scale.

![A chart showing the cost difference between GPT-4 and Contextual Answers TSM.](https://streamlit.ghost.io/content/images/2024/03/202403_blog-image_chart_ai21-rag-streamlit_TSMCost-1.png)

### **What is AI21’s RAG Engine?**

Building a RAG pipeline may seem easy, but scaling your pipeline while maintaining performance is difficult. When developers use a variety of different models and processes, orchestration is challenging. Multiple areas impact RAG performance, including:

* Efficiency of chunking and embedding processes
* Support for multiple file types
* Scaling as data volume increases

AI21's RAG Engine offers a scalable all-in-one solution accessible via API. The Contextual Answers TSM seamlessly plugs into the RAG Engine, creating an end-to-end pipeline.

Learn more about the RAG Engine in [this blog post](https://www.ai21.com/blog/the-promise-of-rag-bringing-enterprise-generative-ai-to-life?ref=streamlit.ghost.io).

**Architecture Diagram**

![An architecture diagram for the application in this tutorial.](https://streamlit.ghost.io/content/images/2024/03/202403_blog-image_diagram_ai21-rag-streamlit_architecture-diagram.png)

### On Streamlit Community Cloud

You can check out a hosted version of the app on Streamlit Community Cloud [here](https://ai21-studio-demos.streamlit.app/Multi_Document_Q&A?ref=streamlit.ghost.io). Read on to learn how you can build you own.

### Build your own Q&A app powered by a task-specific small language model

This app allows you to upload a PDF or `.txt` file and ask questions to your uploaded document as a knowledge base.

To build and run your own version of our application locally, clone the GitHub [repo](https://github.com/AI21Labs/studio-demos?ref=streamlit.ghost.io) and use your AI21 credentials.

1. Request your AI21 Studio account: [https://studio.ai21.com/login](https://studio.ai21.com/login?ref=streamlit.ghost.io)
2. Locate your AI21 API Key: [https://studio.ai21.com/account/api-key](https://studio.ai21.com/account/api-key?ref=streamlit.ghost.io)
3. Create `secrets.toml` in a `.streamlit` folder and add your credentials, replacing `<YOUR_API_KEY>` with your AI21 API Key:

   ```
   [api-keys]
   ai21-api-key = "<YOUR_API_KEY>"
   ```
4. Install all dependencies listed in the requirements.txt, including AI21 Labs Python SDK
5. Run [Welcome.py](http://welcome.py/?ref=streamlit.ghost.io) by entering streamlit run Welcome.py in your console
6. The Welcome page of the AI21 Studio Streamlit app should be opened in your browser once you run the command above
7. Navigate to the Multi Document Q&A page

### Breaking down the app

1. Import AI21 library and load credentials:

   ```
   # import AI21 SDK library
   from ai21 import AI21Client

   # initiate AI21 client with your API key
   client = AI21Client(api_key=st.secrets['api-keys']['ai21-api-key'])
   ```
2. Upload files to AI21 Document Library with document labels (optional):

   ```
   # Streamlit file uploader widget
   uploaded_files = st.file_uploader("choose .pdf/.txt file",
      accept_multiple_files=True,
      type=["pdf", "text", "txt"],
      key="a")

   # upload the files to AI21 RAG Engine library
   for uploaded_file in uploaded_files:
      client.library.files.create(file_path=uploaded_file, labels=label)
   ```
3. Ask questions against the uploaded documents with AI21 Contextual Answers model:

   ```
   # Streamlit text input widget 
   question = st.text_input(label="Question:", value="Your Question")

   # send your question to AI21 Contextual Answers LLM and getting back the response
   response = client.library.answer.create(question=question, label=label)
   ```

### **Wrapping up**

We hope this guide makes it straightforward to build a grounded, contextual Q&A application. With this app, users can interact with complex bodies of knowledge to improve workflows like customer support, contract analysis, product optimization, and more.

For Streamlit users, AI21 is excited to offer an extended Starter Bundle that provides free credits for our AI21 Studio playground and a guided 1:1 session to discuss your use case and help you get started.

If you have any questions, please post them in the comments below, reach out to [studio@ai21.com](mailto:studio@ai21.com), or create a [GitHub Issue](https://github.com/AI21Labs/studio-demos/issues?ref=streamlit.ghost.io).

---
title: "snowChat: Leveraging OpenAI's GPT for SQL queries"
subtitle: "Interact with your Snowflake database using natural language queries"
date: 2023-07-25
authors:
  - "kaarthik Andavar"
category: "Snowflake powered \u2744\ufe0f"
---

![snowChat: Leveraging OpenAI's GPT for SQL queries](https://streamlit.ghost.io/content/images/size/w2000/2023/07/snowchat.svg)


Hey, fellow tech enthusiasts! 👋

I'm Kaarthik, an analytics engineer with a passion for building innovative AI applications. My expertise lies at the intersection of AI and data, where I explore and refine the power of AI to redefine data-driven solutions.

Do you struggle with complex SQL queries? Are you lost in a sea of tables while trying to locate a single piece of data? Fear not, for I have created snowChat to solve these problems!

In this post, I'll show you:

* How to embed a Snowflake schema into a vector database
* How to create a conversational chain using LangChain
* How to connect the chain response to Snowflake
* How to design a chat-like interface using Streamlit
* How to deploy your solution to the Streamlit Community Cloud

❄️

Ready to leap right in? Check out the [app](https://snowchat.streamlit.app/?ref=streamlit.ghost.io) and the full [code](https://github.com/kaarthik108/snowChat?ref=streamlit.ghost.io).

But first, let's talk about…

## What is snowChat?

snowChat is a powerful and user-friendly application that enables users to interact with their Snowflake DataBase using natural language queries.

snowChat leverages OpenAI's GPT model to convert natural language into SQL queries, making it ideal for users who may not have a firm grasp of SQL syntax. And it has a  transformative impact on data interaction by expediting and streamlining data-driven decision-making.

Let's take a look at the tech stack on which snowChat is built:

* **Streamlit:** The UI magic
* **Snowflake**: The database powerhouse
* **GPT-3.5 and LangChain**: The language model maestros
* **Supabase**: The vector database virtuoso

Here's a glance at snowChat's architecture:

![snowchat-architecture](https://streamlit.ghost.io/content/images/2023/07/snowchat-architecture.png#border)

All set? Let's get cracking!

## How to embed Snowflake schema into a vector database

To start, follow these steps:

* Clone the GitHub repo
* Run `pip install -r requirements.txt` to install all the required packages
* Get the Data Definition Language (DDL) for all tables from `snowflake.account_usage.tables`:

```
OPENAI_API_KEY=

#snowflake
ACCOUNT=
USER_NAME=
PASSWORD=
ROLE=
DATABASE=
SCHEMA=
WAREHOUSE=

SUPABASE_URL=
SUPABASE_SERVICE_KEY=
```

* Use ChatGPT to convert the DDL to markdown format.
* Store the schema files for each table in the `docs/` folder.
* Create an account with [Supabase](https://supabase.io/?ref=streamlit.ghost.io), set up a free database, and configure environment variables for the `.streamlit` folder in `secrets.toml` (remember to include your Snowflake credentials).

Your final `secrets.toml` should look like this:

```
[streamlit]
SUPABASE_URL = "<https://yourapp.supabase.co>"
SUPABASE_KEY = "yourkey"

[snowflake]
SNOWFLAKE_ACCOUNT = "youraccount"
SNOWFLAKE_USER = "youruser"
SNOWFLAKE_PASSWORD = "yourpassword"
SNOWFLAKE_DATABASE = "yourdatabase"
SNOWFLAKE_SCHEMA = "yourschema"
SNOWFLAKE_WAREHOUSE = "yourwarehouse"
```

* Run the Supabase scripts found under `supabase/scripts.sql` in the Supabase SQL editor to activate the `pgvector` extension, create tables and set up a function.
* Run `python ingest.py` to convert your documents into vectors and store them in the Supabase table named 'documents.'

The 'documents' table in Supabase should look like this:

```
| id | vector   | contents         |
|----|----------|------------------|
| 1  | [1,2,3]  | This is document |
| 2  | [4,5,6]  | This is another  |
| 3  | [7,8,9]  | This is a third   |
```

![supabase-table](https://streamlit.ghost.io/content/images/2023/07/supabase-table.png#browser)

Et voila, the left part of the architecture is done!

## How to create a conversational chain using LangChain

The core of snowChat is the "chain" function, which manages OpenAI's GPT model, the embedding model, the vector store, and the prompt templates. This functionality is encapsulated in [LangChain](https://github.com/hwchase17/langchain?ref=streamlit.ghost.io).

The chain function takes user input, applies a prompt template to format it, and then passes the formatted response to an LLM with context retrieved from the vector store:

```
def get_chain(vectorstore):
    """
    Get a chain for chatting with a vector database.
    """
    q_llm = OpenAI(
        temperature=0,
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        model_name="gpt-3.5-turbo-16k",
    )

    llm = ChatOpenAI(
				temperature=0,
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        model_name="gpt-3.5-turbo",
    )

    question_generator = LLMChain(llm=q_llm, prompt=condense_question_prompt)

    doc_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=QA_PROMPT)
    chain = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
    )
    return chain
```

Your `get_chain` function is now ready to use. Simply run `chain = get_chain(SupabaseVectorStore)` and start your fun with `chain({"question": "Did you understand the chain?", "chat_history": chat_history})`.

## How to connect the chain response to Snowflake

After creating the chain, use this code to destructure the response from the answer key:

```
result = chain({"question": query, "chat_history": chat_history})

response = result['answer']
```

The `response` variable contains both SQL and an explanation. A helper function called `get_sql` extracts only the SQL code from the response. Once the SQL is obtained, it's sent to Snowflake (Snowpark) to fetch the data and create a DataFrame object.

There are two possible outcomes:

1. The model generates the SQL **correctly**: Display the output directly in Streamlit.
2. The model generates the SQL **incorrectly**: Send it back to the GPT model along with the error message and the SQL it generated (self-healing). This way, the model can correct its mistake and return the corrected response.

With this setup, the model is ready to work in full.

## How to design a chat-like interface using Streamlit

Moving on to the design phase, let's shape up the chat interface.

![chat-like-interface](https://streamlit.ghost.io/content/images/2023/07/chat-like-interface.png#browser)

The input will be designed using the `st.chat_input()` container from Streamlit's chat element:

```
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
```

A helper function called `message_func` takes care of the styling for each message, including avatars on the side.

Following the steps outlined, you should have a fully functional chat app ready!

```
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
```

## How to deploy to the Streamlit Community Cloud

Let's bring snowChat to the world! To get started, head to [Community Cloud](https://share.streamlit.io/?ref=streamlit.ghost.io), click "Create a new app," select your GitHub repo, and deploy. Don't forget to add the necessary secrets to the settings.

Congratulations! Now you can chat with your Snowflake data.

## Wrapping up

That's a wrap, folks! In this post, we've discussed building snowChat, an intuitive tool that leverages the power of OpenAI's GPT to convert natural language into SQL queries. By breaking down the intimidating walls of SQL syntax, snowChat fosters swift and effective data-driven decisions, even for those not well-versed in SQL.

I hope snowChat will increase your productivity and impress you with its cool functionalities (see what we did there? 😜). If you have any questions or doubts, please post them in the comments below or contact me on [GitHub](https://github.com/kaarthik108?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/kaarthik-andavar-b32a27143/?ref=streamlit.ghost.io), or [Twitter](https://twitter.com/kaarthikcodes?ref=streamlit.ghost.io).

Happy Streamlit-ing, and keep it cool! ❄️🎈

---
title: "How to build a real-time LLM app without vector databases"
subtitle: "Create a discount finder app using Pathway and Streamlit in 10 steps"
date: 2023-10-20
authors:
  - "Bobur Umurzokov"
category: "LLMs"
---

![How to build a real-time LLM app without vector databases](https://streamlit.ghost.io/content/images/size/w2000/2023/10/Screenshot-2023-10-16-at-10.05.16-AM.png)


👉

****TL;DR:**** Learn how to build a discount finder app ****without**** using vector databases, additional frameworks, and a complex stack. Use the [project source code](https://github.com/Boburmirzo/chatgpt-api-python-sales?ref=streamlit.ghost.io) to clone the repo and run the code sample by following the instructions in the [README.md](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/README.md?ref=streamlit.ghost.io) file.

Ever tried asking ChatGPT a question about real-time discounts, deals, or coupons?

For example, “Can you give me discounts for Adidas men's shoes?” If you did, I’m sure you’ve been frustrated by the generic response it gave you, “I’m sorry, but I don’t have real-time growing capabilities or access to current promotion.”

Why? Because GPT **lacks specific information**.

**Challenges of Existing Solutions**

You could try typing in a single JSON item from the [Amazon products deal](https://www.rainforestapi.com/docs/product-data-api/overview?ref=streamlit.ghost.io), but you’ll face two problems:

1. **Text length.** The text length is restricted—a big problem when dealing with thousands of sale items.
2. **Unusable data.** The data may need to be cleaned and formatted.

[![](https://img.spacergif.org/v1/1920x1080/0a/spacer.png)](https://streamlit.ghost.io/content/media/2023/10/ChatGPTNotRespond.mp4)

0:00

/0:20

1×

You could also try using the OpenAI [Chat Completion endpoint](https://platform.openai.com/docs/api-reference/chat?ref=streamlit.ghost.io) or building custom plugins, but you’ll face additional problems:

1. **Cost.** Providing more detailed information and examples to improve the model's performance can increase costs. For example, with GPT-4, the cost is $0.624 per prediction for an input of 10k tokens and an output of 200 tokens. Sending identical requests repeatedly can escalate costs unless you use a local cache system.
2. **Latency.** Utilizing ChatGPT APIs for production, like those from OpenAI, can be unpredictable in terms of latency. There is no guarantee of consistent service provision.
3. **Security.** Integrating custom plugins requires specifying every API endpoint in the [OpenAPI spec](https://platform.openai.com/docs/plugins/getting-started?ref=streamlit.ghost.io) for functionality. This means exposing your internal API setup to ChatGPT, which may be a risk that many enterprises are skeptical of.
4. **Offline evaluation.** When you conduct offline tests on code and data output or replicate the data flow locally, each system request may yield varying responses.

To solve these challenges (and to buy cool Adidas shoes at a discount, of course! 👟), I built a custom Language Learning Model (LLM) discount finder app **without** using vector databases, additional frameworks, and a complex stack.

The same solution can be applied to develop production-ready AI apps that use real-time data available in your data sources.

In this post, I’ll walk through 10 steps on how to develop and expose an AI-powered HTTP REST API using [Pathway](https://pathway.com/?ref=streamlit.ghost.io) and [LLM App](https://github.com/pathwaycom/llm-app?ref=streamlit.ghost.io) and design the UI with Streamlit to consume the API data through REST.

### The role of Pathway and LLM App

**Pathway** is a powerful data processing framework in Python that takes care of real-time data updates from various data sources using its built-in connectors for structured, unstructured, and live data. For the discount finder app, I used Pathway to ingest sales data as streams to app and make sure that the app detects every change in a data input that changes frequently.

**LLM App** is a production Python framework for building and serving AI applications. LLM App uses Pathway libraries under the hood to achieve real-time data indexing and vector similarity search. Using a combination of these two tools, the app is not only aware of changes in the documents but also updates vector indexes in real time and uses this new knowledge to answer the next questions without the need for storing and retrieving vector indexes to/from a vector database.

### Overall app architecture

Let’s take a look at the app’s overall architecture. I was inspired by [this article](https://www.pathway.com/blog/building-enterprise-search-apis-with-llms-for-production?ref=streamlit.ghost.io) and wanted my app to expose the HTTP REST API endpoint—so you could get the best deals by using CSVs, JSON Lines, APIs, message brokers, or databases.

The app supports two types of data sources (if you want, you can add custom input connectors):

* **JSON Lines:** The data source expects each line to contain a `doc` object. Make sure to convert your input data to the Jsonlines format. You can find a sample data file at [discounts.jsonl](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/data/csv_discounts.jsonl?ref=streamlit.ghost.io).
* [Rainforest Product API](https://www.rainforestapi.com/docs/product-data-api/overview?ref=streamlit.ghost.io): This API gives you the daily discount data from [Amazon products](https://www.amazon.com/deals?ref=streamlit.ghost.io).

![](https://streamlit.ghost.io/content/images/2023/10/pathway-streamlit-1.png)

Go to the app and try typing in “Show me discounts”:

[![](https://img.spacergif.org/v1/1920x1080/0a/spacer.png)](https://streamlit.ghost.io/content/media/2023/10/Discountstwosources.mp4)

0:00

/0:23

1×

The app will index [Rainforest API](https://www.rainforestapi.com/docs/product-data-api/overview?ref=streamlit.ghost.io) and an example `discounts.csv` file documents in real-time and use the data when processing queries.

## How to build a real-time discount tracking app

### **Step 1. Data collection (custom data ingestion)**

To add custom data for ChatGPT, you need to build a data pipeline for ingesting, processing, and exposing data in real-time.

For simplicity, use any [JSON Lines](https://jsonlines.org/?ref=streamlit.ghost.io) file as a data source. The app accepts files like [discounts.jsonl](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/data/rainforest_discounts.jsonl?ref=streamlit.ghost.io) and uses this data when processing user queries. Each line in the data source should contain a `doc` object. Make sure to convert your input data to JSON Lines format.

Here is an example of a JSON Lines file with a single entry:

```
{"doc": "{'position': 1, 'link': '<https://www.amazon.com/deal/6123cc9f>', 'asin': 'B00QVKOT0U', 'is_lightning_deal': False, 'deal_type': 'DEAL_OF_THE_DAY', 'is_prime_exclusive': False, 'starts_at': '2023-08-15T00:00:01.665Z', 'ends_at': '2023-08-17T14:55:01.665Z', 'type': 'multi_item', 'title': 'Deal on Crocs, DUNLOP REFINED(\\u30c0\\u30f3\\u30ed\\u30c3\\u30d7\\u30ea\\u30d5\\u30a1\\u30a4\\u30f3\\u30c9)', 'image': '<https://m.media-amazon.com/images/I/41yFkNSlMcL.jpg>', 'deal_price_lower': {'value': 35.48, 'currency': 'USD', 'symbol': '$', 'raw': '35.48'}, 'deal_price_upper': {'value': 52.14, 'currency': 'USD', 'symbol': '$', 'raw': '52.14'}, 'deal_price': 35.48, 'list_price_lower': {'value': 49.99, 'currency': 'USD', 'symbol': '$', 'raw': '49.99'}, 'list_price_upper': {'value': 59.99, 'currency': 'USD', 'symbol': '$', 'raw': '59.99'}, 'list_price': {'value': 49.99, 'currency': 'USD', 'symbol': '$', 'raw': '49.99 - 59.99', 'name': 'List Price'}, 'current_price_lower': {'value': 35.48, 'currency': 'USD', 'symbol': '$', 'raw': '35.48'}, 'current_price_upper': {'value': 52.14, 'currency': 'USD', 'symbol': '$', 'raw': '52.14'}, 'current_price': {'value': 35.48, 'currency': 'USD', 'symbol': '$', 'raw': '35.48 - 52.14', 'name': 'Current Price'}, 'merchant_name': 'Amazon Japan', 'free_shipping': False, 'is_prime': False, 'is_map': False, 'deal_id': '6123cc9f', 'seller_id': 'A3GZEOQINOCL0Y', 'description': 'Deal on Crocs, DUNLOP REFINED(\\u30c0\\u30f3\\u30ed\\u30c3\\u30d7\\u30ea\\u30d5\\u30a1\\u30a4\\u30f3\\u30c9)', 'rating': 4.72, 'ratings_total': 6766, 'page': 1, 'old_price': 49.99, 'currency': 'USD'}"}
```

The app is always aware of the changes in the [data](https://github.com/Boburmirzo/chatgpt-api-python-sales/tree/main/examples/data?ref=streamlit.ghost.io) folder. If you add another JSON Lines file, it will automatically update the AI model's response.

### **Step 2. Data loading and mapping**

Using Pathway's [JSON Lines input connector](https://pathway.com/developers/api-docs/pathway-io-jsonlines/?ref=streamlit.ghost.io), read the local JSON Lines file, map data entries into a [schema](https://pathway.com/developers/user-guide/introduction/types/?ref=streamlit.ghost.io#data-types-and-schemas), and create a Pathway [Table](https://pathway.com/developers/api-docs/pathway-table/?ref=streamlit.ghost.io) (see the full source code in [app.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/api/app.py?ref=streamlit.ghost.io)):

```
...
sales_data = pw.io.jsonlines.read(
    "./examples/data",
    schema=DataInputSchema,
    mode="streaming"
)
```

Map each data row into a structured document schema (see the full source code in [app.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/app.py?ref=streamlit.ghost.io)):

```
class DataInputSchema(pw.Schema):
    doc: str
```

### **Step 3. Data embedding**

Each document is [embedded](https://platform.openai.com/docs/guides/embeddings?ref=streamlit.ghost.io) with the OpenAI API and retrieves the embedded result (see the full source code in [embedder.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/common/embedder.py?ref=streamlit.ghost.io)):

```
...
embedded_data = embeddings(context=sales_data, data_to_embed=sales_data.doc)
```

### **Step 4. Data indexing**

Construct an instant index on the generated embeddings:

```
index = index_embeddings(embedded_data)
```

### **Step 5. User query processing and indexing**

Create a REST endpoint, take a user query from the API request payload, and embed the user query with the OpenAI API.

```
...
query, response_writer = pw.io.http.rest_connector(
    host=host,
    port=port,
    schema=QueryInputSchema,
    autocommit_duration_ms=50,
)

embedded_query = embeddings(context=query, data_to_embed=pw.this.query)
```

### **Step 6. Similarity search and prompt engineering**

To perform a similarity search, utilize the index to identify the most relevant matches for the query embedding. Then create a prompt that combines the user's query with the retrieved relevant data results. This prompt is then sent to the ChatGPT completion endpoint to generate a comprehensive and detailed response.

```
responses = prompt(index, embedded_query, pw.this.query)
```

You used the same in-context learning approach when creating the prompt and incorporated internal knowledge into ChatGPT in the [prompt.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/common/prompt.py?ref=streamlit.ghost.io) file.

```
prompt = f"Given the following discounts data: \\\\n {docs_str} \\\\nanswer this query: {query}"
```

### **Step 7. Return the response**

The final step is just to return the API response to the user.

```
# Build prompt using indexed data
responses = prompt(index, embedded_query, pw.this.query)
```

### **Step 8. Put everything together**

Combine all the steps to get a Python API enabled with LLM for custom discount data. You can use it by referring to the implementation in the [app.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/api/app.py?ref=streamlit.ghost.io) Python script.

```
import pathway as pw

from common.embedder import embeddings, index_embeddings
from common.prompt import prompt

def run(host, port):
    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Real-time data coming from external data sources such as jsonlines file
    sales_data = pw.io.jsonlines.read(
        "./examples/data",
        schema=DataInputSchema,
        mode="streaming"
    )

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=sales_data, data_to_embed=sales_data.doc)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()

class DataInputSchema(pw.Schema):
    doc: str

class QueryInputSchema(pw.Schema):
    query: str
```

### Step 9. Design the UI with Streamlit

Use Streamlit to make your app more interactive (refer to the implementation in the [app.py](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/examples/ui/app.py?ref=streamlit.ghost.io) file). You can build UI for your backend services without having knowledge of front-end tools. The use of Streamlit's **`st.sidebar`** allows for the organization of secondary information, keeping the main area focused on the primary interaction. You create a sidebar to explain to users how to use the app:

```
with st.sidebar:
    st.markdown(
        "## How to use\\n"
        "1. Choose data sources.\\n"
        "2. If CSV is chosen as a data source, upload a CSV file.\\n"
        "3. Ask a question about the discounts.\\n"
    )
```

Users are presented with a multi-select dropdown to choose data sources, and if CSV is chosen, they can upload a CSV file via the **`st.file_uploader`** widget. Streamlit's declarative nature stands out in the code, with the interface updating based on the state of variables. For example, the file uploader's **`disabled`** state is linked to the selected data sources.

```
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=("csv"),
    disabled=(DataSource.CSV.value not in data_sources)
)
```

Once a CSV file is uploaded, its content is processed and written into a **`jsonlines`** file format, displaying a progress bar to inform the user of the ongoing operation. and the progress bar offers real-time feedback while processing the uploaded CSV.

```
if uploaded_file and DataSource.CSV.value in data_sources:
    df = pd.read_csv(uploaded_file)

    # Start progress bar
    progress_bar = st.progress(0, "Processing your file. Please wait.")
```

Depending on the selected data sources and the provided question, the application interfaces with a Discounts API to fetch relevant answers.

```
question = st.text_input(
    "Search for something",
    placeholder="What discounts are looking for?",
    disabled=not data_sources
)
```

Here is the code that handles Discounts API requests when the user selects a data source and asks a question. Error messages and responses from the API are handled smoothly, giving direct feedback to the user through **`st.error`** and **`st.write`** methods.

```
if data_sources and question:
    if not os.path.exists(csv_path) and not os.path.exists(rainforest_path):
        st.error("Failed to process discounts file")

    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Discounts API. Status code: {response.status_code}")
```

### Step 10. Run the app

Follow the instructions in the [README.md](https://github.com/Boburmirzo/chatgpt-api-python-sales/blob/main/README.md?ref=streamlit.ghost.io) file's **How to run the project** section to run the app. Note that you’ll need to run the API and UI as separate processes. Streamlit will automatically connect to the Discounts backend API, and you’ll see the UI frontend running in your browser.

![](https://streamlit.ghost.io/content/images/2023/10/discounts-tracker-streamlit-1.png)

In this tutorial, Pathway's LLM App and Streamlit communicate over HTTP REST API. You can run the app using Docker with a single `docker compose up` command (refer to the [run with the Docker](https://github.com/Boburmirzo/chatgpt-api-python-sales?ref=streamlit.ghost.io#run-with-docker) section in the [README.md](http://readme.md/?ref=streamlit.ghost.io) file). The inability to embed the LLM App into Streamlit as a single process is due to Streamlit having its own program lifecycle loop, which triggers a complete app rerun whenever there is a change. This behavior can disrupt the data flow, especially since Pathway operates in streaming mode. Considering the above, there are two more ways to integrate Pathway's LLM app with Streamlit:

1. Run Pathway's LLM app as a subprocess and communicate with it over inter-process communications such as sockets or TCP/IP. This can involve using random ports or signals to trigger actions like state dumps that can be picked up or pickled. For example, you can leverage Python’s [Subprocess](https://docs.python.org/3/library/subprocess.html?ref=streamlit.ghost.io) module to achieve that.
2. Pathway's LLM App and Streamlit share the same file storage to communicate. For example, you upload documents with a user query to a folder on your local disk. LLM App can listen to every change in that folder and access the files to process them, answer user queries, and write responses back to the file.

## Wrapping up

I’ve only scratched the surface of what you can do with an [LLM app](https://github.com/pathwaycom/llm-app?ref=streamlit.ghost.io) by incorporating domain-specific knowledge like discounts into ChatGPT. You can also:

* Incorporate additional data from external APIs, formats such as JSON Lines, PDF, Doc, HTML, or text, and databases like PostgreSQL or MySQL.
* Stream data from platforms like Kafka, Redpanda, or Debedizum.
* Enhance the Streamlit UI to accept any deals API, not just the Rainforest API.
* Maintain a data snapshot to observe changes in sales prices over time. [Pathway](https://pathway.com/?ref=streamlit.ghost.io) provides a built-in feature to calculate differences between two alterations.
* Send processed data to other downstream connectors, such as BI and analytics tools. For example, you can configure it to receive alerts when price shifts are detected.

If you have any questions, please leave them in the comments section below or contact me on [LinkedIn](https://www.linkedin.com/in/boburumurzokov/?ref=streamlit.ghost.io) and [Twitter](https://twitter.com/BoburUmurzokov?ref=streamlit.ghost.io). Join the [Discord channel](https://discord.com/invite/pathway?ref=streamlit.ghost.io) to see how the **AI ChatBot assistant** works.

Happy Streamlit-ing! 🎈

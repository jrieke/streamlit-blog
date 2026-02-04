---
title: "How to build a movie recommendation app without the complexities of vector databases"
subtitle: "Use the Streamlit-Weaviate Connection to integrate a vector database"
date: 2024-09-10
authors:
  - "Liz Acosta"
category: "AI Recipes"
---

![How to build a movie recommendation app without the complexities of vector databases](https://streamlit.ghost.io/content/images/size/w2000/2024/09/2024-recipe-weaviate-formatted-title-image.png)


You are what you eat; your model is what your model ingests.

Not only does data inform AI systems, data is the output you ultimately receive. That’s why it’s important to have “good” data. It doesn’t matter how powerful your model is, garbage in will always result in garbage out.

In software development, this isn’t a new concept or problem. However, AI demands a more sophisticated data strategy throughout the ETL process. This can slow the delivery of your AI-integrated applications.

In this recipe, you’ll use Weaviate to abstract away the complexity associated with vector databases, allowing you to implement a powerful search and recommendation system with way less technical overhead. Then we’ll use Streamlit to build the chatbot part of the app.

And don’t panic! There’s no frontend involved!

Read on to learn:

* What Weaviate is
* What Streamlit is
* How to build a demo Weaviate movie recommendation Streamlit app
* How to query a Collection in Weaviate Cloud

Don’t feel like reading? Here are some other ways to explore this demo:

* [Find the code in the Streamlit Cookbook repo](https://github.com/streamlit/cookbook/tree/main/recipes/weaviate?ref=streamlit.ghost.io)
* [Watch a video walkthrough](https://www.youtube.com/watch?v=SQD-aWlhqvM&ref=streamlit.ghost.io) with Weaviate technical curriculum developer, JP Hwang
* [Check out a deployed version of the app](https://weaviate-movie-magic.streamlit.app/?ref=streamlit.ghost.io) or see the embedded app below (click to view it in full frame):




## What is Weaviate?

[Weaviate](https://weaviate.io/?ref=streamlit.ghost.io) is an AI-native database designed to help you build amazing, scalable, and production-grade AI-powered applications. It offers robust features for data storage, retrieval, and querying as well as integrations with AI models, making it an excellent choice for developers looking to integrate AI capabilities into their apps.

### The Streamlit-Weaviate Connection

The [Streamlit-Weaviate connection](https://github.com/weaviate/st-weaviate-connection?ref=streamlit.ghost.io) is a wrapper that simplifies the process of integrating Weaviate with Streamlit applications. This connection allows you to perform various operations, such as connecting to a remote or local Weaviate instance, performing queries, and using the underlying Weaviate Python client. The project is open-source so contributions are always welcome.

**Key features**

* **Connect to a Weaviate Cloud instance:** Easily connect to a Weaviate cloud instance using a URL and API key
* **Perform queries:** Execute simple and advanced queries using the query or GraphQL query methods
* **Use the Weaviate Python client:** Leverage the full capabilities of the Weaviate Python client for more complex operations
* **Support for local instances:** Connect to a local Weaviate instance using default parameters
* **Secrets management:** Streamlit can handle secret management for secure connections

## What is Streamlit?

Streamlit is an open-source Python framework to build highly interactive apps – in only a few lines of code. Streamlit integrates with all the latest tools in [generative AI](https://streamlit.io/generative-ai?ref=streamlit.ghost.io), such as any LLM, vector database, or various AI frameworks like [LangChain](https://streamlit.ghost.io/langchain-streamlit/), [LlamaIndex](https://streamlit.ghost.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/), or Weights & Biases. Streamlit’s [chat elements](https://docs.streamlit.io/develop/api-reference/chat?ref=streamlit.ghost.io) make it especially easy to interact with AI so you can build chatbots that “talk to your data.”

Combined with a platform like Replicate, Streamlit allows you to create generative AI applications without any of the app design overhead.

To learn more about Streamlit, [check out the 101 guide](https://streamlit.ghost.io/streamlit-101-python-data-app/).

💡

To learn more about how Streamlit biases you toward forward progress, check out this [blog post](https://streamlit.ghost.io/just-build-it-streamlit-opinionated-framework/).

## Try the app recipe: Weaviate + Streamlit

In this demo, you’ll spin up a movie recommendation app that utilizes Weaviate for backend data management and Streamlit chat elements on the frontend for interaction. The app accepts a natural language input from a user and uses Weaviate to translate the input into a query and then generate a list of movie titles.

There are three different kinds of search modes available:

**Keyword:** This search mode uses BM25 to rank documents based on the relative frequencies of search terms. In this particular app, that means the results returned are based on how often the search keywords appear in the different movie properties.

**Semantic:** This type of search uses vectors to generate results based on their similarity to your search query. In other words, the results returned are based on a similarity of “meaning.” To learn more about vector databases, check out Weaviate’s [*Gentle Introduction to Vector Databases*](https://weaviate.io/blog/what-is-a-vector-database?ref=streamlit.ghost.io).

**Hybrid:** A hybrid search combines vector and BM25 searches to offer best-of-both-worlds search results.

### Prerequisites

* Python >=3.8, !=3.9.7
* [A Weaviate sandbox instance](http://console.weaviate.cloud/?ref=streamlit.ghost.io)  
  (This will give you the API and URL to use in the code as well)
* [A Cohere API key](https://dashboard.cohere.com/welcome/register?ref=streamlit.ghost.io)

In this app, the Cohere API is used for two different operations:

* To summarize the query results into a natural language recommendation
* [To transform the MovieDemo data and queries into high-dimensional vector representations](https://weaviate.io/developers/weaviate/model-providers/cohere?ref=streamlit.ghost.io) for the semantic and hybrid search modes

Please note that both [Weaviate](https://weaviate.io/pricing?ref=streamlit.ghost.io) and [Cohere](https://docs.cohere.com/docs/rate-limits?ref=streamlit.ghost.io) have limits on their trial accounts. Check their websites for more details.

💡

To learn more about API keys, check out the blog post [here](https://streamlit.ghost.io/8-tips-for-securely-using-api-keys/).

### Environment setup

**Local setup: Create a virtual environment**

1. Clone the Cookbook repo: git clone `https://github.com/streamlit/cookbook.git`
2. From the Cookbook root directory, change directory into the recipe: `cd recipes/weaviate
3. Add the necessary secrets to the .streamlit/secrets\_template.toml file:

   ```
   WEAVIATE_API_KEY = "your weaviate key goes here"
   WEAVIATE_URL = "your weaviate url goes here"
   COHERE_API_KEY = "your cohere api key goes here"
   ```
4. Update the filename from secrets\_template.toml to secrets.toml: `mv .streamlit/secrets_template.toml .streamlit/secrets.toml`  
   (To learn more about secrets handling in Streamlit, refer to the documentation [here](https://docs.streamlit.io/develop/concepts/connections/secrets-management?ref=streamlit.ghost.io).)
5. Create a virtual environment: `python3 -m venv weaviatevenv`
6. Activate the virtual environment: `source weaviatevenv/bin/activate`
7. Install the dependencies: `pip install -r requirements.txt`

**Add data to your Weaviate Cloud**

1. Create a Weaviate Cloud [Collection](https://weaviate.io/developers/weaviate/config-refs/schema?ref=streamlit.ghost.io#introduction) and add data to it: `python3 helpers/add_data.py`
2. (Optional) Verify the data: `python3 helpers/verify_data.py`

### Query the MovieDemo collection in Weaviate Cloud

You can access the [Query](https://weaviate.io/developers/weaviate/connections/connect-query?ref=streamlit.ghost.io#example-query) panel via the Weaviate Cloud UI.

1. Copy and paste the following query in the editor:

   ```
   { Get 
   {MovieDemo (limit: 3 where: {
   	path: ["release_year"],
   	operator: Equal,
   	valueInt: 1985}){
   budget
   movie_id
   overview
   release_year
   revenue
   tagline
   title
   vote_average
   }}}
   ```
2. Click on the arrow to execute the query

![A screenshot of the Weaviate Cloud UI and Query tool.](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdufPHaFscBz3WAEP943zzLzF8l5Ylt4rSiX-sSWMhbmcGr7C5M-TbkJCc0PjfCEn-f9gLx7aosweXHGfdRJVFtvFQHMP4-bMQs6I4q3Tljh2NQ0vZWdqgYx4oTBPsQiBfTehWYWNMXGw5232Rx5hoFQP1v?key=I3XPnLBZfnTKn4Hrum-sGA)

The Weaviate Cloud Query tool is a browser-based GraphQL IDE. In the example query above, we are telling Weaviate to return the `budget, movie_id, overview, release_year, revenue, tagline, title, vote_average, vote_count` properties for the objects in the MovieDemo collection with a `release_year` of `1985`. We do this by setting the `path` to `["release_year"]`, the `operator` to `Equal`, and the `valueInt` to `1985`.  We also limit the query results to three objects with `limit: 3`.

You should get back a result of three movies with the release year 1985.

This is a simple query that forms the foundation of more complex queries. To learn more about different kinds of searches available with the Weaviate Cloud Query tool, [check out the documentation](https://weaviate.io/developers/weaviate/search/basics?ref=streamlit.ghost.io).

### Run the demo Weaviate Streamlit recommendation app

To run the demo app, use the Streamlit CLI: `streamlit run demo_app.py`.

Running this command deploys the app to a port on `localhost`. When you access this location, you should see a Streamlit app running. Please note that this version of the demo app does not feature the poster images so it will look different from the [deployed app](https://weaviate-movie-magic.streamlit.app/?ref=streamlit.ghost.io).

![](https://streamlit.ghost.io/content/images/2024/09/weaviate-movie-recommendation-app-demo.gif)

### Vector databases made easy

Using Streamlit-Weaviate Connection means you can easily create and integrate vector databases in your Streamlit apps.

In `demo_app.py`, the Weaviate connection is created here:

```
def setup_weaviate_connection(env_vars):
    """Setup Weaviate connection"""
    return st.connection(
        "weaviate",
        type=WeaviateConnection,
        url=env_vars["WEAVIATE_URL"],
        api_key=env_vars["WEAVIATE_API_KEY"],
        additional_headers={"X-Cohere-Api-Key": env_vars["COHERE_API_KEY"]},
    )
```

Using Streamlit [chat elements](https://docs.streamlit.io/develop/api-reference/chat?ref=streamlit.ghost.io), a prompt is created and a query is made here:

```
with conn.client() as client:
    collection = client.collections.get("MovieDemo")
    response = collection.generate.hybrid(
        query=movie_type,
        filters=(Filter.by_property("release_year").greater_or_equal(year_range[0]) & Filter.by_property("release_year").less_or_equal(year_range[1])
        ),
        limit=SEARCH_LIMIT,
        alpha=SEARCH_MODES[mode][1],
        grouped_task=rag_prompt,
        grouped_properties=["title", "tagline"],
    )
```

The result is a fully interactive recommendation app with no JavaScript experience required!If you would like to learn more about Weaviate, check out the [Weaviate Quickstart](https://weaviate.io/developers/weaviate/quickstart?ref=streamlit.ghost.io) and [Weaviate Academy](https://weaviate.io/developers/academy?ref=streamlit.ghost.io).

## Unlock the potential of AI with Streamlit

With Streamlit, months and months of app design work are *streamlined* to just a few lines of Python. It’s the perfect framework for showing off your latest AI inventions.

Get up and running ***fast*** with other [AI recipes](https://streamlit.ghost.io/tag/ai-recipes/) in the [Streamlit Cookbook](https://github.com/streamlit/cookbook/tree/main?ref=streamlit.ghost.io). (And don’t forget to show us what you’re building in the [forum](https://discuss.streamlit.io/c/streamlit-examples/9?ref=streamlit.ghost.io)!)

Happy Streamlit-ing! 🎈

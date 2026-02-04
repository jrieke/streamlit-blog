---
title: "Connect your Streamlit apps to Supabase"
subtitle: "Learn how to connect your Streamlit apps to Supabase with the st-supabase-connection component"
date: 2023-12-20
authors:
  - "Siddhant Sadangi"
---

![Connect your Streamlit apps to Supabase](https://streamlit.ghost.io/content/images/size/w2000/2023/12/Supabase-1.svg)


👉

****TL;DR:**** st-supabase-connection is a Supabase connection for Streamlit that caches API calls and simplifies the needed code. I’ll walk you through how to:  
1. Install and configure the connection  
2. Use the tutorial app to explore Supabase storage, database, and auth features  
3. Construct reusable code snippets to interact with Supabase  
  
Want to dive right in? Check out the [GitHub repo](https://github.com/SiddhantSadangi/st_supabase_connection?ref=streamlit.ghost.io) and [demo app](https://st-supabase-connection.streamlit.app/?ref=streamlit.ghost.io).

I’ve been building Streamlit apps for a while now, and a common requirement is to connect to a database. That’s when I stumbled upon [Supabase](https://supabase.com/?ref=streamlit.ghost.io).

Their web interface was powerful yet user-friendly, and when Streamlit launched their Connections Hackathon, I saw an opportunity to make it even easier to use Supabase with Streamlit. My aim was to help Streamlit users and build on the functionality of Supabase’s existing Python SDK.

In this article, you’ll learn:

1. Why I chose Supabase
2. How to install and set up `st-supabase-connection`
3. How to use the tutorial app provided with the connection
4. My learnings while working on the connection and the tutorial app

## Why I built a Streamlit connection to Supabase

I was introduced to Supabase by a friend. I found the docs and the user interface so intuitive that I was able to have a hosted database up and running in under 10 minutes. I didn’t feel the need to research alternatives as Supabase offered everything I was looking for: the ability to perform CRUD operations from the UI and an open-source Python SDK that I could build upon.

My connection offers three advantages that improve the experience of building with Supabase and Streamlit:

1. It leverages Streamlit's [caching feature](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io) to store API responses. This speeds up subsequent similar requests, reducing API calls, which ultimately decreases the cost of using Supabase.
2. It simplifies the boilerplate code needed to connect your Streamlit apps to Supabase.
3. It exposes more storage methods than [Supabase’s Python client](https://supabase.com/docs/reference/python/introduction?ref=streamlit.ghost.io).

## How to use the app

This app is designed to showcase and teach you how to use the connection's features. The connection currently works with Supabase Storage, Database, and Auth.

💡

Supabase offers a free tier. You need to [sign up](https://supabase.com/dashboard/sign-up?ref=streamlit.ghost.io) and get a Supabase API key to use it. For this app, I made it possible for you to demo the app without signing up for Supabase. If you like what you see and want to use it for your own project, sign up and enter your own API key to unlock all the features of the app and connect it with your own Supabase project.

If you are new to Supabase and don’t have a Supabase API key, you can follow the below quickstart to get acquainted with Supabase, the connection, and the app.

To get started, head over to [the app](https://st-supabase-connection.streamlit.app/?ref=streamlit.ghost.io) hosted on Streamlit Community Cloud.

### **Step 1: Initialize the client for the demo project**

✅

Since the connection is built on top of [st.connection()](https://docs.streamlit.io/library/api-reference/connections/st.connection?ref=streamlit.ghost.io), the client is [cached](https://docs.streamlit.io/library/api-reference/performance/st.cache_resource?ref=streamlit.ghost.io) so that it can handle network interruptions and does not need to be initialized frequently. That said, the tutorial app overrides this caching to show you the latest results.

The first thing you’ll need to do is initialize the connection to Supabase — you can do this by clicking “Initialize client” and you can either use a demo project or connect to your own Supabase instance.

Once the client is initialized, you’ll see the demo database or storage bucket. There are some tables and files that you can use for testing, and the app provides example queries.

You can also choose to explore storage, the database, or authentication. For each option, you’ll be able to test the functionality of the Supabase connection, as well as copy a code snippet that can be used in your Streamlit app to perform that operation.

### Step 2: Explore the database, storage, or auth

**Exploring the database**

By default, database queries are not cached, so they always show the most recent data.

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--1-.png)

**Exploring storage**

Storage queries are cached forever, so they are very fast. You can change this by using the “Results cache duration” option, which affects the `ttl` parameter of the query.

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--2-.png)

**Exploring auth**

`auth` methods don’t have a cache, so you always get the latest results.

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--3-.png)

### Step 3: Click on “Run query 🏃” to get the results

Click “Run query” or “Execute” to execute the specific command against the demo Supabase instance, and the results will be displayed in the app.

**Example database view**

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--4-.png)

**Example storage view**

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--5-.png)

**Example auth view**

![](https://streamlit.ghost.io/content/images/2023/12/Untitled--6-.png)

Once you feel that Supabase would add value to your Streamlit apps, you can start using the connection as described in the [Streamlit docs](https://docs.streamlit.io/knowledge-base/tutorials/databases/supabase?ref=streamlit.ghost.io)!

## What I learned while building this connection

This was the first time I built something like this, so it was a great learning experience for me, especially around things experienced folks might take for granted. I’ve tried to mention a few of them below.

### **Reusing Supabase methods**

One of the challenges I faced while developing this project was how to reuse the existing methods from the Supabase Python API, yet add caching functionality on top of them. I was not very familiar with Object Oriented Programming in Python, so I had to learn some concepts along the way.

For example, for the database operations, I assigned `self.table` to `self.client.table`, so that I could access all the methods Supabase provides, and benefit from their method chaining feature, which is very convenient and elegant. However, I also wanted to cache the results of the `select()` method without losing the ability to chain other methods. I could not find a way to do this while still using `self.client.table`, so I decided to create a new `query()` function that works like `select()`, but also stores the results in a cache. This way, you can use `query()` if you want to use the cache, or `select()` if you don't.

For some methods that modify or delete data, such as `delete_bucket()` and `empty_bucket()`, I did not need to add any caching functionality, so I used the Supabase Python client’s methods as-is.

```
self.delete_bucket = self.client.storage.delete_bucket
self.empty_bucket = self.client.storage.empty_bucket
```

For others, I wrapped Supabase’s methods around a function to add the `st.cache_resource` decorator. For example:

```
def get_bucket(
    self,
    bucket_id: str,
    ttl: Optional[Union[float, timedelta, str]] = None,
):
    """Retrieves the details of an existing storage bucket.

    Parameters
    ----------
    bucket_id : str
        Unique identifier of the bucket you would like to retrieve.
    ttl : float, timedelta, str, or None
        The maximum time to keep an entry in the cache. Defaults to `None` (cache never expires).
    """

    @cache_resource(ttl=ttl)
    def _get_bucket(_self, bucket_id):
        return _self.client.storage.get_bucket(bucket_id)

    return _get_bucket(self, bucket_id)
```

### **Single-sourcing versioning for consistency**

`st-supabase-connection` follows [Semantic Versioning](https://semver.org/?ref=streamlit.ghost.io) (as everyone should).

The version number is needed by `[setuptools](<https://pypi.org/project/setuptools/>)` to install the library using `pip install`. Besides the library, this package also includes an application that demonstrates its usage. I wanted to display the current library version in the application as well.

Additionally, I like to mention the version number that corresponds to a change in the commit message. This implies that I have to keep track of the version number in at least three different places–`setup.py`, the demo application, and the commits.

To simplify this, I decided to use a `__version__` attribute in the package itself. This attribute is imported to the Streamlit app as `from st_supabase_connection import __version__`.

To use this version in `setup.py`, I use the following function that reads the script and extracts the version:

```
def get_version(rel_path):
    with open(rel_path, "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")
```

Now I only need to update the version in the script, and both the app and the setup script use the same version. Adding the version manually to commit messages doesn’t take enough time to warrant automation, but I am sure you could do that if you wanted to.

## What I learned while building the Streamlit app

### Reusing components

Most of my apps use the same template. I have a `sidebar.html` that populates the sidebar with a few sections that are present in all my apps. I just need to update a few links and captions.

Any additional sections can be added in the `with sidebar()` context:

```
with open("demo/sidebar.html", "r", encoding="UTF-8") as sidebar_file:
    # Replaces the "VERSION" placeholder with the current version from the script
		sidebar_html = sidebar_file.read().replace("{VERSION}", VERSION)

with st.sidebar:
		# Additional sections
    with st.expander("💡**How to use**", expanded=True):
        st.info(
            """
                1. Select a project and initialize client
                2. Select the relevant DB or Storage operation and options
                3. Run the query to get the results 
                4. Copy the constructed statement to use in your own app.
                """
        )

    if st.button(
        "Clear the cache to fetch latest data🧹",
        use_container_width=True,
        type="primary",
    ):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared")
		
		# Reused sidebar template
    st.components.v1.html(sidebar_html, height=600)
```

### **Demo project for unregistered users**

The company I currently work for, [neptune.ai](http://neptune.ai/?ref=streamlit.ghost.io), allows users to test our product without signing up. This is a user-friendly way to let potential customers try the product before they decide to share their personal information and create an account. That's why I decided to implement a similar feature in my own app.

I created a project with sample data and files that users can explore in my Supabase org. Then I added my own Supabase keys as Streamlit secrets, so that users can access the project with my credentials if they don't have or want their own Supabase account.

However, I also had to limit some actions that could affect the sample project for these users, so I used a Streamlit `session_state` variable to check if the user was using the demo project or their own project, and enable or disable functions accordingly.

For example, if the user is using the demo project, the `session_state` variable "project" is set to "demo", and some buttons are greyed out:

```
if st.session_state["project"] == "demo" and operation in RESTRICTED_STORAGE_OPERATORS:
  help = f"'{selected_operation.capitalize()}' not allowed in demo project"
```

### **Constructing valid code snippets that can be copied by the user**

One of the features of the app is that it constructs code-snippets based on your inputs that you can then copy and paste into your own app.

This had the added benefit of helping me debug if I was doing something wrong while building the app and passing values from widgets to the connector.

I used formatted strings with placeholders that would be filled based on the chosen operation and options.

For example, this is the template I used for creating a new bucket:

```
constructed_storage_query = f"""st_supabase.create_bucket('{bucket_id}',{name=},{file_size_limit=},allowed_mime_types={allowed_mime_types},{public=})"""
```

I then display this snippet using Streamlit code(), and to make sure that this is the same statement that will be executed in the backend to perform the operation, I use Python’s eval() function to get results:

```
st.code(constructed_storage_query)
response = eval(constructed_storage_query)
```

## Wrapping up

In this blog post, I have shared my experience and insights on how to use `st-supabase-connection` and build a tutorial app with it. I hope this has given you some guidance on how to install and configure the connection, how to use the tutorial app to learn about Supabase storage and database features, and how to use the connection in other Streamlit apps.

I would love to hear your feedback and suggestions on how to improve the connection or the app. You can reach me on [GitHub](https://github.com/SiddhantSadangi/st_supabase_connection?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/siddhantsadangi/?ref=streamlit.ghost.io), or [email](mailto:siddhant.sadangi@gmail.com).

Happy Streamlit-ing! 🎈

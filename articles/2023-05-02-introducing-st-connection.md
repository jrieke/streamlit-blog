---
title: "Introducing st.connection!"
subtitle: "Quickly and easily connect your app to data and APIs"
date: 2023-05-02
authors:
  - "Joshua Carroll"
category: "Product"
---

![Introducing st.connection!](https://streamlit.ghost.io/content/images/size/w2000/2023/04/Announcement-1.svg)


📣

st.experimental\_connection is now ****st.connection****  
  
Check out the [docs](https://docs.streamlit.io/library/api-reference/connections/st.connection?ref=streamlit.ghost.io) to learn more. These updates should make it even easier to connect to your data:  
  
1) The Snowpark connection is now a simpler, more powerful [Snowflake connection](https://docs.streamlit.io/library/api-reference/connections/st.connections.snowflakeconnection?ref=streamlit.ghost.io).  
  
2) More passthrough methods and hints have been added to make data connection bugs self-correcting or easier to fix.

---

In our last-year survey (N=315), 29% of you told us that **setting up data connections was the most frustrating part of your work.**

We get it. Connecting to data sources and APIs can be painful. 🤕

You need to find and install external packages, figure out how to manage your credentials securely outside of code, then find the right methods to get data out in the format you need. Oh, and you can’t forget to add Streamlit caching capabilities! For example, you can see the 14 lines of code in our [original MySQL tutorial](https://web.archive.org/web/20230330050343/https://docs.streamlit.io/knowledge-base/tutorials/databases/mysql#write-your-streamlit-app) using a mysql.connector, st.cache\_resource, st.cache\_data, managing a cursor, and converting the row result format!

Today, we’re thrilled to release…

### `st.experimental_connection` 🥂

Connect your Streamlit apps to data and APIs with just **four lines of code:**

```
import streamlit as st

conn = st.experimental_connection('pet_db', type='sql')
pet_owners = conn.query('select * from pet_owners')
st.dataframe(pet_owners)
```

Here is the [demo app](https://experimental-connection.streamlit.app/?ref=streamlit.ghost.io), or you can play with it below:




## How does st.experimental\_connection work

Streamlit comes installed with generic connections for SQL and Snowflake Snowpark. You may need to install additional packages or one of the community connections to make it work properly.

Today, it supports:

* SQL dialects (MySQL, Postgres, Snowflake, BigQuery, Microsoft SQL Server, etc.)
* Snowflake Snowpark
* Cloud file storage (S3, GCS, Azure Blob Storage, etc.) via [FilesConnection](https://github.com/streamlit/files-connection?ref=streamlit.ghost.io)
* HuggingFace Datasets and Models via [HfFileSystem](https://huggingface.co/docs/huggingface_hub/main/package_reference/hf_file_system?ref=streamlit.ghost.io) and FilesConnection
* Google Sheets via [GSheetsConnection](https://github.com/streamlit/gsheets-connection?ref=streamlit.ghost.io)

![connection-logos](https://streamlit.ghost.io/content/images/2023/05/connection-logos.png)

We’re making it easier than ever to extend this list and build your own data connections and share them with the Streamlit community!

For the purpose of this post, we’ll be using MySQL examples. If you want to follow along with other data sources, check out our tutorials on [Snowflake](https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake?ref=streamlit.ghost.io) or [AWS S3](https://docs.streamlit.io/knowledge-base/tutorials/databases/aws-s3?ref=streamlit.ghost.io).

### Step 1. Install dependencies

To start, install any necessary packages in your environment (such as with `pip` and `requirements.txt`). You can find these in Streamlit’s [data source tutorials](https://docs.streamlit.io/knowledge-base/tutorials/databases?ref=streamlit.ghost.io) or the data source documentation. If something is missing when you run your app, Streamlit will try to detect that and give you a hint about what to install (we’ll make this even easier in the future!):

```
pip install SQLAlchemy mysqlclient
```

### Step 2. Set up credentials and connection information in .streamlit/secrets.toml

Next, let’s set up the connection information in [secrets.toml](https://docs.streamlit.io/library/advanced-features/secrets-management?ref=streamlit.ghost.io). Create a new section called `[connections.<name>]` and add the parameters you need. You can name the section whatever you’d like - you’ll use the same name to reference it in your app code.

```
# .streamlit/secrets.toml

[connections.pet_db]
dialect = "mysql"
url = "mysqldb://scott:tiger@192.168.0.134/pet_db"
```

We added support for a [global secrets.toml](https://docs.streamlit.io/library/advanced-features/secrets-management?ref=streamlit.ghost.io), so if you keep using the same database, you can set this up once instead of copying it to every app. Many connections will also support their native configuration, like `AWS_*` environment variables or `~/.snowsql/config` file.

### Step 3. Import and initialize the connection in your app

Now, let’s initialize the connection in your app:

```
# streamlit_app.py

import streamlit as st

conn = st.experimental_connection('pet_db', type='sql')
```

The first argument is the name of the connection you used in `secrets.toml`. The `type` argument tells Streamlit what type of connection it is. For community-developed connections that don’t ship with Streamlit, you can import the connection class and pass it directly to type. See the [AWS S3 tutorial](https://docs.streamlit.io/knowledge-base/tutorials/databases/aws-s3?ref=streamlit.ghost.io) or [API Reference](https://docs.streamlit.io/library/api-reference/connections/st.experimental_connection?ref=streamlit.ghost.io) for examples.

### Step 4. Query your data with one line of code

For the common use case of reading data or getting some response from an API, the connection will provide a simple method that returns an easy-to-use output. It’s also cached in Streamlit by default to make your app ⚡*blazing fast!* ⚡

For example, SQLConnection has a `query()` method that takes a query input and returns a pandas DataFrame:

```
# streamlit_app.py

import streamlit as st

conn = st.experimental_connection('pet_db', type='sql')
pet_owners = conn.query('select * from pet_owners')
st.dataframe(pet_owners)
```

That’s it!

The method also supports `params`, paging, custom cache TTL, and other common arguments (read more in the [API Reference](https://docs.streamlit.io/library/api-reference/connections/st.connections.sqlconnection?ref=streamlit.ghost.io#sqlconnectionquery)).

Depending on the underlying data format, the specific methods may differ but should be natural, straightforward, and intuitive to that data source. Connection objects are fully type annotated, so your IDE can provide hints. `st.help()` and `st.write()` can also give you more information about what is supported on a specific connection!

### Step 5. Perform complex operations with .session

If you need the full power of the underlying data source or library, it’s easily accessible too! SQL and Snowpark both support this with `.session`, and other connections may have a domain-specific name for easier discovery.

For example, if you need to use transactions, write back, or interact via [ORM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping?ref=streamlit.ghost.io), you can access the [SQL Session](https://docs.sqlalchemy.org/en/14/orm/session_basics.html?ref=streamlit.ghost.io) with `SQLConnection.session`:

```
with conn.session as s:
    pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
    for k in pet_owners:
        s.execute(
            'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
            params=dict(owner=k, pet=pet_owners[k])
        )
    s.commit()
```

Check out the tutorials or use `st.help()` to learn more about what’s supported for a specific data set.

## How to build your own connection

We’re excited for the community to extend and build on the `st.experimental_connection` interface. We want to make it super easy to build Streamlit apps with lots of data sources (we’ve built the interface with this in mind).

To use a community-built connection in your app, install and import it, then pass the class to `st.experimental_connection()`:

```
import streamlit as st
from st_gsheets_connection import GSheetsConnection

conn = st.experimental_connection("pets_gsheet", type=GSheetsConnection)
pet_owners = conn.read(worksheet="Pet Owners")
st.dataframe(pet_owners)
```

These types of connections work the same as the ones built into Streamlit and have access to the same capabilities. Build a connection class by extending `streamlit.connections.ExperimentalBaseConnection`. You can find basic information in the [API Reference](https://docs.streamlit.io/library/api-reference/connections/st.connections.experimentalbaseconnection?ref=streamlit.ghost.io), and a simple [fully working example here](https://github.com/streamlit/release-demos/blob/master/1.22/st-experimental-connection/duckdb_connection/connection.py?ref=streamlit.ghost.io). The [SQLConnection](https://github.com/streamlit/streamlit/blob/develop/lib/streamlit/connections/sql_connection.py?ref=streamlit.ghost.io) built into Streamlit is another great starting point.

## **What’s next?**

We’ve been hard at work on `st.experimental_connection`, so we’re very excited to finally share it with you! Please let us know how you're using it on the [forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io), [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io), [Discord](https://discord.com/invite/bTz5EDYh9Z?ref=streamlit.ghost.io), or in the comments below.

Expect more connections, guides, and features in the coming weeks and months to make it *even easier* to connect your Streamlit app to data. And keep an eye out for a community connection-building contest a little bit later this spring. 🙂

Happy app-building! 🎈

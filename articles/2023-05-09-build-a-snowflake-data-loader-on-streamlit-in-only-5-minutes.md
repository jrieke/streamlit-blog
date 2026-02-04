---
title: "Build a Snowflake DATA LOADER on Streamlit in only 5\u00a0minutes"
subtitle: "Drag and drop your Excel data to Snowflake with a Streamlit app"
date: 2023-05-09
authors:
  - "Sasha Mitrovich"
category: "Snowflake powered \u2744\ufe0f"
---

![Build a Snowflake DATA LOADER on Streamlit in only 5 minutes](https://streamlit.ghost.io/content/images/size/w2000/2023/05/Snowflake-DATA-LOADER.svg)


A customer recently challenged me to create a data loader app for Snowflake that even kindergarteners could use. And when I say kindergarteners, I’m talking about the business users who think SQL is a mythical creature.

Now, I’m not one to back down from a challenge, especially when someone’s already promised something on my behalf. So, I decided to take on the task and create a data loader app for kindergarteners in just five minutes. And let me tell you, it was a wild ride.

**By the end of this post, you’ll learn how to create a simple drag-and-drop data loader app on Streamlit that anyone can use.**

I work as a solutions engineer at Snowflake. My passion is data, data science, and building data applications that I can showcase to my customers. Streamlit is just the tool for that.

And it complements [Snowflake’s Data Cloud platform](https://medium.com/coriers/what-is-snowflake-and-why-you-should-use-it-for-your-cloud-data-warehouse-199c62b0a09e?ref=streamlit.ghost.io) perfectly. While database specialists working in SQL and data engineers using Python DataFrames feel at home working with Snowflake, it’s a bit different for business users. There’s no easy way for non-technical users to drop data into Snowflake and jump into their business intelligence tool of choice, such as Tableau, to analyze it and share it with others.

In this post, I’m changing all that! You’ll learn how to:

1. Create a virtual Python environment for Streamlit
2. Connect to Snowflake from Streamlit
3. Create a simple drag-and-drop UI in Streamlit for CSV files
4. Load the dropped file to Snowflake
5. Bonus: Add data quality checks

Keep reading till the end. I’ll also show how to add quality checks on the loaded data and display that in the app for the business to immediately assess the data quality with just a glance at the UI.

Let’s start.

## 1. Create a virtual Python environment for Streamlit

I use [conda](https://docs.conda.io/en/latest/?ref=streamlit.ghost.io) to manage my virtual environments so I can work with correct versions of Python packages and avoid the dependency hell. If you don’t know what that is, I’ve explained it in my video [“Stuck learning Python? Make it fun with Streamlit!”](https://youtu.be/1qTQWATaywI?t=206&ref=streamlit.ghost.io)

Here’s how to create an environment for our app with all the necessary Python packages:

```
conda create --name snowshovel -c <https://repo.anaconda.com/pkgs/snowflake> python=3.8 pandas snowflake-snowpark-python
conda activate snowshovel
conda install -c conda-forge streamlit
```

If you don’t use conda, that’s fine; you can install these packages using pip, for instance.

## 2. Connect to Snowflake from Streamlit

We’ll store our credentials in the creds.json.Here’s an example that contains all the required properties for connecting to Snowflake:

```
{
    "account": "account.region",
    "user": "myuser",
    "role": "myrole",
    "password": "************",
    "warehouse": "mywarehouser",
    "database": "mydb",
    "schema": "myschema"
  }
```

Make sure to replace these placeholders with real values for your Snowflake account.

We’ll use this credentials file later to create a connection to Snowflake. Snowflake supports many other authentication methods, such as key-pair or single sign-on.

## 3. Create a simple drag-and-drop UI in Streamlit for CSV files

I use VS Code as my development environment. If you want to learn why I like VS Code so much — make sure you watch this clip:

Let’s jump into VS Code and start working on our Python code.

To start building a Streamlit app, we need to import the streamlit Python package, like this:

```
import streamlit as st
```

Now we can run the app from the terminal like so:

```
streamlit run app.py
```

Now that we have the app running let’s add the amazing [file uploader component](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader?ref=streamlit.ghost.io) that does all the job for us:

```
file = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv"})
```

That’s it. It literally takes two lines of code to build a Drag and Drop Web app with Streamlit. If anyone can beat this, I’m buying them a beverage of their choice (and I will ship it internationally).

## 4. Load the dropped file to Snowflake

The return value of the file uploader component is an UploadedFile class object, a subclass of BytesIO. Therefore, it is “file-like.” This means you can use that anywhere a file is expected and read its meta-data to get the filename, for example.

That’s exactly what we need in the next step.

We’ll load this file to a Pandas DataFrame. Why Pandas DataFrame? For two reasons:

1. Pandas has a convenient [read\_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?ref=streamlit.ghost.io)() method that will infer the CSV schema automatically, so we don’t need to build that complex logic of recognizing column types ourselves. Yay to the open-source community!
2. Pandas can be serialized to a Snowflake table with a single line of code using Snowflake’s Snowpark function [write\_pandas()](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api?ref=streamlit.ghost.io#write_pandas). The table will be automatically created, re-using the schema from the Pandas DataFrame.

Let’s add these two lines of code to complete our app:

```
file_df = pd.read_csv(file)
snowparkDf=session.write_pandas(file_df,file.name,auto_create_table = True, overwrite=True)
```

Notice I’m using the session object to serialize the DataFrame to a Snowflake table, and remember, we’ve prepared a JSON file with our Snowflake credentials.

Let’s create that object before using it in our code. Here’s the complete application code for our simple Snowflake data loader. I’ve imported all the needed Python packages and checked if a file has been dropped.

```
import streamlit as st
import pandas as pd
import json
from snowflake.snowpark import Session

# connect to Snowflake
with open('creds.json') as f:
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

file = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv"})
file_df = pd.read_csv(file)
snowparkDf=session.write_pandas(file_df,file.name,auto_create_table = True, overwrite=True)
```

That’s it. I’ve written a CSV data loader for Snowflake with less than 20 lines of Python code in under 5 minutes!

## Bonus: Add data quality checks

Now that we’ve enabled business users to load their data to Snowflake without knowing anything about Snowflake, let’s provide some data quality checks.

With this, they can immediately see what they have in terms of data quality and make informed decisions on how to process this data further so they get added value from it.

Here’s a Python function that does just that:

```
def describeSnowparkDF(snowpark_df: snowpark.DataFrame):
    
    st.write("Here's some stats about the loaded data:")
    numeric_types = [T.DecimalType, T.LongType, T.DoubleType, T.FloatType, T.IntegerType]
    numeric_columns = [c.name for c in snowpark_df.schema.fields if type(c.datatype) in numeric_types]

    # Get categorical columns
    categorical_types = [T.StringType]
    categorical_columns = [c.name for c in snowpark_df.schema.fields if type(c.datatype) in categorical_types]

    st.write("Relational schema:")
  
    columns = [c for c in snowpark_df.schema.fields]
    st.write(columns)
    
    col1, col2, = st.columns(2)
    with col1:
        st.write('Numeric columns:\\t', numeric_columns)

    with col2:
        st.write('Categorical columns:\\t', categorical_columns)
    
    # Calculte statistics for our dataset
    st.dataframe(snowpark_df.describe().sort('SUMMARY'), use_container_width=True)
```

Let’s break this down a little bit.

First, we’ll list all the column names and types for the newly created table. This is useful to check if the schema was inferred as the user expected:

```
  st.write("Here's some stats about the loaded data:")
  numeric_types = [T.DecimalType, T.LongType, T.DoubleType, T.FloatType, T.IntegerType]
  numeric_columns = [c.name for c in snowpark_df.schema.fields if type(c.datatype) in numeric_types]

  # Get categorical columns
  categorical_types = [T.StringType]
  categorical_columns = [c.name for c in snowpark_df.schema.fields if type(c.datatype) in categorical_types]
  st.write("Relational schema:")

  columns = [c for c in snowpark_df.schema.fields]
  st.write(columns)
```

Then, we’ll present two more lists: numeric columns and categorical columns. This is useful to understand which further data processing we might undertake, like enriching with more data from other sources or transforming the values in a way required for analysis, like machine learning, perhaps:

```
col1, col2, = st.columns(2)
with col1:
  st.write('Numeric columns:\\\\t', numeric_columns)
with col2:
  st.write('Categorical columns:\\\\t', categorical_columns)
```

Finally, we’ll show the column statistics for each column, including counts of null values or value ranges. Based on this, the business user can decide if they will be able to use this dataset for their intended analysis with just a glance:

```
# Calculte statistics for our dataset
st.dataframe(snowpark_df.describe().sort('SUMMARY'), use_container_width=True)
```

## Wrapping up

I built a basic data loader app for Snowflake that any business user immediately understands and can use. Building this app took me only 5 minutes and less than 20 lines of code.

Then, I spent another 15 minutes providing meaningful information about the loaded data so a business user could decide on the data quality with just a glance.

You’ll fund the code for this app and instructions on how to install and use it in this [GitHub repo](https://github.com/sashamitrovich/snowshovel?ref=streamlit.ghost.io).

If you found this post useful, clap and subscribe to my Medium. And if you have any questions, please post them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/sashamitrovich/?ref=streamlit.ghost.io).

---
title: "Data analysis with Mito: A powerful spreadsheet in Streamlit"
subtitle: "Replace st.dataframe or st.data_editor with the Mito spreadsheet to edit dataframes in your app"
date: 2023-08-08
authors:
  - "Nate Rush"
category: "Advocate Posts"
---

![Data analysis with Mito: A powerful spreadsheet in Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/08/Announcement.svg)


**TL;DR:** The Mito spreadsheet is a drop-in replacement for `st.dataframe` or `st.data_editor`. View and edit dataframes using spreadsheet formulas, pivot tables, graphs, and more. For every edit, Mito generates the corresponding Python code. Check out the [sample app](https://mito-data-cleaning-demo.streamlit.app/?ref=streamlit.ghost.io) and the [code](https://github.com/mito-ds/data-cleaning-demo?ref=streamlit.ghost.io). Enjoy!

Hiya, Streamlit users! 👋

I'm Nate, co-founder of [Mito](https://trymito.io/?ref=streamlit.ghost.io)—a spreadsheet that helps analysts transition from Excel to Python. I've been working on Mito for almost four years now (oof). For the past two years, our [open-source community](https://github.com/mito-ds/monorepo?ref=streamlit.ghost.io) and enterprise clients have been [asking us to bring](https://discuss.streamlit.io/t/mito-on-streamlit/16344?ref=streamlit.ghost.io) Mito to Streamlit. Here is why.

## Why Mito?

Streamlit apps that let users upload unstructured data often encounter issues because users upload data in many different formats.

The typical solution is for the users to upload a file of their choosing and for the app creator to provide a variety of `st.text_input`, `st.selectbox`, and `st.button` that let them:

1. Rename, move, and delete columns
2. Change the types of columns
3. Filter null and other unwanted values
4. And much more

This leads to apps with many inputs and strict requirements for user-provided data, effectively drowning users in basic data cleaning and transformation options.

![lots-of-configuration-options](https://streamlit.ghost.io/content/images/2023/08/lots-of-configuration-options.gif#browser)

It's not easy to provide enough configuration options for the data formats that users bring to the table. Users often get stuck configuring a single additional parameter (e.g., how many rows to skip before the header row). As a result, they can't use the app you worked so hard to create.

Check out this [sample app](https://mito-data-cleaning-demo.streamlit.app/?ref=streamlit.ghost.io) to try Mito's flexible data importing, cleaning, preprocessing tools, and importing methods, including:

1. Importing CSV/Excel files, including advanced configuration options
2. Renaming, reordering, and removing columns in place
3. Filtering in a classic interface with many filter conditions
4. Writing spreadsheet formulas to transform your data

![mito-data-cleaning](https://streamlit.ghost.io/content/images/2023/08/mito-data-cleaning.gif#browser)

Mito provides data cleaning options beyond your basic data importing. Here are a few examples.

### Tab renaming

Need to rename columns to match the expected format? Rename the tabs directly in a spreadsheet:

![mito-rename-headers](https://streamlit.ghost.io/content/images/2023/08/mito-rename-headers.gif#browser)

### Column filtering

Want to run the rest of your app on a subset of your data? Use a spreadsheet to filter out the data you need:

![ezgif.com-resize--1--1](https://streamlit.ghost.io/content/images/2023/08/ezgif.com-resize--1--1.gif#browser)

### Formula writing

Need to let users transform columns in a more complex way? Let them **write formulas as they do in Excel**:

![mito-write-formulas](https://streamlit.ghost.io/content/images/2023/08/mito-write-formulas.gif#browser)

With Mito, users can import a dataset of their choice into your app and format it as your app requires.

## Use case 1: Mito internal Streamlit app

At Mito, we use an internal Streamlit app to monitor the current state of our company. It displays our current revenue, expenses, customer information, the number of blog posts from the previous week, and other relevant data. You can select variables to compare, contrast, regress, and more—to understand how Mito performs over time.

![mito-streamlit-app](https://streamlit.ghost.io/content/images/2023/08/mito-streamlit-app.png#border)

NOTE: Making our internal app was a breeze. Streamlit can be the easiest way to explore datasets of varying complexity. Check out this [fantastic app example](https://goodreads.streamlit.app/?ref=streamlit.ghost.io) which provides helpful, pre-configured views for gaining insight from data and graphs.

As the app's creator, I wanted my team members to be able to compare the number of sales we made this month with the number of sales from the previous month. So I created the following input:

```
min_date, max_date = st.date_input('Compare within Range', value=(one_week_ago, today))
```

This method is great for comparing date ranges but can't answer ad-hoc questions like "How has the number of motorcycles we've sold per month changed?" To answer questions like that, you can use Mito's pivot table feature (you can also write formulas and generate graphs right within your Streamlit app):

![mito-pivot-table](https://streamlit.ghost.io/content/images/2023/08/mito-pivot-table.gif#browser)

## Use case 2: Python script without coding

At Mito, we work with financial institutions that have thousands of users poring over spreadsheets and running multiple spreadsheet processes. Those spreadsheets can have hundreds of tabs and thousands of formulas. And if the person responsible for the spreadsheet leaves, it can take weeks or even months for someone else to audit and use it.

So, what can you do?

One option is to train your spreadsheet users to learn Python. But not everyone wants to do that.

```
print("hello world, I don't think I love programming...")
```

Another option is to use Mito! Mito enables non-programmers to write Python code without ever needing to see it. Every spreadsheet edit generates the corresponding code in the backend (a full script is created to codify the process).

Try this sample app to see how it works (here is the [code](https://github.com/mito-ds/mito-for-streamlit-demo?ref=streamlit.ghost.io) for it):

## Use case 3: Mito in any Streamlit app

Using Mito is super simple.

Just install the Mito package with `pip install mitosheet`:

```
# In a terminal
pip install mitosheet
```

```
# In your Streamlit app
from mitosheet.streamlit.v1 import spreadsheet

...

spreadsheet(df)
```

Next, display any dataframes inside the `spreadsheet` component:

```
import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet

# Create a dataframe with pandas (you can pass any pandas dataframe)
dataframe = pd.DataFrame({'A': [1, 2, 3]})

# Display the dataframe in a Mito spreadsheet
final_dfs, code = spreadsheet(dataframe)

# Display the final dataframes created by editing the Mito component
# This is a dictionary from dataframe name -> dataframe
st.write(final_dfs)

# Display the code that corresponds to the script
st.code(code)
```

![writing-formulas-in-a-spreadsheet](https://streamlit.ghost.io/content/images/2023/08/writing-formulas-in-a-spreadsheet.gif#browser)

And you're done!

## Wrapping up

Mito has been four years in the making, and we're excited to finally share it with you! Over the coming weeks, we'll be improving our Streamlit support, including the additional functionality within the spreadsheet, the ability to set predefined views, and more configuration options.

As we roll out more features, we'd love to hear your feedback. Please [open an issue on GitHub](https://github.com/mito-ds/mito/issues?ref=streamlit.ghost.io) or leave us comments below.

Happy app-building! 🧑‍💻

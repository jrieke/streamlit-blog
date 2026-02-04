---
title: "Create a search engine with Streamlit and Google Sheets"
subtitle: "You\u2019re sitting on a goldmine of knowledge!"
date: 2023-03-14
authors:
  - "Sebastian Flores Benner"
category: "Advocate Posts"
---

![Create a search engine with Streamlit and Google Sheets](https://streamlit.ghost.io/content/images/size/w2000/2023/03/python-chile-app-2.svg)


Hi! I'm Sebastian Flores. You might remember me from my posts on [creating interactive books](https://streamlit.ghost.io/how-to-create-interactive-books-with-streamlit-and-streamlit-book-in-5-steps) and [fostering data processing innovation](https://streamlit.ghost.io/uplanner-fosters-data-processing-innovation-with-streamlit/).

In 2022 I attended the PyCon Chile conference and saw it was a gold mine for educational content. From the years 2020, 2021, and 2022 alone, there were 150+ YouTube recordings on Python and related topics! The downside? It was hard to find a specific recording by title or by the speaker’s name.

So on the bus ride back, I coded a working MVP of a Streamlit app to solve it. The main ingredients were Streamlit, pandas, and Google Sheets (for easy collaboration and updates). When I was done, I realized this combo could be used for other projects. I hope this post sparks your imagination. If you build an app, please share it with me on [Twitter](https://twitter.com/sebastiandres?ref=streamlit.ghost.io) or [LinkedIn](https://www.linkedin.com/in/sebastiandres/?ref=streamlit.ghost.io) (and don't forget to tag @Streamlit as well!).

Now, let's start our journey. There are three steps:

* **Step 1:** Set up a Google Sheet with your data
* **Step 2:** Use Streamlit to read the data from the Google Sheet
* **Step 3:** Build the user interface and search functionality using Streamlit
* **Bonus step:** Other app ideas

👉

If you want to take a look, here's my [app](https://pythonchile.streamlit.app/?ref=streamlit.ghost.io) and the [repo](https://github.com/sebastiandres/st_pythonchile?ref=streamlit.ghost.io) for it.

### Step 1: Set up a Google Sheet with your data

First, you need to create a Google Sheet that contains your information. In my case, it included columns for the year, speaker, title, and talk description.

Next, create two links:

1. **A public link** with view permissions to be freely shared. The app will use this link to read the data (you can safely put it directly into the code).
2. **A private link** shared with the people who can edit the data. Click the "Share" button in the top right corner and add the email addresses of the users you want to share with.

The database should look something like this:

![database-1](https://streamlit.ghost.io/content/images/2023/03/database-1.png#browser)

[Here](https://www.notion.so/64ef974d4cc44c73ba4c60c12b851ac3?ref=streamlit.ghost.io) is the public link.

### Step 2: Use Streamlit to read the data from the Google Sheet

Next, connect your Streamlit app to the Google Sheet (easy thanks to the pandas library). From the spreadsheet, get the `sheet_id` (from the URL) and the `sheet_name`. In this example, the `public_link` has the long name [`https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/`](https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/edit?ref=streamlit.ghost.io#gid=0) so you can recognize that the `google_id` is `"1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"`. I have defined the tab name of the talks as “charlas” so I can set up `sheet_name` to the string `"charlas"`. You can take any other convenient convention.

Now comes the magic. You can read the data directly from the spreadsheet as a CSV using pandas on one line:

```
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str)
```

An initial app that reads the Google Sheet and displays it would only need this code:

```
# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Python Talks Search Engine", page_icon="🐍", layout="wide")
st.title("Python Talks Search Engine")

# Connect to the Google Sheet
sheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
sheet_name = "charlas"
url = f"<https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}>"
df = pd.read_csv(url, dtype=str).fillna("")

# Show the dataframe (we'll delete this later)
st.write(df)
```

The app will look like this:

![python-talks-app](https://streamlit.ghost.io/content/images/2023/03/python-talks-app.png#browser)

Note that the data is read every time you refresh, so any changes you make to your spreadsheet changes are immediately reflected in the app. It’s that simple!

### Step 3: Build a user interface and search functionality using Streamlit

Now that your spreadsheet is connected to your Streamlit app, you can get as crazy as you want. The most basic functionality would be a search bar:

```
# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search videos by title or speaker", value="")
```

This creates a simple text box, where the user can enter the text to be searched:

![python-talks-search-engine](https://streamlit.ghost.io/content/images/2023/03/python-talks-search-engine.png#browser)

We use the input to apply some filters:

```
# Filter the dataframe using masks
m1 = df["Autor"].str.contains(text_search)
m2 = df["Título"].str.contains(text_search)
df_search = df[m1 | m2]
```

And we show it to the user:

```
# Show the results, if you have a text_search
if text_search:
    st.write(df_search)
```

For a more refined look, split the content into rows and columns. For the sake of simplicity, I have called each element of a row and column a "card":

```
# Another way to show the filtered results
# Show the cards
N_cards_per_row = 3
if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
            st.markdown(f"**{row['Autor'].strip()}**")
            st.markdown(f"*{row['Título'].strip()}*")
            st.markdown(f"**{row['Video']}**")
```

This creates blocks with clickable content:

![python-talks-blocks](https://streamlit.ghost.io/content/images/2023/03/python-talks-blocks.png#browser)

Note that we used some tricks to keep things aligned: we use the row number (from 0 to n) and split them into groups of `N_cards_per_row`. Each time we completed a row, we asked Streamlit for a new group of columns, so that the cards in each row are always aligned to the top.

And that's the basic app functionality! Simple and short with Streamlit.

If you want, you can make additional improvements:

* Convert all strings to lowercase and de-accent the vowels (á,é,í,ó,ú,ü → a,e,i,o,u) for fewer word-strict matches.
* Instead of the links, provide a clickable image.
* Inject some JavaScript to create a dynamic border around the cards.

![python-chile-app](https://streamlit.ghost.io/content/images/2023/03/python-chile-app.gif#browser)

## Bonus step: Other app ideas

There are many other applications for the Streamlit + pandas + Google Sheet combo:

1. **Secret Santa generator:** An app that allows users to enter the names and email addresses of people participating in a Secret Santa gift exchange. The app could randomly assign gift givers and recipients and send out emails with the information. The Google Sheet could be used to store the list of participants and their assignments.
2. **Survey analysis:** An app to visualize survey results data in real-time. The Google Sheet could be used to store the raw data and automatically update the app with the latest results.
3. **Recipe organizer:** An app to search and organize a large collection of recipes. The Google Sheet could be used to store the recipe data (including ingredients, instructions, notes, etc.)
4. **Birthday and event tracker:** If you're like me and forget 99% of people's birthdays, you can make an app that shows you the next 3 important events or the important events of the next 7 days! All you have to do is put all those birthdays into a Google Sheet (like me!).

The beauty of this is that you can easily customize your app and manage private/public access to the spreadsheet to prevent unwanted changes.

### **Wrapping up**

Congratulations! You have learned how to build a Streamlit app using a Google Sheet as a database. Now even your most non-technical team members can update the data (remember to give them editing permissions!).

Streamlit made building this app super easy. If you have any questions or encounter any problems, please reach out to me on [Twitter](https://twitter.com/sebastiandres?ref=streamlit.ghost.io), [GitHub](https://github.com/sebastiandres?ref=streamlit.ghost.io), or [LinkedIn](https://www.linkedin.com/in/sebastiandres/?ref=streamlit.ghost.io). I'm always happy to help.

Happy Streamlit-ing and learning! 🧑‍💻

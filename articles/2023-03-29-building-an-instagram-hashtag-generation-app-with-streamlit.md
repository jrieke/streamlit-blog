---
title: "Building an Instagram hashtag generation app with Streamlit"
subtitle: "5 simple steps on how to build it"
date: 2023-03-29
authors:
  - "William Mattingly"
category: "Advocate Posts"
---

![Building an Instagram hashtag generation app with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/03/instagram-hashtag-generator.svg)


Hey, community! 👋

My name is Dr. William Mattingly, and I'm a postdoc at the Smithsonian Institution's Data Science Lab. I work primarily with applying machine learning (ML) and natural language processing (NLP) to humanities data and museum archival records.

I wanted to build an app for my social media accounts—and to learn more about web scraping, data visualization, and data storage. Generating hashtags from an Instagram hashtag collection and analyzing the output counts sounded like fun, so I built an Instagram Hashtag Generation App!

In this post, you'll learn:

Step 1. How to scrape data from Instagram and a site that contains data about hashtag relationships

Step 2. How to clean and structure the output from web scraping

Step 3. How to display that data visually

Step 4. How to create dynamic components with custom keys

Step 5. How to display your output within Streamlit

👉

Want to jump right in? Here's the [app](https://instagram-hashtags.streamlit.app/?ref=streamlit.ghost.io) and the [repo](https://github.com/wjbmattingly/instagram-analysis?ref=streamlit.ghost.io).

### Step 1. How to scrape data from Instagram and a site that contains data about hashtag relationships

Let's start by gathering two key pieces of data about Instagram hashtags:

1. How many times has a hashtag been used
2. Which hashtags are frequently used alongside a given hashtag

You'll need to have some functions for making requests to Instagram and an Instagram-related site called [best-hashtag.com](http://best-hashtag.com/?ref=streamlit.ghost.io) (you'll use requests and BeautifulSoup instead of Selinium to keep it simple and make integration on other platforms like Streamlit Community Cloud much easier):

```
def get_count(tag):
	"""
	This function takes a hashtag as an input and returns the approx. times it has been used
	on Instagram.
	"""
  url = f"<https://www.instagram.com/explore/tags/{tag}>"
  s = requests.get(url)
  soup = BeautifulSoup(s.content)
  return int(soup.find_all("meta")[6]["content"].split(" ")[0].replace("K", "000").replace("B", "000000000").replace("M", "000000").replace(".", ""))

def get_best(tag, topn):
	"""
	This function takes two arguments, a hashtag and topn.
	Topn is the number of similar hashhtags you wish to find.
	This allows you to cultivate a set of 30-hashtags quickly.
	"""
  url = f"<https://best-hashtags.com/hashtag/{tag}/>"
  s = requests.get(url)
  soup = BeautifulSoup(s.content)
  tags = soup.find("div", {"class": "tag-box tag-box-v3 margin-bottom-40"}).text.split()[:topn]
  tags = [tag for tag in tags]
  return tags
```

You'll store user data in a JSON file to avoid unnecessary repeat requests. Let's set up your JSON database using a fairly standard function called `load_data()` (you won't be using Streamlit's cache feature because you'll be updating this information regularly):

```
def load_data():
    with open("database.json", "r") as f:
        data = json.load(f)
    return data
```

### Step 2. How to clean and structure the output from web scraping

Now that you have developed your basic web scraping functions start building your app. First, import all requisite libraries:

```
import streamlit as st

# scraping
import requests
from bs4 import BeautifulSoup

#data
import json
import pandas as pd

# plotting
import plotly.express as px
import seaborn as sns
```

Next, load up your data by calling the `load_data()` function:

```
data = load_data()
```

### Step 3. How to display that data visually

Once the data is loaded, start designing your app.

You want to let the user dynamically create multiple tags to automatically populate a collection of hashtags. They should be able to enter anywhere from 1 to 30 hashtags (30 is the maximum number allowed on Instagram). You can do this using Streamlit `number_input()` class:

```
num_tags = st.sidebar.number_input("Select number of tags", 1, 30)
```

### Step 4. How to create dynamic components with custom keys

Since you want the tag inputs to be dynamically loaded, you'll need to create them dynamically. You can do this in a `for` loop and assign a unique key to each text input.

You also want the user to tell you how many similar hashtags to generate. To do this, you'll also need to create number inputs dynamically. Each of these will be appended to separate lists called `tags` and `sizes`:

```
st.sidebar.header("Tags")
col1, col2 = st.sidebar.columns(2)

tags = []
sizes = []
for i in range(num_tags):
    tag = col1.text_input(f"Tag {i}", key=f"tag_{i}")
    size = col2.number_input(f"Top-N {i}", 1, 10, key=f"size_{i}")
    tags.append(tag)
    sizes.append(size)
```

### **Step 5.** How to display your output in Streamlit

Once the user has provided an input, it's time to use that input to do something.

For your app, you want to use hashtags to identify the number of times it's been used on Instagram and the common hashtags associated with it. When a button is clicked, you want that event to be triggered—do that with a conditional statement.

Here is the code in its entirety:

```
#only execute if the `Create Hashtags` button is pressed
if st.sidebar.button("Create Hashtags"):
		#create a list of tab names that begin with `all`
    tab_names = ["all"]
    tab_names = tab_names+[tags[i] for i in range(num_tags)]

		#create our Streamlit tabs
    tag_tabs = st.tabs(tab_names)

		#create lists to store our data outside of our loop
    all_hashtags = []
    hashtag_data = []

		#loop for the number of tags we have
    for i in range(num_tags):
        hashtags = get_best(tags[i], sizes[i])
        for hashtag in hashtags:
            if hashtag in data["hashtag_data"]:
                hashtag_count = data["hashtag_data"][hashtag]
            else:
                hashtag_count = get_count(hashtag.replace("#", ""))
                data["hashtag_data"][hashtag] = hashtag_count
            hashtag_data.append((f"{hashtag}<br>{hashtag_count:,}", hashtag_count))

		    #We can use our integer, i, to populate the list of Streamlit tag objects.
        tag_tabs[i+1].text_area(f"Tags for {tags[i]}", " ".join(hashtags))
        all_hashtags = all_hashtags+hashtags
  
    tag_tabs[0].text_area("All Hashtags", " ".join(all_hashtags))

    st.header("Hashtag Count Data")
    df = pd.DataFrame(hashtag_data, columns=["hashtag", "count"])
    df = df.sort_values("count")

    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)
    
    fig = px.bar(df, x='hashtag', y='count')
    st.plotly_chart(fig, use_container_width=True)
```

### **Wrapping up**

Thank you for reading my post! You have learned how to use Streamlit to perform web scraping, make dynamic inputs with unique keys, and display your output nicely.

If a tutorial video is your thing, check out the video below:

And if you have any questions, please leave them in the comments below or contact me on [Twitter](https://twitter.com/wjb_mattingly?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

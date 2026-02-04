---
title: "Build a Neural Search | Use Jina to Search Text or Images"
subtitle: "Use Jina to search text or images with the power of deep learning"
date: 2021-04-15
authors:
  - "Alex C-G"
category: "Advocate Posts"
---

![Build a Jina neural search with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--6-.svg)


Do you ever think, “Darn this stupid cloud. Why can’t there be an easier way to build a neural search on it?”

Well, if you have, this article is for you. I’m going to walk through how to use [Jina's](https://github.com/jina-ai/jina/?ref=streamlit.ghost.io) new Streamlit component to search text or images to build a neural search front end.

![jina](https://streamlit.ghost.io/content/images/2022/09/jina.gif#border)

Want to jump right in? Check out the [component's repo](https://github.com/jina-ai/streamlit-jina?ref=streamlit.ghost.io).

### Why use Jina to build a neural search?

Jina is an open-source deep learning-powered search framework for building cross-/multi-modal search systems (e.g. text, images, video, audio) on the cloud. Essentially, it lets you build a search engine *for* any kind of data *with* any kind of data.

So you could build [your own text-to-text search engine](https://github.com/jina-ai/examples/blob/master/wikipedia-sentences?ref=streamlit.ghost.io) ala Google, a [text-to-image search engine](https://github.com/jina-ai/examples/blob/master/cross-modal-search?ref=streamlit.ghost.io) ala Google Images, an [audio-to-audio search engine](https://github.com/jina-ai/examples/tree/master/audio-to-audio-search?ref=streamlit.ghost.io) and so on. Companies like Facebook, Google, and Spotify build these searches powered by state-of-the-art AI-powered models like FAISS, DistilBERT and Annoy.

### Why use Streamlit with Jina?

I've been a big fan of Streamlit since before I even joined Jina. I used it on a project to create terrible Star Trek scripts that later turned into a [front end for text generation with Transformers](https://github.com/alexcg1/easy_text_generator?ref=streamlit.ghost.io). So I'm over the moon to be using this cool framework to build something for our users.

Building a Streamlit component helps the data scientists, machine learning enthusiasts, and all the other developers in the Streamlit community build cool stuff powered by neural search. It offers flexibility and, being written in Python, it can be easier for data scientists to get up to speed.

Out of the box, the streamlit-jina component has text-to-text and image-to-image search, but Jina offers a rich search experience *for* any kind of data *with* any kind of data so there's plenty more to add to the component!

### How does it work?

Every Jina project includes two [Flows](https://docs.jina.ai/fundamentals/flow/?ref=streamlit.ghost.io):

**Indexing:** for breaking down and extracting rich meaning from your dataset using neural network models

**Querying:** for taking a user input and finding matching results

Our Streamlit component is a front end for *end users*, so it doesn't worry about the indexing part.

1. Admin spins up a Jina Docker image: `docker run -p 45678:45678 jinahub/app.example.wikipedia-sentences-30k:0.2.9-1.0.1`
2. User enters a query into the Streamlit component (currently either a text input or an image upload) and hits 'search'
3. The input query is wrapped in JSON and sent to Jina's query API
4. The query Flow does its thing and returns results in JSON format (along with lots of metadata)
5. The component parses out the useful information (e.g. text or image matches) and displays them to the user

### Example code

Let's look at our [text search example](https://github.com/jina-ai/streamlit-jina/blob/main/examples/jina_text.py?ref=streamlit.ghost.io), since it's easier to see what's going on there:

```
import streamlit as st
from streamlit_jina import jina
st.set_page_config(page_title="Jina Text Search",)

endpoint = "http://0.0.0.0:45678/api/search"

st.title("Jina Text Search")
st.markdown("You can run our [Wikipedia search example](https://github.com/jina-ai/examples/tree/master/wikipedia-sentences) to test out this search")

jina.text_search(endpoint=endpoint)
```

As you can see, the above code:

* Imports `streamlit` and `streamlit_jina`
* Sets the REST endpoint for the search
* Sets the page title
* Displays some explanatory text
* Displays the Jina text search widget with `endpoint` defined

For the Jina Streamlit widgets you can also pass in [other parameters](https://github.com/jina-ai/streamlit-jina?ref=streamlit.ghost.io#parameters) to define number of results you want back or if you want to hide certain widgets.

## Behind the scenes

The source code for our module is just one file, `__init__.py`. Let's just look at the high-level functionality for our text search example for now:

### Set configuration variables

```
headers = {
    "Content-Type": "application/json",
}

# Set default endpoint in case user doesn't specify and endpoint
DEFAULT_ENDPOINT = "http://0.0.0.0:45678/api/search"
```

### Render component

```
class jina:
    def text_search(endpoint=DEFAULT_ENDPOINT, top_k=10, hidden=[]):
        container = st.beta_container()
        with container:
            if "endpoint" not in hidden:
                endpoint = st.text_input("Endpoint", endpoint)

            query = st.text_input("Enter query")

            if "top_k" not in hidden:
                top_k = st.slider("Results", 1, top_k, int(top_k / 2))

            button = st.button("Search")

            if button:
                matches = text.process.json(query, top_k, endpoint)
                st.write(matches)

        return container
```

In short, the `jina.text_search()` method:

* Creates a Streamlit container to hold everything, with sane defaults if not specified
* If widgets aren't set to hidden, present them to user
* [User types query]
* [User clicks button]
* Sends query to Jina API and returns results
* Displays results in the component

Our method's parameters are:

![](https://streamlit.ghost.io/content/images/2021/08/1-3-1.png)

`jina.text_search()` calls upon several other methods, all of which can find in `__init__.py`. For image search there are some additional ones:

* `image.encode.img_base64()` encodes a query image to base64 and wraps it in JSON before passing to Jina API
* Jina's API returns matches in base64 format. The `image.render.html()` method wraps these in `<IMG>` tags so they'll display nicely

## Use it in your project

**In your terminal:**

Create a new folder with a virtual environment and activate it. This will prevent conflicts between your system libraries and your individual project libraries:

```
mkdir my_project
virtualenv env
source env/bin/activate
```

Install the [Streamlit](https://pypi.org/project/streamlit/?ref=streamlit.ghost.io) and [Streamlit-Jina](https://pypi.org/project/streamlit-jina/?ref=streamlit.ghost.io) packages:

```
pip install streamlit streamlit-jina
```

[Index your data in Jina and start a query Flow](https://docs.jina.ai/datatype/image/small-images-inside-big-images/building-flows/?highlight=index&ref=streamlit.ghost.io). Alternatively, use a pre-indexed Docker image:

```
docker run -p 45678:45678 jinahub/app.example.wikipedia-sentences-30k:0.2.9-1.0.1
```

Create your `app.py`:

```
import streamlit as st
from streamlit_jina import jina
st.set_page_config(page_title="Jina Text Search",)

endpoint = "http://0.0.0.0:45678/api/search" # This is Jina's default endpoint. If your Flow uses something different, switch it out

st.title("Jina Text Search")

jina.text_search(endpoint=endpoint)
```

Run Streamlit:

```
streamlit run app.py
```

And there you have it – your very own text search!

For image search, simply swap out the text code above for our [image example code](https://github.com/jina-ai/streamlit-jina/blob/main/examples/jina_image.py?ref=streamlit.ghost.io) and run a Jina image (like our [Pokemon example](https://github.com/jina-ai/examples/tree/master/pokedex-with-bit?ref=streamlit.ghost.io)).

## What to do next

Thanks for reading the article and looking forward to hearing what you think about the component! If you want to learn more about Jina and Streamlit here are some helpful resources:

### Jina

* [Streamlit-Jina component](https://github.com/jina-ai/streamlit-jina?ref=streamlit.ghost.io)
* [Jina docs](https://docs.jina.ai/?ref=streamlit.ghost.io)
* [Jina Fundamentals](https://docs.jina.ai/fundamentals/concepts/?ref=streamlit.ghost.io)
* [Jina hello-world demos](https://docs.jina.ai/get-started/hello-world/?ref=streamlit.ghost.io)

### Streamlit

* [Streamlit docs](https://docs.streamlit.io/en/stable/?ref=streamlit.ghost.io)
* [Components gallery](https://streamlit.io/gallery?type=components&category=featured&ref=streamlit.ghost.io)
* [App gallery](https://streamlit.io/gallery?type=apps&category=featured&ref=streamlit.ghost.io)
* [Community forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)

## A big thank you!

Major thanks to Randy Zwitch, TC Ricks and Amanda Kelly for their help getting our component live. And thanks to all my colleagues at Jina for building the backend that makes this happen!

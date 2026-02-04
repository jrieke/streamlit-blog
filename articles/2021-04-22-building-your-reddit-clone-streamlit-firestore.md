---
title: "Building Your Reddit Clone | Streamlit & Firestore"
subtitle: "Aka the NoSQL sequel: Building a Reddit clone and deploying it securely"
date: 2021-04-22
authors:
  - "Austin Chen"
category: "Tutorials"
---

![Streamlit ❤️ Firestore (continued)](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--7-.svg)


## Recap

[Last time](https://streamlit.ghost.io/streamlit-firestore/), in Parts 1 & 2, we walked through all the necessary steps to set up [Streamlit](https://streamlit.io/?ref=streamlit.ghost.io), [Streamlit sharing](https://streamlit.io/sharing?ref=streamlit.ghost.io), and [Firestore](https://firebase.google.com/docs/firestore?ref=streamlit.ghost.io) as well as went over what Firestore is and how it can help in your Streamlit apps.   
  
Today, we'll dive into the exciting stuff: In Part 3 we'll code up the [Firestore Reddit app](https://github.com/akrolsmir/streamlit-reddit?ref=streamlit.ghost.io), then in Part 4 we'll [add secrets](https://streamlit.ghost.io/secrets-in-sharing-apps/) and make it live for the whole world!

## Part 3: Building your Reddit clone

### Reading one post

Let's start by replacing our `streamlit_app.py` , to check that Firestore is indeed set up correctly:

```
import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Create a reference to the Google post.
doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())(
```

What is `doc_ref` here? It's short for "document **reference**". You can think of a reference to be like the *title* of a book that you want to get from the library. Creating a reference is really fast, but there's no data in the reference itself. In order to download the data that the reference is talking about, you have to call `.get()` on that reference — which, going by the analogy, is when the librarian takes the *title* and fetches the corresponding book. Creating a `doc_ref` is really fast; calling `.get()` can be a lot slower!

💡 **Pro-tip:** Remember, it's `$ streamlit run streamlit_app.py` to run your code locally, and you will see it on `http://localhost:8501`. I'd encourage you to turn on "Always rerun" in the top right hamburger menu of your app at this point, so that Streamlit will automatically update each time you save your Python code.

If this is what you see after running through the above:

![1-10](https://streamlit.ghost.io/content/images/2021/08/1-10.png#border)

Then congrats! Your Streamlit app has successfully read from the Firestore database.

### Writing one post

Next up, let's create a new document directly in Python. Start the same way — by making a `doc_ref`, but this time filling in the ID you want to use for your new document. Then, you can call `.set()` with a Python dictionary containing the data you wanted. Here's what that looks like:

```
# This time, we're creating a NEW post reference for Apple
doc_ref = db.collection("posts").document("Apple")

# And then uploading some data to that reference
doc_ref.set({
	"title": "Apple",
	"url": "www.apple.com"
})
```

### Reading ALL posts

If we don't know the ID of the post we want, or want to list all of the posts, that's straightforward too! Form a reference to the whole collection of `posts`, and call `.stream()` to get a list of docs you can iterate through.

You may have noticed already, but for each `doc` we get, we convert it to a Python dict using `.to_dict()` so that we can work with it. As with any Python dict, you can then get its values with bracket notation (`doc.to_dict()["url"]`).

```
# Now let's make a reference to ALL of the posts
posts_ref = db.collection("posts")

# For a reference to a collection, we use .stream() instead of .get()
for doc in posts_ref.stream():
	st.write("The id is: ", doc.id)
	st.write("The contents are: ", doc.to_dict())
```

![2-11](https://streamlit.ghost.io/content/images/2021/08/2-11.png#border)

That's all the database operations we'll need to build our Reddit clone! Now we can start diving into combining these database calls with our Streamlit widgets to build the full app.

### Streamlit Widgets and Firestore

To let our users create new posts, we can use 3 widgets:

* A `st.text_input` to write in the `title` of the post
* A `st.text_input` for the `url`
* And a `st.button` to allow the user to submit

Then, let's clean up the rendering of the posts to use some nice Markdown formatting. Here's what we have so far in `streamlit_app.py`

```
import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json("firestore-key.json")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")
```

Which turns into this Streamlit app:

![3-8](https://streamlit.ghost.io/content/images/2021/08/3-8.png#border)

Isn't that cool? In less than 30 lines of code, you've made a web app that creates new posts and saves them. Your database means that all this data is backed up. Run this Streamlit app on another browser tab (or even another computer entirely) and you'll see the exact same data! And changes on one app will be shared to EVERY app 😮

## Part 4: Securely deploying on Streamlit sharing

💡 **Pro-tip:** To use [secrets](https://streamlit.ghost.io/secrets-in-sharing-apps/) in your Streamlit deployed apps you'll first need an invite to sharing. [Request an invite here](https://streamlit.io/sharing-sign-up?ref=streamlit.ghost.io) if you're not already in the beta!  
  
All right. Before we deploy this lovely Reddit clone to Streamlit sharing so that the whole world can access it, there's one thing we need to take care of. Remember the `firestore-key.json` file, the password that our Python code uses to sign in to Firestore? If we commit and push that file onto GitHub, it would be like sharing your password with the entire internet...

This is where Secrets comes in! Secrets are a way to pass in information that your app needs to know, but you don't want to publish on GitHub. Here's how we can securely upload our Firestore key:

### **Convert our JSON key into a `secrets.toml` file**

[JSON](https://learnxinyminutes.com/docs/json/?ref=streamlit.ghost.io) and [TOML](https://learnxinyminutes.com/docs/toml/?ref=streamlit.ghost.io) are two different file formats, but the core idea is pretty similar - they both make it easy to pass around a bunch of string keys and their corresponding values. (One way to think of JSON & TOML are as representations of a Python dictionary, but written as a file.) Firestore gave us our secrets as a JSON file, but Streamlit secrets expect a TOML; let's convert between them with a Python script!

Go ahead and copy this code into a new script, `key-to-toml.py`

```
import toml

output_file = ".streamlit/secrets.toml"

with open("firestore-key.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)
```

And then run the script:

```
$ python key-to-toml.py
```

Your  `firestore-key.json` has now been written out to `.streamlit/secrets.toml`! Now we can update our Streamlit app to use this new TOML file when initializing the Firestore library:

```
# Replace:
db = firestore.Client.from_service_account_json("firestore-key.json")

# With:
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit")
```

When you're done, double-check your Streamlit app — everything should work the same, reading and writing from Firestore. That's because the new `st.secrets` knows to look for a file called `.streamlit/secrets.toml` when Streamlit is running on your local machine!

### Ignoring **our local secret files in git**

Now that we've converted our secret key, we're almost ready to push the code to GitHub. We just need to configure git to ignore our secret files, done by the handy-dandy `.gitignore` file:

```
secrets.toml
firestore-key.json
```

Now, all changes in these two secret files will be safely excluded when you push your code. Let's do that now. From a command line:

```
$ git commit -am 'Read and write to Firestore, securely!'
$ git push
```

You can look on GitHub to see that your code is all there, minus the two secret files~

### Adding the **secret to Streamlit sharing**

Normally, a git push is all we need to update any Streamlit sharing app. But because we're adding secrets, we need paste those secrets to the sharing dashboard. You can do this by copying the entire contents of `.streamlit/secrets.toml`, and pasting it here:

![4.1-2](https://streamlit.ghost.io/content/images/2021/08/4.1-2.png#browser)

Aaaand that's it! Go to your app; you should see it deployed to the entire world. Congrats🎈

## Wrapping up

That's the end of this tutorial... but it doesn't have to be the end of your app! There's a lot of other cool things you can do with Firestore in Streamlit, such as:

* [Nesting documents inside of documents](https://firebase.google.com/docs/firestore/manage-data/structure-data?ref=streamlit.ghost.io) (e.g. to implement upvotes and comments)
* [Forming complex queries](https://firebase.google.com/docs/firestore/query-data/queries?ref=streamlit.ghost.io#python) (e.g. getting the 10 most recent posts created by Alice)
* [Listening for updates in REAL TIME](https://firebase.google.com/docs/firestore/query-data/listen?ref=streamlit.ghost.io#python) (e.g. to make a chat app)

There's so many awesome places to go from here — I can't wait to see what you make. Share your work with the entire community by posting below in the comments!

## Resources

* [Firestore](https://firebase.google.com/docs/firestore?ref=streamlit.ghost.io)
* [Streamlit docs](https://docs.streamlit.io/en/stable/index.html?ref=streamlit.ghost.io)
* [Streamlit Github](https://github.com/streamlit/?ref=streamlit.ghost.io)
* [Streamlit Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)
* [Sharing sign-up](https://streamlit.io/sharing?ref=streamlit.ghost.io)

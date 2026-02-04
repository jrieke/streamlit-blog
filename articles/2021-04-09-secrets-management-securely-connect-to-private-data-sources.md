---
title: "Secrets Management & Securely Connect to Private Data Sources"
subtitle: "Use Secrets Management in Streamlit sharing to securely connect to private data sources"
date: 2021-04-09
authors:
  - "James Thompson"
category: "Tutorials"
---

![Add secrets to your Streamlit apps](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--5-.svg)


Many Streamlit apps require access to private data like API keys, database passwords, or other credentials. To keep your data safe, it's best practice to never store such credentials directly in your hosted repo. That's why we're excited to introduce **Secrets Management** -a simple way to securely store your passwords, keys, or really anything you wouldn't want stored in your hosted repo, as secrets that get passed to your app as environment variables.

Below is a quick guide on how to add secrets to your deployed apps – it's really easy to do, we promise 😊.   
  
💡 **But before we jump in**, Secrets Management is a feature of Streamlit's free sharing platform, so if you're not already using that - [request an invite here](https://streamlit.io/sharing?ref=streamlit.ghost.io). Invites are sent out daily, so the wait won't be long!

## How to use Secrets Management

### Deploy an app and set up secrets

The first thing you'll want to do is go to [http://share.streamlit.io/](http://share.streamlit.io/deploy?ref=streamlit.ghost.io) and click "New app." Next, click the "Advanced settings..." option. A modal with Advanced settings will appear. And here you'll see an input box to insert your secrets.

![gif-1-4](https://streamlit.ghost.io/content/images/2021/08/gif-1-4.gif#browser)

Add your secrets in the "Secrets" field using the [TOML](https://toml.io/en/latest?ref=streamlit.ghost.io) format. For example:

```
# Everything in this section will be available as an environment variable 
db_username = "Jane"
db_password = "12345qwerty"

# You can also add other sections if you like.
# The contents of sections as shown below will not become environment variables,
# but they'll be easily accessible from within Streamlit anyway as we show
# later in this doc.   
[my_cool_secrets]
things_i_like = ["Streamlit", "Python"]
```

Click save and then your secrets will be added!

### Use secrets in your Streamlit app

To use secrets in your app, you'll want to access your secrets as environment variables or by querying the `st.secrets` dict. For example, if you enter the secrets from the section above, the code below shows you how you can access them within your Streamlit app.

```
import streamlit as st

# Everything is accessible via the st.secrets dict:

st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:

import os
st.write(
	"Has environment variables been set:",
	os.environ["db_username"] == st.secrets["db_username"])
```

### Edit your app's secrets

Adding or updating secrets in deployed apps is straightforward. You'll want to:

* Go to [https://share.streamlit.io/](https://share.streamlit.io/?ref=streamlit.ghost.io)
* Open the menu for the app that needs updating, and click "Edit Secrets." A modal will appear with an input box to insert your secrets.

![4.1-1](https://streamlit.ghost.io/content/images/2021/08/4.1-1.png#browser)

* Once you finish editing your secrets, click "Save". It might take a few seconds for the update to be propagated to your app, but the new values will be reflected when the app re-runs.

### Develop locally with secrets

While the above focuses on deployed apps, you can also add secrets while developing locally. To do this, add a file called `secrets.toml` in a folder called `.streamlit` at the root of your app repo and paste your secrets into that file.

💡 **NOTE:** Be sure to add `.streamlit` to your `.gitignore` so you don't commit your secrets!

## **Let us know how it works for you 🎈**

That's it! You'll now be able to add secrets to any of your sharing apps. And if you aren't deploying yet, then remember to [request an invite here](https://streamlit.io/sharing?ref=streamlit.ghost.io).

We can't wait to hear what you think and we hope this gives you more flexibility in what you can deploy. We'd love to see your updated apps so make sure to tag `@streamlit` when you share on [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io) or [LinkedIn](https://www.linkedin.com/company/streamlit/?ref=streamlit.ghost.io), and please let us know if you have any questions [on the forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)!

## Resources

* [Streamlit docs](https://docs.streamlit.io/en/stable/index.html?ref=streamlit.ghost.io)
* [Secrets Management docs](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management?ref=streamlit.ghost.io)
* [Github](https://github.com/streamlit/?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)
* [Sharing sign-up](https://streamlit.io/sharing?ref=streamlit.ghost.io)

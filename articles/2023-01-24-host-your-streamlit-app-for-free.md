---
title: "Host your Streamlit app for free"
subtitle: "Learn how to transfer your apps from paid platforms to Streamlit Community Cloud"
date: 2023-01-24
authors:
  - "Chanin Nantasenamat"
category: "Tutorials"
---

![Host your Streamlit app for free](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--4-.svg)


If you have a Streamlit app but don’t want to pay a monthly fee to host it on a commercial cloud platform, one option is to migrate it to Streamlit Community Cloud. It’s FREE!

In this post, I’ll show you how to build a demo app and deploy it to Community Cloud step-by-step:

* Step 1. Create a simple Streamlit app
* Step 2. Set up an account on Community Cloud
* Step 3. Connect your account to GitHub
* Step 4. Create a GitHub repo of your app
* Step 5. Deploy your app in a few clicks

Can’t wait to see it in action? Here's the [demo app](https://coding-hello.streamlit.app/?ref=streamlit.ghost.io) and the [repo code](https://github.com/coding-professor/st-hello-world/tree/main?ref=streamlit.ghost.io).

But before we get to the fun stuff, let’s talk about…

### Why deploy your apps to the internet?

Deploying your apps to the internet allows users to access them from a web browser—without having to set up a coding environment and installing dependencies.

You have two options:

1. Manually set up a virtual private server for deploying your app.
2. Host the app in a GitHub repository and deploy it to a cloud platform.

![](https://streamlit.ghost.io/content/images/2022/08/E55BB258-DA30-4262-BDAA-7B2C6A0E5E15.jpeg)

The first option gives you full control. You can set up everything locally. But it can take time—for both the setup and the maintenance (like keeping OS up-to-date, etc.).

The second option is the simplest. Just push your app to GitHub. If it’s properly configured with a cloud platform, it’ll automatically update your code changes.

### Why use Community Cloud?

Here’s why you might want to use Community Cloud to host your apps:

| Advantages | Description |
| --- | --- |
| Free | You can deploy Streamlit apps for free! |
| Deploy in one click | Your fully hosted app is ready to be shared in under a minute. |
| Keep your code in your repo | No changes to your development process. Your code stays on GitHub. |
| Live updates | Your apps update instantly when you push code changes. |
| Securely connect to data | Connect to all your data sources using secure protocols. |
| Restrict access to apps | Authenticate viewers with per-app viewer allow-lists. |
| Easily manage your apps | View, collaborate, and manage all your apps in a single place. |

### Step 1. Create a simple Streamlit app

First, let’s make a simple app that prints out `Hello world!` . It takes only two lines of code (for a deeper dive, read [this post](https://streamlit.ghost.io/how-to-master-streamlit-for-data-science/)).

Go ahead and create a `streamlit_app.py` file:

```
import streamlit as st

st.write('Hello world!')
```

### Step 2. Set up an account on Community Cloud

Go to [Community Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io) and click “Sign up” to create a free account with your existing Google, GitHub, or email account:

![324BEA1A-997C-49E7-A279-040300162E27](https://streamlit.ghost.io/content/images/2022/08/324BEA1A-997C-49E7-A279-040300162E27.jpeg#browser)

Next, enter your GitHub credentials and click on “Authorize streamlit” to let Streamlit access your GitHub account:

![40F6254E-3523-4ADE-B9B6-D4436FE8B68A](https://streamlit.ghost.io/content/images/2022/08/40F6254E-3523-4ADE-B9B6-D4436FE8B68A.jpeg#browser)

Finally, enter your information and click “Continue”:

![2B353264-DDBA-4251-94E4-7CF77A256B9B](https://streamlit.ghost.io/content/images/2022/08/2B353264-DDBA-4251-94E4-7CF77A256B9B.jpeg#browser)

Congratulations! You have signed up for your workspace in Community Cloud.

### Step 3. Connect your account to GitHub

There are two options to connect your Community Cloud account to GitHub:

**Option  1**

Click on “New app”:

![6FD187E5-2A74-4205-97B9-E19890E6C741](https://streamlit.ghost.io/content/images/2022/08/6FD187E5-2A74-4205-97B9-E19890E6C741.jpeg#browser)

On the authorization page, click on “Authorize streamlit."

**Option 2**

Click “Settings,” then “Linked accounts,” then “Allow access”:

![F2A5148A-2F6F-48D2-B935-A38542A87468](https://streamlit.ghost.io/content/images/2022/08/F2A5148A-2F6F-48D2-B935-A38542A87468.jpeg#browser)

This will let Community Cloud deploy your Streamlit apps from your GitHub repositories. On the authorization page, click “Authorize streamlit."

**GitHub-linked account**

Once you log in, Community Cloud will get access to your GitHub account:

![16FA6767-9630-4C65-869D-77E2B2FC4199](https://streamlit.ghost.io/content/images/2022/08/16FA6767-9630-4C65-869D-77E2B2FC4199.jpeg#browser)

Now you’re ready to deploy Streamlit apps!

But first, let’s create a GitHub repo.

### Step 4. Create a GitHub repo of your app

Click “+” and then “New repository”:

![A15327B7-F711-448A-BB97-A1CF2580BBC7](https://streamlit.ghost.io/content/images/2022/08/A15327B7-F711-448A-BB97-A1CF2580BBC7.jpeg#browser)

This will bring you to the “Create a new repository” page.

In the field “Repository name” type in `st-hello-world`, click “Public,” check “Add a README file” (your new repo will get a `README.md` file), and click “Create repository”:

![1F88C1F7-893E-432D-9E7B-AEFD23D4D0B3](https://streamlit.ghost.io/content/images/2022/08/1F88C1F7-893E-432D-9E7B-AEFD23D4D0B3.jpeg#browser)

Your repo is all set up!

Now create your app file:

![7A37797E-C57A-4560-8104-790FA5537DEF](https://streamlit.ghost.io/content/images/2022/08/7A37797E-C57A-4560-8104-790FA5537DEF.jpeg#browser)

Next, create the `streamlit_app.py`:

![1825A4E6-9D5C-43DF-A4E3-DCC3FE2A5F37](https://streamlit.ghost.io/content/images/2022/08/1825A4E6-9D5C-43DF-A4E3-DCC3FE2A5F37.jpeg#browser)

Your GitHub repo will be populated with `README.md` and `streamlit_app.py` files.

Next, head back to Community Cloud:

![72631AEA-B0B9-412E-BA7C-06B3382855FA](https://streamlit.ghost.io/content/images/2022/08/72631AEA-B0B9-412E-BA7C-06B3382855FA.jpeg#browser)

### Step 5. Deploy your app in a few clicks

At last, here comes the fun part. You get to deploy your app!

Click “New app" and fill out the information for your app:

![9E0C7298-B079-4074-9DBB-EE9C04D14C31](https://streamlit.ghost.io/content/images/2022/08/9E0C7298-B079-4074-9DBB-EE9C04D14C31.jpeg#browser)

This will spin up a new server. You’ll see the message, “Your app is in the oven.”

In the bottom right-hand corner, click “Manage app” to see the log messages (use them for debugging and troubleshooting errors):

![EE1466B0-0A0C-4BD9-8B1E-02A37A380CF4](https://streamlit.ghost.io/content/images/2022/08/EE1466B0-0A0C-4BD9-8B1E-02A37A380CF4.jpeg#browser)

The side menu displays all log messages in real-time:

![153F5C49-8CDC-4B1E-AFAE-AECC7AA4F849](https://streamlit.ghost.io/content/images/2022/08/153F5C49-8CDC-4B1E-AFAE-AECC7AA4F849.jpeg#browser)

Once your app finishes compiling, you’ll see the output. In our example, it’ll be a simple message: `Hello world!`

![IMG_0430](https://streamlit.ghost.io/content/images/2022/08/IMG_0430.png#browser)

### Wrapping up

Congratulations! You have successfully deployed your app to Streamlit Community Cloud. Now you can share the [app URL](https://coding-professor-st-hello-world-streamlit-app-qj9a1u.streamlitapp.com/?ref=streamlit.ghost.io) with the community.

If a tutorial video is your thing, check out the following video:

Read more about:

* [Self-hosting](https://docs.streamlit.io/knowledge-base/deploy/deploy-streamlit-heroku-aws-google-cloud?ref=streamlit.ghost.io) Streamlit apps on your own servers (AWS, Azure, etc.).
* Different [Streamlit use cases](https://streamlit.ghost.io/tag/community/) from the community.

If you have any questions, please leave them in the comments below or contact me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=streamlit.ghost.io) or on [LinkedIn](https://www.linkedin.com/in/chanin-nantasenamat/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

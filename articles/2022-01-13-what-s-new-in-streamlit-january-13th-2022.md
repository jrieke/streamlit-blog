---
title: "What\u2019s new in Streamlit (January 13th,  2022)"
subtitle: "Check out what\u2019s new in Streamlit Cloud and the 1.4.0 release"
date: 2022-01-13
authors:
  - "Krista Muir"
category: "Release Notes"
---

![What’s new in Streamlit (January 13th,  2022)](https://streamlit.ghost.io/content/images/size/w2000/2022/01/Sign-In-Image.png)


Hey, Streamlit community! 👋

We’re excited to share what’s new in the 1.4.0 release and some recent updates to Streamlit Cloud, including notable updates like introducing `st.camera_input`, clearing individual memo and singleton functions in code, signing in to Streamlit Cloud with your email, and app email invites.

Keep reading to learn more.

# **✨ New in Streamlit**

## ⛑️ **Release 1.4.0**

### **📸 Introducing `st.camera_input` for uploading camera images**

We’re introducing a new widget to use webcams! It’s great for computer vision apps. For example, imagine an app for face detection or style transfer.

Here is how you can use this widget:

```
img_file = st.camera_input("Webcam image")
```

The returned `img_file` is a file-like object, similar to the return value of `st.file_uploader`. For a simple app, you can display the image captured by the webcam by using `st.image`:

```
img_file = st.camera_input("Webcam image")
if img_file is not None:
    st.image(img_file)
```

Of course, if you want to, you can do any processing steps on the image in between.

Here’s what the new widget looks like in the app:

![](https://streamlit.ghost.io/content/images/2022/01/st.camera_input.png)

Try it out in [our demo app](https://share.streamlit.io/streamlit/release-demos/1.4.0/1.4.0/streamlit_app.py?page=headliner&ref=streamlit.ghost.io) and take a look at the [documentation](https://docs.streamlit.io/library/api-reference/widgets/st.camera_input?ref=streamlit.ghost.io).

### **🪁 Clear memo + singleton caches procedurally**

Do you need more control over cache invalidation? Now you can finally clear caches of functions decorated with `@st.experimental_memo` and `@st.experimental_singleton` *in code*. (The Streamlit community has been asking for this *forever*—and so have we, internally.)

We have implemented programmatic clearing of memo + singleton functions. For example, you can do the following:

```
@st.experimental_memo
def foo(x):
    return x**2

if st.button("Clear Foo"):
    # Clear foo's memoized values:
    foo.clear()

if st.button("Clear All"):
	  # Clear values from *all* memoized functions:
		st.experimental_memo.clear()
```

**API Details**

* Any function annotated with `@st.experimental_memo` or `@st.experimental_singleton` gets its own `clear()` function automatically.
* Additionally, you can use `st.experimental_memo.clear()` and `st.experimental_singleton.clear()` to clear *all* memo and singleton caches, respectively.

Note that because memo/singleton themselves are experimental APIs, these cache-clearing functions are experimental as well. See the docs for [memo](https://docs.streamlit.io/library/api-reference/performance/st.experimental_memo?ref=streamlit.ghost.io) and [singleton](https://docs.streamlit.io/library/api-reference/performance/st.experimental_singleton?ref=streamlit.ghost.io).

### 🔦 **Other notable 1.4.0 release updates**

One other notable update in this release:

* 🚦 Widgets now have the `disabled` parameter that removes interactivity ([#4154](https://github.com/streamlit/streamlit/pull/4154?ref=streamlit.ghost.io)).

[Click here](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io#version-140) to check out all updates.

## **☁️ Streamlit Cloud updates**

### 📩 **Sign in with email**

You can now sign in to Streamlit Cloud by using an email!

![](https://streamlit.ghost.io/content/images/2022/01/sign-in-2.png)

After entering your email on the sign-in page, you’ll get an email with a sign-in link:

![](https://streamlit.ghost.io/content/images/2022/01/Image-13.01.22.png)

Clicking on the link will log you into your Streamlit Cloud console. From there you can view all of your apps. See the [docs](https://docs.streamlit.io/streamlit-cloud/get-started?ref=streamlit.ghost.io#log-in-to-sharestreamlitio) for more information.

### 📲 **Share apps with any email address**

Apps deployed with [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io) come with built-in authentication. Until now, sharing has been limited to Google email addresses (Gmail) or accounts that have SSO setup.

Starting today, you can share your app with any viewer whether they’re part of your company or another company. Simply add the viewers’ email addresses, and you’re done!

### 🔦 **Other notable Streamlit Cloud updates**

* 🤯 The error page when your app goes over resource limits now shows more helpful info for debugging.
* 🐙 Your app now prints a message to its Cloud logs whenever it updates due to a Github commit.
* ⭐ Streamlit Cloud now supports a "favorite" feature that lets you quickly access your apps from the app dashboard (favorited apps appear at the top).
* 🚀 When you invite someone to view your app in Streamlit Cloud, the recipient will receive an invitation to view the app as an email in their inbox!
* 🔒 We're committed to meeting industry standards and are now SOC 2 Type 1 certified. [Read more](https://streamlit.ghost.io/streamlit-cloud-is-now-soc-2-type-1-compliant/) about securely sharing your apps using Streamlit Cloud.

If you're new to Streamlit, now is the time to try [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io#plans)!

## 🌞 **Wrapping up**

Thanks for checking out what’s new with Streamlit. You can always see the most recent updates to our core library on our [changelog](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io) or via [this tag on the forum](https://discuss.streamlit.io/tag/release-notes?ref=streamlit.ghost.io) and to Streamlit Cloud via the [Cloud Release Notes](https://share.streamlit.io/streamlit/cloud_release_notes_app/main/main.py?ref=streamlit.ghost.io).

Got questions? Let us know in the comments below. We're looking forward to hearing what you think!

Happy Streamlit-ing! 🎈

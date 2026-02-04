---
title: "Develop Streamlit-WebRTC Component for Real-Time Video Processing"
subtitle: "Introducing the WebRTC component for real-time media streams"
date: 2021-02-12
authors:
  - "Yuichiro Tachibana (Tsuchiya)"
category: "Advocate Posts"
---

![Developing a streamlit-webrtc component for real-time video processing](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--13-.svg)


Real-time video processing is one of the most important applications when developing various computer vision or machine learning models. It’s useful because it allows users to quickly verify what their models can do with handy video input from their own devices, such as webcams or smartphones.

But it also presents a challenge to those of us using Streamlit, since Streamlit doesn’t natively support real-time video processing well yet through its own capabilities.

I created [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc?ref=streamlit.ghost.io), a component that enables Streamlit to handle real-time media streams over a network to solve this problem. In this in-depth tutorial, I’ll also briefly introduce you to WebRTC (check out [my article here](https://dev.to/whitphx/python-webrtc-basics-with-aiortc-48id?ref=streamlit.ghost.io) for more in-depth info on WebRTC). If you want to jump right to playing with the component [here is a sample](https://share.streamlit.io/whitphx/streamlit-webrtc-example/main/app.py?ref=streamlit.ghost.io) app.

Ready?

Let’s dive in.

(This tutorial requires Python >= 3.6 and a webcam.)

## The problem with existing approaches

Streamlit is actively used by many developers and researchers to prototype apps backed with computer vision and machine learning models, but it can’t yet natively support real-time video processing.

One existing approach to achieve real-time video processing with Streamlit is to use OpenCV to capture video streams. However, this only works when the Python process can access the video source - in other words, only when the camera is connected to the same host the app is running on.

Due to this limitation, there have always been problems with deploying the app to remote hosts and using it with video streams from local webcams. `cv2.VideoCapture(0)` consumes a video stream from the first (indexed as 0) locally connected device, and when the app is hosted on a remote server, the video source is a camera device connected to the *server* - not a local webcam.

### How WebRTC resolves this issue

WebRTC (Web Real-Time Communication) enables web servers and clients, including web browsers, to send and receive video, audio, and arbitrary data streams over the network with low latency.

It is now supported by major browsers like Chrome, Firefox, and Safari, and its specs are open and standardized. Browser-based real-time video chat apps like Google Meet are common examples of WebRTC usage.

WebRTC extends Streamlit’s powerful capabilities to transmit video, audio, and arbitrary data streams between frontend and backend processes, like browser JavaScript and server-side Python.

# The WebRTC basics

The following tutorial uses knowledge about WebRTC concepts such as "Signaling", "Offer", and "Answer". The below figure provides a simple summary of how to establish a WebRTC connection.

![5-5](https://streamlit.ghost.io/content/images/2021/08/5-5.png#border)

* WebRTC has a preparation phase called "Signaling", during which the peers exchange data called "offers" and "answers" in order to gather necessary information to establish the connection.
* Developers choose an arbitrary method for Signaling, such as the HTTP req/res mechanism.

If you want to know more about these concepts, read [this article](https://dev.to/whitphx/python-webrtc-basics-with-aiortc-48id?ref=streamlit.ghost.io).

Just as in the article linked above, **this tutorial will use `aiortc`, a Python library for WebRTC, and [an example from the `aiortc` repository](https://github.com/aiortc/aiortc/tree/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server?ref=streamlit.ghost.io) as the basis for our sample project.**

# The basics of Streamlit's execution model

To read further, you should know about the development of Streamlit bi-directional custom components and about Streamlit's execution model. You can learn about it [here](https://docs.streamlit.io/en/stable/streamlit_components.html?ref=streamlit.ghost.io).

Here is a short summary:

![2-8](https://streamlit.ghost.io/content/images/2021/08/2-8.png#border)

* Upon each execution, the Python script is executed from top to bottom.
* Each execution of the Python script renders the frontend view, sending data from Python to JS as arguments to the component.
* The frontend triggers the next execution via `Streamlit.setComponentValue()`, sending data from JS to Python as a component value.

# Integrate `aiortc` into a Streamlit component

In this section, to understand how to integrate a WebRTC implementation into a Streamlit custom component, we will create a minimal version of `streamlit-webrtc` called `tiny-streamlit-webrtc`, as a hands-on tutorial.

The source code of `tiny-streamlit-webrtc` is [hosted on GitHub](https://github.com/whitphx/tiny-streamlit-webrtc?ref=streamlit.ghost.io). Throughout this tutorial, we will refer to this repository and review each intermediate commit step-by-step to reach the final version.

It is recommended for you to clone the repository:

```
$ git clone https://github.com/whitphx/tiny-streamlit-webrtc.git
$ cd tiny-streamlit-webrtc
```

With the below command, you can check out the specific revision referenced in each section in order to see the entire codebase and to actually try running it.

```
$ git checkout <revision>
```

### Install dependencies

Install the necessary packages. Note that this tutorial does not work with the latest version of `aiortc` (`1.1.1`) and `1.0.0` must be used.

```
$ pip install streamlit opencv-python
$ pip install aiortc==1.0.0
```

### Setting up the project

As usual, we start with the [official template of a bi-directional component](https://github.com/streamlit/component-template/tree/4b90f5277379a548792af51506254aee31854316/template?ref=streamlit.ghost.io). The reference [`tiny-streamlit-webrtc` implementation](https://github.com/whitphx/tiny-streamlit-webrtc?ref=streamlit.ghost.io) is based on the revision `4b90f52`.

After copying the template files, complete the rest of the setup, including the steps below.

* Rename "`my_component`" to "`tiny_streamlit_webrtc`".
* Run `npm install` in `tiny_streamlit_webrtc/frontend`.
* Remove the existent code, comments, and docstrings.
* Add necessary files such as `.gitignore`

Check out [what this section does](https://github.com/whitphx/tiny-streamlit-webrtc/compare/13660f3..f6daf28?ref=streamlit.ghost.io), with code version `f6daf28`.

### Rolling out the first frontend implementation

Let's start writing code.

First, we will simply copy and paste some lines of code from `index.html` and `client.js` in [the `aiortc` example](https://github.com/aiortc/aiortc/tree/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server?ref=streamlit.ghost.io) into our React component, but with some fixes.

`e3f70e4` is the actual edit, and you can try this version by checking out the commit, as explained above.

```
$ git checkout e3f70e4
```

The view contains only a `<video />` element with `autoPlay` and `playsInline` props, as it is in the original `index.html`, and a button element to start the WebRTC session. The start button's `onClick` handler is bound to the `start()` method, which is copied from `client.js` and slightly modified to remove some lines unnecessary for this tutorial and adjust to the React class-based component style. We will do the same for `negotiate()` and `createPeerConnection()`.

Let's run this component in the usual manner for Streamlit custom component development.

```
$ cd tiny_streamlit_webrtc/frontend/
$ npm start
```

```
$ streamlit run tiny_streamlit_webrtc/__init__.py
```

After opening the app with a web browser, open the developer tools, and click the "Start" button. You can see the offer is generated and printed in the console as below.

![3-5](https://streamlit.ghost.io/content/images/2021/08/3-5.png#border)

This is printed via [this line](https://github.com/whitphx/tiny-streamlit-webrtc/commit/e3f70e44bbd17d383abfdbef2f2d9e961d1a47e6?ref=streamlit.ghost.io#diff-c0bb5335a5a993d716414831b4151b2a7070e4533adb552831b5f22a4b32da1cR83). Please follow the steps leading up to it. This code is equivalent to [the code in the original example](https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/client.js?ref=streamlit.ghost.io#L70) *before* sending the offer to the Python server. Yes, this case is different from the original example. How can we send the offer to the Python process?

(You also see your webcam become active since `navigator.mediaDevices.getUserMedia()` requests its use.)

### Send offer from JS to Python

`streamlit-webrtc` makes use of `Streamlit.setComponentValue()` for this purpose. We will learn about it in this section.

[`7b7dd2d`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/7b7dd2d2f9289b7f6697a3ab915fd8dc6438afd9?ref=streamlit.ghost.io) is the next update. Use `git checkout 7b7dd2d` to check out it.

With this change, the offer is sent from the frontend to the server as a component value.

```
const offerJson = offer.toJSON()
Streamlit.setComponentValue({
  offerJson,
})
```

The offer can be read on the server-side as below.

```
component_value = _component_func(key=key, default=None)
if component_value:
    offer_json = component_value["offerJson"]
```

Let's run this version and confirm the offer is displayed after clicking the "Start" button, which means the offer is received by the Python process and shown with `st.write()` [here](https://github.com/whitphx/tiny-streamlit-webrtc/commit/7b7dd2d2f9289b7f6697a3ab915fd8dc6438afd9?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR24).

![4-3](https://streamlit.ghost.io/content/images/2021/08/4-3.png#border)

### Server-side implementation with `asyncio`

Now the offer is received on the server-side, so let's implement the code to process it. Just as we did with the frontend, let's copy and paste from the example `server.py` to our `streamlit_webrtc/__init__.py`, like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/92416e63b6d09ee77f6b5739af73a888d15fe96b?ref=streamlit.ghost.io), which is copied from [`offer()` coroutine in the example `server.py`](https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/server.py?ref=streamlit.ghost.io#L102-L167).

Note that a video transformer is temporarily omitted from the `track` event listener [like this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/92416e63b6d09ee77f6b5739af73a888d15fe96b?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR37) to focus on the WebRTC part for now. It now just passes through the input track to the output.

However, as you can see, this code contains `async` and `await` and does not work in a function. So, we have to wrap this part in a coroutine like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/a6f7cc050b5fd07f49800bf264ec7fc34d70bdbb?ref=streamlit.ghost.io).

Please run [this version: `a6f7cc0`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/a6f7cc050b5fd07f49800bf264ec7fc34d70bdbb?ref=streamlit.ghost.io) and confirm the answer is displayed following the offer from [here](https://github.com/whitphx/tiny-streamlit-webrtc/commit/a6f7cc050b5fd07f49800bf264ec7fc34d70bdbb?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR55). That means the server-side `pc` object has processed the offer and generated the answer.

![5-6](https://streamlit.ghost.io/content/images/2021/08/5-6.png#border)

What we have to do next is send it back to the frontend.

### Send back the answer from Python to JS

To do this, `streamlit-webrtc` simply relies on Streamlit's data sending mechanism from Python to JavaScript as below.

```
_component_func(key=key, answer=answer)
```

However, one problem arises. We’ve already called `component_value = _component_func(...)` and obtained the offer from it. After that, we generated the answer. So, how can we set the argument to the already called `_component_func()` again?

Simply calling the second `_component_func()` as below does not work, because in the Streamlit app, different `_component_func()` calls are recognized as different instances of the component.

```
component_value = _component_func()
offer = component_value["offer"]
answer = generate_answer(offer)  # Pseudo code
_component_func(answer=answer)  # This does not work!
```

invalid\_answering.py

To resolve this problem, we have to introduce a hack: `SessionState` and `st.experimental_rerun()`. With these tools, we can rerun the script to call a `_component_func()` in the same line again and hold a variable over the runs to feed it to the `_component_func()` in the second and later executions.

`SessionState` has been discussed in [this forum topic](https://discuss.streamlit.io/t/is-there-any-working-example-for-session-state-for-streamlit-version-0-63-1/4551?ref=streamlit.ghost.io) and the source is available on [this page in Gist](https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92?ref=streamlit.ghost.io).

`st.experimental_rerun()` seems, as its name implies, to be an experimental API and not documented yet. It has been discussed in [this GitHub issue](https://github.com/streamlit/streamlit/issues/653?ref=streamlit.ghost.io) and can now be used.

Please see [this version of the server-side code](https://github.com/whitphx/tiny-streamlit-webrtc/commit/aa2ab49606060e4a038f392500aecbe95c4ec758?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7e), where `SessionState` and `st.experimental_rerun()` are used to feed the generated answer to the component.

This illustrates how it works.

![6-1](https://streamlit.ghost.io/content/images/2021/08/6-1.png#border)

Another important thing here is that the `key` argument is no longer optional but must be explicitly provided like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/aa2ab49606060e4a038f392500aecbe95c4ec758?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR83). As the answer is fed as an argument to `_component_func()` and its value changes over the runs, `key` is necessary as a stable identifier of the component instance.

If `key` is `None`, Streamlit identifies the component instance based on arguments other than `key`, so Streamlit cannot trace the identity of the component instance over the runs as the answer changes.

Note that [this if-clause](https://github.com/whitphx/tiny-streamlit-webrtc/commit/aa2ab49606060e4a038f392500aecbe95c4ec758?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR64) is added to invoke `st.experimental_rerun()` only the first time the server-side process gets the offer from the frontend. This may also be achieved by resetting the component value on the frontend once the offer is passed to Python.

With [this version: `aa2ab49`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/aa2ab49606060e4a038f392500aecbe95c4ec758?ref=streamlit.ghost.io), you can see the answer is provided as a field of the `args` prop like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/aa2ab49606060e4a038f392500aecbe95c4ec758?ref=streamlit.ghost.io#diff-c0bb5335a5a993d716414831b4151b2a7070e4533adb552831b5f22a4b32da1c) on the frontend. Let's confirm it with the browser's devtools.

![7-1](https://streamlit.ghost.io/content/images/2021/08/7-1.png#border)

### Implement `processAnswer()`

Now we have the answer on the frontend. Let's implement the rest of the frontend code like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/7fbf0eb5a72de4ea84b21708df80a396fa3222ff?ref=streamlit.ghost.io).

This code is copied from the [part following receiving the answer in the example `client.js`](https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/client.js?ref=streamlit.ghost.io#L95-L99) and fixed to adjust to ours.

### Introduce a thread running over script executions

It seems we have done all things we have to do, but no video appears when you click the "Start" button with [this version: `7fbf0eb`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/7fbf0eb5a72de4ea84b21708df80a396fa3222ff?ref=streamlit.ghost.io).

The problem resides on the server-side. The server-side WebRTC code from `aiortc` runs on an event loop, which is implicitly started with `asyncio.run()` [here](https://github.com/whitphx/tiny-streamlit-webrtc/blob/7fbf0eb5a72de4ea84b21708df80a396fa3222ff/tiny_streamlit_webrtc/__init__.py?ref=streamlit.ghost.io#L67) now. An event loop is created on which `aiortc` functions rely throughout one Streamlit script execution. But this event loop will be trashed in the next script execution and the `aiortc` can no longer keep working.

To resolve this problem, we will fork a thread and create an event loop inside it to run `aiortc` functions. And the thread object is stored in the `SessionState` to be maintained over the multiple Streamlit script executions.

![8-1](https://streamlit.ghost.io/content/images/2021/08/8-1.png#border)

See [this version of the code: `093f81b`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io). [This `webrtc_worker()` function](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR45-R67) is forked as a thread [here](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR93). Inside this thread, [a new event loop is created](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR48) and the `process_offer()` coroutine is running on it - which was invoked by `asyncio.run()` in the previous revisions of this code. With this change, [`queue.Queue` is introduced](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR92) to [get the answer object in the main thread](https://github.com/whitphx/tiny-streamlit-webrtc/commit/093f81be648ad66082e15448b90b74e24e5897b8?ref=streamlit.ghost.io#diff-6abc149a63c4cc57ae904cb1f4bad9f0d063f70011a4cb9266fb4411ec839a7eR97), which is now generated in the forked thread.

There is one drawback of forking a thread - the `streamlit run` command does not stop when you hit `Ctrl+c`. This is because the forked thread remains even after the main thread is terminated.

To forcefully terminate the process, send it SIGKILL as below.

```
$ ps aux | grep python | grep streamlit  # Find the process ID
whitphx         19118  11.2  0.6  4759304  99928 s003  S+    5:27PM   0:02.06 /path/to/venv/bin/python3.8 /path/to/venv/bin/streamlit run tiny_streamlit_webrtc/__init__.py
$ kill -9 19118  # Send SIGKILL to the process specified with the ID
```

To fix it, the `daemon` option of the forked thread is set to `True` like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/fc48060224bd69e85528a4b0859107a70dfbe0bf?ref=streamlit.ghost.io). With this flag, the script stops correctly when necessary.

> A thread can be flagged as a “daemon thread”. The significance of this flag is that the entire Python program exits when only daemon threads are left.  
> ["Thread Objects"](https://docs.python.org/3/library/threading.html?ref=streamlit.ghost.io#thread-objects) (Python.org)

### Component height adjustment

Let's try out the [current version: `fc48060`](https://github.com/whitphx/tiny-streamlit-webrtc/commit/fc48060224bd69e85528a4b0859107a70dfbe0bf?ref=streamlit.ghost.io). Now, WebRTC works and the video appears with this component! However, the displayed video is cropped and the lower part of it is hidden like below.

![9](https://streamlit.ghost.io/content/images/2021/08/9.png#border)

To fix it, we have to call `Streamlit.setFrameHeight()` when the size of `<video />` element changes. Although it is automatically called when the props are updated, the element resize is not associated with props updates but with starting video streaming.

Now attach `onCanPlay` event handler on the `<video />` element and call `Streamlit.setFrameHeight()` from it like [this](https://github.com/whitphx/tiny-streamlit-webrtc/commit/1a57a9755e0325ed3839bb259a7655bfe94b679e?ref=streamlit.ghost.io#diff-c0bb5335a5a993d716414831b4151b2a7070e4533adb552831b5f22a4b32da1cR39). (While using `ResizeObserver` may be the right way to observe DOM element resizes, we use the `onCanPlay` event here as a substitute, for simplicity's sake.)

Cool! Now it works correctly. 🎉`1a57a97` is this version.

![10](https://streamlit.ghost.io/content/images/2021/08/10.png#border)

Now all the core parts for WebRTC are complete. We’ll implement the rest in the following sections.

### Implementing your own video filter

First, let's try to implement some video filters. `3ba703d` is an example with a simple edge extractor, copied from the [sample code of `aiortc`](https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/server.py?ref=streamlit.ghost.io#L66-L75).

### Implement a stop button

Refer to [the `aiortc` example](https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/client.js?ref=streamlit.ghost.io#L184-L210) to create a stop button to gracefully stop the stream. `13a38c1` is the current version.

# The execution model of `streamlit-webrtc`

We have followed the steps to develop a minimal Streamlit component utilizing WebRTC to stream video.

As we’ve seen in this component, we chose a design in which the computer vision code is running in a callback in the forked thread, triggered by new frame arrivals from the input stream, independent of Streamlit's script execution timings. It looks a little bit weird the first time you see it, but it's necessary and natural when dealing with real-time streams.

Let's see it from a more abstract view. When processing frames coming from real-time streams, the streams are additional event sources other than user interactions through the frontend view. In normal Streamlit apps, all the events triggering Python script executions are only sourced from the frontend and they are nicely encapsulated by Streamlit.

With its execution model, then, developers can write the apps in a clean world where there are no callbacks and no (or little) side effects. In turn, if we want to handle the streams with good performance, we have to explicitly handle the events sourced from the streams like frame generations, which breaks the elegant encapsulation, causing callbacks and events to appear in the script.

# What `tiny-streamlit-webrtc` lacks

Though we’ve created a small subset of `streamlit-webrtc`, `tiny-streamlit-webrtc`, it still lacks many important features `streamlit-webrtc` has. Here we will review some of them.

## Parameters input from Streamlit components

One of the biggest benefits of using Streamlit is interactive controls such as sliders and radio buttons. With computer vision and machine learning models, these controls are very useful to change the parameters during execution.

Because the computer vision code is running in the forked thread with this component, we have to pass the values obtained from Streamlit widgets to the CV code over the threads. But it is not difficult, like [here in the `streamlit-webrtc` sample](https://github.com/whitphx/streamlit-webrtc/blob/f03d3150adfa27c44bb7f2d22d495351090d9341/app.py?ref=streamlit.ghost.io#L184).

With `tiny-streamlit-webrtc`, you can do this by adding a public property to `VideoTransformTrack` and read and write it from each thread, just like the sample code linked above. Please try it if you are interested, and be careful about thread safety when you pass complex values.

## Frame drops

We’ve used edge extraction as an example in the tutorial. However, if you replace it with more computationally expensive filters like deep neural networks, you will see the displayed video slows down. You can test it simply by putting `time.sleep(1)` in `VideoTransformTrack.recv()`.

This is because `VideoTransformTrack.recv()` processes all the input frames one by one - if it delays, generating the output frames is also delayed.

To solve this problem, `VideoTransformTrack.recv()` has to drop some input frames and pick the latest one each time it runs. In `streamlit-webrtc`, it's done [here](https://github.com/whitphx/streamlit-webrtc/blob/f03d3150adfa27c44bb7f2d22d495351090d9341/streamlit_webrtc/transform.py?ref=streamlit.ghost.io#L97-L98) when [`async_transform`](https://github.com/whitphx/streamlit-webrtc/blob/f03d3150adfa27c44bb7f2d22d495351090d9341/streamlit_webrtc/__init__.py?ref=streamlit.ghost.io#L98) option is set as `True`.

![11](https://streamlit.ghost.io/content/images/2021/08/11.png#border)

## Extendability

In `tiny-streamlit-webrtc`, the video transformation is hard-coded inside `VideoTransformTrack.recv()`, but of course, this is bad design as a library. To be reusable, it should expose an injectable interface through which developers can implement arbitrary kinds of video transformation, encapsulating details such as `VideoTransformTrack.recv()` and WebRTC-related code.

With `streamlit-webrtc`, developers can implement their own video transformations by creating a class extending `VideoTransformerBase` class like [this](https://github.com/whitphx/streamlit-webrtc/blob/f03d3150adfa27c44bb7f2d22d495351090d9341/app.py?ref=streamlit.ghost.io#L233) and [this](https://github.com/whitphx/streamlit-webrtc/blob/f03d3150adfa27c44bb7f2d22d495351090d9341/app.py?ref=streamlit.ghost.io#L129).

# Key takeaways

Streamlit is a nifty framework with a useful library, but it doesn’t handle real-time video processing well on its own.

WebRTC makes Streamlit even more awesome by enabling server-side processes and clients to send and receive data streams over the network with low latency.

Have an amazing project in mind to use WebRTC for? Share it with us in the comments or [message me](https://discuss.streamlit.io/u/whitphx?ref=streamlit.ghost.io).

---

# Credits

Reviewed by Yu Tachibana ([@z\_reactor](https://twitter.com/z_reactor?ref=streamlit.ghost.io))

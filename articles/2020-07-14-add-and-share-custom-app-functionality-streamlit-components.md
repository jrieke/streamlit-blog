---
title: "Add and Share Custom App Functionality | Streamlit Components"
subtitle: "A new way to add and share custom functionality for Streamlit apps"
date: 2020-07-14
authors:
  - "Adrien Treuille"
category: "Product"
---

![Introducing Streamlit Components](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--12-.svg)


---

In the ten months since Streamlit was released, the community has created over 250,000 apps for everything from [analyzing soccer games](http://adilmoujahid.com/posts/2020/06/streamlit-messi-ronaldo/?ref=streamlit.ghost.io) to [measuring organoids](https://github.com/TKassis/OrgaQuant?ref=streamlit.ghost.io), and from [COVID-19 tracking](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html?ref=streamlit.ghost.io) to [zero-shot topic classification](https://huggingface.co/zero-shot/?ref=streamlit.ghost.io). Inspired by your creativity, we added [file uploaders](https://github.com/streamlit/streamlit/pull/488?ref=streamlit.ghost.io), [color pickers](https://github.com/streamlit/streamlit/pull/1325?ref=streamlit.ghost.io), [date ranges](https://github.com/streamlit/streamlit/pull/1483?ref=streamlit.ghost.io), and other features. But as the complexity of serving the community grew, we realized that we needed a more scalable way to grow Streamlit’s functionality. So we’re turning to Streamlit’s best source of ideas: you!

Today, we are excited to announce *Streamlit Components,* the culmination of a multi-month project to enable the Streamlit community to create and share bits of functionality. Starting in Streamlit version 0.63, you can tap into the component ecosystems of React, Vue, and other frameworks. Create new widgets with custom styles and behaviors or add new visualizations and charting types. The possibilities are endless!

### The Streamlit Components Gallery

The first thing you should do is check out the [Streamlit Components Gallery](http://streamlit.io/components?ref=streamlit.ghost.io) to see what others have created and shared.

Each component can be installed with just a single line of code:

```
pip install some_cool_component
```

If you don’t find a component that works for you, you can make your own!

### Building your own components

Streamlit has a unique, functional style which lets you create rich, interactive experiences in very few lines of code. For example, let’s check out this simple Streamlit app:

```
import streamlit as st

x = st.slider('x')
st.markdown(f'`{x}` squared is `{x * x}`')
```

![1-11](https://streamlit.ghost.io/content/images/2021/08/1-11.png#browser)

Looking at this code, you can see that Streamlit calls come in two flavors: **static components** like `st.markdown` are stateless and only send data *to* the browser, whereas **bidirectional components** like `st.slider` have internal state and send data *back from* the browser.

Our challenge was to provide an API that embraces Streamlit’s functional style while capturing these use-cases as simply as possible. A few months ago, two amazing Streamlit engineers, Tim Conkling and Henrikh Kantuni, tackled this challenge and came up with a super elegant solution. The result is the new `streamlit.components.v1` package which comprises three functions. For static components, we added:

* `html(...)`, which lets you build components out of HTML, Javascript, and CSS
* `iframe(...)` , which lets you embed external websites

For bidirectional components, we added:

* `declare_component(...)`, which lets you build interactive widgets which bidirectionally communicate between Streamlit and the browser.

Let’s dive into how it works!

### Static Components

Let’s start with a simple **static component** to embed snippets of code called *Github gists* in your app. Ideally, adding the component should just be a single function call:

```
# Render a gist
github_gist('tc87', '9382eafdb6eebde0bca0c33080d54b58')
```

which would render a gist like this:

![2-12](https://streamlit.ghost.io/content/images/2021/08/2-12.png#browser)

To create such a component, we start by importing the Streamlit Components library:

```
import streamlit.components.v1 as components
```

This somewhat wordy import statement serves two purposes:

1. It versions the components API so that future changes don’t break existing components.
2. It reminds us that we’re starting to use deep magic which we should hide from the user.

Now let’s use the `html(...)` method to serve up the gist:

This approach has a few awesome properties. First, it’s really simple and functional. In fact, this pattern lets you hide the ugly-looking HTML and wrap it into a pretty, Pythonic function call, `github_gist(...)`. You can wrap code in a function and reuse it throughout your project. (Better yet, put it in a package and share it with the community in the gallery.) Second, note that we can add arbitrary HTML in this component — `div`s, `span`s, and yes, `script`s! We can do this safely because the component is sandboxed in an `iframe` which lets us include external scripts without worrying about security problems.

### Getting widget with it!

What if you want to create a stateful **bidirectional component** that passes information back to Python from the browser, or in other words, a *widget*? You can do this too! For example, let’s create a counter component:

```
count = counter(name="Fanilo")st.write('The count is', count)
```

which creates this:

![3-9](https://streamlit.ghost.io/content/images/2021/08/3-9.png#browser)

Note that this code follows Streamlit’s unique functional style and captures the counter *state* embedded in the component. How did we achieve this? Happily, a single function call, `declare_component`, does all the work to enable bidirectional communication with Streamlit.

```
# Declare a simple counter component.import streamlit.components.v1 as componentscounter = components.declare_component("counter", path=BUILD_PATH)
```

Nice! Under the hood, `BUILD_PATH` points to a component built using React, Vue, or any frontend technology you like. For this example we decided to use React and Typescript giving us this render function:

and this callback:

Donezo! You’ve now created a simple, stateful component which “feels like React” on the website, and “feels like Streamlit” on the Python side. Information is passed back to Python using `Streamlit.setComponentValue(...)`. Because we’re using React in this case, the component’s state is stored in `this.state`. For more details on this example, see our [component template](http://github.com/streamlit/component-template?ref=streamlit.ghost.io).

A neat benefit of this architecture is that you’re not limited to React. You can use any language or framework which compiles for the web. [Here is the same counter component](https://github.com/kantuni/streamlit-meets-cljs?ref=streamlit.ghost.io) written in ClojureScript.

Another cool feature of this API is that you can do hot-reloading as you develop your component like this:

```
components.declare_component(name, url="http://localhost:3001")
```

Here, the `url` parameter lets you specify a dev server for the component [created with](https://github.com/streamlit/component-template?ref=streamlit.ghost.io#quickstart) `npm run start`.

What we’ve shown you so far just scratches the surface. For more details, [please check our documentation](https://docs.streamlit.io/en/stable/streamlit_components.html?ref=streamlit.ghost.io).

### Sharing with the world

Did you create something broadly useful for the Streamlit community? Sure, you could keep that superpower for yourself, but it would be even cooler to share it! Get community feedback and praise. 😇 You can easily wrap your component in a PyPi package and [submit it to our Gallery by following these instructions](https://docs.streamlit.io/en/stable/publish_streamlit_components.html?ref=streamlit.ghost.io#publish-streamlit-component-to-pypi).

### Try it out and let us know what you think!

We’re excited to unlock for the community a new way to plug-and-play functionality into Streamlit. Streamlit Components let you write simple HTML extensions or tap into the whole ecosystem provided by React, Vue, and other frameworks. Your feedback drives innovation in Streamlit. Please tell us what you think and what you’d like next. Show off your shiny new components and share them with the world. We can’t wait to see what you build! 🎈

---

*Special thanks to Fanilo Andrianasolo, Daniel Haziza, Synode, and the entire Streamlit Components beta community who helped refine this architecture and inspired us with their feedback and ideas. Thanks also to TC Ricks, Amanda Kelly, Thiago Teixeira, Beverly Treuille, Regan Carey, and Cullan Carey for their input on this article.*

---
title: "Announcing Streamlit 1.0! \ud83c\udf88"
subtitle: "Streamlit used to be the simplest way to write data apps. Now it's the most powerful"
date: 2021-10-05
authors:
  - "Adrien Treuille"
category: "Product"
---

![Announcing Streamlit 1.0! 🎈](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--8--2.svg)


We launched Streamlit in 2019 with a radical idea: making data apps should be simple. Your response exceeded our highest hopes. Tens of thousands of data scientists and thousands of companies turned to Streamlit to share rich models, deep analyses, and complex datasets.

![streamlit-1.0](https://streamlit.ghost.io/content/images/2022/09/streamlit-1.0.gif#browser)

Overnight, expectations became sky-high. You filled our forums. You inundated our issue boards. You wanted Streamlit to be more beautiful, more powerful, more programmable, and *faster*.

Inspired by this swell of energy, we set out to make your dreams real. But the features you wanted threatened to complicate Streamlit. How could we make Streamlit a powerful, production-ready app framework while preserving its core simplicity?

We had to boil it down. Why was Streamlit simple? What made it so special?

The answer was our initial insight...

### **Apps were just scripts!**

These two lines said it all:

```
x = st.slider("Select a value")
st.write(x, "squared is", x * x)
```

![](https://streamlit.ghost.io/content/images/2021/10/image.png)

In just two lines of Python, Streamlit dissolved all complexity of app development: layout, input, output, interaction, and callbacks. The learning curve was [zero!](https://docs.streamlit.io/en/stable/getting_started.html?ref=streamlit.ghost.io) ✨

So far so good. But as data scientists, we didn't just square numbers. We built models. We conjured visualizations. We wrangled datasets. We harmonized geographic data with sentiment analysis and feature libraries. We shaped thinking.

**Could Streamlit's simple scripting model scale?!**

For help, we turned to Streamlit's guiding light. The community. *You.* We asked you questions. You listened and responded. Together, we worked on countless revisions to the APIs. We simplified. Then we simplified even more.

One by one, we tackled the challenges of making each of your dreams real:

**1. Layouts.** The first step was to make [beautiful layouts](https://streamlit.ghost.io/introducing-new-layout-options-for-streamlit/) that danced and reacted to user input. How could we fit this into Streamlit's simple scripting model?

This led us to code like this:

```
airports = ["La Guardia Airport", "JFK Airport", "Newark Airport"]
for airport, col in zip(airports, st.columns(len(airports)):
   with col:
      st.subheader(airport)
      render_airport(airport)
```

See how the columns fit perfectly into a simple `for` loop? Awesome! A new layout superpower! 💪

![](https://streamlit.ghost.io/content/images/2021/10/Component-1--3-.png)

**2. Components.** Next, we wanted to transcend the structures of [Streamlit's 37 core functions](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py?ref=streamlit.ghost.io). So we added support for [third-party components](https://streamlit.ghost.io/introducing-streamlit-components/):

```
from webcam_component import webcam

captured_image = webcam()
if captured_image is not None:
   st.image(captured_image)
```

You swept in and filled our gallery with an [incredible ecosystem of components](https://streamlit.io/components?ref=streamlit.ghost.io). Now Streamlit apps could refract a full rainbow of web technologies:

![](https://streamlit.ghost.io/content/images/2021/10/Component-2.png)

**3. State.** Up next, we worked on [state](https://streamlit.ghost.io/session-state-for-streamlit/), adding new complexity in a few lines of code:

```
if st.button('Increment'):
    st.session_state.count += 1
st.write('Count = ', st.session_state.count)
```

**4. Speed.** You wanted speed. So we introduced powerful new [caching primitives](https://streamlit.ghost.io/new-experimental-primitives-for-caching/) that made your apps *fast:*

```
@st.experimental_singleton
def connect_to_database(url):
   engine = create_engine(url)
   return sessionmaker(engine)

@st.experimental_memo
def query_database(_db):
   with _db() as session:
      query = session.query(user.id, user.last_name, user.ltv)
   return pd.read_sql(query.statement, query.session.bind)
```

With each challenge conquered, our confidence and excitement grew. Streamlit's core developers joined with the community to build [more and more features](https://docs.streamlit.io/en/stable/changelog.html?ref=streamlit.ghost.io), faster and faster.

But you didn't stop there. You hacked at our rough edges. You tore apart our abstractions. You encouraged us to make Streamlit even better, even simpler, and infinitely more powerful. You believed in us.

And then it happened. We have built powerful new features *and* preserved Streamlit's core simplicity. The abstractions scaled!

On the wave of this excitement, a new milestone came into view...

### **Streamlit 1.0!** 🎈

This signifies the end of our first journey:

* We've grown from three co-founders to a team of **almost 50** ([we're hiring!](http://streamlit.io/careers?ref=streamlit.ghost.io)).
* Our community has grown beyond our wildest dreams with more than **4.5 million downloads.**
* Streamlit now has more than **16,000 GitHub stars** and is used by more than **10,000 organizations** (including **over half of the Fortune 50**).

Funnily enough, we feel like we're back where we started. Once again, our community wants powerful features. But this time it's different. This time we *know* that the Streamlit model will scale.

So today we're also sharing with you [our new roadmap](https://share.streamlit.io/streamlit/roadmap/?ref=streamlit.ghost.io):

* **Magical apps.** We already made it 10x faster for you to make great apps. Now we want to make those apps even better. We'll be adding an unbeatable set of widgets—everything from sortable/filterable/editable databases and tables to clickable charts, to image selectors and editors, to amazing audio and video players and uploaders (and more options for layout and customization!).
* **First-class developer experience.** We want everything about coding a Streamlit app to be an awesome experience. So we'll make it easier for you to connect to data sources, cache data, interact with it, and debug your apps.
* **Enhanced user experience.** We want to help you make great apps for your users. We'll be designing a distinct user experience. App users will be able to understand the app, interact with it, and give you direct feedback.
* **Rapidly expanding ecosystem.** You wanted it to be even easier for fellow developers to share code, components, apps, and answers. So we'll be launching new features that make it super simple to get started with new apps, find code snippets, search for the right add-on components, engage with the community, and get recognized for your contributions.

Oh, and one more exciting thing. We’re committing to follow a loose variant of [semantic versioning](https://semver.org/?ref=streamlit.ghost.io). For details, see our upcoming release notes.

That's it for the Streamlit 1.0 announcement!

We're very proud to have shared our journey with you—our magical community. You are what makes Streamlit special. Thank you for inspiring us with your feedback, enthusiasm, and creativity. Please keep sharing your apps with the world. And keep sending us comments, ideas, bugs, feature requests, articles, and words of encouragement.

We wouldn't be here without you. ❤️

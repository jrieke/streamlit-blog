---
title: "Just build it"
subtitle: "How we design Streamlit to bias you toward forward progress."
date: 2024-08-07
authors:
  - "Thiago Teixeira"
category: "Product"
---

![Just build it](https://streamlit.ghost.io/content/images/size/w2000/2024/08/just-build-it_title-image.png)


If you’re reading this, you’re probably already familiar with Streamlit. If not, here’s a summary: Streamlit is a Python framework for building data apps. It’s opinionated, it has batteries included, and it’s deeply tied to a specific design system.

* **It’s focused on data apps.** Everything we do stems from this. We don’t target generic apps like the ones on your phone or your favorite SaaS, but the kinds of apps data scientists and ML engineers need to make their work impactful at their organizations.
* **It’s opinionated** because we want to promote a fast, iterative workflow, and to uphold what we think are best practices in engineering.
* **It has batteries included** so most of what you need to get started is in the library itself.
* And finally, **it’s tied to a design system** so you don’t spend time building a component library, visual language, or identity. You just get started — and *fast*.

At this point, I could tell you about how we started Streamlit. About how it started from a good hunch, based on our previous experience in industry and academia. About how we dove deep into different companies and observed their data scientists and ML engineers at work in order to shape Streamlit. But [Adrien already did that very well 5 years ago](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace?ref=streamlit.ghost.io), and I don’t think I can top it!

So instead, I’ll talk about how our deep focus on data apps translates into product decisions we make every day. And for this, I’ll start with a tale …

## The 10x new hire

Once upon a time, a Data Science team built a powerful forecast model of the company’s most important metrics. The Finance Team saw it and loved it, and then asked for a live version they could use in their weekly meetings. So the Data Team filed a request with the Tools Team to build a data app, and the Tools Team put it on their queue.

Three months and many meetings later, the app was delivered and it was beautiful.

But there was a wrinkle: When Finance tried it out, it wasn’t quite what they needed. So they filed another request with the Data Team, who passed it onto the Tools Team, and the Tools Team put it on their queue. Many months passed.

At that point, an unsuspecting New Hire joined the Data Team and was assigned a starter project: Putting together a quick data app to unblock the Finance Team while they waited for *the real app* from the Tools Team.

After some googling, the New Hire discovered Streamlit and, within a day, was able to share a minimal app with colleagues. It wasn’t perfect, but she addressed some of the feedback and updated the app. The next day, she showed it to her contact in the Finance Team, got more feedback, and refined the app accordingly.

Within three days, the Finance Team was regularly using the app in their meetings. They had more feedback and the New Hire quickly addressed it in newer versions.

Within a week, the CEO was using the app and the New Hire was hailed as a hero 💪

## Why this happens

We’ve seen that story transpire countless times.The reason the New Hire’s app wins in the end is because **a simple app today is better than an over-designed app 3 months late.**

In fact, this is exactly how the best startups build their products! They ship a minimum viable product ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product?ref=streamlit.ghost.io)), put it in customers’ hands as soon as possible, and iterate relentlessly.

And in the process, they incrementally harden the underlying infrastructure. Because there’s a corollary to the New Hire’s story: As the team continues to use the app, they gradually productionize it.

That set of bespoke Pandas transformations that are super slow? They pull it into a separate data pipeline and some materialized tables.

That complex computation that other apps want to use? They move it into a RESTful service. They refactor the app into multiple pages as it grows. They write tests, they set up CI. And the app becomes bullet-proof.

The benefits of this flow are clear:

1. **You build better apps** because you often don’t know what you need until you try it out. So by building and user-testing, and building and user-testing again, you end up with a better app than if you had planned the whole thing ahead of time only to belatedly realize it’s not the solution you thought it was.
2. **You get value from day 1.** As you’re building and user-testing, you *already* have a useful app. And it only gets more and more useful along the way.
3. **You don’t overbuild.** Instead of building a pipeline at the same time as you build your app, you just get the app out and then harden it as it proves its usefulness. However, not all apps are useful, and not all useful apps live for long enough to require hardening. So you only spend your precious brain cycles on apps that are both useful and long-lived.

The way you start is simple: You **just build it.**

## Intentional design

We like to think that it’s no accident the New Hire’s story happens at so many different companies. We like to think this story happens because **we intentionally design Streamlit to promote forward progress**.

When you first start writing an app, *forward progress* means having a draft in 5 minutes that is already useful in *some* way. And one thing that definitely makes an app more useful is interactivity. So, from early on, we had a strong sense that we should make interactivity as simple as possible.

For example, you shouldn’t have to create a “View” with a slider in it, then a “Controller” with a callback function that modifies the “Model” used by the slider (in other words, the [MVC paradigm](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller?ref=streamlit.ghost.io)). Instead we came up with a single-line solution:

```
value = st.slider("Pick a number", 0, 100)
```

You type that and get an app that already does something. *Forward progress!*

Then, when building [Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state?ref=streamlit.ghost.io) two years later, we quickly learned that the proposed API would easily lead to off-by-one errors, and the only solution that worked was callbacks. Scarred by our past experiences with MVC and similar paradigms, we spent quite some time on the problem to come up with a decidedly “*Streamlit-y”* version of callbacks that avoided all that complexity. And — more importantly — the solution doesn’t force you to use callbacks from the get-go, but allows you to layer them on later as needed. *Forward progress!*

Another example that is near and dear to us —and certainly to the community— is styling. On one hand, the easiest thing for us to do would be to simply tack on support for CSS directly into Streamlit, with something like `st.css(...)` or `st.write(..., style="css goes here")`. But when we experiment with it, we notice unfettered access to styling quickly becomes a *hindrance* toward forward progress. Rather than get that first version out to stakeholders, people get stuck combing through [MDN](https://developer.mozilla.org/en-US/?ref=streamlit.ghost.io), fighting the [cascade](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance?ref=streamlit.ghost.io), tweaking selectors, and obsessing about single pixels. And, to top it off, the end result is often flaky and distracting.

So we tackle these requests by asking ourselves these questions:

* “What is the underlying problem people are trying to solve?”
* “How common is that problem?”
* “Can we solve it ourselves and help free the developer?”

Depending on the answers to these questions, we follow one of two approaches:

1. **Provide a one-line, opinionated solution to the problem**  
     
   This happened a few months ago. We noticed tons of developers using CSS hacks to place a logo at the top-left corner of their apps, so we decided to give them a one-line solution with `st.logo()`. [This new command](https://docs.streamlit.io/develop/api-reference/media/st.logo?ref=streamlit.ghost.io) draws their custom logo, makes it responsive to the sidebar’s state, makes sure it doesn’t overlap any content, and just looks good by default.  
     
   That’s also how we added [text colors,](https://docs.streamlit.io/develop/api-reference/text/st.markdown?ref=streamlit.ghost.io) [lines under headers,](https://docs.streamlit.io/develop/api-reference/text/st.header?ref=streamlit.ghost.io) [borders around containers,](https://docs.streamlit.io/develop/api-reference/layout/st.container?ref=streamlit.ghost.io) [vertical alignment,](https://docs.streamlit.io/develop/api-reference/layout/st.columns?ref=streamlit.ghost.io) [Material](https://docs.streamlit.io/develop/api-reference/status/st.info?ref=streamlit.ghost.io) [icons](https://docs.streamlit.io/develop/api-reference/navigation/st.page?ref=streamlit.ghost.io), and so on. They’re certainly opinionated solutions in terms of visuals and behavior, but the advantage is you just say what you want, Streamlit does it, and you move on to the next thing. *Forward progress!*
2. **Provide a curated set of knobs … and watch**  
     
   When a one-line opinionated solution won’t cut it, we introduce a minimal set of “knobs,” observe the result, and iterate. Since we don’t want to break compatibility, most of our features are [one-way doors,](https://www.youtube.com/watch?v=rxsdOQa_QkM&ref=streamlit.ghost.io) meaning we must proceed with caution.  
     
   An example of this is *theming*. Everyone wants their apps to match their company’s colors and, of course, the exact colors vary by company. But Streamlit’s interface is made up of several dozen colors, and selecting a visually-pleasing combination can consume several hours. So our first stab at this problem was to [let you pick just 4 colors,](https://docs.streamlit.io/develop/concepts/configuration/theming?ref=streamlit.ghost.io) and Streamlit calculates all the others for you. *Forward progress!*  
     
   We’re now busy behind the scenes thinking up *a second stab* at this problem — an expanded solution that gives you [more knobs](https://youtu.be/eQY7hfkw-Ag?t=1066&ref=streamlit.ghost.io) (beyond colors, even!) without sacrificing iteration speed. Similarly, we’re also considering new, more flexible layout options beyond columns.  
     
   We have nothing to announce right now, but definitely keep an eye out 😉

In sum, we don’t want anything to distract you from forward progress. With every step we take, we try our hardest to provide a framework that abstracts away HTML, JS, CSS, HTTP, routes, serialization, callbacks, and all sorts of engineering details. This way, **you’re able to focus on putting the power of data at the fingertips of your stakeholders so they, too, can make *forward progress***.

![A stylized image of a rocket ship taking off.](https://streamlit.ghost.io/content/images/2024/08/An-illustration-of-forward-progress.jpeg)

## Iteration makes perfect

At Streamlit, we are avid users of Streamlit ourselves, which means we have our own pet peeves and feature requests. We share your pain points, and we’re always iterating on the library. We never want to stop iterating! Our commitment to this is demonstrated in the way we ship a new release each month.

We’re also inspired by the Streamlit community and your ingenuity. We constantly encounter [apps](https://streamlit.io/gallery?ref=streamlit.ghost.io) and [custom components](https://streamlit.io/components?ref=streamlit.ghost.io) that push the boundaries of Streamlit in ways we never thought possible, giving us new ideas for things to bring into the core library. The community is easily the best part of this job!

Because of that, we have so much more in store for you. We develop [in the open](https://github.com/streamlit/streamlit/pulls?ref=streamlit.ghost.io), so you can always find our roadmap at [roadmap.streamlit.app](https://roadmap.streamlit.app/?ref=streamlit.ghost.io) or attend the next [Quarterly Showcase](https://www.youtube.com/watch?v=eQY7hfkw-Ag&t=16s&ref=streamlit.ghost.io), where our product managers discuss the latest in Streamlit, like [vertical alignment](https://www.youtube.com/live/eQY7hfkw-Ag?si=q8JpIEH3yxeOrTGu&t=1019&ref=streamlit.ghost.io) and advanced theming.

The beauty about iterating is that the best days are always ahead. We’re humbled to have you along for the ride.

Happy Streamlit-ing! 🎈

---
title: "Streamlit Components: Our Security Model & Design Philosophy"
subtitle: "The story of allow-same-origin"
date: 2021-01-20
authors:
  - "Tim Conkling"
category: "Tutorials"
---

![Streamlit Components, security, and a five-month quest to ship a single line of code](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--6-.svg)


In the [changelog for Streamlit 0.73.0](https://docs.streamlit.io/en/stable/changelog.html?ref=streamlit.ghost.io#version-0-73-0), released in December 2020, there’s a small callout: “Component iframes now include the allow-same-origin sandbox attribute.”

This change enables dramatically more powerful [Streamlit Components](https://docs.streamlit.io/en/latest/streamlit_components.html?ref=streamlit.ghost.io) - you can now use webcams and microphones in Streamlit apps and more easily embed and interact with external resources - and it was just a single line of code! (Check out our ever-expanding [Component Gallery](https://www.streamlit.io/components?ref=streamlit.ghost.io) for examples of quality Components created by the Streamlit community.)

![webrtc-1](https://streamlit.ghost.io/content/images/2021/08/webrtc-1.gif#border)

But this is not a post about how to use or build Streamlit Components. If you're interested in that, we have a [tutorial here](https://docs.streamlit.io/en/latest/streamlit_components.html?ref=streamlit.ghost.io) or check out the great [community tutorial](https://streamlit-components-tutorial.netlify.app/?ref=streamlit.ghost.io) by Fanilo Andrianasolo! Instead, we want to peel back the curtain and discuss how we make changes to Streamlit itself. Because we *could* have shipped that single line in July [when we launched Streamlit Components](https://medium.com/streamlit/introducing-streamlit-components-d73f2092ae30?ref=streamlit.ghost.io). We could've shipped it in any of the 9 releases that followed! But instead, it took us 5 months.

This is an engineering-focused post about why such a small change took such a long time. It'll touch on the Streamlit security model, our design philosophy, and the competing constraints that can lead to long development times for seemingly-simple features. And for the masochists out there, we'll stare briefly into the abyss that is *cross-origin web security*.

# Components: security + design

Let's start with a humble-brag: Streamlit has *lots* of users, many of whom are storing and accessing sensitive data in Streamlit apps. We take security very seriously. What this means in practice is that any change or feature we add to Streamlit *must not* reduce the security of either the [Streamlit open source library](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io) or [Streamlit sharing](https://www.streamlit.io/sharing?ref=streamlit.ghost.io), our "press button → deploy to cloud" hosting platform.

Additionally, we care dearly about the *design* of Streamlit - not just the way it looks, but the way it works, all the way down to API names. This means that, as much as possible:

* Streamlit should *just work.*
* Streamlit features should be robust and powerful.
* New features should *not* increase the complexity of installing, using, or deploying Streamlit.

So we have these three broad goals: add new features to Streamlit, don't undermine its simplicity, and ensure it's safe. When we're fortunate, these goals are not at odds with each other. When we're less fortunate, we have the `allow-same-origin` situation and we end up writing blog posts like this one.

Before getting into the weeds, let's first consider the story around Streamlit Components and security:

* Fundamentally, a Streamlit Component is a *Python library*. You should exercise the same judgement with a Component as you would with any other Python library you `pip install` in your project.
* A Component *also* runs code on the frontend, which means it can make requests from the browser, and can access data on your app's frontend.
* You should assume that any library you use - Component or otherwise - can access any data in your app.
* If your app deals with sensitive data, only install libraries and Components that you have written, or that you otherwise trust.

No big surprises. But there's a wrinkle: as Streamlit Components was under development, so too was Streamlit sharing. We needed to make sure that a rogue Component in a shared app couldn’t peek at Streamlit sharing data, or execute commands on behalf of the developer.

tl;dr for the rest of the blog post: *nothing* in a Streamlit app - malicious Component or otherwise - can hijack Streamlit sharing. But we treaded carefully - and a bit slowly - to make sure this was the case.

# allow-same-origin and the iframe sandbox

*(This section gets into the details of `<iframe>` sandboxing, the `allow-same-origin` sandbox flag, and cross-origin requests. It'll be of primary interest to those who work with, or are curious about, web security. If you have no interest in the nitty-gritty, skip ahead to the next section!)*

Broadly speaking, Streamlit Components are [user-created plugins that extend Streamlit.](https://www.streamlit.io/components?ref=streamlit.ghost.io) You `pip install` a Component into your Python environment, and now you [can add a forum](https://github.com/okld/streamlit-discourse?ref=streamlit.ghost.io), or an [interactive 3D molecule viewer](https://github.com/napoles-uach/streamlit_3dmol?ref=streamlit.ghost.io), or a [Facebook HiPlot data graph](https://github.com/facebookresearch/hiplot?ref=streamlit.ghost.io), or [custom charting libraries](https://github.com/andfanilo/streamlit-echarts?ref=streamlit.ghost.io) - or really any feature that Streamlit doesn't include out of the box - to your Streamlit app.

![group_selection_example](https://streamlit.ghost.io/content/images/2021/08/group_selection_example.gif#browser)

During development, we had two primary concerns around the Component security model:

* A Component shouldn't be able to break assumptions about its surrounding page (changing the host app's CSS or DOM, for example).
* A Component in an app deployed with [Streamlit sharing](https://www.streamlit.io/sharing?ref=streamlit.ghost.io) shouldn’t be able to hijack its owner's sharing credentials and read secret data or execute a [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery?ref=streamlit.ghost.io) exploit.

Under the hood, each instance of a Streamlit Component is mounted inside its own `<iframe>` in its containing Streamlit app, which means it lives in its own little world with its own DOM, its own CSS, and its own restrictions. Each iframe has a sandbox with a number of different attributes that specify what it can and can't do. For our purposes here, we're interested in two sandbox flags: `allow-same-origin` and `allow-scripts`.

`allow-scripts` is self-explanatory: if it’s missing, then the iframe will not be able to execute any JavaScript. Executing JavaScript is a fundamental part of Streamlit Components, so this attribute must be enabled. `allow-same-origin` is related to [“cross-origin-resource-sharing”, or CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS?ref=streamlit.ghost.io) - which means that it’s destined to be confusing and annoying. If you *omit* this attribute, the iframe won't be able to use certain browser features (like webcams and microphones), and it will be unable to make requests to many other web servers (which often expect a non-null origin).

When Streamlit Components launched, we left off `allow-same-origin` because of how it interacts with `allow-scripts`. The [MDN iframe page](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe?ref=streamlit.ghost.io) explains it thusly:

> When the embedded document has the same origin as the embedding page, it is strongly discouraged to use both allow-scripts and allow-same-origin, as that lets the embedded document remove the sandbox attribute — making it no more secure than not using the sandbox attribute at all.

Streamlit Components *are* served from the same origin as their embedding page, which means that combining `allow-scripts` and `allow-same-origin` would render our sandbox moot. This isn't *necessarily* a big deal, because Components are not "untrusted code" - but would potentially undercut our Component security concerns.

There's a big document memorializing weeks of discussion and argument on our `allow-same-origin` woes: should we serve components from a separate origin? Should we allow devs to opt into the `allow-same-origin` flag via a config option? Should we maintain an allow-list within Streamlit of Components that can use this flag?

We developed a number of prototypes that solved the issue in different ways. But all of them undercut Streamlit's "keep things simple" design principle:

* Some prototypes made Streamlit *use* more difficult (by requiring that dev deeply understand the Component sandbox model).
* Some made Streamlit *deployment* more difficult (by exposing more server ports to be forwarded and routed through proxies).
* And some made Component *development* more difficult (by imposing restrictions on Component creators).

# Breaking the sandbox

After several months of proposals, prototypes, and arguments, we shipped Streamlit 0.73, which solved the problem by simply adding the `allow-same-origin` iframe flag. In other words, we decided to allow Components to break the iframe sandbox.

Why are we ok with this? And what are the ramifications? Here's where we landed on our original sandboxing concerns:

### First, "don't hijack my CSS"

> "A Component shouldn't be able to break assumptions about its surrounding page (changing the host app's CSS or DOM, for example)."

Our decision here is simple: we decided that, while we won't *encourage* this sort of thing (not least because it's unsupported and therefore subject to break when Streamlit is updated), we're fundamentally ok with it. Official theming support is on the Streamlit roadmap for 2021, but if enterprising developers want to hack on Streamlit and create this sort of thing before we officially ship it, we won't stand in their way.

Streamlit is an [open source project](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io) anyway; if you don't like the way something works or looks, you can just fork the project and change it. We don't need a Component sandbox to enforce a rule that's incompatible with our open source nature.

### And more importantly, "don't hijack Streamlit Sharing"

> "A Component in an app deployed with Streamlit sharing shouldn’t be able to hijack its owner's Sharing credentials and execute a CSRF exploit."

We need to ensure that a malicious Component - or any other rogue code that could be running within a Streamlit app - cannot execute Streamlit sharing commands surreptitiously.

Googling for ["CSRF example"](https://www.google.com/search?q=csrf+example&ref=streamlit.ghost.io) will return all sorts of resources that explain this type of exploit in detail. The important thing to know is that CSRF attacks use the fact that each HTTP request made by a browser will include the cookies associated with site to which the request is made. (There are various [cookie attributes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies?ref=streamlit.ghost.io) that make this story slightly more complex, but that's the basic rule.)

When you're logged into Streamlit sharing and visit a deployed app you own, you get a management dashboard that lets you view logs and perform various administrative tasks:

![1](https://streamlit.ghost.io/content/images/2021/08/1.png#browser)

If the Streamlit sharing administrator wrapper is served from the same HTTP origin as the app it's managing, a malicious Component could bypass Sharing's CSRF protections by making requests against the Streamlit sharing API and reading the CSRF token from the response headers.

The solution to this doesn't involve relying on Component sandboxing. In Streamlit sharing, an app's admin dashboard is *simply served from a different origin than the app itself*. This is similar to a "serve Components from a different origin" prototype we'd rejected on the basis of making deployment more complicated for users - but with the burden pushed up to Streamlit sharing instead. (We are *more than happy* to make deployment more complicated for the Streamlit sharing engineers while keeping it simple for you. Sorry not sorry, friends!)

# Wrapping up

Within the Streamlit engineering team, the phrase "allow same origin" has practically achieved meme status - it was the issue we were always *right on the verge* of coming to consensus on. Throughout much of 2020, during our start-of-month company-wide planning meetings, the Components team kept claiming that we were about to make a final decision, only to walk back our over-eager prediction shortly afterwards.

But the saga is finally over! We've jettisoned the `allow-same-origin` iframe sandbox flag, and now you can stream webcam video, add a Disqus forum, embed Tweets, and use a whole host of other Components that were previously out of reach. Most importantly, your Streamlit sharing apps will remain safe from malicious code.

And if you're lucky, you'll never have to think about null origins, CORS, or CSRF again. We'll handle it.

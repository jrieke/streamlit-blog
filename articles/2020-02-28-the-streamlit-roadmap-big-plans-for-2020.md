---
title: "The Streamlit roadmap\u2014big plans for 2020!"
subtitle: "Devoting 2020 to giving the Streamlit community a vastly expanded new set of superpowers"
date: 2020-02-28
authors:
  - "Adrien Treuille"
category: "Product"
---

![The Streamlit roadmap—big plans for 2020!](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--8-.svg)


**We created Streamlit to give the Python data community a new superpower: the ability to create beautiful apps as easily as writing Python scripts.**

[We launched](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace?ref=streamlit.ghost.io) a minimal version of Streamlit in October with only basic output and interaction primitives. Despite these limitations, the response has been overwhelming: almost 7,000 Github stars and 13,000 monthly active users in less than four months! Most exciting has been to see the emergence of an intricate archipelago of [Streamlit apps](https://www.streamlit.io/gallery?ref=streamlit.ghost.io), from simple, fun [demos of open-source projects](https://gist.github.com/ines/b320cb8441b590eedf19137599ce6685?ref=streamlit.ghost.io), to [community-spanning infrastructure](http://awesome-streamlit.org/?ref=streamlit.ghost.io) and complex internal tooling at major companies used in production by hundreds of employees.

Inspired by your energy and creativity, **we’re devoting 2020 to giving the Streamlit community a vastly expanded new set of superpowers**. Our goal is to make Streamlit not only the most productive (and fun!) app building experience in the Python ecosystem, but also the most powerful by adding:

* Improved **caching** that’s easier to use and understand
* A **custom component** system to extend Streamlit’s capabilities in the browser
* **Layout** primitives to customize layout and other visual elements
* User-programmable **state**, especially for multi-page apps
* Enabling you to easily **deploy** apps from Streamlit (closed source)

A detailed [feature list is on GitHub](https://github.com/streamlit/streamlit/wiki/Roadmap?ref=streamlit.ghost.io), and it’s really just a distillation of the ideas coming from Streamlit’s amazingly smart and creative community. Please help us understand what to build by [submitting issues](https://github.com/streamlit/streamlit/issues/new/choose?ref=streamlit.ghost.io) and [pull requests](https://github.com/streamlit/streamlit/compare?ref=streamlit.ghost.io), and by sharing your thoughts in the comments below.

### Caching

Caching enables you to reuse data and computation in your apps, allowing scripts to run quickly by saving the results of expensive functions. We recently released [hash\_funcs](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io#the-hash_funcs-parameter) so that you can set your own hash function for specific data types like TensorFlow sessions or live database connections. And we added more documentation on [basic](https://docs.streamlit.io/library/api-reference/performance/st.cache?ref=streamlit.ghost.io) and [advanced caching](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io). Coming up are even more improvements to caching for other function types and some added magic to make everything around caching even more straightforward. [Please share thoughts here](https://discuss.streamlit.io/t/help-us-stress-test-streamlit-s-latest-caching-update/1944?ref=streamlit.ghost.io) about how you’d like to see caching work.

### Custom components

The Streamlit custom components system will give you the ability to write arbitrary React or Javascript code and insert it into your app. This opens the door for a lot of possibilities for custom solutions to visualization, interactivity with chart/maps/tables, and other unique needs of your app. [Please share thoughts here](https://github.com/streamlit/streamlit/issues/327?ref=streamlit.ghost.io) about how you’d like to see custom components work.

### Customizable layout

Our community has already created [some great style and layout](https://pmbaumgartner.github.io/streamlitopedia/front/introduction.html?ref=streamlit.ghost.io) resources (and we have [**no plans**](https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/69?ref=streamlit.ghost.io) **to deprecate html, unsafe\_allow\_html=True!**), but Streamlit in its current form doesn’t make layout nearly as easy as we think it should be. We’ll be adding style and customization options to Streamlit, and also building new layout primitives: [horizontal](https://github.com/streamlit/streamlit/issues/241?ref=streamlit.ghost.io), [grid](https://github.com/streamlit/streamlit/issues/309?ref=streamlit.ghost.io), scroll views, and more. This is a tricky one to get right because layouts make up some of the most complex parts of display logic like CSS, not to mention it’s really easy to make these layouts look ugly. What are your thoughts? What are your favorite layout systems in other languages? [Please share thoughts here](https://discuss.streamlit.io/t/customizable-layout-for-streamlit/2053?ref=streamlit.ghost.io) about how you’d like to see layout work.

### Programmable state

Right now, getting a Streamlit app to store internal state, like information a user entered in a form, is simply too tricky. There are some workarounds for [session state](https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92?ref=streamlit.ghost.io), but we want to give you a baked-in and elegant version of programmable state so you can build apps with sequential logic, apps with multiple pages, apps that incrementally ask users for input, and so on. [Please share thoughts here](https://discuss.streamlit.io/t/programmable-state-for-streamlit/2052?ref=streamlit.ghost.io) about the use cases you’d like to see supported.

### Deploy

We know that building a great app is only half of the equation. You also want to deploy and share your app with others. We want Streamlit’s deployment workflow to be as elegant and awesome as its app-building workflow. That’s why we’re creating **Streamlit for Teams**: a single-click deployment solution for Streamlit apps with built-in enterprise-grade features like auth, logging, and auto-scaling. The first version of this will be rolled out for **free to the community** in a few months (and we’re expanding [the beta](https://www.streamlit.io/for-teams?ref=streamlit.ghost.io) soon, apologies if we haven’t gotten back to you yet!).

For now, you can check out some great community resources about deploying on [AWS](https://mlwhiz.com/blog/2020/02/22/streamlitec2/?ref=streamlit.ghost.io), [GCP](https://blog.jcharistech.com/2020/01/14/how-to-deploy-streamlit-apps-to-google-cloud-platformgcp-app-engine/?ref=streamlit.ghost.io), [Heroku](https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83?ref=streamlit.ghost.io), and [Azure](https://towardsdatascience.com/deploying-a-streamlit-web-app-with-azure-app-service-1f09a2159743?ref=streamlit.ghost.io), and you help us by [providing feedback](https://discuss.streamlit.io/t/how-does-your-team-use-streamlit/2051?ref=streamlit.ghost.io) on how you’d like to use Streamlit in your company.

We’ve been tinkering with and refining these features over at Streamlit HQ. We’re so excited to share these new superpowers and iterate on them with the community!

Thank you for your part in the Streamlit journey and here’s to a great 2020 ❤️

### Resources

[Roadmap](https://github.com/streamlit/streamlit/wiki/Roadmap?ref=streamlit.ghost.io)  
[Documentation](https://docs.streamlit.io/?ref=streamlit.ghost.io)  
[GitHub](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)  
[Changelog](https://docs.streamlit.io/library/changelog?ref=streamlit.ghost.io)

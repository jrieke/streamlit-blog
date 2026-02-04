---
title: "Qiusheng Wu uses Streamlit to build a popular geospatial application"
subtitle: "Learn how Qiusheng created Earth Engine web apps with geemap"
date: 2022-07-21
authors:
  - "Qiusheng Wu"
category: "Case study"
---

![Qiusheng Wu uses Streamlit to build a popular geospatial application](https://streamlit.ghost.io/content/images/size/w2000/2022/06/qiusheng-hero.jpeg)


In April 2020, Assistant Professor in the Department of Geography at the University of Tennessee Qiusheng Wu launched [geemap](https://geemap.org/?ref=streamlit.ghost.io), an open-source Python package for interactive mapping with [Google Earth Engine](https://earthengine.google.com/?ref=streamlit.ghost.io) and open-source mapping libraries (e.g., ipyleaflet, folium). It quickly became one of the most popular geospatial packages with over 2,000 GitHub stars.

![https://i.imgur.com/7eyMcZQ.gif](https://i.imgur.com/7eyMcZQ.gif)

“Before Google Earth Engine, generating a satellite timelapse like this could take hours or even days,” Qiusheng said. “You can now create satellite timelapses in minutes, but it can still take hundreds of lines of Earth Engine JavaScript.”

### Jupyter environment wasn’t enough

Qiusheng wanted to apply geospatial big data, machine learning, and cloud computing to study environmental change (surface water, wetland inundation dynamics, etc.).

With [geemap](https://github.com/giswqs/geemap?ref=streamlit.ghost.io), users could explore large geospatial datasets, perform planetary-scale analysis, and create satellite timelapses with a few lines of code or a few clicks. But they still needed to install Python and run geemap in a Jupyter environment.

Qiusheng wanted his app to let *anyone* create satellite timelapses with no code. So he used [Voilà](https://voila.readthedocs.io/?ref=streamlit.ghost.io) for turning notebooks into standalone web apps and dashboards.

![https://i.imgur.com/adwTxEo.png](https://i.imgur.com/adwTxEo.png)

### Geemap got so popular, it maxed out free cloud hosting options

To make the notebooks public, Qiusheng needed to host them on a server.

“I’ve been using [ngrok](https://ngrok.com/?ref=streamlit.ghost.io) to turn a local computer into a secure web server and connect it to the ngrok cloud service, which accepts traffic on a public address,” Qiusheng said. “It’s one of the easiest ways to turn a Jupyter notebook into an app and it’s great for demos. But the downside of using a local computer as a public server is that it might be hacked.”

He switched to hosting it on a [Heroku](https://www.heroku.com/?ref=streamlit.ghost.io) cloud server. Soon after, the app became so popular, and it used up the free monthly dyno hours.

“I had to shut down the app when it exceeded the free limit and restart it at the beginning of each month, which was inconvenient,” Qiusheng said.

### Discovering Streamlit

Qiusheng first discovered Streamlit in October 2021. It quickly became his favorite package for developing and deploying interactive web apps. He used it for geemap because:

* It was free.
* It was open-source.
* It had similar functionality to ipywidgets but was much easier to use (no need for a callback function).
* He could deploy *unlimited* public apps from GitHub to Streamlit Community Cloud for free (no need for a server).
* Deployment was automatic, so he could focus on coding.
* The apps were publicly accessible.

### Streamlit powers the new version of geemap — and makes it available to anyone

Soon after Qiusheng released the [Streamlit Geospatial app](https://geospatial.streamlitapp.com/?ref=streamlit.ghost.io) for creating satellite timelapse animations for any location in less than 60 seconds, it got widely circulated on social media (check out the [blog post](https://streamlit.ghost.io/creating-satellite-timelapse-with-streamlit-and-earth-engine/), the [video tutorial](https://youtu.be/CVD42d3ejO0?ref=streamlit.ghost.io), and the [repo code](https://github.com/giswqs/streamlit-geospatial?ref=streamlit.ghost.io)).

People all over the world made animations of environmental changes: urban growth, land reclamation, river dynamics, vegetation dynamics, coastal erosion, and volcanic eruptions (use hashtags [#streamlit](https://twitter.com/search?q=%28%23streamlit%29+%28%40giswqs%29&src=typed_query&f=live&ref=streamlit.ghost.io) on Twitter and [#BigRiverAnimation](https://www.linkedin.com/search/results/content/?keywords=%23bigriveranimation&ref=streamlit.ghost.io) on LinkedIn to see examples).

![https://i.imgur.com/9qqk06V.png](https://i.imgur.com/9qqk06V.png)

There are now more than ten apps in [Streamlit Geospatial](https://geospatial.streamlitapp.com/?ref=streamlit.ghost.io), including the app for visualizing U.S. real estate data in 3D.

![https://i.imgur.com/Y8tJ4CC.gif](https://i.imgur.com/Y8tJ4CC.gif)

There is even an [app for creating maps of hurricane tracks](https://cartopy.streamlitapp.com/?ref=streamlit.ghost.io) built with Streamlit and [Tropycal](https://tropycal.github.io/tropycal/index.html?ref=streamlit.ghost.io) (check out the [repo code here](https://github.com/giswqs/streamlit-cartopy?ref=streamlit.ghost.io)).

![https://i.imgur.com/OCAb80v.png](https://i.imgur.com/OCAb80v.png)

To make it easier for users to make their own geospatial apps, Qiusheng created an [app template](https://multipage-app.streamlitapp.com/?ref=streamlit.ghost.io) based on Streamlit’s native support for multipage apps. Users can fork the repository and add more apps if needed. The app can be deployed to Streamlit Cloud, Heroku, or MyBinder (here is the [repo code](https://github.com/giswqs/streamlit-multipage-template?ref=streamlit.ghost.io)).

![https://i.imgur.com/OdLT4yf.gif](https://i.imgur.com/OdLT4yf.gif)

### Wrapping up

“I’m an advocate of open science and reproducible research,” Qiusheng said. “I love sharing Streamlit apps and making geospatial technologies more accessible to everyone. I have developed several open-source packages for geospatial analysis and interactive mapping (e.g., [geemap](https://github.com/giswqs/geemap?ref=streamlit.ghost.io), [leafmap](https://github.com/giswqs/leafmap/?ref=streamlit.ghost.io), [geospatial](https://github.com/giswqs/geospatial?ref=streamlit.ghost.io), [pygis](https://github.com/giswqs/pygis?ref=streamlit.ghost.io), [lidar](https://github.com/giswqs/lidar?ref=streamlit.ghost.io)). You can see my open-source projects on [GitHub](https://github.com/giswqs?ref=streamlit.ghost.io) and video tutorials on [my YouTube channel](https://www.youtube.com/c/QiushengWu?ref=streamlit.ghost.io).”

Thank you for reading Qiusheng’s story! If you have any questions, please leave them below in the comments or reach out to Qiusheng on [Twitter](https://twitter.com/giswqs?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/qiushengwu?ref=streamlit.ghost.io), or [YouTube](https://www.youtube.com/c/QiushengWu?ref=streamlit.ghost.io).

Happy coding and learning! 🧑‍💻

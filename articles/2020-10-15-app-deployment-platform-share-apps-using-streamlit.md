---
title: "App Deployment Platform | Share Apps Using Streamlit"
subtitle: "A sneak peek into Streamlit's new deployment platform"
date: 2020-10-15
authors:
  - "Tyler Richards"
category: "Tutorials"
---

![Deploying Streamlit apps using Streamlit sharing](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--15-.svg)


*This is a community piece that originally appeared on Towards Data Science - to see the original article [click here](https://towardsdatascience.com/deploying-streamlit-apps-using-streamlit-sharing-16105d257852?ref=streamlit.ghost.io).*

Over the past couple of weeks, I’ve been playing around with a new Streamlit feature called Streamlit sharing, which makes it super easy to deploy your custom apps. I’m going to go through a bit of background first, so if you want to see the docs for Streamlit sharing to get started you can find them [here](http://docs.streamlit.io/sharing?ref=streamlit.ghost.io).

# Streamlit background

For a bit of background, Streamlit is a framework that lets you quickly and confidently turn a python script into a web app and is an incredible tool for data scientists working on teams where they need to quickly share a model or an interactive analysis, or for data scientists working on personal projects they want to show the world. Here’s a [Streamlit beginner tutorial](https://docs.streamlit.io/en/stable/?ref=streamlit.ghost.io) if you want to try it out!

I’ve been using Streamlit for the past ~6 months, and it’s been ****so**** useful. Previously, if I knew I wanted to make a web app at the end of a project, I would always opt to switch to R for the wonderful R shiny framework, even though I am a much better python programmer than an R one. Going through Django or flask is just so much development friction to take on that it’s rarely worth it for a personal project and always takes too long for anything at work. But after using Streamlit, I now not only had options but found myself preferring python+Streamlit to R+shiny.

# Streamlit sharing

This brings me to a couple of months ago. I started a [DS project](http://www.tylerjrichards.com/books_reco.html?ref=streamlit.ghost.io) focused on analyzing reading habits using data from the [Goodreads](http://www.tylerjrichards.com/books_reco.html?ref=streamlit.ghost.io) app. I decided to try Streamlit out, and it turned a multi-day long process of getting a Django/flask app running well locally into one that took around a half-hour for local Streamlit use. It really is as easy as throwing your analysis into a script, and calling Streamlit functions whenever you want to put a graph, widget, or text explainer on the app.

However, the most annoying process on Streamlit was the deployment and management process. The [tutorial I followed](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3?ref=streamlit.ghost.io) was straightforward, and didn’t take that much time, but was fairly extensive. It required launching an ec2 instance, configuring SSH, using tmux, and going back to this terminal every time you wanted to change anything about your web app. ****It was doable but annoying.****

![1-4](https://streamlit.ghost.io/content/images/2021/08/1-4.png#browser)

A few weeks ago, Streamlit saw my Goodreads app and asked if I wanted to test out their Streamlit sharing beta, which was supposed to remove the friction explained above. I, obviously, gave it a shot.

****All I had to do was:****

1. Push my app to a Github repo
2. Add a requirements.txt file that listed all the python libraries I used
3. Point Streamlit to my app via the link to the repository
4. Click Deploy

It genuinely was ****that easy**** to figure out. I had sectioned off a couple of hours to figure it out, as I expected various bugs to pop up (it is in beta!), but it took me fewer than 10 minutes to get it up and running.

I currently have three apps running, one is a test app, the second is the [Goodreads book recommendation app](https://share.streamlit.io/tylerjrichards/book_reco/master/books.py/+/?ref=streamlit.ghost.io) I mentioned earlier, and the third is an [interactive analysis](http://www.tylerjrichards.com/survey.html?ref=streamlit.ghost.io) of a tech survey that I spun up (from idea to functioning and deployed web app) in around an hour and a half.

Switching to Streamlit sharing has also saved me the ~$5 a month AWS bill, which I would gladly pay for this feature just for the savings in time spent on deployment alone.

![2-4](https://streamlit.ghost.io/content/images/2021/08/2-4.png#browser)

If I wanted to try out a new app, I could just click the new app button, point it to my repo, and they would handle literally everything else.

![3-2](https://streamlit.ghost.io/content/images/2021/08/3-2.png#border)

If your Streamlit app uses any other packages, make sure to include a requirements.txt file in your repo — otherwise you’ll immediately get an error when deploying. You can use something like pip freeze to get requirements but that will give you all of the packages in the environment including those that you don’t use in your current project. And that will slow down your app deployment! So I’d suggest using something like pipreqs to keep it to just the core requirements for your app.

```
pip install pipreqs
pipreqs /home/project/location
```

If you have requirements for apt-get, add them to `packages.txt -`, one package per line.

# Conclusion

So as a wrap-up, Streamlit sharing has saved me $ on both a development time saved and hosting cost basis (shoutout to the VC funds that make this all possible), has made my personal projects more interactive and prettier, and has taken away the headaches of deploying quick models or analyses. No wonder I’m a Streamlit fan.

Want to see more of this content? You can find me on [Twitter](https://twitter.com/tylerjrichards?ref=streamlit.ghost.io), [Substack](https://insignificantdatascience.substack.com/p/starting-a-data-science-newsletter?ref=streamlit.ghost.io), or on [my portfolio site](http://www.tylerjrichards.com/?ref=streamlit.ghost.io).

****Happy Stream(lit)ing!****

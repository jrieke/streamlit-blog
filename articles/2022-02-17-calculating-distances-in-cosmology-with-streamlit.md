---
title: "Calculating distances in cosmology with Streamlit"
subtitle: "Learn how three friends made the cosmology on-the-go app Cosm\u03a9racle"
date: 2022-02-17
authors:
  - "Nikolina Sarcevic"
category: "Advocate Posts"
---

![Calculating distances in cosmology with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/02/Cosmoracle-banner.png)


Ever looked at the night sky and wondered, "Hey, how far away is that star?" We wondered about it too, and we wanted an app that could calculate this distance *in one click*. So we made CosmΩracle!

In this post, you’ll learn:

* What is CosmΩracle?
* How it all started
* How we worked together in a virtual setting
* Where to go from here?

Want to jump right in? Here's the [app](https://www.cosmoracle.com/?ref=streamlit.ghost.io) and the [source code](https://github.com/nikosarcevic/CosmOracle?ref=streamlit.ghost.io).

But first, let’s talk about...

## What is CosmΩracle?

CosmΩracle is an app that calculates distances for different sets of cosmological parameters. Go to [www.cosmoracle.com](http://www.cosmoracle.com/?ref=streamlit.ghost.io) and click on *Cosmological Distances*. You’ll see a menu in the sidebar with fields for redshift, the Hubble constant, the energy content in the Universe from matter, radiation, dark energy, and different equation of state parameters.

Some sets of parameters are more popular than others (they’re favored by different observational datasets), so we have pre-programmed some values for you. The only thing you need to get started is the value of the redshift. Want to know a certain distance of those galaxies at redshift 2? Simply plug that value into the redshift field, and CosmΩracle will get cracking!

![](https://streamlit.ghost.io/content/images/2022/02/Cosmoracle-GIF--1920-px-.gif)

It’s important in science that everyone agrees on what the input parameters represent, and CosmΩracle is no exception. As you can see above, we’ve included a *Definitions* page where you can see how each parameter is defined and how CosmΩracle uses these parameters to compute quantities that are used in cosmology.

## How it all started

There are plenty of “somethings” in the field of physics. If you’re working in cosmology and/or astronomy, at some point you’ll need to use one of the many “[distances](https://arxiv.org/pdf/astro-ph/9905116.pdf?ref=streamlit.ghost.io).” The need for many different types of distances is due to the Universe being very complicated—space expanding, objects moving, interacting, and mixing, things getting shifted and distorted. Depending on the problem you’re working on, you’ll need a certain distance calculated.

On top of this, these distances will depend on the kind of Universe you’re working with and on how much matter it contains. It probably sounds weird at first, but give it some thought. The amount of matter affects the expansion rate of the Universe, so different quantities lead to different increases in distance.

Other things that affect distances are the curvature of the Universe and dark matter or dark energy. If you have all the necessary ingredients, it’s possible to calculate these distances. Most of the time, you just “want the thing calculated” without going through the process of installing Python libraries and writing the code just to get that number.

Until recently, we calculated these distances with the first online version of the famous [Ned Wright’s Cosmo Calculator](https://www.astro.ucla.edu/~wright/CosmoCalc.html?ref=streamlit.ghost.io) from 1999 or with the [astropy cosmology package](https://docs.astropy.org/en/stable/cosmology/index.html?ref=streamlit.ghost.io). Although these are great tools, *we felt that there was a need for an improved and modern version*.

The three of us met online and decided that our app needs to:

* be user-friendly (everyone should be able to use it without spending a lot of time on learning it)
* work across all devices: desktop, tablet, and mobile (a la “astronomy on the go”)
* be fast and accessible
* be correct in terms of physics
* be designed in a modern way
* represent the results in a numerical and illustrative way (think plots)
* have an option to download the calculated data (to be used for further analysis)
* be designed in a way that’s easy to maintain and upgrade
* be open-source

How to achieve it?

All three of us have a programming background. We work in physics and love exploring the latest advancements in the field of data visualization. Sure, we could “code up” functions to calculate all sorts of things. But we wanted a simple and neat way of putting apps online. Every option we found needed knowledge beyond our skillset or wasn't open-source.

In the spring of 2021, Niko’s best friend Robert (also an astrophysicist) shared “a super cool new way of making apps online called Streamlit🎈.” While transitioning from research into data science, Robert made an incredible app called “[Distribution Analyser”](https://share.streamlit.io/rdzudzar/distributionanalyser/main/main.py?ref=streamlit.ghost.io). It analyses all [scipy.stats functions](https://docs.scipy.org/doc/scipy/reference/stats.html?ref=streamlit.ghost.io#module-scipy.stats). You can read more about it in this [Towards Data science article](https://towardsdatascience.com/distribution-analyser-b826b88b7b8d?ref=streamlit.ghost.io). When the time came to test the best way to combine Python code and make it into an app, Streamlit was one of our first choices.

## How we worked together in a virtual setting

![](https://streamlit.ghost.io/content/images/2022/02/map.png)

Since we’re all researchers at different institutions, it was hard for us to find the time to work together. We dedicated a few days during the holidays to exclusively work on CosmΩracle. After we decided on the functions to start with, we distributed the tasks, finalized the first Python code, and discussed how to deploy it.

CosmΩracle calculates the time that passed between a distant object emitting a photon and that same photon reaching Earth. Functions like this form the backbone of CosmΩracle but need to be deployed in order to be useful.

```
def get_lookback_time(z, H0=constants['Hubble0'], ΩM=constants['matter-density'],
                      ΩDE=constants['DE-density'], ΩR=constants['rad-density'],
                      w0=constants['w0'], wa=constants['wa']):
    """
    Method to compute the lookback time in Gyrs
    """
    integrand = lambda x: 1/(get_E_z(x, ΩM, ΩDE, ΩR, w0, wa)*(1+x))
    if isinstance(z, float) or isinstance(z, int):
        if z < 0:
            raise ValueError("Enter a non-negative redshift.")
        result, _ = integrate.quad(integrand, 0, z)
    elif isinstance(z, np.ndarray):
        if any(t < 0 for t in z):
            raise ValueError("Enter a non-negative redshift.")
        result = np.vectorize(lambda x: integrate.quad(integrand, 0, x)[0])(z)
    else:
        raise TypeError(f'Expected "Union[float, np.ndarray]", got {type(z)}')
    c0 = constants['speed-of-light']
    return result*hubble_time(H0)
```

That first day we worked until midnight. Too tired to keep going, we decided to talk later. But Niko stayed up and tried Streamlit. It worked! She immediately wrote to Matthijs and Marco, “We need to meet. This is wonderful. This is like magic." So we met on Zoom and continued working into the morning. In a week, we had the first working version of CosmΩracle!

![](https://streamlit.ghost.io/content/images/2022/02/craig-mckay-p3dGOGBFbP4-unsplash.jpg)

The unofficial fourth member of the gang: coffee. It supported every one of us during the small hours of the morning. Photo by [Craig McKay](https://unsplash.com/@ccmckay91?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

What worked well is the combination of several important factors:

* We had a clear goal in mind
* We had a lot of enthusiasm
* We were having fun

Also, the crucial part was that our communication was wonderful. We’re friends in real life. That makes everything easier.

Last but definitely not least, the Streamlit platform was essential. It’s very intuitive, powerful, customizable, and very easy to use. As scientists, we’re used to computations but have no experience in deploying web apps. Without Streamlit, we wouldn't have been able to build the momentum to finish this project.

We also used:

* [Slack](https://slack.com/intl/en-gb/?ref=streamlit.ghost.io) for creating tasks/private discussions or sending messages.
* [GitHub](https://github.com/?ref=streamlit.ghost.io) for version control, keeping track of issues that have to be dealt with, and for hosting a [GitHub Page](https://pages.github.com/?ref=streamlit.ghost.io) that links to the page hosted on Streamlit.
* [Zoom](https://zoom.us/?ref=streamlit.ghost.io) for in-person discussions.
* [Python](https://www.python.org/?ref=streamlit.ghost.io) for coding.

## Where to go from here?

Thanks to Streamlit, the code implementation was very easy. We have organized the code into blocks dedicated to configuration, computation, or presentation. The result is that CosmΩracle is structured in a way that makes it easy to create extensions.

For example, here is the script that’s at the center of the Streamlit app:

```
import streamlit as st

import page_introduction as pi
import page_distances as pd
import page_documentation as doc

st.sidebar.write(" ")

pages = {
        "Introduction": pi,
        "Cosmological Distances": pd,
        "Definitions": doc,
    }

st.sidebar.title("Main options")

# Radio buttons to select desired option
page = st.sidebar.radio("", tuple(pages.keys()))

pages[page].show_page()
```

The parts of CosmΩracle that do all the work (*Introduction,* *Cosmological Distances,* and *Definitions*) are stored in separate scripts. This makes CosmΩracle modular and extensible.

We plan to build a new feature that will let CosmΩracle compute the growth of matter density fluctuations in inflationary cosmology. After we finish the script, adding this new functionality to the app will be a simple matter of adding a line like `import page_perturbations` to the code above. This will make the corresponding adjustments to the list of pages and will be available on the website.

We also plan to extend the existing features of CosmΩracle.

For example, the current pre-set parameters are based on the latest analysis of the data of the *Planck satellite*. They’re hardcoded into the app in `page_distances.py` above. People from different parts of astronomy and cosmology will have different preferences for CosmΩracle’s parameters. We’ll be adding more sets (based on WMAP or the astronomical 70-30-70 cosmology).

Here is a sneak peek for you:

![](https://streamlit.ghost.io/content/images/2022/02/Cosmoracle_Sneak_Peak.gif)

We want to give CosmΩracle more functionality for quantities that are directly calculated from the cosmological distance measures. Currently, it can calculate angular sizes and convert between these angular sizes and physical sizes. But it can only give you an indication of the physical size of an object for a fixed angular extension of 1’’ (1 arcsecond or 1/3600th of a degree). We plan to add an option for you to set the angular size yourself. So if you want to know the real size of those 0.3’’ galaxy lobes, stay tuned!

## Wrapping up

With the increasing amount of knowledge and data, we need to develop ways of communicating findings and creating better and more accessible ways to disseminate knowledge. Accessibility and open-source are key to achieving it.

We’re very impressed with how easy it is to use Streamlit. And it’s open-source! For us, to have the code open to the public is extremely valuable because the community can inspect our work, point out our mistakes, and give suggestions for improvements.

We believe that science belongs to everyone. If our app helps the astronomy community with research and teaching, then we’ve achieved a great deal. And all of this was possible because Streamlit is *so easy to use.*

We hope you enjoyed our story. If you have any questions, please leave them in the comments below or reach out to Niko at [nikolina.sarcevic@gmail.com](mailto:nikolina.sarcevic@gmail.com), Matthijs at [primarius@gmail.com](mailto:primarius@gmail.com), and Marco at [bonici.marco@gmail.com](mailto:bonici.marco@gmail.com).

Happy Streamlit-ing! 🎈

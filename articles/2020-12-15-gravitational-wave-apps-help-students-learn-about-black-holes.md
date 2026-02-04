---
title: "Gravitational-Wave Apps Help Students Learn About Black Holes"
subtitle: "Exploring distant space with gravitational waves"
date: 2020-12-15
authors:
  - "Jonah Kanner"
category: "Advocate Posts"
---

![Gravitational-wave apps help students learn about black holes](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--39-.svg)


*Written by Jonah Kanner and Jameson Rollins of LIGO Laboratory, California Institute of Technology and Leo Singer of NASA Goddard Space Flight Center.*

Gravitational-wave detectors - like [LIGO](https://ligo.org/?ref=streamlit.ghost.io) and [Virgo](https://www.virgo-gw.eu/?ref=streamlit.ghost.io) - are some of the newest tools being used to explore objects in distant galaxies. The current generation of detectors began observing in 2015, and since then, have published observations of 50 collisions of black holes and neutron stars. These exciting discoveries are changing the way astrophysicists are learning about a broad range of topics - including how stars evolve, the expansion rate of the universe, and the deep laws that describe gravity and other fundamental forces.

LIGO and Virgo data are freely available through the [Gravitational Wave Open Science Center (GWOSC)](https://www.gw-openscience.org/about/?ref=streamlit.ghost.io). These public data sets are being used all over the world, by scientists, teachers, students, and artists, and have contributed to the publication of over 100 scientific articles over the past year.

## Barriers to learning

There’s one challenge encountered by everyone getting started with gravitational-wave data for the first time:  most options for working with these data sets demand installing specialized software libraries and writing computer code to process and display the results. For professional scientists, this is often OK - a full-time researcher can afford to spend a few hours installing and learning new software, and likely has already had some experience programming. But for a much broader audience - including high school students, teachers, and artists - writing code in Python to just get started with gravitational-wave data is a significant barrier.

We’d experimented with a few different options to make this transition easier. In fact, cloud hosted [Jupyter notebooks](https://www.gw-openscience.org/tutorials/?ref=streamlit.ghost.io) provided a big step forward, and we were able to show students how to write code to work with our data, without asking them to install any libraries on their own machines. But when we shared these notebooks with teachers and artists, they were not interested: **they wanted some way to work with gravitational-wave data without using any code at all!**

Moreover, it's not just new students who can benefit from an easier method to access LIGO/Virgo data. Even though professional scientists often *could* write specialized code to make the plot they want, it’s not efficient to have lots of scientists re-writing code to make the most popular plots.

## Enter Streamlit

Knowing that we had a need for a web app for the most common plots - both to broaden access and to improve research efficiency - we were excited to discover [Streamlit](https://www.streamlit.io/?ref=streamlit.ghost.io). Python is very popular in our research community, so Streamlit apps can easily make use of some of the most cutting-edge modules used for gravitational-wave research. For example, [pycbc](https://pycbc.org/?ref=streamlit.ghost.io) and [gwpy](https://gwpy.github.io/?ref=streamlit.ghost.io) are packages used by many gravitational-wave researchers to process and display LIGO/Virgo data. With Streamlit, we can easily write apps that let students and scientists use these packages, without writing any code themselves. Because GWOSC provides data access through a simple API, we found that Streamlit apps can access data on demand, and so process and display any segment of public data.

[Getting started video from GWOSC Learning Paths - video created by Cardiff University Physics & Astronomy](https://www.gw-openscience.org/path/?ref=streamlit.ghost.io)

Today, we’re using two Streamlit apps to introduce students to LIGO/Virgo data as part of the [GWOSC Learning Paths](https://www.gw-openscience.org/path/?ref=streamlit.ghost.io), and a third app, the [Gravitational Wave Inspiral Range Calculator](https://range.ligo.org/?ref=streamlit.ghost.io), allows scientists and astronomers to easily calculate how far into the universe current and future detectors can see.

## Working with data

To help students and scientists get started working with gravitational-wave data, we wrote the [GW Quickview App](https://share.streamlit.io/jkanner/streamlit-dataview/app.py?ref=streamlit.ghost.io) to make some common plots with any stretch of data. Users can instantly make plots by selecting a published gravitational-wave event from a list, or by entering any time LIGO and Virgo were running. The Quickview App has access to the full public archive of LIGO/Virgo data - around 30 TB and growing! Sliders allow the user to set filter and plotting options, and even to directly download the filtered data. In most cases, you can see the signal from a black hole merger or neutron star collision with just a few clicks. This app is a great way to take a first peak at a segment of data and explore the archive.

![gravitational](https://streamlit.ghost.io/content/images/2022/08/gravitational.gif#browser)

## How far can LIGO see?

One of the most important things to know about a gravitational-wave detector is how sensitive it is to the kinds of signals it’s capable of detecting. Ground-based gravitational-wave detectors primarily target the mergers of black holes or neutron stars, also known as compact binary coalescences (CBCs). Since the amplitude of a CBC signal is inversely proportional to how far away it is, the question is usually asked in terms of how far away can we detect the signal from a given type of CBC. In LIGO’s first observing run (O1) the LIGO detectors could detect binary neutron star (BNS) mergers out to a distance of roughly 70 megaparcecs (Mpc), or 230 million light-years. As the detectors have improved, the so-called “inspiral range” has increased as well; during the O3 run the LIGO BNS inspiral range was nearly 120 Mpc. Every time the range doubles the volume of space searched goes up by a factor of 8, and the event rate is proportional to volume. That’s a lot more events!

While plenty of tools exist to calculate the range for a given detector, all of them required special access and knowledge to run. With Streamlit, we were able to create a simple web app tool for anyone to [calculate the inspiral range for any type of CBC](https://range.ligo.org/?ref=streamlit.ghost.io) they wish, for any point of the past observing runs, or even for hypothetical detectors that are yet to be built. This app should be useful for LIGO scientists, for the general astronomy community, and for the public at large.

![2](https://streamlit.ghost.io/content/images/2021/08/2.png#browser)

## Finding signals in the noise

Gravitational wave signals are typically buried in noise; finding them requires a few signal processing tricks. These signal processing concepts are new to many students, and can be a barrier to understanding data from LIGO and Virgo. Working with Professor Amber Stuver at Villanova, we created an app to let students try out some signal processing in an easy to use, interactive environment. The [Signal Processing Tutorial](https://share.streamlit.io/jkanner/streamlit-audio/main/app.py?ref=streamlit.ghost.io) asks visitors to apply high-pass filtering and whitening to noisy data, to find a secret sound hidden in the noise. Then, they can try their new skills on some real data, and try to recreate a well known plot showing the first gravitational-wave observation of a binary black hole merger. Following hints from a [post by Pranav Pandit](https://streamlit.ghost.io/uc-davis-tool-tracks-californias-covid-19-cases-by-region/), we found we were able to speed up the app by porting plots from `matplotlib` to `altair`, so that students can adjust plot parameters and see updates almost instantly.

![3](https://streamlit.ghost.io/content/images/2021/08/3.png#browser)

## Building the app

We built the GW Quickview App partly as an experiment, to see how easy it would be to run some of our favorite python modules in Streamlit. In this case, we tried using gwpy, which has a number of handy methods for finding, processing, and plotting LIGO and Virgo data.

### Data discovery and download

The [app code](https://github.com/jkanner/streamlit-dataview?ref=streamlit.ghost.io) uses the gwosc client for data discovery, to get a list of all published gravitational-wave events, and find their GPS times:

```
from gwosc import datasets
eventlist = datasets.find_datasets(type='events')
chosen_event = st.sidebar.selectbox('Select Event', eventlist)
t0 = datasets.event_gps(chosen_event)
```

Then, it uses gwpy to download the data file with the corresponding time:

```
from gwpy.timeseries import TimeSeries
strain = TimeSeries.fetch_open_data(detector, t0-14, t0+14, cache=False)
```

The strain data are stored in some pretty big files (up to 500 MB), so we used the cache feature of `streamlit` to allow users to change plot parameters without needing to repeat the data download.

### Data processing

To make plots where you can see a signal in GW data, some signal processing steps are needed to reduce the impact of noise. The app uses the `bandpass()` and `whiten()` methods of gwpy to do this. Sliders allow the user to set the limits on the band-pass filter, and to toggle whitening on or off. The app also uses the gwpy `q_transform` method to make a beautiful time-frequency plot, which allows most detectable events to be clearly seen in the figure. Additional sliders allow setting plot parameters, so the user can fine-tune the time-frequency plot to look just right. We even used the new `streamlit beta_expander()`to allow the user to display hints about how to understand the plots and set the parameters.

### Display the plots

Finally, the app displays several plots to visualize the data. We opted to use convenient methods in gwpy to make plots with `matplotlib`, which saved us from writing code to style and label the plots. That fact that Streamlit can easily display these plots with `streamlit.pyplot()` was a big plus for us, and the Streamlit team helped us fix some [issues related to thread-safety](https://streamlit.ghost.io/uc-davis-tool-tracks-californias-covid-19-cases-by-region/) when using this feature.

Though we know that Streamlit apps run faster when plotting with `altair` (we used this trick in another app!), for the GW Quickview App, we chose to keep the `matplotlib` plots, mainly to demonstrate the handy plotting features built into gwpy.

## The big picture

A number of break-throughs in the past few years have proved that gravitational-wave detectors represent a new and exciting way to learn about our universe. To make use of this new technology, we’ll need to train the next generation of scientists who will build the instruments of the future and study their observations. After getting started with Streamlit apps and [GWOSC Learning Paths](https://www.gw-openscience.org/path/?ref=streamlit.ghost.io), we hope some students will move on to use other tools, such as large scale computing clusters, to participate in research activities. We’ve had fun building apps that make gravitational-wave data easier to access, and we hope they will spark imagination and interest in this emerging field.

---

*Special thanks to Amey Deshpande, Randy Zwitch, and the Streamlit team for improving the apps and editing this blog post*

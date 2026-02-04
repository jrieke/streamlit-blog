---
title: "UC Davis Dashboard That Tracks California's COVID-19 Cases By Region"
subtitle: "Regional tracking of COVID-19 cases aids day-to-day decision making in the UC Davis School of Veterinary Medicine"
date: 2020-11-19
authors:
  - "Pranav Pandit"
category: "Advocate Posts"
---

![New UC Davis tool tracks California's COVID-19 cases by region](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--19--1.svg)


*Written by Pranav Pandit - Postdoctoral Research Fellow at One Health Institute at UC Davis*

## Building a tool to understand COVID-19 at a regional level

The COVID-19 pandemic has highlighted the importance of constant and real-time disease surveillance to better control unprecedented local outbreaks. Early on in the pandemic, the state of California came up with its own distinct phases for opening the economy and community activities. These phases were based on county-wide thresholds of daily COVID-19 incidence, test positivity, and availability of ICU beds in the county. While county-wide data is continuously available, a composite picture of a group of counties is not as easy to understand. Such information is especially useful for bigger organizations that serve regional communities, such as universities, corporate companies, or dense urban regions that are highly connected.

At the UC Davis School of Veterinary Medicine, faculty, staff, and students come from many parts of California, but primarily from three counties—Yolo, Solano and Sacramento. University students, staff, and faculty commute from these nearby communities, so it's key to not just follow up on the COVID-19 statistics in Yolo County but rather look at a combination of the three counties to make informed decisions on reopening policies. Similarly, larger metropolitan areas such as the San Francisco Bay Area can benefit greatly from composite COVID-19 statistics for the region.

My team in the [Epicenter for Disease Dynamics](https://ohi.vetmed.ucdavis.edu/centers/epicenter-disease-dynamics?ref=streamlit.ghost.io) within the school’s One Health Institute was tasked with developing a tool that would go beyond county data and help us understand regional risk. Drawing from statistics already provided by the [California Department of Public Health](https://covid19.ca.gov/?ref=streamlit.ghost.io), [John Hopkins University](https://github.com/CSSEGISandData/COVID-19?ref=streamlit.ghost.io) and [CovidActNow.org](https://covidactnow.org/?s=1337332&ref=streamlit.ghost.io), we have created a COVID-19 tool that lets the university better understand our regional data and plan our day-to-day decisions.

## Creating the tool in Streamlit

By using Streamlit we were able to convert our Python code into an interactive tool that enables users to select counties of interest and get composite COVID-19 intelligence for the combined region. You can [check out the tool here](https://share.streamlit.io/panditpranav/svm_covid_tracking/main/COVID_app.py?ref=streamlit.ghost.io) and [the source code for the tool here](https://github.com/PanditPranav/SVM_COVID_tracking/blob/master/COVID_app.py?ref=streamlit.ghost.io).

![Counties_v2](https://streamlit.ghost.io/content/images/2022/08/Counties_v2.gif#browser)

### Compiling and presenting the data

We already had a lot of code developed to track and visualize cases in California with live data provided [through the state's data portal](https://covid19.ca.gov/?ref=streamlit.ghost.io). We also started capturing daily case data from the Center for Systems Science and Engineering (CSSE) at [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19?ref=streamlit.ghost.io) and decided to highlight informational snippets related to positive test rates and ICU rooms which is available through [CovidActNow.org](https://covidactnow.org/?s=1337332&ref=streamlit.ghost.io).

The application starts with displaying a dashboard that shows composite data of three counties surrounding the University of California Davis (Yolo, Sacramento and Solano). Users can either choose a single county or a combination of multiple counties of their choice to get trends on A) daily new cases per 100,000 population (averaged over the last seven days), (B) daily incidence (new cases), (C) Cumulative cases and deaths and (D) Daily new tests (testing data is available only for a few counties in California).

If you'd like to learn more about how to interpret these metrics, [covidlocal.org](https://covidlocal.org/?ref=streamlit.ghost.io) is a good resource - but in short, the initial reopening of a community is indicated when daily cases decline for 21 consecutive days and estimates for new cases per 100,000 are below 25 cases per day (Phase 2). Similarly, Phase 3 economic recovery opening is indicated when estimates for new cases per 100,000 are below 10 cases per day.

### Sharing our app with the rest of the world

Once the initial version of the app was ready, I wanted my teammates at UC Davis to access the app, but I didn't want to put them through the ordeal of downloading the source code, setting up the development environment, and running the app locally. We hosted it on Heroku, but soon realized its limitations in terms of the number of users that can access it simultaneously.   
  
Around the same time, Streamlit had launched a beta version of their sharing platform. [The Streamlit sharing platform](https://www.streamlit.io/sharing?ref=streamlit.ghost.io) allows deploying Streamlit apps directly from a public repository in Github and sharing with external shareholders for free (as of writing this sharing is currently invite only, but [you can sign-up here](https://www.streamlit.io/sharing?ref=streamlit.ghost.io)).

Once I was enrolled in the beta program, I was able to deploy the app in just a couple of clicks. All I had to do was host the app source code in [a public Github repository](https://github.com/PanditPranav/SVM_COVID_tracking?ref=streamlit.ghost.io).

After the app was deployed to the Streamlit sharing platform, I shared the URL with the Dean's office, and the URL shortly made it's way to school's internal portal and became a tool used in planning field operations while minimizing the risk of exposing students and researchers to Covid-19.

## Getting the app to shine

Around this time we noticed a couple of issues related to the performance and stability of the app. I will explain the issues along with the solutions below.

### Improving app stability

During one of my team meetings, when some of my teammates tried to access the app simultaneously, we noticed the app crashed and restarted. With the help of the engineering team at Streamlit, we narrowed down these issues to the use of `matplotlib` as the library for rendering charts based on data frames in the app. It turned out that `matplotlib` is not best suited for applications running in a highly concurrent environment, in fact, the official `matplotlib` documentation claims that [the library is not thread-safe](https://matplotlib.org/3.3.3/faq/howto_faq.html?ref=streamlit.ghost.io#working-with-threads). As a result, when multiple users tried to access the app simultaneously, the app would crash and restart. We were able to solve this problem by eliminating the use of `matplotlib` 's global API, and more importantly, by using explicit synchronization semantics when accessing `matplotlib` figures in the Python code (see [example code](https://github.com/PanditPranav/SVM_COVID_tracking/commit/62b7f8b374a17e6dd385d491829c33e764b0b5cf?ref=streamlit.ghost.io)).

### Improving app performance

As the app was becoming more popular within UC Davis, another concern I had was around the noticeably high latency of the charts loading when a user visits the app. I was already using Streamlit's built-in caching using `st.cache()` annotations, so I knew the app was not doing the heavy-lifting of downloading datasets and computing aggregates every time. We profiled the app's performance using Python's built-in `cProfile` package and observed that most of the time was spent plotting the charts inside `matplotlib`.  Taking inspiration from [a Streamlit user community forum](https://discuss.streamlit.io/t/fastest-plotting-library/1191?ref=streamlit.ghost.io) thread, which recommends `altair` as a more performant library for plotting, I ported the visualizations from `matplotlib` to `altair` , and noticed up to 3x improvement in the time it takes to run the app.

Here's a code snippet showing how easy it is to plot Altair charts in Streamlit:

```
# We use a custom scale to modify legend colors.
scale = alt.Scale(domain=["cases", "deaths"], range=['#377eb8', '#e41a1c'])

# Create a base chart layer using the dataframe.
base = alt.Chart(cases_and_deaths, title='(C) Cumulative cases and deaths'
    ).transform_calculate(
    cases_="'cases'", deaths_="'deaths'")
    
# Overlay a plot of number of cases.
c = base.mark_line(strokeWidth=3).encode(
    x=alt.X("Datetime", axis=alt.Axis(title = 'Date')),
    y=alt.Y("cases", axis=alt.Axis(title = 'Count')),
    color=alt.Color("cases_:N", scale=scale, title=""))
    
# Overlay a plot of number of deaths.
d = base.mark_line(strokeWidth=3).encode(
    x=alt.X("Datetime", axis=alt.Axis(title='Date')),
    y=alt.Y("deaths", axis=alt.Axis(title = 'Count')),
    color=alt.Color("deaths_:N", scale=scale, title=""))
    
# Finally, render the chart.
st.altair_chart(c + d, use_container_width=True)
```

## In closing

At the UC Davis School of Veterinary Medicine, the tool is being used to track metrics to better inform campus safety services and communications, but we believe the tool can be used for a wider audience as well.   
  
At this stage of the pandemic, many individuals, families, and smaller organizations are debating their own decisions - whether to take a vacation, if they can visit family during holidays, when to make a work trip, or if it's too much of a risk to conduct daily activities such as grocery shopping. Such activities often require an additional aspect of regional risk assessment, and we hope that our tool can help provide that context. Please try it out, send feedback, and continue to share your own data and create your own great tools. We'll all get through this together.

---

*Special thanks to Amey Deshpande and the Streamlit team for helping to optimize the app code and to Kat Kerlin, Tom Hinds and the UC Davis marketing team for the help editing the blog post.*

---

**About the author**

*Pranav Pandit*, BVSc & AH, MPVM, Ph.D. is a postdoctoral scholar at the EpiCenter for Disease Dynamics, part of the One Health Institute at the UC Davis School of Veterinary Medicine. A veterinary epidemiologist specializing in mathematical modeling, Pranav is interested in understanding transmission diseases in animal populations and factors affecting spillover to humans. After completing his MPVM from UC Davis, Pranav completed his Ph.D. from *École nationale vétérinaire de Nantes*, in France. Follow Pranav and the EpiCenter for Disease Dynamics on Twitter: [@PanditPranav](https://twitter.com/PanditPranav?ref=streamlit.ghost.io) and [@EpiCenterUCD](https://twitter.com/EpiCenterUCD?ref=streamlit.ghost.io).

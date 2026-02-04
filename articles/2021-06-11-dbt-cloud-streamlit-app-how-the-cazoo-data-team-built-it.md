---
title: "dbt Cloud & Streamlit App | How the Cazoo Data Team Built It"
subtitle: "How the Cazoo data science team built their dbt Cloud + Streamlit app"
date: 2021-06-11
authors:
  - "Martin Campbell"
category: "Advocate Posts"
---

![Easy monitoring of dbt Cloud jobs with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--7--1.svg)


*This post also appeared on the Cazoo Tech Blog, [read more here](https://medium.com/cazoo/easy-monitoring-of-dbt-cloud-jobs-with-streamlit-d33c43a5bbe0?ref=streamlit.ghost.io).*

Here in the [Cazoo](https://www.cazoo.co.uk/?ref=streamlit.ghost.io) data team, [dbt](https://www.getdbt.com/?ref=streamlit.ghost.io) is a core tool for taking raw data from our S3 datalake and transforming it into a form that is much more easily consumed by our reporting & analytics tools (Looker and AWS Athena to name just two).  We run multiple jobs throughout the day to serve data that is somewhat near real time (updated hourly) to keep our internal customers informed on how the business is performing.

We use dbt cloud to schedule our jobs, which unfortunately comes with one reasonably frustrating issue - detailed information on the status of jobs (including any reasons for failure) is not available for standard users, only Admins get access. Ideally we want to expose this information to a wider audience without needing to grant admin access, both because that would increase costs, but also, most people don't need admin level access, a read only view on these jobs is more than sufficient.  Fortunately dbt Cloud does provide an API, that allows us to pull some fairly detailed data from our jobs which we can use to, we just need some suitable way to display this.

Below we'll get into how we solved this, but if you want to jump right into the source code, [here it is](https://github.com/Cazoo-uk/dbt-streamlit?ref=streamlit.ghost.io).

## How Streamlit fits in

This is where Streamlit comes in. [Streamlit](https://streamlit.io/?ref=streamlit.ghost.io) is a fantastic way to build shareable web applications without any knowledge of front end technologies (which is rather handy for me, as whilst I can spell HTML and CSS that’s about as far as my knowledge goes). I’ve tried similar libraries (such as Dash) in the past but Streamlit has blown us all away with how easy it is to use, and how nice the resulting apps look.  Streamlit is open source, so you can deploy apps locally, or on your own infrastructure if you so wish.

At Cazoo, we have a broad strategy of making use of external expertise for running tools to lessen the overhead for our engineering teams, and so instead of deploying Streamlit on some Fargate instances at AWS we’ve been enthusiastic participants in the ongoing [Streamlit for Teams](https://streamlit.io/for-teams?ref=streamlit.ghost.io) beta.  This allows us to deploy our apps at the click of a button, and let someone else (the nice folks at Streamlit) worry about keeping the lights on.

As well as using Streamlit for the more obvious case of Analytics & Data Science apps - here in Data Engineering we’re also making use of it for apps where we want to expose operational information such as Dead Letter Queues, or in this case what’s happening with our dbt jobs.

## The dbt Cloud + Streamlit app

Full disclosure, I didn’t build this app, one of my colleagues [Oliver Morgans](https://github.com/OliverMorgans?ref=streamlit.ghost.io) did. I’m just helping out on this one.

![cazoo-1](https://streamlit.ghost.io/content/images/2022/09/cazoo-1.png#browser)

We’ve made the app available for anyone who wants to use it, and we’d certainly welcome any questions, comments or pull requests for ways to make this better. I’m sure as our analysts start using this they’ll be making suggestions for things they want to see also. You can find the source code at [here](https://github.com/Cazoo-uk/dbt-streamlit?ref=streamlit.ghost.io).

Detailed instructions for getting up and running are in the repo README.  You’ll need to add a few things like your dbt Cloud account\_id and API key into the streamlit secrets.toml, and you’ll probably want to swap out the logo we’ve stored in images too (unless you’re particularly enamoured with the Cazoo logo of course).

We have included basic username/password auth in the code, though if you’re using [Streamlit for Teams](https://streamlit.io/for-teams?ref=streamlit.ghost.io) I’d recommend you use the built in SSO as that’s a much nicer experience than typing in a long password each time.

The app is currently composed of a few pieces:

### Sidebar

![0_7XCiGHafU_Cy1xc0--3-](https://streamlit.ghost.io/content/images/2021/08/0_7XCiGHafU_Cy1xc0--3-.png#browser)

You can select to see all runs, successful runs or failed runs. And you can filter down by project (this project list is driven by a set of project ids you can add in secrets.toml)

### RAG Status

![0_bLyrD_iCLEzljxfg](https://streamlit.ghost.io/content/images/2021/08/0_bLyrD_iCLEzljxfg.png#browser)

We’re pulling the last 500 job runs, and this table will let you sort by the columns to get at what you’re after.

### Failed Steps

Of particular interest to our analysts, is the step (or steps) that a dbt job failed on, as most often that represents a unit test that has failed. So you have the option to select a specific run, and to see any failed steps in that run.

![0_zL052KWOPvXxGOo6](https://streamlit.ghost.io/content/images/2021/08/0_zL052KWOPvXxGOo6.png#browser)

That blue text is indeed a link which will take you to GitHub and the specific file that threw the error. You can configure the base URL for your repo as part of the secrets.toml.

### Historical Runs

![0_di0AIuD61ak2AfQC](https://streamlit.ghost.io/content/images/2021/08/0_di0AIuD61ak2AfQC.png#browser)

Picking a job name also exposes the last ten historical runs, which will also allow you to inspect them for failure steps if needed.

## Wrapping up

I am a huge fan of Streamlit, and the fact we’re able to easily use it not just for data science but for other operational things in engineering is making it a really key part of our toolbox.  I’d welcome any comments below on what you would add to this app, or feel free to tell us if we’re doing it all wrong - because every day is a school day!

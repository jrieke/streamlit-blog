---
title: "Labeling ad videos with Streamlit"
subtitle: "How Wavo.me uses Streamlit\u2019s Session State to create labeling tasks"
date: 2021-09-02
authors:
  - "Anastasia Glushko"
category: "Advocate Posts"
---

![Labeling ad videos with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--17-.svg)


*The clips labeled in the app preview are sample cutouts from [a music video "Pony"](https://www.google.com/url?q=https://www.youtube.com/watch?v%3DFlyY-3tv5DQ&source=gmail-imap&ust=1631133033000000&usg=AOvVaw0vzGmHHW-OteqWpWcJJ3WN) by a Montreal-based hip-hop artist [SLM](https://www.google.com/url?q=https://www.youtube.com/channel/UC1IOSWM092fcXW9sP-iFd4g&source=gmail-imap&ust=1631133033000000&usg=AOvVaw2x41SJJ4z3xAtXAZrkbH9r).*

Marketing ROI (return-on-investment) in the music industry is unpredictable. To break through, new artists have to invest in advertising. But will it succeed? A lot depends on [the ad creative's quality](https://martech.org/its-the-creative-stupid-3-reasons-why-ad-creative-trumps-technology-every-time/?ref=streamlit.ghost.io).

There are [many tips out there](https://www.facebook.com/business/help/370852930116232?id=271710926837064) on how to make a video ad stand out. But advertising music is different from advertising physical products, like clothing and house decor: music can be consumed directly in the ad.

At [Wavo](https://wavo.me/?ref=streamlit.ghost.io), we use the latest machine learning technology to make investing in artists more predictable and scalable. Our unique combination of technology and music industry expertise helps develop data-driven solutions to understand and optimize the quality of music marketing.

In this post, we'll cover:

1. Why does Wavo label ad videos?
2. What makes Streamlit a great labeling solution?
3. How to build a creative labeling app using Streamlit's SessionState

Let's jump right in!

## 1. Why does Wavo label ad videos?

Ads perform according to the features of the promotional materials used in them, or *Ad Creatives* (AC for short)*.*

Labeling AC features with Streamlit makes it possible to link them to performance metrics such as click-through rate, impressions, and views. By analyzing labeled data, we can better understand which ad features drive these performance metrics and build more effective campaigns.

To test this, we created a protocol for a proof-of-concept data science project. Our goal was to link metrics like click-through rate and video views to specific AC features and best practices.

We had three big resources:

1. 500 music video clips
2. 10 creative best practices from 5 years of running music advertising campaigns
3. 22 media analysts with vast experience running music marketing campaigns

## 2. What makes Streamlit a great labeling solution?

At first, we looked into using AWS Ground Truth and LimeSurvey. Both tools were quite powerful.  But for our purposes, most features would go unused and only add complexity to the labeling process. We wanted a fast, simple, and inexpensive prototype, and Streamlit fit the bill!

I knew about Streamlit from my [Insight Fellows](https://insightfellows.com/?ref=streamlit.ghost.io) days. While I spent days struggling with editing Bootstrap templates in html (ugh!), other “fellows” from my cohort used Streamlit. Their first machine learning apps were up in hours, all made in Python. The code looked impressively straightforward. I made a mental note to use only Streamlit going forward.

A year later, I had the opportunity to try it. I crossed my fingers that Streamlit could help me create a cohesive questionnaire: present a creative labeling form, store the labeler's response, and move on to the next AC. As it turned out, it could.

## 3. How to build a creative labeling app using Streamlit's SessionState

![streamlit-st_labelling-2021-07-29-11-07-52](https://streamlit.ghost.io/content/images/2021/09/streamlit-st_labelling-2021-07-29-11-07-52.gif#browser)

### Come up with a simple app layout

We built the labeling questionnaire in one sprint, with 150 lines of Python code.

You can do it, too! Here's how it worked.

The user (our in-house marketing expert) selected their name from a dropdown of user IDs. This triggered an individual list of ACs to be loaded by the app. The first video creative appeared on the screen with the corresponding labeling tasks. The user then watched the video and rated the creative quality (low, medium, or high).

![high_medium_low--1-](https://streamlit.ghost.io/content/images/2021/09/high_medium_low--1-.png#browser)

Next, the user entered the length of the video. Several checkboxes appeared—one for each creative best practice we recommend our clients to follow. The user had then selected all the best practices. This also included flags for the creative type: whether the video was a static visualizer or an animation.

![app_layout-1](https://streamlit.ghost.io/content/images/2021/09/app_layout-1.png#browser)

### Use Session State to remember users and labeled videos

[Without the use of Session State](https://streamlit.ghost.io/session-state-for-streamlit/), a simple Streamlit app would run your Python script from top to bottom. With every rerun of the script, it would lose any changes the user had made in the browser. The SessionState feature enables the simple persistence of these browser state changes.

We needed our app to retain two things in Session State, so that it could progress through our list of questions: the user ID (the name of the labeling expert) and the current question number. The user ID was taken from the user’s selection in the dropdown menu:

```
id_provided = st.selectbox('Hello! Who is this?', user_ids) 

# user_ids is a list defined above
```

To allow our labelers to start the questionnaire, take a break, close the app, and return to it later, we stored the answer to every question in a .csv file.

![sample_output-1](https://streamlit.ghost.io/content/images/2021/09/sample_output-1.png#border)

On every run of the script, Session State would be updated with the index of the next unanswered question. So whenever the user would return, they'd be exactly where they left off.

The same code ensured that the question number was updated on every consecutive run of the app (corresponding to all the labeling tasks for one of the video creatives):

```
import os
import pandas as pd
import streamlit as st

# check if the user is new or returning
output_filename = ‘./results_’ + str(id_provided) + ‘.csv’
	df = pd.DataFrame()
	if os.path.isfile(output_filename):
		df = pd.read_csv(output_filename)
	
	if df.shape[0] > 0:
		last_row = df.shape[0] - 1
		question_number = int(df.iloc[last_row].q_num) + 1
	else:
		question_number = 0

# defining our Session State
st.session_state.user_id = id_provided
st.session_state.question_number = question_number
```

When the user clicked through the labeling tasks for a given video and the script reruns, the Session State was updated: the id\_provided didn’t change (unless the user selected a different ID in the dropdown menu) and the question\_number increased by one. For every video labeling iteration, the question\_number was used to access the right link from the list of the videos to label.

### Make the app shine with some fun add-ons

To showcase some more fun use cases of Session State, we also had a progress bar at the top of the page:

```
st.progress((st.session_state.question_number)/(len(creatives))) 

# creatives is a list of links to the labelled video ads
```

![app_layout_progress_bar-1](https://streamlit.ghost.io/content/images/2021/09/app_layout_progress_bar-1.png#browser)

And then there’s one final reward:

```
if st.session_state.question_number >= len(creatives):
		st.text('THANK YOU, YOU ARE DONE!')
		st.balloons()
		st.stop()
```

![balloons-1](https://streamlit.ghost.io/content/images/2021/09/balloons-1.gif#browser)

## Wrapping up

Over the course of one week, 23 marketing experts labeled 500 creatives. This allowed us to report data-driven insights about creative quality to our clients and build better marketing campaigns.

With Streamlit, developing a custom and user-friendly labeling questionnaire for this project took just a few hours of work for one data scientist. 10/10 we would use Streamlit again.

Got questions? Let me know in the comments or via [email](mailto:anastasia@wavo.me).

Article by  
**Anastasia Glushko**  
Machine Learning Researcher

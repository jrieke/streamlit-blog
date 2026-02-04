---
title: "How Delta Dental uses Streamlit to make lightning-fast decisions"
subtitle: "From an idea to a prototype to production in just two weeks"
date: 2022-02-01
authors:
  - "Amanda Kelly"
category: "Case study"
---

![How Delta Dental uses Streamlit to make lightning-fast decisions](https://streamlit.ghost.io/content/images/size/w2000/2022/01/01-outlier-calls.png)


As a dental benefits company, Delta Dental of NJ receives a lot of customer calls. The data science team, led by Lead Scientist Kevin Northover, works with that data to figure out how to improve their operations. This includes creating predictive models for call sentiment analysis, identifying outlier calls, and calculating detailed statistics on individual agents. But the generated insights weren’t making it into the hands of the call center managers who could act on that data.

The challenge was to find an application that allowed them to display all data in a clean, beautiful, and easy-to-understand way. The team analyzed data in notebooks, spreadsheets, and BI tools like Looker and Tableau, but they needed more than just static dashboards. To understand and use the operational insights, they needed to create a powerful, interactive data app that the operations team could use every day.

"I need the speed to insights to drive decisions in the company," says Justin Lahullier, CIO at Delta Dental of NJ. "That's data science. Traditionally, there are long lead times for development to move data from source to target. Then more time for an analyst to work from target to a report or a dashboard. If a business has a question, they want an answer. How fast can we answer it and communicate it to a business user so that they can understand it?"

## Lightning-fast app deployment

Around the time Justin asked the team to create a new application, Kevin became aware of Streamlit. Streamlit takes ordinary Python scripts (with a few magical Streamlit calls sprinkled in) and almost instantly [turns them into beautiful, performant, sharable apps](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace?source=friends_link&sk=f7774c54571148b33cde3ba6c6310086). Kevin knew Python, so he decided to give Streamlit a try. He [learned Streamlit in minutes](http://docs.streamlit.io/?ref=streamlit.ghost.io), made a test app in a few hours, and deployed Delta Dental's first call-center prototype app in just two weeks:

![02-latest-call-detail-screen-1](https://streamlit.ghost.io/content/images/2022/01/02-latest-call-detail-screen-1.png#browser)

The app had a simple analysis dashboard that linked to other operational tools, one of which tagged thousands of phone calls, then scanned them for outliers:

![01-outlier-calls-1](https://streamlit.ghost.io/content/images/2022/01/01-outlier-calls-1.png#browser)

All call analysis was displayed to agents next to the call transcript. The app refreshed regularly, so the call center agents always got the latest data. They could download the call lists, review the call transcripts, fill out the coaching questionnaires, playback the recordings, and leave comments:

![03-drilling-into-intents](https://streamlit.ghost.io/content/images/2022/01/03-drilling-into-intents.png#browser)

"The agents don't need to be technically advanced with this app, as they can easily navigate through data visualizations," says Kevin. "It takes a lot of work to get a good widget interface that feels natural. You spend so much effort on the UI in the initial build. Streamlit's UI actually made a difference. A big part of it is simplicity."

## Fast iteration cycles made the team more agile

The quick prototype-to-production path meant that the team could now get feedback, share ideas, prototype, iterate, and rapidly ship changes to their business users. They could deliver more while keeping the team lean.

"With Streamlit I can just deploy the app and people can go and interact with it and put in comments. Then a week later we go back and iterate on that, figure out what comments to integrate and update," says Kevin. "You don't need a data science team of twenty people to do this," adds Justin. "Streamlit works for smaller organizations to allow you to move faster."

By adopting Streamlit, their data science team delivered relevant data to their operations team with only four people.

## Building more complex apps for more users

Two years into using Streamlit, Delta Dental is now adding more functionality, expanding their apps to more internal users, and making Streamlit their go-to production tool. They want to make their operations even more efficient by exploring forms for the call evaluation within the app—to dissect the structure of a single call, break it down to individual speakers, and track the problem to a specific speaker. This way the agents could listen to one voice rather than the whole call.

Using Streamlit has changed how Justin interacts with his data team. "What I appreciate is the ability for Kevin to send me the URL and say, 'Go interact with the data.' It'll have tables and visualizations. I can interact with it, look at it, ask him questions. It allows us to iterate on where we're trying to get—to answer business questions or fix problem areas. I like the ease of being able to go and look at it rather than him sending me a spreadsheet. The app is being refreshed at a regular interval, so I'm seeing timely data and I can play with it, to think through more questions."

"l do all my data work inside Streamlit now," adds Kevin. "If you're doing something that is standard business reporting, then the standard tools are fine. But if you're doing something where your people are trying to figure out what questions they want to ask, then use Streamlit."

Want to get started with Streamlit in your organization? Head over to [streamlit.io](http://streamlit.io/cloud?ref=streamlit.ghost.io) to learn more.

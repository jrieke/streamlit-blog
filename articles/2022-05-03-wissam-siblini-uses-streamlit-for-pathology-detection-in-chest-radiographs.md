---
title: "Wissam Siblini uses Streamlit for pathology detection in chest radiographs"
subtitle: "Learn how Wissam detected thoracic pathologies in medical images"
date: 2022-05-03
authors:
  - "Wissam Siblini"
category: "Case study"
---

![Wissam Siblini uses Streamlit for pathology detection in chest radiographs](https://streamlit.ghost.io/content/images/size/w2000/2022/05/Frame-18-1.png)


Wissam Siblini always wanted to be a computer scientist. He started coding in middle school, studied engineering in college, and did his PhD in his favorite field, at the intersection of maths and computer science.

When Wissam started as a machine learning researcher, he set out to implement innovative features in fraud detection, natural language processing, and health. But he couldn’t manage the front-end development of an application. He spent most of his time processing data, developing algorithms, and training and evaluating them.

"Machine learning is one of the most exciting fields for the decades to come," Wissam said. "We're seeing the development of groundbreaking image recognition tools, agents that understand our language, and more generative tools for voice, image, sound, and art of all kinds. But I like to question basic facts. While working on fraud detection, I was interested in the very definition of simple evaluation measures like precision and recall. I even proposed variants that are now mentioned on the [F-score Wikipedia page](https://en.wikipedia.org/wiki/F-score?ref=streamlit.ghost.io#Dependence_of_the_F-score_on_class_imbalance)!"

### The need to develop a demo app

With the Covid-19 crisis, chest diseases became a major concern around the world. Deep learning (a subset of machine learning) showed very convincing performances in understanding texts, images, and genomics. It found applications in the medical field, particularly in personalized, predictive, and preventive medicine.

Wissam decided to target a specific "AI for Health" problem—the detection of thoracic pathologies in medical images.

![Untitled](https://streamlit.ghost.io/content/images/2022/04/Untitled.png#border)

To do this, he and Mazine, a colleague who worked on this exploratory project with him, needed to look at the data, interact with it, and discuss it with others. They also had to clean it, select it, transform it, and build it into a model.

"I used to carry out this type of analysis in Jupyter notebooks but it wasn’t interactive," Wissam said. "I wanted to show my results to other project members, especially to non-data scientists."

When his team finished the proof of concept and had a prototype model, they needed a demo app. They wanted the users to upload a radiograph, get predictions (probabilities of pathologies and alerts), and see a visual interpretation of the model’s decision. They also wanted the users to browse the training data and its characteristics, monitor the performance of the model on a validation set, play with model parameters, and see the impact on performance.

This required front-end development, and several back-end functionalities such as an API for model serving. It was very time-consuming and required the knowledge of many different frameworks. It was hard to do in the last stages of a POC when the development had already consumed a lot of time.

### Discovering Streamlit

![Gallery--10-FPS-](https://streamlit.ghost.io/content/images/2022/05/Gallery--10-FPS-.gif#border)

It was then that Wissam discovered Streamlit.

“We had only a few weeks to complete this pathology project,” Wissam said. “I still wanted a demo to show that it was promising and integrable. I was comfortable with Python, but not with frameworks like Angular, Vue, and React. So I googled “frontend development in Python” and ran into Streamlit (the early 0.60.0 version). I was amazed by the app examples on the website—especially the conciseness of their code and deployment procedure.”

After browsing the site for a few minutes, Wissam decided to use Streamlit not only for this project but for many others.

“I looked for solutions on the Streamlit forum and saw [Fanilo Andrianasolo](https://fr.linkedin.com/in/andfanilo?ref=streamlit.ghost.io), a very talented colleague of mine,” Wissam said. “He was an active member of the Streamlit community. We discussed it, and I made my choice.”

### Streamlit seamlessly dressed up our machine learning results as an interactive chest radiographs classification app

Streamlit allowed the team to build exactly what they wanted.

“The most important part of my job is to allow stakeholders to understand my work even if they’re not data scientists,” Wissam said. “Streamlit made my life better *and* easier for that. It took us almost five months to build a very competitive model. With Streamlit, we’ve then built a very cool app that won us an internal innovation prize and convinced the management to keep exploring the theme. And it took **only two weeks!**”

![Untitled--1-](https://streamlit.ghost.io/content/images/2022/04/Untitled--1-.png#border)

The app featured a classifier page where the user could upload imagery, obtain a probability for each pathology (displayed in red if above a critical threshold), and get the [interpretability heat map](https://arxiv.org/abs/1610.02391?ref=streamlit.ghost.io) associated with the pathology of its choice. The imagery could be in a standard image format (PNG or JPEG) or in the more classical DICOM format.

![Chest-Radiographs-Classifier-GIF](https://streamlit.ghost.io/content/images/2022/05/Chest-Radiographs-Classifier-GIF.gif#border)

The app had a Dashboard Data (to visualize the characteristics of the training data) and a Dashboard Model to analyze the model's performance and tune hyperparameters. For example, the user could set the critical threshold for each anomaly and see the impact on True Positive Rate, Precision, or Accuracy.

![dashboard_model_2](https://streamlit.ghost.io/content/images/2022/05/dashboard_model_2.PNG#browser)

### 6 reasons why it was obvious to start with Streamlit

For Wissam these were the reasons why it was so obvious to him to get started with Streamlit:

1. Most of today’s data scientists already use Python. They can easily convert their projects into Streamlit apps.
2. The visuals (the frontend part) and the engine (the backend part/models) are all implemented in the same code.
3. Many built-in features (sliders, buttons, tables, etc.) allow you to build a wide range of utilities in just a few lines of code. And both the Streamlit team and the community enrich these features every day.
4. There are many example apps for your inspiration on the Streamlit website and on GitHub.
5. The Streamlit forum is rich and active, so if you’re stuck, you can get help easily.
6. The apps look very good. They’re more than enough for a great demo!

“In addition to demos, Streamlit can help with the exploratory phase of a project,” Wissam added.  “In this phase, the goal is to see how some variables can impact others, display charts, play with parameters, observe behavior, and test transformation functions. Building a Streamlit exploration app then lets you focus on the analysis itself (not the code) *and* discuss it with subject-matter experts who are not data scientists.”

### Wrapping up

“I’m so used to developing things with Streamlit now, it takes me hardly any time to make apps,” Wissam said. “I once coded an app in the morning, and in the afternoon it was ready for the client.”

Thank you for reading Wissam’s story! If you have any questions, please leave them in the comments below or contact Wissam on [LinkedIn](https://www.linkedin.com/in/wissam-siblini/?ref=streamlit.ghost.io) or via email. Happy coding!

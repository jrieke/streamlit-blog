---
title: "Observing Earth from space with Streamlit"
subtitle: "Learn how Samuel Bancroft made the SatSchool app to teach students Earth observation"
date: 2022-06-16
authors:
  - "Samuel Bancroft"
category: "Advocate Posts"
---

![Observing Earth from space with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/06/satschool-gif-3.gif)


Have you ever tried teaching teenagers Earth observation and environmental science in an interactive way? That was my goal at SatSchool, and that's why I made the SatSchool app!

In this post, we’ll talk about:

* Making a website with satellite data
* Making a quiz
* Why use Streamlit?

Can’t wait to dive in? Here is the [SatSchool app](https://share.streamlit.io/spiruel/satschool/main/app.py?ref=streamlit.ghost.io) and [here](https://github.com/Spiruel/SatSchool?ref=streamlit.ghost.io) is the repo code.

But before we get to the fun stuff…

## What is the SatSchool app?

SatSchool is a school outreach program that introduces Earth observation concepts and career pathways to students (11-15 years old) in the UK. Students get their hands on satellite data to learn how satellites help us study the Earth from space.

As part of this program, I developed the SatSchool app— a “Hands on with Data” module—that introduces technical approaches to Earth observation challenges.

## Making a website with satellite data

The SatSchool app features three themes: land, oceans, and ice (check out the [source code here](https://github.com/Spiruel/SatSchool?ref=streamlit.ghost.io)).

### Land

This theme features an Amazon deforestation page.

Here I used:

* Support Vector Machine (SVM) classifier to make a deforestation map
* Input widgets for more forest/not-forest training points
* `st.session_state` to remember the training points (as students label more data based on what they see)

![satschool-1](https://streamlit.ghost.io/content/images/2022/06/satschool-1.png#browser)

Students can view Landsat-8 satellite imagery centered over a region in Brazil and compare the deforested areas with protected areas. Many explore machine learning and experiment with classifiers for the first time!

They learn how their training data makes the classifier better or worse, how satellite imagery can solve problems, and how to dynamically measure deforestation over thousands of square kilometers without installation, powerful computers, or technical know-how!

### Oceans

This theme explores the relationship between the sea surface temperature and chlorophyll.

Here I used:

* Altair charts to present simple graphs
* `st.number_input` and `st.form` to make answering questions interactive (with `st.balloons` for correct answers! 🎈).

![satschool-2](https://streamlit.ghost.io/content/images/2022/06/satschool-2.png#browser)

By using `geemap` with its split-panel map, students explore two global datasets and the connection between them.

### Ice

This theme explores coding.

Here I used:

* `streamlit_ace` for the terminal
* `st.session_state` for step-by-step instructions in an `st.warning` box for aesthetic appeal

![satschool-3](https://streamlit.ghost.io/content/images/2022/06/satschool-3.png#browser)

Students get introduced to radar satellite data and can bring up satellite images by using code before they realize they’re programming!

## Making a quiz

I wanted to bring gamification into the learning process. Satellite imagery is cool, but how could I keep young people engaged so that they had fun learning?

![satschool-gif-2](https://streamlit.ghost.io/content/images/2022/06/satschool-gif-2.gif#browser)

Our quiz tests students on the SatSchool curriculum concepts. To get the best score, they have 30 seconds to answer as many questions as they can.

Here is how I did it in five steps:

### Step 1

I did the following imports and variables:

```
import streamlit as st 
import time
import random
import math

TIME_LIMIT = 30 #seconds
row = None
```

### Step 2

I randomly generated math questions using the following code:

```
def gen_question():
    #randomly choose two numbers in a range, alongside an operator
    operators = ['+','-','//','*']
    a,b = random.randint(1,10), random.randint(1,10)
    op = random.choice(operators)
    
    #construct the question text and evaluate the calculation
    ques = f"What is {a} {op} {b}?"
    ans = eval(f"{a}{op}{b}")

    #we create some purposely incorrect answer options
    option2 = eval(f"{b}{op}{a}")
    option3 = eval(f"{b-2}{op}{a+5}")
    option4 = eval(f"{b}{op}{a}-{a}")
    #we want to avoid duplicate answer options, so use this inelegant solution
    while option2 == ans:
       option2 += 1
    while option3 == ans or option3 == option2:
       option3 += 1
    while option4 == ans or option4 == option2 or option4 == option3:
       option4 += 1
    
    return {'question': ques,
            'options': {
            ans: True,
            option2: False,
            option3: False,
            option4: False
            }
            }
```

### Step 3

I initialised values in `st.session_state` to keep track of timings, scores, etc.:

```
#initialise the session state if keys don't yet exist
if 'correct' not in st.session_state.keys():
    st.session_state['correct'] = None
if "quiz_active" not in st.session_state.keys():
    st.session_state["quiz_active"] = False

i,j,_ = st.columns([1,1,5])
if i.button("Start quiz", key='start_quiz', disabled=st.session_state['quiz_active']):
    st.session_state['quiz_active'] = True
    st.session_state['total_score'] = 0
    st.session_state['count'] = 0
    st.session_state['time_start'] = time.time()
    st.session_state['time_now'] = time.time()
    st.session_state['score'] = 0
    st.session_state['correct'] = None
    st.experimental_rerun()
if j.button("End quiz and reset", key='reset', disabled=not st.session_state['quiz_active']):
    st.session_state['total_score'] = 0
    st.session_state['count'] = 0
    st.session_state['correct'] = None
    st.session_state['quiz_active'] = False
    st.session_state['time_start'] = None
    st.experimental_rerun()

if not st.session_state['quiz_active']:
    st.write(f'\\n Welcome to the quiz! You have {TIME_LIMIT} seconds to answer as many questions as you can.')
```

### Step 4

I controlled the button layout by using a mix of `st.columns()`, `st.container()`, and `st.empty()`:

```
question_empty = st.empty()

d,e,_ = st.columns([2,2,6])
with d:
    total_score_empty = st.empty()
with e:
    st.write('')
    answer_empty = st.empty()

if st.session_state['quiz_active']:
    #check for time up upon page update
    if time.time() - st.session_state['time_start'] > TIME_LIMIT:
        st.info(f"Time's up! You scored a total of **{st.session_state['total_score']:.2f}** \\
                    and answered **{st.session_state['count']}** questions.")
    else:
        with question_empty:
            with st.container():
                #get a newly generated question with answer options
                row = gen_question()
                
                st.markdown(f"Question {st.session_state['count']+1}: {row['question']}")

                options = list(row['options'].keys())
                random.shuffle(options)

                a,b,_ = st.columns([2,2,6])
                #construct the answer buttons, and pass in whether the answer is correct or not in the args
                a.button(f"{options[0]}", on_click=answer, args=(str(row['options'][options[0]]),))
                a.button(f"{options[1]}", on_click=answer, args=(str(row['options'][options[1]]),))
                b.button(f"{options[2]}", on_click=answer, args=(str(row['options'][options[2]]),))
                b.button(f"{options[3]}", on_click=answer, args=(str(row['options'][options[3]]),))
                
                if st.session_state['correct']  == 'True' and st.session_state['count'] > 0:
                    answer_empty.success(f"Question {st.session_state['count']} correct!")
                elif st.session_state['correct'] == 'False' and st.session_state['count'] > 0:
                    answer_empty.error(f"Question {st.session_state['count']} incorrect!")
                total_score_empty.metric('Total score', value=f"{st.session_state['total_score']:.2f}", delta=f"{st.session_state['score']:.2f}")
```

### Step 5

Finally, I defined a function that takes an answer and does something with the score:

```
def answer(ans):
    st.session_state['correct'] = ans
    if ans == 'True':
        #motivate quickfire answers with an exponential decay
        score = (1 * math.exp(-0.05*(time.time()-st.session_state['time_now'])))*10
        st.session_state['score'] = max(1, score)
    else:
        #penalise wrong answers with a negative score
        st.session_state['score'] = -10
    #update the score but prevent it from becoming negative
    st.session_state['total_score'] += st.session_state['score']
    st.session_state['total_score'] = max(0, st.session_state['total_score'])
    
    st.session_state['time_now'] = time.time()
    st.session_state['count'] += 1
```

I saved my completed script and viewed my app with `streamlit run`.

Also, if I wanted to, I could randomly choose from a selection of pre-written questions and implement a leaderboard functionality so that students could see their scores alongside others in the classroom.

## Why use Streamlit?

Before I wrap this up…one more thing.

Why did I choose Streamlit? I’ve been using Streamlit for the past few years and knew it’d be perfect to make the SatSchool app because:

* I can quickly deploy my Python code without any front-end headaches.
* I can make a good-looking site and deploy my app to the Streamlit Community Cloud to share my work.
* I can easily extend and modify the site. When my SatSchool colleagues want to add new content or demos, I can quickly prototype it (especially with the help of [Sebastian Flores Benner](https://www.linkedin.com/in/sebastiandres/?ref=streamlit.ghost.io)’s fantastic [streamlit\_book](https://github.com/sebastiandres/streamlit_book?ref=streamlit.ghost.io) library).
* Streamlit’s amazing ecosystem of demos and third-party libraries make coding fast and fun. Third-party libraries are easy to integrate and offer lots of exciting functionality. Alongside the above-mentioned [`streamlit_book`](https://github.com/sebastiandres/streamlit_book?ref=streamlit.ghost.io) library, there is [Qiusheng Wu](https://www.linkedin.com/in/qiushengwu/?ref=streamlit.ghost.io)’s [`geemap`](https://github.com/giswqs/streamlit-geospatial?ref=streamlit.ghost.io) for the visualisation of satellite data, `streamlit_timeline`, `streamlit_ace`, `streamlit-lottie`, `streamlit_juxtapose`, and more.

## Wrapping up

I had a lot of fun making the SatSchool app and I’m excited to hear what you think! There’s still a lot to do. Expect updated app demos as we take our program into schools and show people the power of satellite imagery.

I hope this post can show you how easy it is to make great apps with Streamlit. If you have any questions or want to share what you built, contact me on Twitter at [@spiruel](https://twitter.com/Spiruel?ref=streamlit.ghost.io) and check out SatSchool at [@SatSchool\_](https://twitter.com/SatSchool_?ref=streamlit.ghost.io) and on our [website](https://satschool-outreach.github.io/About/?ref=streamlit.ghost.io).

Happy coding! 🛰️

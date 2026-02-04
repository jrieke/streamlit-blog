---
title: "How to build an interconnected multi-page Streamlit app"
subtitle: "From planning to execution\u2014how I built GPT lab"
date: 2023-07-19
authors:
  - "Dave Lin"
category: "LLMs"
---

![How to build an interconnected multi-page Streamlit app](https://streamlit.ghost.io/content/images/size/w2000/2023/07/Community--1-.svg)


Wow! What an incredible three months since I first published my blog post on [the 12 lessons learned from building GPT Lab!](https://streamlit.ghost.io/building-gpt-lab-with-streamlit/) 🚀

Thanks to your tremendous support, GPT Lab has received over 9K app views, 1200+ unique signed-in users, 1000+ sessions with assistants, 700+ prompts tested, and 190+ assistants created. The app has also been featured in the Streamlit App Gallery alongside other great apps.

Many of you have asked me, "How did you plan and build such a large application with Streamlit?" Eager to answer, I've decided to open-source GPT Lab.

By reading this post, you’ll gain insights into the planning it took to build an interconnected multi-page Streamlit app like GPT lab:

* Upfront feature and UX
* Data model
* Code structure
* Session states

I hope it'll inspire you to push Streamlit to its limits and bring your ambitious apps to life!

🤖

Want to skip ahead? Check out the [app](https://gptlab.streamlit.app/?ref=streamlit.ghost.io) and the [code](https://github.com/dclin/gptlab-streamlit?ref=streamlit.ghost.io).

## Planning a large Streamlit app

Building large Streamlit apps like GPT Lab requires careful planning rather than just throwing code together. For GPT Lab, I focused on planning these four key aspects:

1. **Upfront feature and UX.** What will the app do? What kind of user experience do we aim to provide?
2. **Data model.** How will data be persisted? What should be stored in the database versus session state variables?
3. **Code structure.** How should the app be architected to ensure modularity, maintainability, and scalability?
4. **Session states.** Which session state variables are needed to link the user interface?

Understanding these aspects offered a clearer view of what I was trying to build and provided a framework to approach the complex task systematically.

Let's dive into each aspect in more detail.

## Upfront feature and UX: Creating initial spec and low-fi UX mocks

To start, I created a simple specification document (or "spec") outlining the overall scope and approach. I also included a sitemap detailing the use cases I wanted to support. The spec gave me a clear roadmap and a means to measure my progress.

Here's an excerpt from the original spec:

**Scope.** Build a platform that allows generative AI (GA) bot enthusiasts to build their own GPT-3 prompt-based chatbot for their friends and families. The goal is to test the hypothesis that enough GA bot enthusiasts would want to build their niche-domain bots.  
  
**Approach.** A public Streamlit site that allows users to interact with one of the four pre-trained coach bots or create and interact with their bots.

As with most development projects, I made some changes. But the original sitemap remained intact for the most part, as I could implement most of the planned features.

Here is the final version of the sitemap:

```
GPT Lab
│
├── Home
│
├── Lounge
│
├── Assistant
│   ├── Search for assistant
│   ├── Assistant details
│   ├── Active chat
│   └── Chat recap
│
├── Lab
│   ├── Step 1: initial prompt + model config
│   ├── Step 2: test chat
│   ├── Step 3: other configs
│   └── Step 4: confirmation
│
├── FAQ
│
└── Legal
    ├── Terms
    └── Privacy policy
```

I can't overstate the importance of feature planning. It provides a roadmap, a way to measure progress, and a starting point for thinking about the data model.

## Data model: Determining the schema

From the start, I recognized that a backend data store was crucial for persisting user, assistant, and session records. After considering my options, I decided on Google Firestore due to its scalability, real-time capabilities, and generous free tier. I strategically designed the data model with future use cases in mind. For example, it's possible to add prompt version controls to GPT Lab, allowing users to edit or revert their assistants.

🤖

NOTE: In the app backend and data model, assistants are referred to as bots, despite my previous insistence on not calling them bots in the user interface. 😅

Now, let's explore the four main Firestore collections in GPT Lab: users, user\_hash, bots, and sessions.

### Users and user\_hash

The users collection is where the app stores information about its users. To protect user privacy, the app doesn't store any personally identifiable information (PII) about users. Instead, each user is associated only with the one-way hash value of their OpenAI API key. The metric fields are incremented whenever a user creates an assistant or starts/ends a session with an assistant. This allows for basic analytics gathering within the app.

```
Users Collection
   |
   | - id: (Firestore auto-ID)
   | - user_hash: string (one-way hash value of OpenAI API key)
   | - created_date: datetime
   | - last_modified_date: datetime
   | - sessions_started: number
   | - sessions_ended: number
   | - bots_created: number
```

Google Firestore doesn't provide a way to ensure the uniqueness of a document field value within a collection, so I created a separate collection called user\_hash. This ensures that each unique API key has only one associated user record. Each user document is uniquely associated with a user\_hash document, and each user\_hash document may be associated with a user document. The data model is flexible enough to accommodate users who change their API keys in the future (users can log in with their old API key and then swap it out for a new one).

```
User_hash Collection
   |
   | - id = one-way hash value of OpenAI API key
   | - user_hash_type: string (open_ai_key)
   | - created_date: datetime
```

### Bots

The bots collection stores configurations for AI assistants. The crux of each AI assistant is its large language model (LLM), model configurations, and prompts. To enable proper version control of prompts and model configurations in the future, model\_configs and prompts are modeled as subcollections (part of GPT Lab's vision is to be the repository of your prompts).

To minimize subcollection reads (so you don't need to constantly query the subcollections for the active record), the document IDs of the active subcollection are also stored at the document level. The session\_type field indicates whether the assistant is in a brainstorming or coaching session, which affects the session message truncation technique.

Finally, the metric fields are incremented when a user starts or ends a session with an assistant.

```
Bots Collection
   |
   | - id: (Firestore auto-ID)
   | - name: string
   | - tag_line: string
   | - description: string
   | - session_type: number
   | - creator_user_id: string
   | - created_date: datetime
   | - last_modified_date: datetime
   | - active_initial_prompt_id: string
   | - active_model_config_id: string
   | - active_summary_prompt_id: string
   | - showcased: boolean
   | - is_active: boolean
   |
   v
   |--> Model_configs subcollection
   |     |
   |     | - config: map
   |     |     | - model: string 
   |     |     | - max_tokens: number 
   |     |     | - temperature: number 
   |     |     | - top_p: number 
   |     |     | - frequency_penalty: number 
   |     |     | - presence_penalty: number 
   |     | - created_date: datetime
   |     | - is_active: boolean
   |
   v
   |--> Prompts subcollection
         |
         | - message_type: string
         | - message: string
         | - created_date: datetime
         | - is_active: boolean
         | - sessions_started: number
         | - sessions_ended: number
```

### Sessions

The sessions collection stores session data. It contains two types of sessions: lab sessions (used for testing prompts) and assistant sessions (used for chatting with created assistants). To reduce the need for frequent retrieval of the bot document, its information is cached within the session document. This makes conceptual sense, as the bot document could drift if an editing assistant use case were ever implemented.

The `messages_str` field stores the most recent payload sent to OpenAI's LLM. This feature allows users to resume their previous assistant sessions. The `messages` subcollection stores the actual chat messages. Note that lab session chat messages aren't stored.

To ensure user confidentiality and privacy, OpenAI request payloads and session messages are encrypted before being saved in the database. This data model allows users to restart a previous session and continue chatting with the assistant.

```
Sessions Collection
   |
   | - id: (Firestore auto-ID)
   | - user_id: string
   | - bot_id: string
   | - bot_initial_prompt_msg: string
   |
   | - bot_model_config: map
   |     | - model: string 
   |     | - max_tokens: number 
   |     | - temperature: number 
   |     | - top_p: number 
   |     | - frequency_penalty: number 
   |     | - presence_penalty: number 
   |
   | - bot_session_type: number
   | - bot_summary_prompt_msg: string
   | - created_date: datetime
   | - session_schema_version: number
   | - status: number
   | - message_count: number
   | - messages_str: string (encrypted)
   |
   v
   |--> Messages subcollection
         |
         | - created_date: datetime
         | - message: string (encrypted)
         | - role: string
```

By carefully considering all potential use cases from the beginning, I created a data model that is future-proof and able to accommodate the evolving needs and features of the app. In the following section, we'll examine the structure of the backend application code to see how it supports and implements this robust data model.

## Code structure: Structuring for scalability and modularity

I created GPT Lab to empower users with low or no technical skills to build their own prompt-based LLM-based AI applications without worrying about the underlying infrastructure. My goal is to eventually offer backend APIs that connect users' custom front-end apps (whether using Streamlit or not) with their AI assistants. This motivated me to design a decoupled architecture that separates the front-end Streamlit application from the backend logic.

The backend code was structured as follows:

```
+----------------+     +-------------------+     +-------------------+     +------------+
|                |     |                   |     |                   |     |            |
|  Streamlit App |<--->| util_collections  |<--->| api_util_firebase |<--->|  Firestore |
|                |     | (users, sessions, |     |                   |     |            |
|                |     |  bots)            |     |                   |     |            |
+----------------+     +-------------------+     +-------------------+     +------------+
                             |
                             |
                             v
                     +-----------------+     +------------+
                     |                 |     |            |
                     | api_util_openai |<--->|   OpenAI   |
                     |                 |     |            |
                     +-----------------+     +------------+
```

The modules are as follows:

* **api\_util\_firebase** handles CRUD operations with the Firestore database.
* **api\_util\_openai** interacts with OpenAI's models, provides a unified chat model to upstream models, prunes chat messages, and tries to detect and prevent prompt injection attacks.
* **api\_util\_users**, **api\_util\_sessions**, and **api\_util\_bots** are interfaces to their corresponding Firestore collections. They interact with api\_util\_firebase and api\_util\_openai and implement GPT Lab-specific business logic.

This design enables separate development, testing, and scaling of different parts of the code. It also establishes an easier migration path to convert the backend util\_collections modules into Google Cloud Functions, which can be exposed via API Gateways.

## Session states: Managing UI and user flow

As explained in the [first blog article](https://streamlit.ghost.io/building-gpt-lab-with-streamlit/#2-developing-advanced-uis-with-ui-functions-rendered-by-session-states), I used session state variables to control and manage functionalities on Streamlit pages.

This table illustrates how these variables are utilized throughout the app:

|  |  |
| --- | --- |
| Streamlit Page | Session state and UI controls |
| home.py | **user** controls whether to render the OpenAI API key module. |
| pages/1\_lounge.py | **user** controls whether to render the OpenAI API key module, enable assistant selections, and show the My Assistants tab.     After users choose to interact with an assistant, the assistant details are stored in **bot\_info**. |
| pages/2\_assistant.py | **user** controls whether to render the OpenAI API key module.   **bot\_info**, **session\_id**, and**session\_ended** determine which screen variation to display:    • **bot\_info** does not exist: check to see if assistant\_id is in the URL parameter. Else, prompt users to search for an assistant   • **bot\_info** and **session\_id** exist, and **session\_ended** is false: display the chat session screen   • **bot\_info** and **session\_id** exist, and **session\_ended** is true: display the chat session recap screen    In the chat session, **session\_msg\_list** stores the conversation. |
| pages/3\_lab.py | **user** gates whether to render the OpenAI API key module and whether to allow users to start creating assistants in the lab.   **lab\_active\_step** controls which lab session state to render:  • If 1: render step 1 UI to set assistant initial prompt and model  • If 2: render step 2 UI to test chat with assistant  • If 3: render step 3 UI to finalize assistant details. On create, the bot record is created in Firestore DB, and the document ID is saved to **lab\_bot\_id**.  • If 4 and lab\_bot\_id is set: render step 4 UI to show assistant creation confirmation.    During the test chat session, **lab\_msg\_list**stores the test messages. By using separate **lab\_bot\_id** and **bot\_info**, I can allow users to jump back and forth between lounge/assistant and lab without losing progress in each. |

With the upfront planning done, the rest of the execution was a lot more manageable.

## Wrapping up

This post covered the upfront planning required for creating GPT Lab, including the features, data model, code, and session state. I hope this inspires you to build your own ambitious Streamlit apps.

Connect with me on [Twitter](https://twitter.com/dclin?ref=streamlit.ghost.io) or [Linkedin](https://www.linkedin.com/in/d2clin/?ref=streamlit.ghost.io). I'd love to hear from you.

Happy Streamlit-ing! 🎈

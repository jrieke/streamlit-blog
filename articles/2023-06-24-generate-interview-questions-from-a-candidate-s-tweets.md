---
title: "Generate interview questions from a candidate\u2019s  tweets"
subtitle: "Make an AI assistant to prepare for interviews with LangChain and Streamlit"
date: 2023-06-24
authors:
  - "Greg Kamradt"
category: "LLMs"
---

![Generate interview questions from a candidate’s  tweets](https://streamlit.ghost.io/content/images/size/w2000/2023/06/Community.svg)


Hey, team! 👋

My name is Greg Kamradt, and I teach people how to analyze data and build AI apps. I’ve spent much of my career doing product analytics in B2B environments at enterprises and startups. I love enabling people to make an impact in their workplace.

Preparing for an interview can be time-consuming, so I built an app that analyzes a candidate's Twitter, YouTube videos, and web pages to generate a list of interview questions. I use LangChain, ChatGPT4, and Streamlit to package it all into a convenient tool.

In this post, I’ll cover:

* An introduction to working with GPT4 through LangChain
* A UX convention to ensure that users **don’t** need to supply a prompt
* A working understanding of Tweepy (Python library for interacting with Twitter data)
* An introduction to web-scraping with LLMs
* Bringing all your data together with a prompt to prepare for the meeting

👴

Want to skip reading? Here's a link to the [Jupyter Notebook](https://github.com/gkamradt/langchain-tutorials/blob/main/data_generation/Using%20LLMs%20To%20Summarize%20Personal%20Research.ipynb?ref=streamlit.ghost.io), [GitHub repo](https://github.com/gkamradt/llm-interview-research-assistant?ref=streamlit.ghost.io) for the app, and the resultant [app](https://gkamradt-llm-interview-research-assistant-main-1ptqgt.streamlit.app/?ref=streamlit.ghost.io).

If you’re a visual learner, here is a video outlining this process in detail:

## Step 1. Make sure the major pieces of your app work

The app consists of two main steps:

1. Gathering data
2. Processing the data with a language model

The data-gathering process involves three sources:

* **Twitter:** Tweets likely have the most up-to-date and relevant information about what's on the person’s mind
* **Webpages:** To get information about a person, it's best to include a biography or an "About me" page
* **YouTube videos:** This might include an interview with the person or a talk they gave

### Twitter

Let’s create a function that utilizes [Tweepy](https://docs.tweepy.org/en/stable/index.html?ref=streamlit.ghost.io) to pull the most popular recent tweets from a person.

The goal is to return a string of text so you can pass it to your LLM later:

```
def get_original_tweets(screen_name, tweets_to_pull=80, tweets_to_return=80):

	# Tweepy set up
	
	auth= tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
	    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
	    api= tweepy.API(auth)
	
	# Holder for the tweets you'll find
	tweets= []
	
	# Go and pull the tweets
	tweepy_results= tweepy.Cursor(api.user_timeline,
	                                   screen_name=screen_name,
	                                   tweet_mode='extended',
	                                   exclude_replies=True).items(tweets_to_pull)
	
	# Run through tweets and remove retweets and quote tweets so we can only look at a user's raw emotions
    for status in tweepy_results:
        if hasattr(status, 'retweeted_status')or hasattr(status, 'quoted_status'):
        # Skip if it's a retweet or quote tweet
            continue
        else:
            tweets.append({'full_text': status.full_text, 'likes': status.favorite_count})


        # Sort the tweets by number of likes. This will help us short_list the top ones later
    sorted_tweets= sorted(tweets, key=lambda x: x['likes'], reverse=True)

        # Get the text and drop the like count from the dictionary
    full_text= [x['full_text']for xin sorted_tweets][:tweets_to_return]

        # Convert the list of tweets into a string of tweets we can use in the prompt later
    users_tweets= "\\n\\n".join(full_text)

        return users_tweets
```

### Webpages

To pull data from web pages, make a simple request with the requests library and pass that information through [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/?ref=streamlit.ghost.io) and [markdownify](https://pypi.org/project/markdownify/?ref=streamlit.ghost.io).

Again, you want to return a simple piece of text to insert into your prompt later:

```
def pull_from_website(url):

	# Doing a try in case it doesn't work
	try:
	        response= requests.get(url)
	except:
	# In case it doesn't work
		print ("Whoops, error")
		return
	
	# Put your response in a beautiful soup
	soup= BeautifulSoup(response.text, 'html.parser')
	
	# Get your text
	text= soup.get_text()
	
	# Convert your html to markdown. This reduces tokens and noise
	text= md(text)
	
	return text
```

### YouTube videos

Lastly, use [LangChain’s YouTube video document loader](https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/youtube_transcript?ref=streamlit.ghost.io). By default, this loader returns a list of LangChain documents.

You want the plain text to pass through to your prompt later:

```
def get_video_transcripts(url):
    loader= YoutubeLoader.from_youtube_url(url, add_video_info=True)
    documents= loader.load()
    transcript= ' '.join([doc.page_contentfor docin documents])
    
	return transcript
```

### Bring it all together

Once you have all of this information, combine it into a single string:

`user_information = user_tweets + website_data + video_text`

Because the string’s length might be too long for your model, split it into chunks and process them individually:

```
# First we make our text splitter
text_splitter= RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)

# Then we split our user information into different documents
docs = text_splitter.create_documents([user_information])
```

Next, pass the docs through a custom map and reduce prompt (learn more about chain types in [my video](https://www.youtube.com/watch?v=f9_BWhCI4Zo&ref=streamlit.ghost.io)). To help with your custom prompts, use LangChain’s prompt templates.

First, your map step:

```
map_prompt= """You are a helpful AI bot that aids a user in research.
Below is information about a person named {persons_name}.
Information will include tweets, interview transcripts, and blog posts about {persons_name}
Your goal is to generate interview questions that we can ask {persons_name}
Use specifics from the research when possible

% START OF INFORMATION ABOUT {persons_name}:
{text}
% END OF INFORMATION ABOUT {persons_name}:

Please respond with list of a few interview questions based on the topics above

YOUR RESPONSE:"""
map_prompt_template= PromptTemplate(template=map_prompt, input_variables=["text", "persons_name"])
```

Then your combined step:

```
combine_prompt= """
You are a helpful AI bot that aids a user in research.
You will be given a list of potential interview questions that we can ask {persons_name}.

Please consolidate the questions and return a list

% INTERVIEW QUESTIONS
{text}
"""
combine_prompt_template= PromptTemplate(template=combine_prompt, input_variables=["text", "persons_name"])
```

Now that you have your data and prompts set up pass this information through your LLM:

```
llm= ChatOpenAI(temperature=.25, model_name='gpt-4')

chain= load_summarize_chain(llm,
                             chain_type="map_reduce",
                             map_prompt=map_prompt_template,
                             combine_prompt=combine_prompt_template,
#                              verbose=True
)
```

This command will run the API call to OpenAI:

```
output= chain({"input_documents": docs, "persons_name": "Elad Gil"})
```

I tested this out, pretending I was going to interview [Elad Gil](https://eladgil.com/?ref=streamlit.ghost.io). The results had awesome questions!

```
1. As an investor and advisor to various AI companies, what are some common challenges you've observed in the industry, and how do you recommend overcoming them?

2. Can you elaborate on the advantages of bootstrapping for AI startups and share any success stories you've come across?

3. What are some key lessons you've learned from your experiences in high-profile companies like Twitter, Google, and Color Health that have shaped your approach to investing and advising startups?

4. How do you think AI will continue to shape the job market in the coming years?

5. What motivated you to enter the healthcare space as a co-founder of Color Health, and how do you envision the role of AI in improving healthcare outcomes?
```

👴

NOTE: The results likely **won’t** be copy/paste ready. You’ll need to edit the text to match your voice and style.

### Step 2. Port your code over to a single script and add Streamlit support

Finally, combine it into a single script and add Streamlit support!

See the complete code in this app's [main.py](https://github.com/gkamradt/llm-interview-research-assistant/blob/main/main.py?ref=streamlit.ghost.io). I like to add some styling and information at the top of my apps. It provides more context and eases the user into the app.

One of my favorite Streamlit containers is `st.columns`. Let's use that to add some text and a picture:

```
	# Start Of Streamlit page
st.set_page_config(page_title="LLM Assisted Interview Prep", page_icon=":robot:")

# Start Top Information
st.header("LLM Assisted Interview Prep")

col1, col2 = st.columns(2)

with col1:
    st.markdown(("Have an interview coming up? I bet they are on Twitter or YouTube or the web. "
		             "This tool is meant to help you generate interview questions based off of "
		             "topics they've recently tweeted or talked about."
		             "\\n\\n"
		             "This tool is powered by [BeautifulSoup](<https://beautiful-soup-4.readthedocs.io/en/latest/#>), "
		             "[markdownify](<https://pypi.org/project/markdownify/>), [Tweepy](<https://docs.tweepy.org/en/stable/api.html>), "
		             "[LangChain](<https://langchain.com/>), and [OpenAI](<https://openai.com>) and made by "
		             "[@GregKamradt](<https://twitter.com/GregKamradt>)."
		             "\\n\\n"
		             "View Source Code on [Github](<https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py>)"))
with col2:
    st.image(image='Researcher.png', width=300, caption='Mid Journey: A researcher who is really good at their job and utilizes twitter to do research about the person they are interviewing. playful, pastels. --ar 4:7')
# End Top Information
```

![llm-assisted-interview-prep](https://streamlit.ghost.io/content/images/2023/06/llm-assisted-interview-prep.png#border)

Now let's add a few input forms for the user to provide the candidate's information:

![input-1](https://streamlit.ghost.io/content/images/2023/06/input-1.png#border)

The `st.text_input` widgets let you accept information from the user and pass it to the application later:

```
person_name = st.text_input(label="Person's Name",  placeholder="Ex: Elad Gil", key="persons_name")
twitter_handle = st.text_input(label="Twitter Username",  placeholder="@eladgil", key="twitter_user_input")
youtube_videos = st.text_input(label="YouTube URLs (Use , to separate videos)",  placeholder="Ex: <https://www.youtube.com/watch?v=c_hO_fjmMnk>, <https://www.youtube.com/watch?v=c_hO_fjmMnk>", key="youtube_user_input")
webpages = st.text_input(label="Web Page URLs (Use , to separate urls. Must include https://)",  placeholder="<https://eladgil.com/>", key="webpage_user_input")
```

I wanted the user to be able to select the type of output they prefer. They may not want interview questions but a one-page summary about a person.

Using a Streamlit radio button, they can select their preferred option:

```
output_type = st.radio(
"Output Type:",
('Interview Questions', '1-Page Summary'))
```

Based on their selection, you'll pass different instructions to your prompt. You could build out many more options if you'd like!

```
response_types = {
	'Interview Questions' : """
	Your goal is to generate interview questions that we can ask them
	Please respond with list of a few interview questions based on the topics above
""",
'1-Page Summary' : """
	Your goal is to generate a 1 page summary about them
	Please respond with a few short paragraphs that would prepare someone to talk to this person
"""
}
```

Next, let's add a button to control the flow of the application. By default, Streamlit will update the app after any field has changed. While this is great for some use cases, I don't want my LLM to start running until the user is finished.

To control this, I'll add a button that will only run after clicking the "Generate Summary" button. `button_ind` will only be set to true if the button was clicked during the last run:

```
button_ind = st.button("*Generate Output*", type='secondary', help="Click to generate output based on information")

# Checking to see if the button_ind is true. If so, this means the button was clicked and we should process the links
if button_ind:
	# Make the call to your LLM
```

Next, take the code you'd previously written in your Jupyter Notebook and output it to your Streamlit page using `st.write`:

```
output = chain({"input_documents": user_information_docs, # The seven docs that were created before
"persons_name": person_name,
"response_type" : response_types[output_type]
})

st.markdown(f"#### Output:")
st.write(output['output_text'])
```

Let's check out the output for Elad:

![elad-gil-summary](https://streamlit.ghost.io/content/images/2023/06/elad-gil-summary.png#border)

Awesome!

## Step 3. Deploy and test

![deploy-an-app](https://streamlit.ghost.io/content/images/2023/06/deploy-an-app.png#border)

Great! Now that your script works locally, you can deploy it on Streamlit Community Cloud so others can use it. Remember to load your `.env` variables as secrets on Streamlit.

To see a video of this deployment, click [here](https://youtu.be/zvoAMx0WKkw?t=1022&ref=streamlit.ghost.io).

To check out the live app, click [here](https://gkamradt-llm-interview-research-assistant-main-1ptqgt.streamlit.app/?ref=streamlit.ghost.io).

## Wrapping up

Thanks for joining me on this journey! You created an app that summarized the information you needed to prepare for meeting an interview candidate.

If you have any questions, please post them in the comments below or contact me on [Twitter](https://www.notion.so/cfce451487824393a2688dc01b498ec6?pvs=21&ref=streamlit.ghost.io) or email [contact@dataindependent.com](mailto:contact@dataindependent.com).

Happy coding! 👴

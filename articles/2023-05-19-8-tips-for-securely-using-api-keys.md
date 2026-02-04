---
title: "8 tips for securely using API keys"
subtitle: "How to safely navigate the turbulent landscape of LLM-powered apps"
date: 2023-05-19
authors:
  - "Chanin Nantasenamat"
category: "Tutorials"
---

![8 tips for securely using API keys](https://streamlit.ghost.io/content/images/size/w2000/2023/05/8-tips-for-using-API-keys.svg)


An Application Programming Interface (API) refers to how two software entities communicate. For example, OpenAI provides an API that enables developers to programmatically access their large language models (LLMs) such as GPT3, GPT3.5, and GPT4. Such LLMs may be used to create LLM-powered apps that could generate content based on user-provided prompts.

An API key is a unique identifier used to authenticate and authorize access to an API. Typically, API service providers allow developers to generate API keys for subsequent use in apps and tools.

![](https://streamlit.ghost.io/content/images/2023/05/what-is-api-key-3.png)

In this age of generative AI, API keys are no longer restricted to app developers but also extend to end users. Whether you're (1) using them in your code or (2) pasting them into third-party apps, unwarranted key usage could compromise your apps and lead to an unexpectedly large bill.

In this post, I'll share with you eight tips for using API keys safely (to avoid security breaches and prevent unwanted access and large bills):

* Tip 1. Recognize API key risks
* Tip 2. Choose apps with public source code
* Tip 3. Set appropriate key limits
* Tip 4. Use throwaway keys
* Tip 5. Never commit API keys to repositories
* Tip 6. Use environment variables instead of API keys
* Tip 7. Monitor and rotate API keys
* Tip 8. Report concerns about apps

🔑

NOTE: The use of API keys as a developer refers to their use in code, while the use of API keys as a user refers to simply pasting them into apps.

### Generating OpenAI API key

Before we proceed to the tips, let’s generate an OpenAI API key:

* Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys?ref=streamlit.ghost.io)
* Click on `+ Create new secret key`
* Enter an identifier name (optional) and click on `Create secret key`

![generate-openai-apikey](https://streamlit.ghost.io/content/images/2023/05/generate-openai-apikey.gif#browser)

### Using an API key in an app

Let's take a practical look at how to use OpenAI API keys in an app. LLMs can be expensive due to the high volume of tokens consumed by user queries. So you may choose to allow users to provide your own API keys when releasing your app (see Tips 1 and 2 for safeguarding yourself).

Here is an example of entering your own API key as used in the [Ask My PDF app](https://ask-my-pdf.streamlit.app/?ref=streamlit.ghost.io) developed by [Maciej Obarski](https://www.linkedin.com/in/mobarski/?ref=streamlit.ghost.io).

![ask-my-pdf-screenshot-1](https://streamlit.ghost.io/content/images/2023/05/ask-my-pdf-screenshot-1.png#border)

The app will use the API key provided by the user to gain access to OpenAI's LLM model for the generative AI task, such as generating answers to user-provided questions.

## Tip 1. Recognize API key risks

Let's start with the basics: recognizing some risks associated with using API keys.

Have you ever performed the following tasks?

* Hardcoding API keys in your code
* Storing API keys in plain text
* Including API keys in public repositories
* Leaving API keys in publicly accessible places

These are just a few examples of how API keys can be exposed to unwanted users. In other words, there is always a risk associated with using API keys. By following best practices for securing API keys, you can help protect your data and prevent unwanted access to your apps.

API keys can be stolen or leaked through various means, such as phishing attacks, data breaches, and insecure coding practices. Once an API key is stolen or leaked, it can perform unwanted actions, such as accessing sensitive data, making unwanted changes to data, or even taking down an entire system in extreme cases.

## Tip 2. Choose apps with public source code

One of the best ways to ensure the security of your API keys is to choose apps with public source code. This means that anyone can view the code that makes up the app.

There are two major benefits of such code transparency:

1. It helps to identify potential security vulnerabilities or malicious activity.
2. It allows other developers to help identify potential vulnerabilities so that they can be fixed.

To find apps with public source code, use open-source repositories like GitHub and BitBucket. Users can inspect the underlying code to detect malicious activities or security vulnerabilities. Users can use their API keys after verifying that the app is safe.

🔑

NOTE: This tip assumes that you have a proficient level of programming expertise. You’re welcome to consult a friend or an expert for a second opinion.

## Tip 3. Set appropriate key limits

No matter how well you secure your API key, there's always a chance that it may leak. This will have an impact on the app's security vulnerabilities and can lead to financial loss.

![Image Description](https://streamlit.ghost.io/content/images/2023/05/set-key-limits.png)

To resolve this, you can set an upper limit on how much credit is allocated to a particular API key. For example, specify a limit of $5 for an API key you use in a live tutorial as an instructor. Anyone attempting to use the API key will only be able to do so up to a maximum of $5. After that, the API key is no longer valid.

## Tip 4. Use throwaway keys

Throwaway API keys are temporary and short-lived ones that are used briefly and then discarded (or expired).

To use them, generate a new key for each purpose. They can be generated like any other API keys from the API provider's website. As an added safety measure, apply the previous tip on setting credit limits to your keys. When you're done using the throwaway key, you can revoke it to prevent further use.

![](https://streamlit.ghost.io/content/images/2023/05/throwaway-keys-updated.png)

## Tip 5. Never commit API keys to repositories

A common mistake is exposing your API keys by unknowingly committing them to your GitHub repo. To prevent this, store your API keys in a separate file from the main code, then explicitly specify files or directories to ignore in a `.gitignore` file. This will leave out those files/directories when committing code.

### Using .gitignore to hide your API key

For example, if you want to leave out the API key stored in `config.py`, include the following content in the `.gitignore` file:

```
config.py
```

Your API keys will be safe when committing your code to GitHub!

### Storing your API key in a file

Expanding on the `config.py` file used for storing the API key, here is the file content:

```
OPENAI_API_KEY='xxxxxxxxxxxx'
```

In Python, you can retrieve and print the API key as follows:

```
from config import OPENAI_API_KEY

print(OPENAI_API_KEY)
```

In the next tip, we'll consider using environment variables to store API keys.

## Tip 6. Use environment variables instead of API keys

Another common mistake is hard-coding API keys directly into your code.

### Store API key as environment variables

One way to securely store API keys is to save them as environment variables on your computer. This is useful when saving the keys in the user profile, such as in the `~/.bashrc` or `~/.bash_profile` file.

For example, you can store your OpenAI API key as an environment variable in your user profile by creating the `~/.bashrc` or `~/.bash_profile` file with the following content:

```
export OPENAI_API_KEY='xxxxxxxxxxxx'
```

Whenever your code needs to access the API key, it can be detected by the Python library or specified as an input argument.

### Retrieving the API key

Here's how to retrieve your API key from the environment variable:

1. In a terminal window, type the following (`$OPENAI_API_KEY` is the OpenAI API key):

```
$ echo $OPENAI_API_KEY
```

2. In Python, use the following:

```
os.environ['OPENAI_API_KEY']
```

3. Or, to access your stored OpenAI API key, use the following:

```
os.getenv('OPENAI_API_KEY')
```

If the Python library doesn't automatically detect the API key, you can specify it as an input argument. For example, for our OpenAI code, this would be the `openai_api_key` input argument:

```
llm = OpenAI(temperature=0.7, openai_api_key=os.getenv('OPENAI_API_KEY'))
```

### Secrets management on a cloud platform

It's worthwhile to check if the cloud platform on which you're deploying your LLM-powered app provides functionality to manage your API credentials.

For example, the Streamlit Community Cloud has a secrets management capability that enables you to securely store and access secrets in your Streamlit app as environment variables.

You can get the OpenAI API key into the app by pasting the credentials into the secrets text box as shown below:

![streamlit-secrets-management](https://streamlit.ghost.io/content/images/2023/05/streamlit-secrets-management.png#browser)

Afterward, using the credentials in the app can be done as follows (don't forget to `import os`):

```
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
```

## Tip 7. Monitor and rotate API keys

To monitor your API keys, estimate the usual amount of app usage. It may indicate that your API key has been compromised if it exceeds a certain threshold. Also, monitoring the API keys' IP addresses can help identify unwanted access. Set up alerts to notify you immediately of any suspicious activity.

Rotating API keys is another effective way to mitigate security vulnerabilities. You can periodically replace API keys with newly generated ones and revoke the old ones.

## Tip 8. Report concerns about the app

If you come across a potential security compromise while inspecting the code of a publicly shared app, you may want to report it.

Here are two ways to do it:

1. Contact the app developer. Please provide specific details (screenshots or error messages) to help them understand and fix the issue. This protects you *and* helps other users.
2. If you have the time and the skills, fix it yourself and submit a pull request.

## Wrapping up

API keys are important assets that provide developers and users with access to API providers' services. But there are concerns regarding the security of API keys when using them in code or pasting them into third-party apps. This post presents eight tips for using API keys securely, preventing unwanted access and potential financial loss.

While writing this, I asked the community about the secure use of API keys:

![Image Description](https://streamlit.ghost.io/content/images/2023/05/api-keys-survey.png)

Which tips resonated with you the most? Do you use an approach not mentioned here? Please let me know in the comments below or contact me on Twitter at [@thedataprof](https://twitter.com/thedataprof?ref=blog.streamlit.io) or on [LinkedIn](https://www.linkedin.com/in/chanin-nantasenamat/?ref=blog.streamlit.io).

This post was made possible thanks to the brainstorming ideas from Joshua Carroll, Krista Muir, and Amanda Kelly as well as technical reviewing from Lukas Masuch and Charly Wargnier. And as always, I'm grateful to Ksenia Anske for editing this post.

Happy Streamlit-ing! 🎈

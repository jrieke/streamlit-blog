---
title: "Streamlit-Authenticator, Part 1: Adding an authentication component to your app"
subtitle: "How to securely authenticate users into your Streamlit app"
date: 2022-12-06
authors:
  - "Mohammad Khorasani"
category: "Advocate Posts"
---

![Streamlit-Authenticator, Part 1: Adding an authentication component to your app](https://streamlit.ghost.io/content/images/size/w2000/2022/11/streamlit-authenticator-part-1.svg)


🚀

Update: Streamlit now has built-in authentication via OIDC/OAuth2, which may be an alternative to the auth mechanism discussed here. Read more [in our docs](https://docs.streamlit.io/develop/concepts/connections/authentication?ref=streamlit.ghost.io).

Hey, community! 👋

My name is Mohammad Khorasani, and I’m a co-author of the book [Web Application Development with Streamlit](https://www.amazon.com/Web-Application-Development-Streamlit-Applications/dp/1484281101?linkCode=sl1&tag=kho_abd_her-20&linkId=ee9e303b3445d601f8ab440ddc81a4fc&language=en_US&ref_=as_li_ss_tl&ref=streamlit.ghost.io) (Streamlit helped me get into full-stack development, so it was only fair to spread the word about it).

As developers, we often require features that are yet to be made natively. For me, that was implementing user authentication and privileges in a client-related project that eventually grew into a full-fledged package aptly named Streamlit-Authenticator.

Specifically, my client asked for the ability to authenticate users with different privilege levels for their business needs, as well as a whole host of other features. That’s what prompted me into developing this package. While authentication is definitely needed for some apps—especially corporate ones—it's great to make your apps accessible to the community whenever possible to share and spread the learnings!

In this two-part tutorial, you’ll learn:

* How to install Streamlit-Authenticator
* How to hash user passwords
* How to create a login widget
* How to authenticate users
* How to implement user privileges

👉

TL;DR? Here's the [repo code](https://github.com/mkhorasani/Streamlit-Authenticator?ref=streamlit.ghost.io).

## How to install Streamlit-Authenticator

Let’s start by creating a login form to authenticate a list of predefined users. Install the component by using the following command:

```
pip install streamlit-authenticator
```

Next, import the component into your Python script:

```
import streamlit_authenticator as stauth
```

## How to hash user passwords

It’s absolutely vital to hash any password that will be stored on a disk, database, or any other medium. Here, you’ll be defining your users’ credentials in a YAML file.

You’ll also define several other configuration settings pertaining to the key and expiry date of the re-authentication JWT cookie. If you don’t require passwordless re-authentication, just set the ***expiry\_days*** to 0.

You can also define a *preauthorized* list of users who can register their usernames and passwords (I’ll cover this in the next post in this series).

**Step 1.** Create the YAML file:

```
credentials:
  usernames:
    jsmith:
      email: jsmith@gmail.com
      name: John Smith
      password: abc # To be replaced with hashed password
    rbriggs:
      email: rbriggs@gmail.com
      name: Rebecca Briggs
      password: def # To be replaced with hashed password
cookie:
  expiry_days: 30
  key: random_signature_key # Must be string
  name: random_cookie_name
preauthorized:
  emails:
  - melsby@gmail.com
```

**Step 2.** Use the Hasher module to convert your plain text passwords into hashed passwords:

```
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
```

**Step 3.** Replace the plain text passwords in the YAML file with the generated hashed passwords.

## How to create a login widget

Now that you’ve defined your users’ credentials and configuration settings, you’re ready to create an authenticator object.

**Step 1.** Import the YAML file into your script:

```
import yaml
from yaml.loader import SafeLoader
with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
```

**Step 2.** Create the authenticator object:

```
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
```

**Step 3.** Render the login widget by providing a name for the form and its location (i.e., sidebar or main):

```
name, authentication_status, username = authenticator.login('Login', 'main')
```

## How to authenticate users

Once you have your authenticator object up and running, use the return values to read the *name*, *authentication\_status*, and *username* of the authenticated user.

You can ppt-in for a logout button and add it as follows:

```
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

Or you can access the same values through a session state:

```
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
```

![logged-in](https://streamlit.ghost.io/content/images/2022/11/logged-in.png#border)

You can also alter the user if their credentials are incorrect:

![incorrect-login](https://streamlit.ghost.io/content/images/2022/11/incorrect-login.png#border)

After logging out, the *authentication\_status* will revert back to None and the authentication cookie will be removed.

## How to implement user privileges

Given that the authenticator object returns the username of your logged-in user, you can utilize that to implement user privileges where each user receives a more personalized experience as shown below:

```
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'jsmith':
        st.write(f'Welcome *{name}*')
        st.title('Application 1')
    elif username == 'rbriggs':
        st.write(f'Welcome *{name}*')
        st.title('Application 2')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

![user-privileges](https://streamlit.ghost.io/content/images/2022/12/user-privileges.gif#browser)

As you can see, each user is redirected to a separate application to cater to that specific user’s needs.

## Wrapping up

I hope you feel confident now about securely authenticating users into your Streamlit application. In subsequent posts, you’ll learn how to register new users, reset usernames/passwords, and update user data.

In the meantime, feel free to read more about this component in our book [Web Application Development with Streamlit](https://www.amazon.com/Web-Application-Development-Streamlit-Applications/dp/1484281101?linkCode=sl1&tag=kho_abd_her-20&linkId=ee9e303b3445d601f8ab440ddc81a4fc&language=en_US&ref_=as_li_ss_tl&ref=streamlit.ghost.io). And if you have any questions, please leave them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/mkhorasani/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

---
title: "Streamlit-Authenticator, Part 2: Adding advanced features to your authentication component"
subtitle: "How to add advanced functionality to your Streamlit app\u2019s authentication component"
date: 2023-02-07
authors:
  - "Mohammad Khorasani"
category: "Advocate Posts"
---

![Streamlit-Authenticator, Part 2: Adding advanced features to your authentication component](https://streamlit.ghost.io/content/images/size/w2000/2023/01/streamlit-authenticator-part-2.svg)


🚀

Update: Streamlit now has built-in authentication via OIDC/OAuth2, which may be an alternative to the auth mechanism discussed here. Read more [in our docs](https://docs.streamlit.io/develop/concepts/connections/authentication?ref=streamlit.ghost.io).

This is Part 2 of the Streamlit Authenticator component two-part series. In [Part 1](https://streamlit.ghost.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/), we covered how to create an authentication component that allows users to log in and gain privileged access to pages within your app.

In this second part, we'll cover the following:

* How to create a password reset widget
* How to create a new user registration widget
* How to create a forgotten password widget
* How to create a forgotten username widget
* How to create an updated user details widget

TL;DR? Here's the [repo code](https://github.com/mkhorasani/Streamlit-Authenticator?ref=streamlit.ghost.io).

### How to create a password reset widget

If your user needs to reset their password to a new one, use the `reset_password` widget to allow the already logged-in user to change their password:

```
if authentication_status:
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
```

![reset_password.PNG-2](https://streamlit.ghost.io/content/images/2023/01/reset_password.PNG-2.png#border)

### How to create a new user registration widget

If you want to allow pre-authorized or even non-pre-authorized users to register, use the `register_user` widget to allow a user to register for your app. If you want the user to be pre-authorized, set the `preauthorization` argument to True and add their email to the `preauthorized` list in the configuration file. Once they have registered, their email will automatically be removed from the `preauthorized` list in the configuration file.

To let any user register, set the `preauthorization` argument to False:

```
try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)
```

![register_user.PNG](https://streamlit.ghost.io/content/images/2023/01/register_user.PNG.png#border)

### How to create a forgotten password widget

If you want to allow a user to reset a forgotten password, use the `forgot_password` widget to allow them to generate a new random password. This new password will be automatically hashed and stored in the configuration file. The widget will also return the user's username, email, and new random password (for you to securely send to the user):

```
try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success('New password sent securely')
        # Random password to be transferred to user securely
    elif username_forgot_pw == False:
        st.error('Username not found')
except Exception as e:
    st.error(e)
```

![forgot_password.PNG](https://streamlit.ghost.io/content/images/2023/01/forgot_password.PNG.png#border)

### How to create a forgotten username widget

You can also allow users to reset their username with the `forgot_username` widget, which lets them retrieve their forgotten username. The widget will also return the user's username and email (for you to securely send to them):

```
try:
    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    if username_forgot_username:
        st.success('Username sent securely')
        # Username to be transferred to user securely
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)
```

![forgot_username.PNG](https://streamlit.ghost.io/content/images/2023/01/forgot_username.PNG.png#border)

### How to create an updated user details widget

You can allow your users to update their name and/or email with the `update_user_details` widget. The widget will automatically save the updated details in both the configuration file and the reauthentication cookie:

```
if authentication_status:
    try:
        if authenticator.update_user_details(username, 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)
```

![update_user_details.PNG](https://streamlit.ghost.io/content/images/2023/01/update_user_details.PNG.png#border)

### Wrapping up

And that concludes our review of the Streamlit-Authenticator component! I hope you now feel confident about securely authenticating users to your Streamlit application with advanced functionalities.

In the meantime, feel free to read more about this component in our book [Web Application Development with Streamlit](https://www.amazon.com/Web-Application-Development-Streamlit-Applications/dp/1484281101?linkCode=sl1&tag=kho_abd_her-20&linkId=ee9e303b3445d601f8ab440ddc81a4fc&language=en_US&ref_=as_li_ss_tl&ref=streamlit.ghost.io). And if you have any questions, please leave them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/mkhorasani/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

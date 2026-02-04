---
title: "10 most common explanations on the Streamlit forum"
subtitle: "A guide for Streamlit beginners"
date: 2023-03-09
authors:
  - "Debbie Matthews"
category: "Advocate Posts"
---

![10 most common explanations on the Streamlit forum](https://streamlit.ghost.io/content/images/size/w2000/2023/03/Announcement-1-.svg)


## A guide for Streamlit beginners

Hey, community! 👋

My name is Debbie Matthews, and I’m a moderator on [Streamlit’s wonderful forum](http://discuss.streamlit.io/?ref=streamlit.ghost.io). You may have seen me around as [mathcatsand](https://discuss.streamlit.io/u/mathcatsand/summary?ref=streamlit.ghost.io), as in “math, cats, and….”

If you hang around the forum long enough, you’ll start seeing some common pain points and areas of confusion. I thought it’d be helpful for new users to know where many people trip as they get started with Streamlit.

In this post, I’ll talk about 10 of them:

1. Buttons aren’t stateful.
2. Streamlit doesn’t render like a terminal.
3. You can inject your own CSS and JavaScript.
4. The files in your directory aren’t accessible to your front end implicitly.
5. `file_uploader` doesn’t save a file to your directory.
6. Keys in the session state go away when their associated widget is not rendered.
7. Your local environment is not the same as your cloud environment.
8. Streamlit doesn’t do that natively, but…
9. This isn’t an issue with Streamlit.
10. Can you please provide more information?

💡

Code snippets for this post are hosted [in a live app here](https://common-things.streamlit.app/?ref=streamlit.ghost.io), so feel free to open another tab or window to follow along. And if you haven't read or watched a basic introduction about getting started with Streamlit, [check it out here](https://docs.streamlit.io/library/get-started?ref=streamlit.ghost.io).

## 1. Buttons aren’t stateful

**Buttons return True only on the page load right after their click and immediately go back to False.**

If you create an `if` statement to check the value of a button, the body of the `if` statement will execute once per click of the button. The right things to include here are short messages or processes you don’t want to rerun with other user activity.

```
import streamlit as st

if st.button('Submit'):
    st.write('Submitted!')

if st.button('Confirm'):
    st.write('Confirmed!')
```

If you nest buttons, the innermost portion of the code will never execute! As soon as you click on the second button, the page will reload with the first button being `False`.

```
import streamlit as st

if st.button('First Button'):
    st.write('The first button was clicked.')
    if st.button('Second Button'):
        # This will never execute!
        st.write('The second button was clicked')
```

If you need your button to behave more like a checkbox, you can create a key in the session state to save that information.

```
import streamlit as st

# Initialize the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1:False,2:False}

# Function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

# Button with callback function
st.button('First Button', on_click=clicked, args=[1])

# Conditional based on value in session state, not the output
if st.session_state.clicked[1]:
    st.write('The first button was clicked.')
    st.button('Second Button', on_click=clicked, args=[2])
    if st.session_state.clicked[2]:
        st.write('The second button was clicked')
```

💡

Check out [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras?ref=streamlit.ghost.io) which is a collection of many useful custom components from a variety of contributors. It includes a stateful button made by [Zachary Blackwood](https://github.com/blackary?ref=streamlit.ghost.io).

## 2. Streamlit doesn’t render like a terminal

**With every interaction on a page, Streamlit will reload the page. It’s not meant to wait for input and then proceed. It also won’t keep anything on the screen that isn’t explicitly re-rendered.**

Be careful with loops and conditionals! You don’t want a while loop waiting for a user to input something. Streamlit doesn’t pause and wait for input with a new widget; it just plows through with its default value. If you have a widget inside a loop, Streamlit will try to make a new, additional widget with each loop pass. If you need to wait for a user’s selection, place a conditional on the output to check if it has the default value.

```
import streamlit as st

name = st.text_input('Name:')
if name != '':
    st.write(f'Hi, {name}! Nice to meet you.')
```

If you need to confirm the user’s selection which may be the default, you can add a confirmation button. You can require confirmation for any selection or just as a way for the user to accept the default.

```
import streamlit as st

# Create a key in session state to record the user's choice, defaulting to None
if 'favorite_color' not in st.session_state:
    st.session_state.favorite_color = None

# Confirmation function to record the user's choice into the favorite_color key
def confirm_color():
    st.session_state.favorite_color = st.session_state.color_picker

name = st.text_input('Name:')
if name != '':
    st.write(f'Hi, {name}! Nice to meet you.')
    st.write(f'What\\'s your favorite color?')
    # Confirmation function will run if the user changes the widget
    color = st.color_picker('Color:', key='color_picker', on_change=confirm_color)
    if st.session_state.favorite_color is None:
        # Or, Confirmation function will run if user confirms the default
        st.button('Confirm Black', on_click=confirm_color)
    else:
        st.write(f'<span style="color:{color}">Oh, nice color choice!</span>', 
            unsafe_allow_html=True)
```

If you have many interactive steps to display, the nested `if` statements can get a bit out of control. You can instead create a staging value in the session state to control how much is displayed on the page. You can use inequality as in the example below to show all former stages. Alternatively, you can use equality or `elif` to show only the current stage.

```
import streamlit as st

# Create a key in session state to track the stage
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# Stage function to update the stage saved in session state
def set_stage(stage):
    st.session_state.stage = stage

st.write('Welcome! Click to begin.')
# Each button runs the Stage function, passing the stage number as an argument
st.button('Begin', on_click=set_stage, args=[1])

# Content for each stage within the body of an if statement
if st.session_state.stage > 0:
    st.write('This is stage 1. Do some things.') 
    st.button('Next', on_click=set_stage, args=[2])
if st.session_state.stage > 1:
    st.write('This is stage 2. Do some more things.')
    st.button('Finish', on_click=set_stage, args=[3])
if st.session_state.stage > 2:
    st.write('This is the end. Thank you!')
    st.button('Reset', on_click=set_stage, args=[0])
```

If you want a function that “adds data” with each click, you will need something in the session state that accumulates those additions. This is commonly done with `if 'key' not in st.session_state:` at the top of the script. This way, the “new” unmodified object is initialized only on the first load of the page. With each addition, the object doesn't get overwritten with its default value because the key already exists.

```
import streamlit as st
import pandas as pd

# Initialize some object in session state where you will you be storing edits
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({'A':[1,2,3],'B':[4,5,6],'C':[7,8,9]})

# Optional: Assign the stored value to a convenient variable for brevity in code
df = st.session_state.df

st.dataframe(df)

cols = st.columns(3)
cols[0].number_input('A',0,100,step=1, key='A')
cols[1].number_input('B',0,100,step=1, key='B')
cols[2].number_input('C',0,100,step=1, key='C')

def add_row():
    row = [st.session_state.A, st.session_state.B, st.session_state.C]
    next_row = len(st.session_state.df)
    # Make sure modifcation is performed on the object in session state
    st.session_state.df.loc[next_row] = row

st.button('Add Row', on_click=add_row)
```

## 3. You can inject your own CSS and JavaScript

**HTML and CSS can be added via `st.write` and `st.markdown` (with the correct optional keyword). JavaScript requires the more robust components submodule.**

Many different resources describe ways to modify the display of Streamlit. [Fanilo Andrianasolo](https://github.com/andfanilo?ref=streamlit.ghost.io), another Streamlit Creator, has a [short video](https://youtu.be/OVgPJEMDkak?ref=streamlit.ghost.io) explaining the basics. Here are a few examples.

Want to change the font color on your buttons, including hover and focus colors? Here's how:

```
import streamlit as st

st.button('Click me!')

css='''
<style>
    .stButton > button {
        color: red;
    }
    .stButton > button:hover {
        color: violet;
        border-color: violet;
    }
    .stButton > button:focus {
        color: purple !important;
        border-color: purple !important;
        box-shadow: purple 0 0 0 .2rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)
```

Note the use of `unsafe_allow_html=True` when using `st.markdown` or `st.write`. This optional keyword is needed to prevent Streamlit from escaping HTML tags. If you know your CSS selectors, you can get to any element. I often use a set of containers combined with `nth-of-type` selections to get to a specific instance of an element.

```
import streamlit as st

# Layout your containers at the beginning
section1 = st.container()
section2 = st.container()
section3 = st.container()
section4 = st.container()

# Write to the different containers for your display elements
section1.subheader('Section 1')
section1.button('Button 1')

section2.subheader('Section 2')
section2.button('Button 2')

section3.subheader('Section 3')
section3.button('Button 3')

section4.subheader('Section 4')
section4.button('Button 4')

css='''
<style>
    section.main > div > div > div > div:nth-of-type(3) .stButton > button {
        color: green;
    }
    section.main > div > div > div > div:nth-of-type(3) .stButton > button:hover {
        color: violet;
        border-color: violet;
    }
    section.main > div > div > div > div:nth-of-type(3) .stButton > button:focus {
        color: purple !important;
        border-color: purple !important;
        box-shadow: purple 0 0 0 .2rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)
```

Use the components submodule if you need to customize something that can’t be handled with pure CSS. When you insert a component, it will be contained in an iframe. Be aware that your JavaScript queries must reach outside that iframe to work as expected.

```
import streamlit as st

st.header('Screen Width Checker')
st.write('''<h3>The app container is <span id="root-width"></span> x 
<span id="root-height"></span> px.</h3>
''', unsafe_allow_html=True)

js = '''
<script>
    var container = window.parent.document.getElementById("root")

    var width = window.parent.document.getElementById("root-width")
    var height = window.parent.document.getElementById("root-height")

    function update_sizing(){
        width.textContent = container.getBoundingClientRect()['width']
        height.textContent = window.parent.innerHeight
    }
    update_sizing()

    window.parent.addEventListener('resize', function(event) {
        update_sizing()
    }, true);
    
</script>
'''

st.components.v1.html(js)
```

## 4. The files in your directory aren’t accessible to your front end implicitly

**Users can't directly select from files on your app’s server. You can’t access files like you would on a web host.**

Streamlit has a server-client structure. The files that a user can access are on their computer where they have a browser open. Streamlit will only give users access to the files you explicitly tell it to serve. If you have an image `my_image.png` saved in your working directory, that image **cannot** be accessed via `<app url>/my_image.png`.

When you use `st.image` in your app, Streamlit will create a copy of the data and make it accessible to the client's browser via a hashed file name. When using HTML or CSS in your app that contains a path to some file, you need to host that file somewhere. A file will not be accessible to the web just by being in your app directory.

In the case of HTML and CSS, you can open and read the contents of a file to inject its contents manually. The contents of your CSS file should not contain relative paths to other HTML, CSS, or image files, as these will not be accessible to the user’s client.

```
import streamlit as st

if 'css' not in st.session_state:
    with open('files/my_css.css', 'r') as file:
        css = file.read()
    st.session_state.css = css

css = '<style>' + st.session_state.css + '</style>'

st.button('Click me!')

st.markdown(css, unsafe_allow_html=True)
```

There is also a new, exciting feature in Streamlit 1.18.0: [static files](https://docs.streamlit.io/knowledge-base/using-streamlit/how-host-static-files?ref=streamlit.ghost.io)! If you want to make anything in your working directory web-accessible, you can use this, too. Let's say you have a background image that you want to specify in some CSS. If you turn on static hosting and put the background image in a folder named `static`, you can use it in your CSS. Be sure to read the linked documentation for clarification.

```
import streamlit as st

image = './app/static/cat_background.jpg'

css = f'''
<style>
    .stApp {{
        background-image: url({image});
    }}
    .stApp > header {{
        background-color: transparent;
    }}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
```

Your `config.toml` should contain:

```
[server]
enableStaticServing = true
```

Remember to reboot your app any time you change your environment or configuration! Read more about the configuration [here](https://docs.streamlit.io/knowledge-base/using-streamlit/path-streamlit-config-toml?ref=streamlit.ghost.io).

## 5. file\_uploader doesn't save a file to your directory

**The** `file_uploader` **widget returns a “file-like object,” the file's data. This object is not accessed via a name or path.**

You may be familiar with a typical use case of `file_uploader`:

```
import streamlit as st
import pandas as pd

file = st.file_uploader("Choose a file:", key="loader", type='csv')

if file != None:
    df = pd.read_csv(file)
    st.write(df)
```

Since it is very common to specify a data file to `read_csv` via its path, it is easy to forget that pandas accepts *either* a path or a buffer. In the above example, we are passing the latter. The variable file has no “path” associated with it. You can access the file’s name via the name property inherited from BytesIO, but this is just informational. You don't use the file's name to point to its data. There are many libraries and functions that will not accept a file-like object instead of a path. Be mindful of the function you are using and always read its documentation if in doubt.

Also note that the file-like object you get requires processing to be interpreted, even if it is a simple text file.

```
import streamlit as st
import io

file = st.file_uploader("Choose a file:", type=['css','py'])

if file != None:
    bytes_object = file.getvalue()
    string_object = bytes_object.decode("utf-8")

    st.code(string_object)
```

## 6. Keys in session state go away when their associated widget isn’t rendered

**When a key in the session state is associated with a widget, then the key will be removed from the session state when the widget is no longer rendered. This can happen if you navigate to a different page or conditionally render widgets on the same page.**

Here’s a brief description of a widget’s life cycle.

At the specific line where you call upon a widget for the first time, Streamlit will create a new front-end instance of that widget. If you have specified a key, Streamlit will check if that key already exists in the session state. If that key doesn't exist, Streamlit will create one, starting with whatever default value the widget has. However, if Streamlit sees a key already, it will attach the widget to it. In this case, the widget will take on that key’s value even if it is a new widget with a specified initial value.

Example: This slider will always have a value of 1 since the widget will always attach itself to the pre-existing key.

```
import streamlit as st

st.session_state.my_key = 1

st.slider('Test', 0, 10, key='my_key')
```

Although you can edit a widget’s state by assigning different values to its key in the session state, the session state is just an intermediary. The widget will have and retain state while continually rendered on screen, even if you remove its key from the session state.

For example, this widget is and will remain stateful:

```
import streamlit as st

st.session_state.clear()

st.slider('Test', 0, 10, key='my_key')
```

However, as soon as a widget isn’t rendered (even for a single page load), Streamlit will delete all its data, including any associated key in the session state:

```
import streamlit as st

switch = st.radio('Choice:', [1,2])

match switch:
    case 1:
        st.checkbox('1', key='1')
    case 2:
        st.checkbox('2', key='2')
```

1. In the above example, say that `1` is selected for the radio button. While that is the case, there will be a `'1'` in session state duplicating the widget’s state.
2. As soon as a user selects `2` for the radio button, the page will reload. As Streamlit reruns the page, it will still have the `'1'` key in the session state. It doesn't know that the key's associated widget will not be rendered.
3. However, as soon as Streamlit completes rendering the page, it will see that it has information for a widget that isn't rendered. At this point, Streamlit will delete the widget information, including any key in the session state that was tied to it.

This cleanup process has particular importance to conditionally rendered widgets. It is also important for widgets meant to carry over to other pages (often in the sidebar). There is a discussion about changing this behavior and potentially changing the structure on a deeper level. For now, know that when a key is assigned to a widget, the data in the session will get deleted if you navigate away from that instance of the widget.

Two ways around this:

1. Copy data into a new key in the session state to have a place in the session state that is free from unintentional deletion.
2. Recommit your data to the session state at the top of the page. By using `st.session_state.my_key = st.session_state.my_key` at the top of every page, you can artificially “keep it alive.” When navigating away from a widget with `key='my_key'`, this interrupts the cleanup process. This manual value assignment effectively detaches the key from the widget (until a widget is seen again with that key).

## 7. Your local environment is not the same as your cloud environment

**Make sure to specify/use the right environment for any deployment and be sure your file paths are OS-agnostic.**

When you deploy your app to some cloud service, a new Python environment within that cloud service will be used to run your app. It won't know about or use anything you happen to have in your local environment. You have to tell your cloud environment about all the Python packages it has to install and any additional non-Python components.

For Streamlit Cloud, the most common approach is to save a `requirements.txt` file at the top of your working directory. Each line in the `requirements.txt` file specifies a package for the cloud environment to `pip install`. You can also set specific versions of Python packages this way.

Example `requirements.txt` file:

```
streamlit==1.17.0
pandas
numpy
```

Some Python libraries require additional command line tools or software to be installed. Streamlit Cloud is a Debian-based Linux container. Extra software is installed with `apt-get` in a similar way to how `pip` installs Python packages. You need a `packages.txt` file in your working directory alongside your main Python file for your app. Each line in the `packages.txt` file specifies a binary for the cloud environment to `sudo apt-get install`.

Example `packages.txt` file:

```
ffmpeg
chromium
chromium-chromedriver
```

Since many people locally have a different environment than Linux, note that Linux is case-sensitive. The files specifying your environment must be named exactly as stated,  case included. Use forward slashes and not back slashes in your Python script when writing out file paths. Ensure all paths are given from the working directory, even for Python files in your pages folder for multipage apps.

There are other ways to specify your Python packages, as described in the [documentation](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/app-dependencies?ref=streamlit.ghost.io). For example, you can have an `environment.yml` file to use `conda` instead of using `requiremnts.txt` which uses `pip`. If you try to include both, Streamlit Cloud will only process the first one it comes across and ignore the second.

For deployment on Streamlit Cloud, here’s a related warning. If you write to a file in your script, that updated file will only live in the Debian container hosting your app. It will not save back to GitHub and will not survive a reboot of your app.

## 8. Streamlit doesn’t do that natively, but…

**Streamlit is constantly growing and improving, so keep your eye on the road map and note the most commonly used custom components.**

There are a few good places to keep your eyes open for what’s coming up to help you get a feel for where we are now. Keep an eye on the [Roadmap](https://roadmap.streamlit.app/?ref=streamlit.ghost.io) to know what’s just around the corner in development. [GitHub Issues](https://github.com/streamlit/streamlit/issues?ref=streamlit.ghost.io) is the official place for developers to keep track of feature requests. If you want Streamlit to do something new, check there first so you can up-vote any existing request or create a new one if no one has mentioned it yet. I like to [sort the list by the most upvotes](https://github.com/streamlit/streamlit/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc&ref=streamlit.ghost.io) to see what’s getting traction.

Check out the [Streamlit Component Community Tracker](https://discuss.streamlit.io/t/streamlit-components-community-tracker/4634?ref=streamlit.ghost.io) for extra features people have built. Here are a few notable packages:

* [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras?ref=streamlit.ghost.io): a collection of many different small components from many different contributors
* [st-pages](https://github.com/blackary/st_pages?ref=streamlit.ghost.io): settings to customize the layout of navigation in multi-page apps created by [Zachary Blackwood](https://github.com/blackary?ref=streamlit.ghost.io)
* [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc?ref=streamlit.ghost.io): tools for real-time video/audio streams created by [Yuichiro Tachibana](https://github.com/whitphx?ref=streamlit.ghost.io)

💡

If your application is hosted on a different computer (server) than a user’s computer (client), be careful about computer peripherals. Use Streamlit-compatible libraries. There are a lot of components to deal with audio/video input for this reason.

* [streamlit-folium](https://github.com/randyzwitch/streamlit-folium?ref=streamlit.ghost.io) by [Randy Zwitch](https://github.com/randyzwitch?ref=streamlit.ghost.io) brings Folium to Streamlit.
* [streamlit-aggrid](https://github.com/PablocFonseca/streamlit-aggrid?ref=streamlit.ghost.io) by [Pablo Fonseca](https://github.com/PablocFonseca?ref=streamlit.ghost.io) brings AG Grid to Streamlit.

💡

Note that Streamlit 1.18.0 introduced an [experimental editable data](https://streamlit.ghost.io/editable-dataframes-are-here/) frame as well.

## 9. This isn't an issue with Streamlit

**If the problematic lines of code don't include anything from the Streamlit library, think carefully. Ask yourself if you need help with Streamlit or with something else.**

Community members are very generous about helping out with non-Streamlit issues. However, it's best to direct your questions to the right venue. There are many useful forums on the internet with different areas of focus. You will get the best and fastest help by asking questions in a forum dedicated to your issue.

The only thing Streamlit does is provide a front end to your Python code. If you're having trouble creating a data frame from a CSV file in your working directory, you may have a pandas question rather than a Streamlit one. The most efficient path to an answer would be to seek a forum dedicated to pandas.

When you encounter difficulty with a line of code, check if any Streamlit component is involved. If not, I encourage you to try executing that bit of code without Streamlit. If appropriate, you can create and run a plain Python script or try it out in a Jupyter notebook. If something works fine in a Jupyter notebook but isn't behaving as you expect in Streamlit, that's a great question to bring to the Streamlit forum.

## 10. Can you please provide more information?

**If you invest the time to ask your question clearly and succinctly, you'll likely save as much or more time waiting for a response.**

The easier it is for community members to understand your problem, the faster you'll get a response. If you're having problems deploying, we'd like to see your GitHub repository. We want to understand how you configured your environment and check for typos. We'd like to see your terminal output from a fresh reboot to see any error messages. On the other hand, if the front end isn't displaying the way you want, we'd like to know the code you are using and a screenshot of what you are visually seeing. Explain how you expect it to look.

Screenshots of code are less helpful since we can't copy and paste those into a working snippet. Access to your complete GitHub repository can be beneficial and sometimes necessary. However, the smallest amount of code needed to reproduce the issue is always best. If we can copy-paste a snippet you provide and launch it to see your problem, that's perfect! Include your `import` statements as well as any files your script accesses. Provide simplified, dummy data for us to work with. Inline data is the easiest to work with, such as defining a simple data frame within your code snippet. If importing your data is part of the problem, we'd need an example data file to accompany your snippet.

If you spend the time creating a small, self-contained example of your problem, then the community can work on helping you. Otherwise, we spend a lot of time digging through your code, fabricating data, and making all sorts of guesses to fill in the gaps.

Please check out [this guide](https://discuss.streamlit.io/t/using-streamlit-how-to-post-a-question-in-the-streamlit-forum/30960?ref=streamlit.ghost.io) on how to post effectively on the forum. I would especially like to draw your attention to the idea of a [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example?ref=streamlit.ghost.io).

## Wrapping up

Thanks for reading! I hope you found some useful information that will save you time and trouble as you start with Streamlit. If you have any questions, please post them in the comments below or contact me on the [Streamlit Forum](https://discuss.streamlit.io/u/mathcatsand/summary?ref=streamlit.ghost.io). You can also find me on [GitHub](https://github.com/MathCatsAnd?ref=streamlit.ghost.io) and [LinkedIn](https://www.linkedin.com/in/mathcatsand/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

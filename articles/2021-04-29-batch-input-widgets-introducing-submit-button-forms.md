---
title: "Batch Input Widgets | Introducing Submit Button & Forms"
subtitle: "We're releasing a pair of new commands called st.form and st.form_submit_button!"
date: 2021-04-29
authors:
  - "Abhi Saini"
category: "Tutorials"
---

![Introducing Submit button and Forms 📃](https://streamlit.ghost.io/content/images/size/w2000/2022/09/image--8-.svg)


Have you ever tried to build an app around a complex Machine Learning model, and found that rerunning the model every time the user changed an input value led to a less than ideal user experience? If so, it's likely because the parameters being supplied to your model use input widgets like `st.text_input`, `st.number_input` or `st.slider` and any time you change a widget the entire app is re-run.

To help solve this we're introducing a pair of commands called `st.form` and `st.form_submit_button`. This lets you batch input widgets together and submit the widget values with the click of a button — triggering only a single rerun of the entire app!

Check out this [sample app](https://share.streamlit.io/streamlit/release-demos/0.81/0.81/streamlit_app.py?page=forms_demo&ref=streamlit.ghost.io) which shows the new commands in action, but make sure to keep reading if you want to learn more about how it works.

## Getting started

Forms are like any other Streamlit container and can be declared using the `with` statement:

```
# Using the "with" syntax
with st.form(key='my_form'):
	text_input = st.text_input(label='Enter some text')
	submit_button = st.form_submit_button(label='Submit')
```

Or, if you prefer, you can also use object notation:

```
# Declare a form and call methods directly on the returned object
form = st.form(key='my_form')
form.text_input(label='Enter some text')
submit_button = form.form_submit_button(label='Submit')
```

In your app, this creates a form with a submit button as follows:

![Screen_Shot_2021-04-26_at_5.05.10_PM--1-](https://streamlit.ghost.io/content/images/2021/08/Screen_Shot_2021-04-26_at_5.05.10_PM--1-.png#border)

### **What this does**

Outside of forms, any time a user interacts with a widget the app's script is rerun. What `st.form` does is make it so users can interact with the widgets as much as they want, *without causing a rerun!* Instead, to update the app, the user should click on the form's submit button.

![cropped-gif](https://streamlit.ghost.io/content/images/2021/08/cropped-gif.gif#browser)

## Form submit button

In the example above, notice that `st.form_submit_button` is in some ways similar to `st.button`, but differs in others:

### **Similarities**

Just like the regular `st.button`, the submit button for a form, `st.form_submit_button` returns a boolean to indicate whether the form was submitted or not. This allows for building additional logic upon submit button. For e.g.

```
form = st.form(key='my-form')
name = form.text_input('Enter your name')
submit = form.form_submit_button('Submit')

st.write('Press submit to have your name printed below')

if submit:
    st.write(f'hello {name}')
```

### **Differences**

* A **Form submit button** is a special button which ***batch submits*** the state of the widgets contained in the form.
* A form must have an associated `st.form_submit_button` otherwise Streamlit throws an error.

## Form Features

`st.form` can be placed anywhere in a Streamlit app, you can even put columns inside of forms, or forms inside of columns, and everything will work as expected!

### Forms inside columns

```
col1, col2 = st.beta_columns(2)

with col1:
    with st.form('Form1'):
        st.selectbox('Select flavor', ['Vanilla', 'Chocolate'], key=1)
        st.slider(label='Select intensity', min_value=0, max_value=100, key=4)
        submitted1 = st.form_submit_button('Submit 1')

with col2:
    with st.form('Form2'):
        st.selectbox('Select Topping', ['Almonds', 'Sprinkles'], key=2)
        st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
        submitted2 = st.form_submit_button('Submit 2')
```

Changing the contents of a form in the left column or submitting the left form does not impact the form on the right and vice versa.

![2-3-1](https://streamlit.ghost.io/content/images/2021/08/2-3-1.png#border)

## Columns inside forms

```
with st.form(key='columns_in_form'):
    cols = st.beta_columns(5)
    for i, col in enumerate(cols):
        col.selectbox(f'Make a Selection', ['click', 'or click'], key=i)
    submitted = st.form_submit_button('Submit')
```

![Screen_Shot_2021-04-26_at_5.06.52_PM--1-](https://streamlit.ghost.io/content/images/2021/08/Screen_Shot_2021-04-26_at_5.06.52_PM--1-.png#border)

Changing the contents of any one of the select boxes does not impact the other select boxes and a rerun is triggered upon clicking the submit button.

---

### Helpful errors and warnings

To help developers in certain situations where it detects an out-of-place or missing submit button, Streamlit will shows a warning or throws an exception in the following cases:

* If a `st.form_submit_button` is defined without a form scope, Streamlit will throw an exception and stop execution.
* If no submit button is defined, Streamlit will show a warning without interrupting the app flow.

![4-2](https://streamlit.ghost.io/content/images/2021/08/4-2.png#border)

## Limitations and other notes

* An  `st.form` cannot be embedded inside another `st.form`.
* Every form must have an associated `st.form_submit_button`.
* By definition, `st.button`s do not make much sense within a form. Forms are all about batching widget state together, but buttons are inherently stateless. So declaring an `st.button` inside a form will lead to an error.
* Also by definition, interdependent widgets within a form are unlikely to be particularly useful. If you pass the ***output*** of `widget1` into the ***input*** for `widget2` inside a form, then `widget2` will only update to `widget1`'s value when the form is submitted.
* We are currently working on functionality that allows you to programmatically reset all widgets when the submit button is clicked. This should be added in an upcoming release.

## Wrapping up

You can now add `st.form` and `st.form_submit_button` to your apps to help make them more responsive in just two lines of code!

So go ahead and upgrade Streamlit to version 0.81.0 today!

```
pip install --upgrade streamlit
```

We're excited to see how you'll use these new commands, so make sure to come share what you create on [our forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io) or on [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io). If you have any questions about these (or about Streamlit in general) let us know on the forum or in the comments below! 🎈

## Resources

* [Form docs](https://docs.streamlit.io/en/latest/advanced_concepts.html?highlight=form&ref=streamlit.ghost.io#batch-elements-and-input-widgets)
* [Github](https://github.com/streamlit/streamlit?ref=streamlit.ghost.io)
* [Forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io)

---
title: "Building robust Streamlit apps with type-checking"
subtitle: "How to make type-checking part of your app-building flow"
date: 2022-11-10
authors:
  - "Harald Husum"
category: "Advocate Posts"
---

![Building robust Streamlit apps with type-checking](https://streamlit.ghost.io/content/images/size/w2000/2022/11/type-checking-app-1.svg)


Hey, community! 👋

My name is Harald Husum. I’m a Machine Learning Engineer at [Intelecy](https://www.intelecy.com/?ref=streamlit.ghost.io) and a Streamlit Creator.

Have you ever come across an app that promises to solve your problem, only to have it crash as you try it out? Nothing ruins the experience like encountering defects. As app developers, we’re painfully aware of this. Defects are an ever-present concern, so having efficient routines for weeding them out is a must.

In this post, I’ll share a powerful technique for eliminating defects—*type-checking*—and how to make it a part of your app-building flow.

Let’s get started!

💡

If you want to get a feel for how type-checking works, take a look at my [app](https://typing-playground.streamlitapp.com/?ref=streamlit.ghost.io) which lets you type-check Streamlit code directly from your browser (without installing the required tooling). If you’re interested in the code, here’s a [repo](https://github.com/harahu/streamlit-typing-example?ref=streamlit.ghost.io) as well.

## The methods of detecting defects

For some classes of software defects, the only cure is meticulous testing.

When creating an app, writing and running tests should always be part of your toolbox. Not sure about how to test Streamlit apps? [These](https://blog.devgenius.io/testing-streamlit-a1f1fd48ce8f?ref=streamlit.ghost.io) [tutorials](https://streamlit.ghost.io/testing-streamlit-apps-using-seleniumbase/) can help you get started. But testing can be time-consuming, and covering various edge cases of a large code base isn’t always feasible. As software developers, we’re often time-constrained, so we want fast and efficient methods for detecting defects.

Luckily, testing isn’t the only technique that can surface problems in your code.

### Static analysis vs. dynamic analysis

When you want to uncover as many issues as possible with as little work as possible, static analysis tools are your friends.

Static analysis is the process of analyzing code *without* actually running it. Compare it to testing—or dynamic analysis—where to gain any insight into the code, you have to execute it. Of course, static analysis tools can’t discover all your problems, so you should still write tests. But you can catch a lot of issues without investing much effort.

Within the context of Python, [linting](https://en.wikipedia.org/wiki/Lint_(software)?ref=streamlit.ghost.io) is probably the most common form of static analysis. You might’ve come across linting tools like [Pylint](https://pylint.pycqa.org/en/latest/?ref=streamlit.ghost.io) and [Flake8](https://flake8.pycqa.org/en/latest/?ref=streamlit.ghost.io). They help detect potential quality issues in your code. Code formatters like [YAPF](https://github.com/google/yapf?ref=streamlit.ghost.io) and [Black](https://black.readthedocs.io/en/stable/?ref=streamlit.ghost.io) also rely on static analysis. However, automatic linting and formatting only scratch the surface of what static analysis can do for you, as you’ll see shortly. 😊

### Type-checking

In the last decade, Python has seen a [popularity boom](https://insights.stackoverflow.com/trends?tags=java%2Cc%2Cc%2B%2B%2Cpython%2Cc%23%2Cjavascript%2Cphp%2Cswift&ref=streamlit.ghost.io). As a result, Python increasingly sees use in large and complex projects, where demands for code quality are higher. This trend drives the development and adoption of static analysis techniques. Type-checking is one such technique that’s gaining traction in the Python community.

Type-checking ensures that interacting with objects doesn’t lead to obvious errors. For example, calling `x.lower()` will work if `x` is of type `str`. But if `x` is an `int`, you’ll trigger the following exception:

`AttributeError: 'int' object has no attribute 'lower’`

You might ask, “Who would try to call the lower method on an integer?” But variants of this problem happen all the time—by accident—when you write or refactor Python code. Embracing type-checking will let you avoid such errors.

Like other forms of static analysis, type-checking is usually performed by a tool—a type checker. There are many type checkers in the Python ecosystem. Of note are [PyType](https://google.github.io/pytype/?ref=streamlit.ghost.io), [Pyright](https://github.com/Microsoft/pyright?ref=streamlit.ghost.io), and [Pyre](https://pyre-check.org/?ref=streamlit.ghost.io). But the most popular is probably [mypy](http://mypy-lang.org/?ref=streamlit.ghost.io). It’s been around the longest and supports most of the latest typing features in Python. It’ll help you make your Streamlit projects less prone to failure.

### What does this have to do with Streamlit anyway?

Good question! Although type checkers can identify issues in your regular old Python code, they work best when your code is *annotated with type hints*. Type hints inform the type checker about the intention behind the code and allow the type checker to verify that the code functions as intended.

Over the last few months, the community has done [a lot of work](https://github.com/streamlit/streamlit/pulls?page=1&q=is%3Apr+is%3Aclosed+annotations&ref=streamlit.ghost.io) annotating Streamlit’s public APIs with type hints. Type checkers can now correctly understand what types are expected by Streamlit functions and what types are returned. Consequently, type checkers have gone from being *somewhat* useful to *really* useful for checking code that interacts with Streamlit, like your apps. (I expect the Streamlit code base annotations to improve with time).

If you're not already type-checking your Streamlit apps, now is a good time to start!

## How to make type-checking part of your app-building flow

To get a feel for type-checking without committing to anything, use my app to type-check Streamlit code snippets from a browser:

1. Go to [https://typing-playground.streamlitapp.com/](https://typing-playground.streamlitapp.com/?ref=streamlit.ghost.io)
2. Paste in a code snippet
3. Press “Type-check with mypy”
4. Observe how mypy feels about your code

The process should look something like this:

![typing-playground-1](https://streamlit.ghost.io/content/images/2022/11/typing-playground-1.gif#browser)

The app internals are fairly simple. The user input is passed on to mypy for type checking. The resulting type-checking report is somewhat prettified before being presented to the user (check out the [repo](https://github.com/harahu/streamlit-typing-example?ref=streamlit.ghost.io) for details).

Now, let’s make type-checking a part of your Streamlit app-building workflow.

### Step 1. Understanding type hints

Earlier, I mentioned that type hints are essential to get the most out of a type checker. Let’s have a closer look at Python-type hints and what they express (if you’re using Python < 3.10, some examples won't work because of the union operator for types (`|`) addition, unless you add `from __future__ import annotations` to the top of your file).

The first is a *variable* hint. It looks something like this:

```
n: float = 42.42
```

The variable n should always have a float value.

By adding `: float` after your variable name, you inform the type checker that you *intend* that `n` should always remain a float. Should you make a mistake and write something like `n = “I’m no float”` later in your code, mypy will inform you that you made a mistake:

`error: Incompatible types in assignment (expression has type "str", variable has type "float")`

In practice, you won't have to annotate `n` like this because mypy implicitly assumes that variables have the type of whatever value you assign them first. But knowing about variable hints will let you override mypy when this assumption doesn't hold.

For instance, imagine that we want to turn `n` into a constant and disallow changing it at all. We can achieve this by way of a special variable hint:

```
from typing import Final

N: Final = 42.42
```

N is annotated as a constant.

If we now try to change `N` in any way, it will lead to mypy complaining:

```
N = 42  # error: Cannot assign to final name "N"
```

Mypy stops us from overriding a constant.

Another form of type hints is the one used on functions.

```
def greet(name: str | None) -> str:
    if name is None:
        name = "mysterious stranger"
    return f"Happy Streamlit-ing, {name}! 🎈"
```

Here, `name: str | None` means that the function has a parameter, `name`, and that it’s expected to be passed an argument that’s either an instance of `str` or `None`. The function also has a return type annotation `-> str`, which implies that it’ll always return an instance of `str`.

Adding these hints to the function means that mypy will protect you against two potential mistakes:

```
# Trying to pass in a type the function isn't intended to support
# Mypy - error: Argument 1 to "greet" has incompatible type "int"; 
#   expected "Optional[str]"
greet(42)

# Misusing the returned greeting
# Mypy - error: "str" has no attribute "a_method_strings_dont_have"
greet("John Doe").a_method_strings_dont_have()
```

Let’s say you make the following change to the greet function:

```
def greet(name: str | None) -> str:
    if name is None:
        # No greetings for secretive people
        return None
    return f"Happy Streamlit-ing, {name}! 🎈"
```

Mypy will notice that you *say* you’re going to return a `str`. But in practice, you can also return a `None`. Mypy will warn you: `error: Incompatible return value type (got "None", expected "str")`.

This is helpful because it forces you to think carefully about your change. Either `greet` should always return a `str`, in which case you need to take a step back. Or, if you *intended* to create this new behavior, update the function hints to `def greet(name: str | None) -> str | None`. As a result, all usages of `greet` that don't gracefully handle the function returning `None` will need to be updated.

This might sound scary, but mypy will point out any locations in your code base where you might be using the return value from `greet` in a way that assumes it’s a `str`.

💡

There’s more to type hints. Take a look at [PEP484](https://peps.python.org/pep-0484/?ref=streamlit.ghost.io)—the main specification for type hints in Python.

### Step 2. Installing mypy

To type-check your Streamlit project, you need to install mypy. It should be easy, as it's just another Python dependency. Just use pip:

```
$ python3 -m pip install mypy
```

Or use [Poetry](https://python-poetry.org/?ref=streamlit.ghost.io) to manage your dependencies:

```
$ poetry add mypy --group dev
```

### Step 3. Running mypy

Mypy can analyze a single file:

```
$ mypy program.py
```

Or it can analyze all Python code in a directory:

```
$ mypy my_project
```

Try running it on your code and see if it reports any errors. If it doesn't, you're a better developer than me. 😉

### An example from the world of Streamlit

To move from theoretical to practical, I want to share a type of error I experienced in one of my Streamlit apps. It could've been avoided with the type hints added in the latest Streamlit version. I can't share the actual code, so I'll share an imagined example.

Here is a simple app to explore the pastry collections of a few local bakeries. It lets me select a bakery and one of its pastries to see the information about it:

```
"""This is the code for our bakery app"""
from dataclasses import dataclass

import streamlit as st

@dataclass
class Pastry:
    name: str
    description: str

@dataclass
class Baker:
    name: str
    pastries: list[Pastry]

bakers = [
    Baker(
        name="Eager Bakery",
        pastries=[
            Pastry(
                name="Cinnamon Bun",
                description="The best there is",
            ),
            Pastry(
                name="Magic Muffin",
                description="Putting sparkles back in your day.",
            ),
            Pastry(
                name="Dreamy Donut",
                description="Never drink your coffee without it.",
            ),
        ],
    ),
    Baker(
        name="Lazy Bakin'",
        pastries=[],
    ),
]

baker = st.sidebar.selectbox(
    label="Select a bakery:",
    options=bakers,
    format_func=lambda b: b.name,
)

pastry = st.sidebar.selectbox(
    label=f"Select one of {baker.name}'s pastries:",
    options=baker.pastries,
    format_func=lambda p: p.name,
)
st.write(pastry.name)
st.write(pastry.description)
```

Take a look at the code. Can you spot a subtle defect? As you interact with the app, it seems there are no problems:

![subtle-defect](https://streamlit.ghost.io/content/images/2022/11/subtle-defect.png#border)

But when you switch the bakeries, an error strikes:

![attribute-error](https://streamlit.ghost.io/content/images/2022/11/attribute-error.png#border)

Instead of information about a pastry, you get an `AttributeError`. How annoying!

When I encountered this error in my app, I was surprised to learn the cause. It turns out that `streamlit.selectbox` will return `None` if the options sequence you pass to it is empty. In this case, since *Lazy Bakin'* disappointingly hasn't developed any pastries yet, there are no options to select in the pastry `selectbox`. So instead of a pastry to render, you get `None`.

I found this through a runtime error—in *production,* no less. But with the latest version of Streamlit and the support of mypy, you won't have to. Running mypy yields four errors:

```
pastries.py:50: error: Item "None" of "Optional[Baker]" has no attribute "name"
pastries.py:51: error: Item "None" of "Optional[Baker]" has no attribute "pastries"
pastries.py:54: error: Item "None" of "Optional[Any]" has no attribute "name"
pastries.py:55: error: Item "None" of "Optional[Any]" has no attribute "description"
```

To summarize, mypy is alerting you to the fact that both your `baker` and `pastry` variables might be set to `None`. So if mypy is part of your project's CI/CD pipeline, you'll avoid releasing code like this to your users.

Here is how to adapt your code to avoid these errors:

```
baker = st.sidebar.selectbox(
    label="Select a bakery:",
    options=bakers,
    format_func=lambda b: b.name,
)

# Since we know that `bakers` is a non-empty list, the errors mypy points out 
# for `baker` are technically false positives. This is easy enough to deal with.
# By asserting that baker is not None, mypy is placated. And, in practice, the 
# assert should never fail.
assert baker is not None

pastry = st.sidebar.selectbox(
    label=f"Select one of {baker.name}'s pastries:",
    options=baker.pastries,
    format_func=lambda p: p.name,
)

# For the `pastry` case, we must show a bit more care. We now know that we can 
# actually get a None value here. What you want to do when that happens is up 
# to you. In my case, I just choose not to print anything. Moving the 
# `st.write` calls behind a conditional is all that is needed to make mypy happy.
if pastry is not None:
    st.write(pastry.name)
    st.write(pastry.description)
```

That's it!

## Wrapping up

You've now seen how type-checking can help you build more robust Streamlit apps! 🎉

Thank you for taking the time to read this article. I hope that it'll help you with your current and future Streamlit projects. Should you have any thoughts, comments, or questions about type annotations and type-checking, please post them in the comments below or connect with me on [Twitter](https://twitter.com/harahudev?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/harald-husum-27111a3b/?ref=streamlit.ghost.io), or [GitHub](https://github.com/harahu?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

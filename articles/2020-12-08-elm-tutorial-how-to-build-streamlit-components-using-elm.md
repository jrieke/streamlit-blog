---
title: "Elm Tutorial | How to Build Streamlit Components Using Elm"
subtitle: "A tutorial on how to build Streamlit components using Elm"
date: 2020-12-08
authors:
  - "Henrikh Kantuni"
category: "Tutorials"
---

![Elm, meet Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--30-.svg)


Let me start this article by saying—I love Elm!

I enjoy learning new programming languages, and Elm has been my favorite language for almost 2 years now. I like everything about it - compiler error messages, type system soundness, [The Elm Architecture](https://guide.elm-lang.org/architecture/?ref=streamlit.ghost.io), pure functions, immutability, performance, etc. Around the time I discovered Elm, I got a job at [Streamlit](https://www.streamlit.io/?ref=streamlit.ghost.io), and I immediately saw the potential for how Elm and Streamlit could work together to supercharge apps. With the release of the Streamlit components architecture earlier this year, this was finally possible, and I'm excited to show you how! To get a taste, check out this awesome Elm [line charts](https://terezka.github.io/line-charts/?ref=streamlit.ghost.io) library embedded into a Python [data app](https://share.streamlit.io/kantuni/streamlit-elm-chart/app.py?ref=streamlit.ghost.io).

Before we start, if you're new to Streamlit and would like to learn more about it - check out these two articles "[Intro to Streamlit](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace?sk=f7774c54571148b33cde3ba6c6310086&ref=streamlit.ghost.io)" and "[Intro to Streamlit components](https://streamlit.ghost.io/introducing-streamlit-components/)".

## Ready Player One

Here's the "[Hello World](https://guide.elm-lang.org/?ref=streamlit.ghost.io)" of Elm examples:

```
import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)

main =
  Browser.sandbox { init = 0, update = update, view = view }

type Msg = Increment | Decrement

update msg model =
  case msg of
    Increment ->
      model + 1

    Decrement ->
      model - 1

view model =
  div []
    [ button [ onClick Decrement ] [ text "-" ]
    , div [] [ text (String.fromInt model) ]
    , button [ onClick Increment ] [ text "+" ]
    ]
```

It is a simple counter app that demonstrates the simplicity, robustness, and beauty of The Elm Architecture.

We're going to build a Streamlit app that will use the above example as a Streamlit component. Streamlit components let you expand the functionality provided in the base Streamlit package. You can use Streamlit components to share any web-based UI, widget, or data visualization code with the broader Python data science community.

Creating a Streamlit component takes - literally - 2 lines of Python.

```
import streamlit as st
import streamlit.components.v1 as components

counter_component = components.declare_component(
    "counter",
    url="http://localhost:3000/",
)

count = counter_component(key="count", default=0)
st.markdown(f"The value of the counter is **{count}**.")
```

* We declare a new component by passing the name and the location of the component front-end files (or the URL of your development server).
* We provide the default value for the counter.
* We make sure that the component does not re-render unnecessarily by providing the `key`.

## Brave New World

To establish a two-way connection between our app and the component, we are going to add [ports](https://guide.elm-lang.org/interop/ports.html?ref=streamlit.ghost.io) to our Elm app.

To send a message from Elm to Streamlit, let's define a port that receives a number and produces a command.

```
port fromElm : Int -> Cmd msg
```

We will need to send the new value back to Streamlit on `Increment` and `Decrement` events. So let's modify our update function to reflect that.

```
Increment ->
    ( { model | count = model.count + 1 }
    , fromElm (model.count + 1)
    )

Decrement ->
    ( { model | count = model.count - 1 }
    , fromElm (model.count - 1)
    )
```

## **There and Back Again**

To send a message from Streamlit to Elm, let's define a port that receives a number and produces a subscription.

```
port fromJS : (Int -> msg) -> Sub msg
```

Firstly, we will define a new message type.

```
type Msg
    = Default Int
    | Increment
    | Decrement
```

Secondly, we will add a handler for that message type to update.

```
Default value ->
    ( { model | count = value }
    , Cmd.none
    )
```

And finally, we will subscribe to the messages on that port.

```
subscriptions : Model -> Sub Msg
subscriptions _ =
    fromJS Default
```

When a message from JavaScript is sent to that port, the `Default` event will get a number and set the counter value to that number.

And that's [it](https://share.streamlit.io/kantuni/streamlit-elm-counter/app.py?ref=streamlit.ghost.io)!

![Screen-Recording-2020-12-08-at-03.30.25-PM](https://streamlit.ghost.io/content/images/2021/08/Screen-Recording-2020-12-08-at-03.30.25-PM.gif#border)

## Foundation

I hope this tutorial will help you build dazzling components in Elm. I believe there are a lot of incredible Elm packages that would boost the look and feel of Python data apps. To give you an idea, [elm-visualization](https://package.elm-lang.org/packages/gampleman/elm-visualization/latest/?ref=streamlit.ghost.io) would make a fantastic Streamlit Component - and there are many, many more. I'm excited to see more people discover the awesomeness of Elm, and I look forward to seeing what you create!

P.S. [Both](https://share.streamlit.io/kantuni/streamlit-elm-chart/app.py?ref=streamlit.ghost.io) [apps](https://share.streamlit.io/kantuni/streamlit-elm-counter/app.py?ref=streamlit.ghost.io) are available on GitHub and have been deployed using [Streamlit sharing](https://www.streamlit.io/sharing-sign-up?ref=streamlit.ghost.io).

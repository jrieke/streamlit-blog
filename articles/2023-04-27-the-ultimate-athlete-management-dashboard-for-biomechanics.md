---
title: "The ultimate athlete management dashboard for biomechanics"
subtitle: "Learn how to measure jump impulse, max force, and asymmetry with Python and Streamlit"
date: 2023-04-27
authors:
  - "Hansen Lu"
category: "Advocate Posts"
---

![The ultimate athlete management dashboard for biomechanics](https://streamlit.ghost.io/content/images/size/w2000/2023/04/drop-jump-streamlit-app.svg)


Hey, community! 👋

My name is Hansen Lu, and I'm a data scientist specializing in biomechanics. Python and Streamlit help me analyze the body's performance and assess potential injury risks.

I built the Drop Jump app to measure an athlete's ability to adapt to the jump load, the force they generate to get off the ground, the asymmetry of their legs, and the impact of their landing. It captures and analyzes the raw motion and forceplate data so that I can share my insights with other practitioners!

In this post, you'll learn how to build it in six steps:

* Step 1. Importing the necessary Python modules
* Step 2. Establishing the initial UX layout
* Step 3. Reading and displaying the forceplate data
* Step 4: Finding the points of interest with while loops
* Step 5: Getting the net impulse, push-off impulse, and absorption impulse
* Step 6: Saving into a dataframe

👉

If you want to jump right in (no pun intended), here is the [app](https://dropjump.streamlit.app/?ref=streamlit.ghost.io), and here is the [repo code](https://github.com/hungryhansen/Drop-Jump?ref=streamlit.ghost.io).

Let's get right to it!

### **Step 1.** Importing the necessary Python modules

You'll need the following modules:

* Streamlit (to make a dashboard)
* Pandas (to import, store, and save data as dataframes)
* Scipy (to integrate)
* Plotly—graph objects (to create visualizations)

Just type in this code:

```
import numpy as np
import pandas as pd
import streamlit as st
import datetime
import plotly.graph_objects as go
from scipy import integrate
```

### **Step 2. Establishing the initial UX layout**

To build your dashboard, fill out the two required fields:

1. **Body Weight.** Enter it in lbs (it'll convert it to kgs) or in kgs.
2. **Input Zero Velocity Time**. Pair this with video footage synchronized with the force-time data in a lab environment.

Don't have synchronized footage? Use your smartphone's slow-motion feature to get zero velocity time. This will help you identify the touchdown time, zero velocity-time, and takeoff time. Simply get the time interval of the video and use it in your force-time graph.

The zero velocity time helps distinguish between concentric propulsion and eccentric deceleration of the jump, making for better analysis.

![step2.PNG](https://streamlit.ghost.io/content/images/2023/04/step2.PNG.png#browser)

```
st.title("Drop Jump")
name = st.text_input("Athlete Name")
col1, col2 = st.columns([1, 1])
bwkgs = col1.number_input("Body Weight in lbs")
bwkgs = bwkgs / 2.205
zeroVelocityTime = int(col2.number_input("Input Zero Velocity Time (ms)"))
leftdjfp1 = col1.file_uploader("Upload Left Forceplate", type=["txt"], key=88)
rightdjfp1 = col2.file_uploader("Upload Right Forceplate", type=["txt"], key=89)
graph = go.Figure()

if rightdjfp1 is None:
    st.warning("No Right Forceplate Data")
if leftdjfp1 is None:
    st.warning("No Left Forceplate Data")
if bwkgs == 0:
    st.warning("No Bodyweight")
```

Streamlit provides built-in tools such as columns, a file uploader, and number input.

You can separate your forceplate data by the left and right sides. Note that we shortened "Streamlit" to "st" when declaring our modules in the previous step. Fortunately, Streamlit has a [cheat sheet](https://docs.streamlit.io/library/cheatsheet?ref=streamlit.ghost.io) I always keep open to remind me how to program certain tools.

Prompt the user when the file uploader and body weight fields are empty. These three fields are essential for the analysis.

### **Step 3. Reading and displaying the forceplate data**

Depending on your data capture/acquisition platform, you want to export your force-time data in a .txt or .csv file so your app can read it. This is where Pandas become very useful:

```
if leftdjfp1 is not None:
    dfldj1 = pd.read_csv(leftdjfp1, header=(0), sep="\t")
    graph.add_trace(
        go.Scatter(x=dfldj1["Time"], y=dfldj1["Fz"], line=dict(color="red"))
    )
```

If your leftdjfp1 (left drop jump force plate 1) is not empty, read the file with the 0th row as your header. The file is separated by tabs. Your force-time file may have different header names and be separated by spaces, commas, or something else.

![Dropjumptextfile.PNG-1](https://streamlit.ghost.io/content/images/2023/04/Dropjumptextfile.PNG-1.png#browser)

To display the force-time data you just uploaded as a graph, use the Plotly module. Define your x values as your time, calling your force-time data (defined as dfldj1) and values under the header "Time" as your x value.

Similarly, define your y values as your vertical force values using your header "Fz".

Finally, define the color of your left line to red and the right line to green. If data from both force plates are inputted, it will display your force-time graph.

```
if leftdjfp1 is not None:
    dfldj1 = pd.read_csv(leftdjfp1, header=(0), sep="\t")
    graph.add_trace(
        go.Scatter(x=dfldj1["Time"], y=dfldj1["Fz"], line=dict(color="red"))
    )
if rightdjfp1 is not None:
    dfrdj1 = pd.read_csv(rightdjfp1, header=(0), sep="\t")
    graph.add_trace(
        go.Scatter(x=dfrdj1["Time"], y=dfrdj1["Fz"], line=dict(color="green"))
    )
```

![step3.PNG](https://streamlit.ghost.io/content/images/2023/04/step3.PNG.png#browser)

### ******************************Step 4. Finding the points of interest with while loops******************************

To calculate the net impulse of a jump, you must determine the starting and ending points of each jump.

Before the touchdown of the jump, the vertical force 'Fz' has a value of zero. Use while loops to find the right and left leg's touchdown point. This while loop continues stepping until the condition of 'Fz' falls below 10N of force, at which point you can store that value as the touchdown point. You can continue stepping through until the value is above 10N when the athlete is on the forceplate until they jump off.

Finally, you can store the takeoff point of their right and left legs:

```
if rightdjfp1 is not None and leftdjfp1 is not None:
    tab1, tab2, tab3 = st.tabs(["Force-Time Graph", "Impulse Chart", "Metrics"])
    with tab1:
        st.plotly_chart(graph)
    i = 0
    while dfldj1["Fz"][i] < 10:
        i += 1
    j = 0
    while dfrdj1["Fz"][j] < 10:
        j += 1
    lefttouchdown = i
    righttouchdown = j

    while dfldj1["Fz"][i] > 10:
        i += 1
    while dfrdj1["Fz"][j] > 10:
        j += 1
    lefttakeoff = i
    righttakeoff = j
```

### ****************************************************************Step 5. Getting the net impulse, push-off impulse, and absorption impulse****************************************************************

The net impulse is the total impulse minus the body weight impulse. Assuming that the athlete equally distributes their weight through both legs, you can subtract half of their body weight in Newtons from one side's total 'Fz'.

To determine the push-impulse and absorption impulse, you need to know the exact time of zero velocity. If this information is available, it can help identify areas of weakness or asymmetry in the athlete.

For example, many athletes recovering from an ACL injury may have poor force absorption but strong force generation. This can increase the risk of re-injury, especially in an in-game scenario, as they may accelerate beyond their capacity to slow down.

```
data = np.array([[name, bwkgs, zeroVelocityTime, netImpulseL, netImpulseR]])

df = pd.DataFrame(
   	data,
    columns=[
        "Name",
        "Weight-kg",
        "Zero Velocity Time",
        "Net Impulse-L",
        "Net Impulse-R",
     ],
)

with tab3:
        st.dataframe(df)if bwkgs != 0:
        netImpulseRInterval = dfrdj1["Fz"][righttouchdown:righttakeoff] - (
            bwkgs * 9.81 / 2
        )
        netImpulseTimeR = dfrdj1["Time"][righttouchdown:righttakeoff]
        netImpulseLInterval = dfldj1["Fz"][lefttouchdown:lefttakeoff] - (
            bwkgs * 9.81 / 2
        )
        netImpulseTimeLInterval = dfldj1["Time"][lefttouchdown:lefttakeoff]

        netImpulseR = integrate.simps(netImpulseRInterval, netImpulseTimeR)
        netImpulseL = integrate.simps(netImpulseLInterval, netImpulseTimeLInterval)
        if zeroVelocityTime != 0:
            concentricImpulseRInterval = dfrdj1["Fz"][zeroVelocityTime:righttakeoff]
            concentricImpulseTimeR = dfrdj1["Time"][zeroVelocityTime:righttakeoff]
            concentricImpulseLInterval = dfldj1["Fz"][zeroVelocityTime:lefttakeoff]
            concentricImpulseTimeLInterval = dfldj1["Time"][
                zeroVelocityTime:lefttakeoff
            ]

            concentricImpulseR = integrate.simps(
                concentricImpulseRInterval, concentricImpulseTimeR
            )
            concentricImpulseL = integrate.simps(
                concentricImpulseLInterval, concentricImpulseTimeLInterval
            )

            eccentricImpulseRInterval = dfrdj1["Fz"][righttouchdown:zeroVelocityTime]
            eccentricImpulseTimeR = dfrdj1["Time"][righttouchdown:zeroVelocityTime]
            eccentricImpulseLInterval = dfldj1["Fz"][lefttouchdown:zeroVelocityTime]
            eccentricImpulseTimeLInterval = dfldj1["Time"][
                lefttouchdown:zeroVelocityTime
            ]

            eccentricImpulseR = integrate.simps(
                eccentricImpulseRInterval, eccentricImpulseTimeR
            )
            eccentricImpulseL = integrate.simps(
                eccentricImpulseLInterval, eccentricImpulseTimeLInterval
            )
    impulsestyle = ["Net Impulse", "Absorption Impulse", "Push-off Impulse"]
    yLeft = [netImpulseL, eccentricImpulseL, concentricImpulseL]
    yRight = [netImpulseR, eccentricImpulseR, concentricImpulseR]
    totaly = np.array(yLeft) + np.array(yRight)
    leftPercentage = np.round(yLeft / totaly * 100, decimals=1)
    rightPercentage = np.round(yRight / totaly * 100, decimals=1)

    chart = go.Figure(
        data=[
            go.Bar(name="Left", x=impulsestyle, y=yLeft, text=(leftPercentage)),
            go.Bar(name="Right", x=impulsestyle, y=yRight, text=(rightPercentage)),
        ]
    )

    # Change the bar mode
    chart.update_layout(barmode="group")
    with tab2:
        st.plotly_chart(chart)
```

### **Step 6. Saving into a dataframe**

Formatting all the data into a dataframe is convenient for easy exporting and manipulation. You can display the dataframe and view all its values using "st.dataframe()". Additionally, you can save the dataframe as a .csv or a .txt file:

```
	data = np.array([[name, bwkgs, zeroVelocityTime, netImpulseL, netImpulseR]])

    df = pd.DataFrame(
        data,
        columns=[
            "Name",
            "Weight-kg",
            "Zero Velocity Time",
            "Net Impulse-L",
            "Net Impulse-R",
        ],
    )

    with tab3:
        st.dataframe(df)
```

### **Wrapping up**

If you're a sports scientist or aspiring biomechanist, I hope this tutorial can help you with drop-jump analysis. Coding might seem intimidating if you're new, especially without a computer science background. However, it can open limitless possibilities to help you and your athletes!

If you have any questions, please post them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/luhansen96/?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

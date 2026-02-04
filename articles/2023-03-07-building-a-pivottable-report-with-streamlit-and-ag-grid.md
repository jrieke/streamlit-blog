---
title: "Building a PivotTable report with Streamlit and AG Grid"
subtitle: "How to build a PivotTable app in 4 simple steps"
date: 2023-03-07
authors:
  - "Pablo Fonseca"
category: "Advocate Posts"
---

![Building a PivotTable report with Streamlit and AG Grid](https://streamlit.ghost.io/content/images/size/w2000/2023/03/pivottable-report.svg)


Hey, community! 👋

My name is Pablo, and I'm the creator of the Streamlit AgGrid component. A little about me: I started coding 25 years ago and never stopped. Currently, I work as a portfolio manager for renewable energy development in Brazil.

I needed to summarize the data for the available wind-farm energy in a PivotTable report: power sales, purchases, and expected generation. If the sold amount were more than the expected generation, it’d signal the need to buy power from other producers. So I built a simple dashboard with Streamlit and `streamlit-aggrid`!

In this post, I’ll show you:

1. How to load and display data
2. How to configure the grid using gridOptionsBuilder
3. How to configure the grid pivot mode
4. How to add grouping on rows and columns

Want to skip reading and try it out? Here's a [sample app](https://aggridpivottable.streamlit.app/?ref=streamlit.ghost.io) and a [repo code](https://github.com/PablocFonseca/streamlit-aggrid?ref=streamlit.ghost.io).

But first, let’s talk about…

### Some context on data

In Brazil, consumers buy power in advance and sign contracts for future power delivery (PPA—Power Purchase Agreement). The energy portfolio managers need to calculate the energy balance to mitigate the risk and protect the revenue. Is it too short or too long?

Much like a bank statement, the energy balance is a total of transactions. Sales can deplete it, while purchases can add to it.

Here is a sample of fictional balance data for seven wind farms (located across five Brazilian states) that have signed PPAs with customers for their 2023 power supply:

|
|  |
| state | powerPlant | recordType | buyer | referenceDate | hoursInMonth | volumeMWh |
| --- | --- | --- | --- | --- | --- | --- |
| CE | Ocean Breeze Energy Park | Power Sale | ChargeMax Limited Liability | 2023-06-01 | 720 | -158.221 |
| Bahia | Skyline Wind Ranch | Power Sale | PowerPulse Energy Inc. | 2023-08-01 | 744 | -108.894 |
| CE | Ocean Breeze Energy Park | Power Sale | PowerPlus Enterprises | 2023-03-01 | 744 | -371.49 |
| CE | Windfarm at Sunrise | Power Sale | SparkPlug Energy Ltd. | 2023-02-01 | 672 | -172.012 |
| CE | Windward Heights Wind Farm | Power Sale | SparkPlug Energy Ltd. | 2023-07-01 | 744 | -271.877 |
| CE | Windfarm at Sunrise | Power Sale | ShockPower Ltd. | 2023-04-01 | 720 | -366.159 |
| CE | Prairie Wind Power Plant | Power Sale | PowerPulse Energy Inc. | 2023-09-01 | 720 | -76.8527 |
| CE | Prairie Wind Power Plant | Power Sale | EnergyEmpire Corp. | 2023-05-01 | 744 | -926.426 |
| CE | Prairie Wind Power Plant | Expected Generation |  | 2023-08-01 | 744 | 9448.8 |
| SP | Coastal Wind Energy Station | Power Sale | VoltWatt Inc. | 2023-03-01 | 744 | -477.762 |

### Step 1. How to load and display data

Loading data is straightforward. Just use pandas `read_csv` to load it from a text file (or any other preferred method). To render it, use `streamlit-aggrid` with the default parameters. Create a file named [app.py](http://app.py/?ref=streamlit.ghost.io) in the same folder where you downloaded the data and add this code:

```
#app.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

@st.cache_data()
def load_data():
    data = pd.read_csv('./data.csv', parse_dates=['referenceDate'])
    return data

data = load_data()

AgGrid(data, height=400)
```

Launch your dashboard with `streamlit run app.py`. Your browser should open with the sample data loaded in AgGrid. The app will load data and display it using default configurations. They're nice but could be better formatted. Let’s use `GridOptionsBuilder` to customize it.

### **Step 2.** How to configure the grid using gridOptionsBuilder

Update your `app.py` file as follows:

```
#app.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder  #add import for GridOptionsBuilder

@st.cache_data()
def load_data():
    data = pd.read_csv("./data.csv", parse_dates=["referenceDate"])
    return data

data = load_data()

gb = GridOptionsBuilder()

# makes columns resizable, sortable and filterable by default
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

#configures state column to have a 80px initial width
gb.configure_column(field="state", header_name="State", width=80)

#configures Power Plant column to have a tooltip and adjust to fill the grid container
gb.configure_column(
    field="powerPlant",
    header_name="Power Plant",
    flex=1,
    tooltipField="powerPlant",
)

gb.configure_column(field="recordType", header_name="Record Type", width=110)

gb.configure_column(
    field="buyer", header_name="Buyer", width=150, tooltipField="buyer"
)

#applies a value formatter to Reference Date Column to display as a short date format.
gb.configure_column(
    field="referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
)

#Numeric Columns are right aligned
gb.configure_column(
    field="hoursInMonth",
    header_name="Hours in Month",
    width=50,
    type=["numericColumn"],
)
#The last column is the value column and will be formatted using javascript number.toLocaleString()
gb.configure_column(
    field="volumeMWh",
    header_name="Volume [MWh]",
    width=100,
    type=["numericColumn"],
    valueFormatter="value.toLocaleString()",
)

#makes tooltip appear instantly
gb.configure_grid_options(tooltipShowDelay=0)
go = gb.build()

AgGrid(data, gridOptions=go, height=400)
```

The grid should look better now!

### **Step 3. How to configure the grid pivot mode**

Now let’s make the grid pivot over the referenceDate column. Add a checkbox to your app:

```
shouldDisplayPivoted = st.checkbox("Pivot data on Reference Date")
```

Change the referenceDate column definition to enable pivoting:

```
gb.configure_column(
    field="referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=True # this tells the grid we'll be pivoting on reference date
)
```

Configure the aggregation function on the volumeMWh (the value) column (values should sum up for a given month):

```
gb.configure_column(
    field="volumeMWh",
    header_name="Volume [MWh]",
    width=100,
    type=["numericColumn"],
    valueFormatter="value.toLocaleString()",
    aggFunc="sum" # this tells the grid we'll be summing values on the same reference date
)
```

Finally, enable pivotMode when the checkbox is on:

```
gb.configure_grid_options(
    pivotMode=shouldDisplayPivoted # Enables pivot mode
    )
```

**Here is the complete code for this section:**

```
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data()
def load_data():
    data = pd.read_csv("./data.csv", parse_dates=["referenceDate"])
    return data

data = load_data()

shouldDisplayPivoted = st.checkbox("Pivot data on Reference Date")

gb = GridOptionsBuilder()

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)
gb.configure_column(field="state", header_name="State", width=80)

gb.configure_column(
    field="powerPlant",
    header_name="Power Plant",
    flex=1,
    tooltipField="powerPlant",
)
gb.configure_column(field="recordType", header_name="Record Type", width=110)

gb.configure_column(
    field="buyer", header_name="Buyer", width=150, tooltipField="buyer"
)

gb.configure_column(
    field="referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=True,
)
gb.configure_column(
    field="hoursInMonth",
    header_name="Hours in Month",
    width=50,
    type=["numericColumn"],
)
gb.configure_column(
    field="volumeMWh",
    header_name="Volume [MWh]",
    width=100,
    type=["numericColumn"],
    aggFunc="sum",
    valueFormatter="value.toLocaleString()",
)

gb.configure_grid_options(
    tooltipShowDelay=0,
    pivotMode=shouldDisplayPivoted,
)
go = gb.build()

AgGrid(data, gridOptions=go, height=400)
```

### **Step 4. How to add grouping on rows and columns**

So far, your app displays the loaded data and pivot in a single line. Let’s group it into columns using **virtual columns** (so they’re hidden when `pivotMode` it is off). Set the valueGetter property on the columns definition. In this example, Year and Year-Month columns don't exist in the original data. Create them by setting the `valueGetter` with a JavaScript expression for the grid:

```
gb.configure_column(
    field="referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=False, #remove pivoting on this column
)

#add two hidden virtual columns
gb.configure_column(
    field="virtualYear",
    header_name="Reference Date Year",
    valueGetter="new Date(data.referenceDate).getFullYear()",
    pivot=True, #allows grid to pivot on this column
    hide=True #hides it when pivotMode is off.
)

gb.configure_column(
    field="virtualMonth",
    header_name="Reference Date Month",
    valueGetter="new Date(data.referenceDate).toLocaleDateString('en-US',options={year:'numeric', month:'2-digit'})",
    pivot=True,
    hide=True
)
```

Use State, Power Plant, Record Type, and Buyer columns for row grouping. This will create a nice hierarchical menu. The Grid aggregates data by applying `aggFunc` on collapsed rows and column values. To configure this behavior, set rowGroup property on each column definition:

```
gb.configure_column(
    field="powerPlant",
    header_name="Power Plant",
    flex=1,
    tooltipField="powerPlant",
    rowGroup=True if shouldDisplayPivoted else False, # enable row grouping IF pivot mode is on. Could be shortened as rowgroup=shouldDisplayPivoted
)
```

Repeat this for the other grouping columns.

To configure the column that displays group hierarchy, set the following grid options:

```
gb.configure_grid_options(
    autoGroupColumnDef=dict(
        minWidth=300, 
        pinned="left", 
        cellRendererParams=dict(suppressCount=True)
    )
)
```

**Here is the complete code for this app:**

```
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data()
def load_data():
    data = pd.read_csv("./data.csv", parse_dates=["referenceDate"])
    return data

data = load_data()

shouldDisplayPivoted = st.checkbox("Pivot data on Reference Date")

gb = GridOptionsBuilder()

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)
gb.configure_column(
    field="state", header_name="State", width=80, rowGroup=shouldDisplayPivoted
)

gb.configure_column(
    field="powerPlant",
    header_name="Power Plant",
    flex=1,
    tooltipField="powerPlant",
    rowGroup=True if shouldDisplayPivoted else False,
)
gb.configure_column(
    field="recordType",
    header_name="Record Type",
    width=110,
    rowGroup=shouldDisplayPivoted,
)

gb.configure_column(
    field="buyer",
    header_name="Buyer",
    width=150,
    tooltipField="buyer",
    rowGroup=shouldDisplayPivoted,
)

gb.configure_column(
    field="referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=False,
)

gb.configure_column(
    field="virtualYear",
    header_name="Reference Date Year",
    valueGetter="new Date(data.referenceDate).getFullYear()",
    pivot=True,
    hide=True,
)

gb.configure_column(
    field="virtualMonth",
    header_name="Reference Date Month",
    valueGetter="new Date(data.referenceDate).toLocaleDateString('en-US',options={year:'numeric', month:'2-digit'})",
    pivot=True,
    hide=True,
)

gb.configure_column(
    field="hoursInMonth",
    header_name="Hours in Month",
    width=50,
    type=["numericColumn"],
)
gb.configure_column(
    field="volumeMWh",
    header_name="Volume [MWh]",
    width=100,
    type=["numericColumn"],
    aggFunc="sum",
    valueFormatter="value.toLocaleString()",
)

gb.configure_grid_options(
    tooltipShowDelay=0,
    pivotMode=shouldDisplayPivoted,
)

gb.configure_grid_options(
    autoGroupColumnDef=dict(
        minWidth=300, 
        pinned="left", 
        cellRendererParams=dict(suppressCount=True)
    )
)
go = gb.build()

AgGrid(data, gridOptions=go, height=400)
```

### **Wrapping up**

And that’s it! You now know how to use `streamlit-aggrid` to create a nice PivotTable report. If you have any questions, please post them in the comments below or contact me on [GitHub](https://github.com/PablocFonseca/streamlit-aggrid?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

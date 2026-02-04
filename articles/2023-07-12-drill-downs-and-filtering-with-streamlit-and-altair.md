---
title: "Drill-downs and filtering with Streamlit and\u00a0Altair"
subtitle: "Display an Altair chart definition in Streamlit using the st.altair_chart widget"
date: 2023-07-12
authors:
  - "Carlos D Serrano"
category: "Advocate Posts"
---

![Drill-downs and filtering with Streamlit and Altair](https://streamlit.ghost.io/content/images/size/w2000/2023/07/streamlit-altair.svg)


For the last few months, I've written several apps using Streamlit, and one of my favorite libraries for optimizing the look and feel of my app is Altair. You can display an Altair chart definition in Streamlit using the `st.altair_chart` widget. Altair is a powerful library full of styling, configurations, and interactions.

In this post, I'll show you how to create interactive and dynamic visualizations using Altair in Streamlit.

🍩

To jump right in, check out the [demo app](https://st-altair-drilldowns.streamlit.app/?ref=streamlit.ghost.io) and the [code](https://github.com/sqlinsights/streamlit-altair-drilldowns/blob/main/streamlit_app.py?ref=streamlit.ghost.io).

## Avoiding re-runs

One significant advantage of creating drill-downs and filters with Altair on Streamlit is that these interactions occur at the front-end level and don't require a re-run of your Streamlit app.

## Let's create some data first

I used a simple approach for this example and created a Pandas DataFrame with sales data. I also used the `st.cache_data` decorator to save the DataFrame in the cache:

```
@st.cache_data
def get_data():
    dates = pd.date_range(start="1/1/2022", end="12/31/2022")
    data = pd.DataFrame()
    sellers = {
        "LATAM": ["S01", "S02", "S03"],
        "EMEA": ["S10", "S11", "S12", "S13"],
        "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
        "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
    }
    rows = 25000
    data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
    data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
    data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
    data["seller"] = data.apply(
        lambda x: np.random.choice(sellers.get(x["region"])), axis=1
    )
    return data.sort_values(by="transaction_date").reset_index(drop=True)
```

## Color consistency

When creating drill-downs, it's crucial to maintain color consistency to enhance the clarity of your charts. Altair scales can be used to specify color domains and ranges that persist during drill-down.

Use the following three list variables in the Altair chart definitions:

```
regions = ["LATAM", "EMEA", "NA", "APAC"]
colors = ["#aa423a","#f6b404", "#327a88","#303e55","#c7ab84","#b1dbaa",
    "#feeea5","#3e9a14","#6e4e92","#c98149", "#d1b844","#8db6d8"]
months = [
    "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",
]
```

## Selections

To define a selection in Altair, you can use the single, interval, or point methods.

In this example, a single selection is used to drill down based on region. The "empty" attribute can be specified to determine whether all objects or no objects are visible when no selection has been made.

```
region_select = alt.selection_single(fields=["region"], empty="all")
```

## Filtering chart

This chart definition includes an Altair `add_selection` method for filtering other chart definitions that will be created later.

To create a dynamic experience, the opacity attribute is used to reduce the opacity of unselected objects to 25%. Note that the color method uses the scale attribute to limit the available colors to the domain and range variables defined previously:

```
region_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Sum of Transactions",
            ),
            color=alt.Color(
                field="region",
                type="nominal",
                scale=alt.Scale(domain=regions, range=colors),
                title="Region",
            ),
            opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
        )
    )
    .add_selection(region_select)
    .properties(title="Region Sales")
)
```

## Filtered and faceted charts

To enable filtering, implement the Altair `transform_filter` method. Faceting is enabled by using the facet method inside the encoding method, which uses a field attribute and a column attribute to break down the chart into multiple related charts.

If you need to facet by two different fields, use the `repeat()` method:

```
region_summary = (
    (
        alt.Chart(sales_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "month(transaction_date)",
                type="temporal",
            ),
            y=alt.Y(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Sales",
            ),
            color=alt.Color(
                "region",
                type="nominal",
                title="Regions",
                scale=alt.Scale(domain=regions, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=4,
                ),
            ),
        )
    )
    .transform_filter(region_select)
    .properties(width=700, title="Monthly Sales")
)

sellers_monthly_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=10)
        .encode(
            theta=alt.Theta(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Transactions",
            ),
            color=alt.Color(
                "month(transaction_date)",
                type="temporal",
                title="Month",
                scale=alt.Scale(domain=months, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=12,
                ),
            ),
            facet=alt.Facet(
                field="seller",
                type="nominal",
                columns=8,
                title="Sellers",
            ),
            tooltip=alt.Tooltip(["sum(transaction_amount)", "month(transaction_date)"]),
        )
    )
    .transform_filter(region_select)
    .properties(width=150, height=150, title="Sellers transactions per month")
)
```

### All of it in just one widget

To enable selections and filters, enclose them within a single Streamlit widget. To arrange charts, use the following methods:

* VConcat and HConcat methods to concatenate charts
* Pipe symbol "|" to place charts next to each other
* Ampersand symbol "&" to set charts below or above each other
* Plus sign “+” to overlay charts

To make a dashboard-like arrangement, create a variable called `top_row` and use the pipe symbol to arrange your `region_pie` and `region_summary` charts side by side. Then, using the ampersand, place `top_row` and `sellers_monthly_pie` below it. This creates a variable containing all the concatenated charts in a single Streamlit `altair_chart` widget.

Note that when using concatenated charts, the `use_container_width` attribute won't work. Therefore, you must specify the width of the charts in their properties:

```
#Create first row by concatenating horizontally
top_row = region_pie | region_summary
#Create dashboard by concatenating top_row with faceted chart
full_chart = top_row & sellers_monthly_pie

#Single Streamlit Object
st.altair_chart(full_chart)
```

### Dashboard

### Full code

```
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
regions = ["LATAM", "EMEA", "NA", "APAC"]
colors = [
    "#aa423a",
    "#f6b404",
    "#327a88",
    "#303e55",
    "#c7ab84",
    "#b1dbaa",
    "#feeea5",
    "#3e9a14",
    "#6e4e92",
    "#c98149",
    "#d1b844",
    "#8db6d8",
]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
st.title("2022 Sales Dashboard")

@st.cache_data
def get_data():
    dates = pd.date_range(start="1/1/2022", end="12/31/2022")
    data = pd.DataFrame()
    sellers = {
        "LATAM": ["S01", "S02", "S03"],
        "EMEA": ["S10", "S11", "S12", "S13"],
        "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
        "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
    }
    rows = 25000
    data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
    data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
    data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
    data["seller"] = data.apply(
        lambda x: np.random.choice(sellers.get(x["region"])), axis=1
    )
    return data.sort_values(by="transaction_date").reset_index(drop=True)

sales_data = get_data()

region_select = alt.selection_single(fields=["region"], empty="all")
region_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Sum of Transactions",
            ),
            color=alt.Color(
                field="region",
                type="nominal",
                scale=alt.Scale(domain=regions, range=colors),
                title="Region",
            ),
            opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
        )
    )
    .add_selection(region_select)
    .properties(title="Region Sales")
)

region_summary = (
    (
        alt.Chart(sales_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "month(transaction_date)",
                type="temporal",
            ),
            y=alt.Y(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Sales",
            ),
            color=alt.Color(
                "region",
                type="nominal",
                title="Regions",
                scale=alt.Scale(domain=regions, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=4,
                ),
            ),
        )
    )
    .transform_filter(region_select)
    .properties(width=700, title="Monthly Sales")
)

sellers_monthly_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=10)
        .encode(
            theta=alt.Theta(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Transactions",
            ),
            color=alt.Color(
                "month(transaction_date)",
                type="temporal",
                title="Month",
                scale=alt.Scale(domain=months, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=12,
                ),
            ),
            facet=alt.Facet(
                field="seller",
                type="nominal",
                columns=8,
                title="Sellers",
            ),
            tooltip=alt.Tooltip(["sum(transaction_amount)", "month(transaction_date)"]),
        )
    )
    .transform_filter(region_select)
    .properties(width=150, height=150, title="Sellers transactions per month")
)

top_row = region_pie | region_summary
full_chart = top_row & sellers_monthly_pie
st.altair_chart(full_chart)
```

### **Wrapping up**

Altair charts in Streamlit are an efficient and performant way to add interactive charts to your app. There are many styles and combinations of interactions to create using these tools.

If you loved this post, check out my other articles on [client-side filtering using Altair Sliders](https://medium.com/streamlit/client-side-filtering-in-streamlit-using-altair-sliders-b04988ab1f6c?ref=streamlit.ghost.io), [paginating dataframes](https://medium.com/streamlit/paginating-dataframes-with-streamlit-2da29b080920?ref=streamlit.ghost.io), and the [multiselect widget](https://medium.com/streamlit/multi-select-all-option-in-streamlit-3c92a0f20526?ref=streamlit.ghost.io). And if you have any questions, please post them in the comments below or contact me on [GitHub](https://github.com/sqlinsights?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/carlosdserrano/?ref=streamlit.ghost.io), [Twitter](https://twitter.com/serrano_carlosd?ref=streamlit.ghost.io), or [Medium](https://medium.com/@serranocarlosd?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

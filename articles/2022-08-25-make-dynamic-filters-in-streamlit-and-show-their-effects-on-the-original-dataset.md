---
title: "Make dynamic filters in Streamlit and show their effects on the original dataset"
subtitle: "Quickly and easily add dynamic filters to your Streamlit app"
date: 2022-08-25
authors:
  - "Vladimir Timofeenko"
category: "Tutorials"
---

![Make dynamic filters in Streamlit and show their effects on the original dataset](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--6--1.svg)


In this tutorial, I'll show you how to add dynamic filters to your Streamlit app with a bit of functional Python programming. As an example, we'll be using a Streamlit demo app that connects to Snowflake and retrieves the data by using Snowpark Python, pushing the computations into a Snowflake warehouse.

You’ll learn how to:

1. Build dynamic filters
2. Transform the data
3. Use Sankey chart
4. Show generated SQL statements

Want to dive right in? Here's the [repo code](https://github.com/Snowflake-Labs/streamlit-examples?ref=streamlit.ghost.io) that also contains a set of SQL statements to seed the tables with the data.

### 1. Build dynamic filters

First, let’s take a look at the app’s architecture:

![](https://streamlit.ghost.io/content/images/2022/08/Untitled-1.png)

Your data lives in Snowflake. To present it in Streamlit:

1. [Install Streamlit](https://docs.streamlit.io/library/get-started/installation?ref=streamlit.ghost.io);
2. Set up [Streamlit secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management?ref=streamlit.ghost.io);
3. Fill in the boilerplate that connects Streamlit to Snowflake Snowpark:

```
# main.py
# Initialize connection.
def init_connection() -> Session:
    return Session.builder.configs(st.secrets["snowpark"]).create()

if __name__ == "__main__":
    # Initialize the filters
    session = init_connection()
```

To make your app look beautiful, use the sidebar and the main area to visually separate the filters. Build out the UI with `draw_sidebar` and `draw_main_ui`:

![](https://streamlit.ghost.io/content/images/2022/08/Untitled--1-.png)

Next, implement the dynamic filters in the sidebar. The data is retrieved from Snowflake and transformed by using dataframes, so your filter class will be the bridge between the Streamlit framework and the Snowpark dataframes.

Let’s use Python’s awesome [dataclasses](https://docs.python.org/3.8/library/dataclasses.html?ref=streamlit.ghost.io) as the basis for the class. It provides a great framework for writing a class and has some convenient methods you’ll be using.

To control the widget presentation, you’ll need a `human_name` field (when the page prompts for inputs and it’s showing information in the charts) and a `widget_type` field (to create an interactive element).

To access your [filter’s state](https://docs.streamlit.io/library/api-reference/session-state?ref=streamlit.ghost.io) across the application, give it a `widget_id`.

Since the filters can't be both static (an on/off checkbox) and dynamic *and* depend on the source data (slider), you need a way to store the maximum value that’s retrieved from the table - instance field `_max_value`.

I used a checkbox and slider widgets as an example, but you can extend the code to work with other Streamlit components.

Your starting class will look like this:

```
@dataclass
class OurFilter:
    """This dataclass represents the filter that can be optionally enabled.

    It is created to parametrize the creation of filters from Streamlit and to keep the state."""
    human_name: str
    widget_type: callable  # Should be one of st.checkbox or st.select_slider. Other elements could be implemented similarly
    widget_id: str
    is_enabled: bool = False  # Controls whether the filter has been enabled. Useful for filtering the list of filters
    _max_value: int = 0
```

Next, add the other side—the one that will work with Snowpark to filter the data.

You’ll need a way to connect to Snowflake so the Snowpark session could be shared among all instances of class. Cue [class variables](https://docs.python.org/3.8/library/dataclasses.html?ref=streamlit.ghost.io#class-variables) to the rescue!

I’m working with a single table in Snowflake, so I’ll keep the `table_name` as yet another class variable. Each filter represents its own column in the table, so it’ll be `table_column`.

For the `OurFilter` class to have a generic interface, keep the name of the dataframe’s filtering method as an internal variable:

```
from dataclasses import dataclass
from typing import ClassVar
from snowflake.snowpark.session import Session

@dataclass
class OurFilter:
    """This dataclass represents the filter that can be optionally enabled.

    It is created to parametrize the creation of filters from Streamlit and to keep the state."""
    # Class variables
    table_name: ClassVar[str]
    session: ClassVar[Session]

    # The name to display in UI
    human_name: str
    # Column in the table which will be used for filtering
    table_column: str
    # ID of the streamlit widget
    widget_id: str
    # The type of streamlit widget to generate
    widget_type: callable
    # Field to track if the filter is active. Can be used for filtering the list of filters
    is_enabled: bool = False
    # max value
    _max_value: int = 0
    # dataframe method that will be used for filtering the data
    _df_method: str = ""
```

You can define the `__post_init__` [dataclass method](https://docs.python.org/3.8/library/dataclasses.html?ref=streamlit.ghost.io#post-init-processing) to automatically populate the value of `_max_value` and control the value of `_df_method`. This hides the internals of implementation from the class interface:

```
def __post_init__(self):
        if self.widget_type not in (st.select_slider, st.checkbox):
            raise NotImplemented

        if self.widget_type is st.select_slider:
            self._df_method = "between"
            self._max_value = (
                self.session.table(MY_TABLE)
                .select(max(col(self.table_column)))
                .collect()[0][0]
            )
        elif self.widget_type is st.checkbox:
            self._df_method = "__eq__"
```

Let’s add a way to render `OurFilter` in Streamlit and show some text to the user:

```
def create_widget(self):
        if self.widget_type is st.select_slider:
            base_label = "Select the range of"
        elif self.widget_type is st.checkbox:
            base_label = "Is"
        else:
            base_label = "Choose"
        widget_kwargs = dict(label=f"{base_label} {self.widget_id}", key=self.widget_id)
        if self.widget_type is st.select_slider:
            widget_kwargs.update(
                dict(
                    options=list(range(self.max_value + 1)),
                    value=(0, self.max_value),
                )
            )
        # Invocation of the streamlit method to place the widget on the page
				# e.g. st.checkbox(**widget_kwargs)
        self.widget_type(**widget_kwargs)
```

To apply the filters to a sequence of dataframes, let’s make the class callable. This will allow us to use them more expressively:

```
def __call__(self, _table: Table):
        """This method turns this class into a functor allowing to filter the dataframe.

        This allows to call it like so:

        f = OurFilter(...)
        new_table = last_table[f(last_table)]"""
        return methodcaller(self.df_method, **(self._get_filter_value()))(
            _table[self.table_column.upper()]
        )

def _get_filter_value(self):
        """Custom unpack function that retrieves the value of the filter
        from session state in a format compatible with self._df_method"""
        _val = st.session_state.get(self.widget_id)
        if self.widget_type is st.checkbox:
            # For .eq
            return dict(other=_val)
        elif self.widget_type is st.select_slider:
            # For .between
            return dict(lower_bound=_val[0], upper_bound=_val[1])
        else:
            raise NotImplemented
```

If you rewrite the `main.py` to import the filter class and draw the sidebar, you’ll see the dynamic filters on the page:

```
from typing import Iterable

import streamlit as st
from lib.filterwidget import OurFilter
from toolz import pluck

MY_TABLE = "CUSTOMERS"

def _get_active_filters() -> filter:
    return filter(lambda _: _.is_enabled, st.session_state.filters)

def _is_any_filter_enabled() -> bool:
    return any(pluck("is_enabled", st.session_state.filters))

def _get_human_filter_names(_iter: Iterable) -> Iterable:
    return pluck("human_name", _iter)

def draw_sidebar():
    """Should include dynamically generated filters"""

    with st.sidebar:
        selected_filters = st.multiselect(
            "Select which filters to enable",
            list(_get_human_filter_names(st.session_state.filters)),
            [],
        )
        for _f in st.session_state.filters:
            if _f.human_name in selected_filters:
                _f.enable()

        if _is_any_filter_enabled():
            with st.form(key="input_form"):

                for _f in _get_active_filters():
                    _f.create_widget()
                st.session_state.clicked = st.form_submit_button(label="Submit")
        else:
            st.write("Please enable a filter")

if __name__ == "__main__":
    # Initialize the filters
    session = init_connection()
    OurFilter.session = session
    OurFilter.table_name = MY_TABLE

    st.session_state.filters = (
        OurFilter(
            human_name="Current customer",
            table_column="is_current_customer",
            widget_id="current_customer",
            widget_type=st.checkbox,
        ),
        OurFilter(
            human_name="Tenure",
            table_column="years_tenure",
            widget_id="tenure_slider",
            widget_type=st.select_slider,
        ),
        OurFilter(
            human_name="Weekly workout count",
            table_column="average_weekly_workout_count",
            widget_id="workouts_slider",
            widget_type=st.select_slider,
        ),
    )

    draw_sidebar()
```

This will produce something like this:

![1.2](https://streamlit.ghost.io/content/images/2022/08/1.2.gif#browser)

Now that you have the filter presentation working, let’s see how those filters apply to the data and how it’s presented to the user.

### 2. Transform data

To show what effects the filters have on the dataset, preserve some data references. Since the `OurFilter` class already contains the logic to perform the filtering and hides it behind an interface, the transformation will be pretty light:

```
# main.py

def draw_main_ui(_session: Session):
    """Contains the logic and the presentation of the main section of the UI"""
    if _is_any_filter_enabled():  # Do not run any logic if no filters are actually enabled

        customers: Table = _session.table(MY_TABLE)
        table_sequence = [customers]

        _f: MyFilter
        for _f in _get_active_filters():
            # This block generates the sequence of dataframes as continually applying AND filtering set by the sidebar
            # The dataframes are to be used in the Sankey chart.

            # First, get the last dataframe in the list
            last_table = table_sequence[-1]
            # Apply the current filter to it
            new_table = last_table[
                # At this point the filter will be applied to the dataframe using the __call__ method
                _f(last_table)
            ]
            # And save it in the sequence
            table_sequence += [new_table]
        
        st.header("Dataframe preview")

        st.write(table_sequence[-1].sample(n=5).to_pandas().head())
    else:
        st.write("Please enable a filter in the sidebar to show transformations")
```

With this bit of code in the `main.py` file, the preview of all applied filters will show up in Streamlit:

![2](https://streamlit.ghost.io/content/images/2022/08/2.gif#browser)

### 3. Use Sankey chart

Sankey chart (or [Sankey diagram](https://en.wikipedia.org/wiki/Sankey_diagram?ref=streamlit.ghost.io)) shows the user how the data flows through the filter (the filtering effect). To dynamically visualize it as a graph, use the `Sankey` class from `plotly.graph_objects` and Streamlit’s built-in integration with Plotly library.

The interface for `plotly.graph_objects.Sankey` looks like this (color-coded):

![](https://streamlit.ghost.io/content/images/2022/08/Untitled--2-.png)

The `source` and the `target` lists describe which labels are connected, and the `value` describes the size of the flow.

To generate the `labels` as well as the `link`, create a few helper functions that’ll take the `table_sequence` from the code above and produce the needed values for the visualization:

```
# lib/chart_helpers.py
from typing import Iterable, List, Tuple

from snowflake.snowpark.table import Table

def mk_labels(_iter: Iterable[str]) -> Tuple[str, ...]:
    """Produces the labels configuration for plotly.graph_objects.Sankey"""
    first_label = "Original data"
    return (first_label,) + tuple(map(lambda _: f"Filter: '{_}'", _iter)) + ("Result",)

def mk_links(table_sequence: List[Table]) -> dict:
    """Produces the links configuration for plotly.graph_objects.Sankey"""
    return dict(
        source=list(range(len(table_sequence))),
        target=list(range(1, len(table_sequence) + 1)),
        value=[_.count() for _ in table_sequence],
    )
```

Now go back to `main.py` to show the Sankey chart on the page:

```
# main.py
import plotly.graph_objects as go
# ...
 
def draw_main_ui(_session: Session):
		if _is_any_filter_enabled():
				# ...
				# Generate the Sankey chart
				fig = go.Figure(
				    data=[
				        go.Sankey(
				            node=dict(
				                pad=15,
				                thickness=20,
				                line=dict(color="black", width=0.5),
				                label=mk_labels(_get_human_filter_names(_get_active_filters())),
				            ),
				            link=mk_links(table_sequence),
				        )
				    ]
				)
				st.header("Sankey chart of the applied filters")
				st.plotly_chart(fig, use_container_width=True)
```

The visualization shows how the filters are applied to the original dataset:

![3](https://streamlit.ghost.io/content/images/2022/08/3.gif#browser)

### 4. Show generated SQL statements

Since the program already tracks the sequence of transformations, you can show which SQL statements will produce the same results. To generate them from the `table_sequence` and show them in Streamlit, use `st.markdown` and build the table element with this code:

```
# main.py
# ...
 
def draw_main_ui(_session: Session):
		if _is_any_filter_enabled():
				# ...
				# Add the SQL statement sequence table
				statement_sequence = """
				| number | filter name | query, transformation |
				| ------ | ----------- | --------------------- |"""
				st.header("Statement sequence")
				for number, (_label, _table) in enumerate(
				    zip(
				        mk_labels(_get_human_filter_names(_get_active_filters())),
				        table_sequence,
				    )
				):
				    statement_sequence += f"""\\n| {number+1} | {_label} | ```{_table.queries['queries'][0]}``` |"""
				
				st.markdown(statement_sequence)
```

As the filters are applied, this code runs and maintains the table of statements:

![Untitled--3--1](https://streamlit.ghost.io/content/images/2022/08/Untitled--3--1.png#browser)

### Wrapping up

And that’s how you can implement dynamic filters in Streamlit! It takes only a few lines of code to add them to your app and let the user see their effects.

Have any questions or want to share a cool app you made? Join us on the [forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io), tag us on [Twitter](https://twitter.com/streamlit?ref=streamlit.ghost.io), or let us know in the comments below.

Happy coding! 🧑‍💻

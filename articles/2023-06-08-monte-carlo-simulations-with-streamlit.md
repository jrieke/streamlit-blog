---
title: "Monte Carlo simulations with Streamlit"
subtitle: "Learn how to predict future stock prices"
date: 2023-06-08
authors:
  - "Mats Stellwall"
category: "Snowflake powered \u2744\ufe0f"
---

![Monte Carlo simulations with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/06/monte-carlo-simulations.svg)


A Monte Carlo simulation, also known as a probability simulation, is a method for predicting possible outcomes of uncertain events. It consists of input variables, output variables, and a mathematical model. The name Monte Carlo comes from the famous casino town of Monaco, as chance is a core element of the modeling approach, similar to a game of roulette.

[I've used](https://medium.com/snowflake/doing-monte-carlo-simulations-at-scale-with-snowpark-for-python-5de6b367fdb6?ref=streamlit.ghost.io) Monte Carlo simulations to predict future stock prices with Snowpark for Python. Since running them was an interactive process, I decided to make a Streamlit app that lets users set parameters and generate predictions—to predict future stock prices. 🎲

![sis_mc_app](https://streamlit.ghost.io/content/images/2023/06/sis_mc_app.png#browser)

In this post, I'll show you how to build it step-by-step.

🎲

You can find the code for the app in my GitHub [repository](https://github.com/mstellwa/snowpark_examples/tree/main/py_scripts/streamlit/mcs?ref=streamlit.ghost.io).

## Python environment

To start, set up your Python environment (to use any Python-supported IDE for development):

* Install Python 3.8
* Install libraries `streamlit`, `snowflake-snowpark-python`, `scipy`, and `plotly`

## App structure

This is a [multipage](https://docs.streamlit.io/library/get-started/multipage-apps?ref=streamlit.ghost.io) app, so you'll use different Python files for each page.

For example, you'll use `01_Snowflake_connect.py` to handle the connection to Snowflake and `02_Run_Monte_Carlo_Simulations.py` to run and display the simulations. These files will be imported into the main file, `Monte_Carlo_Simulations.py`. You'll also create a Python file `snf_functions.py` to store common functions.

Here is the app's structure:

```
mcs
 |- lib
      |- snf_functions.py
 |- pages
      |- 01_Snowflake_connect.py
      |- 02_Run_Monte_Carlo_Simulations
 |- Monte_Carlo_Simulations.py
```

## `snf_functions.py` functions

The purpose of the `snf_functions.py` file is to hold common functions, such as connecting/disconnecting to Snowflake or retrieving the names of database objects.

To start, import the necessary modules and functions:

```
import streamlit as st

from scipy.stats import norm
import numpy as np
from typing import Tuple, Iterable

from snowflake.snowpark import Session
import snowflake.snowpark.functions as F
import snowflake.snowpark.types as T
```

Next, you'll need functions to connect to and disconnect from the Snowflake account. The [st.session\_state](https://docs.streamlit.io/library/api-reference/session-state?ref=streamlit.ghost.io) object lets you store variables that are available across multiple pages.

For example, you can set the account, user, password, and virtual warehouse values in your login page and then use them in your function:

```
def connect_to_snf():
    if 'snowsession' in st.session_state:
        return st.session_state['snowsession']

    creds = {
        'account': st.session_state['snow_account'],
        'user': st.session_state['snow_user'],
        'password': st.session_state['snow_password'],
        'warehouse': st.session_state['snow_wh']
    }
    session = Session.builder.configs(creds).create()
    st.session_state['snowsession'] = session

    return session

def disconnect_snf():
    if 'snowsession' in st.session_state:
        session = st.session_state['snowsession']
        session.close()
        del st.session_state['snowsession']
        del st.session_state['install_db']
        del st.session_state['install_schema']
        del st.session_state['install_stage']
```

The app relies on a couple of [UDFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-introduction?ref=streamlit.ghost.io) to run simulations.

There are two ways to handle this:

1. Assume they're available
2. Handle their deployment as part of the app flow

Let's choose the latter and create a function that checks if the UDFs exist in Snowflake.

The [@st.cache\_data](https://docs.streamlit.io/library/advanced-features/caching?ref=streamlit.ghost.io#stcache_data) decorator ensures that the function runs only if any parameters have changed. Otherwise, it returns the value from the last run. This avoids unnecessary data selections and makes the app run faster:

```
@st.cache_data()
def check_udfs(data_db: str, data_schema: str):
    snf_session = st.session_state['snowsession']
    udf_funcs = ['NORM_PPF', 'COLLECT_LIST', 'CALC_CLOSE']

    n_udfs = snf_session.table(f"{data_db}.INFORMATION_SCHEMA.FUNCTIONS").filter(
        (F.col("FUNCTION_SCHEMA") == F.lit(data_schema)) & (F.col("FUNCTION_NAME").in_(udf_funcs))).count()

    if n_udfs == len(udf_funcs):
        st.session_state['install_stage'] = ''
        return True
    else:
        return False
```

You'll also need a function to deploy the UDFs, in the case where they do not exist.

This code can be improved, but for now, it'll do the job:

```
def deploy_udf():
		# Values are set when connecting to to Snowflake
    snf_session = st.session_state['snowsession']
    data_db = st.session_state['install_db']
    data_schema = st.session_state['install_schema']
    stage_name = st.session_state['install_stage']

    stage_loc = data_db + '.' + data_schema + '.' + stage_name
    # Check for stage and create it if it does not exists
    snf_session.sql(f"CREATE STAGE IF NOT EXISTS {stage_name}").collect()

    @F.udf(name=f"{data_db}.{data_schema}.norm_ppf", is_permanent=True, replace=True, packages=["scipy"],
           stage_location=stage_loc)
    def norm_ppf(pd_series: T.PandasSeries[float]) -> T.PandasSeries[float]:
        return norm.ppf(pd_series)

    @F.udtf(name=f"{data_db}.{data_schema}.collect_list", is_permanent=True, replace=True
        , packages=["typing"], output_schema=T.StructType([T.StructField("list", T.ArrayType())])
        , stage_location=stage_loc)
    class CollectListHandler:
        def __init__(self) -> None:
            self.list = []

        def process(self, element: float) -> Iterable[Tuple[list]]:
            self.list.append(element)
            yield (self.list,)

    @F.udf(name=f"{data_db}.{data_schema}.calc_close", is_permanent=True, replace=True
        , packages=["numpy"], stage_location=stage_loc)
    def calc_return(last_close: float, daily_return: list) -> float:
        pred_close = last_close * np.prod(daily_return)
        return float(pred_close)

    return True
```

The user will be able to choose in which database and schema they want to install the UDFs when connecting to their Snowflake account. Since the users will also have the possibility to choose the table to use for the simulations as well the table to save the simulations to, I need functions to get the databases, schema, tables and columns.

Use `st.cache_data` to retrieve the names of those objects and to ensure that the SQL query is only run when something has changed:

```
@st.cache_data()
def get_databases():
    snf_session = st.session_state['snowsession']
    lst_db = [dbRow[1] for dbRow in snf_session.sql("SHOW DATABASES").collect()]
    # Add a default None value
    lst_db.insert(0, None)
    return lst_db

@st.cache_data()
def get_schemas(db: str):
    snf_session = st.session_state['snowsession']
    lst_schema = [schemaRow[0] for schemaRow in snf_session.sql(
        f"SELECT SCHEMA_NAME FROM {db}.INFORMATION_SCHEMA.SCHEMATA WHERE CATALOG_NAME = '{db.upper()}' AND SCHEMA_NAME != 'INFORMATION_SCHEMA' ORDER BY 1").collect()]
    lst_schema.insert(0, None)
    return lst_schema

@st.cache_data()
def get_tables(db: str, schema: str):
    snf_session = st.session_state['snowsession']
    lst_table = [tableRow[0] for tableRow in snf_session.sql(
        f"SELECT TABLE_NAME FROM {db}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{db.upper()}' AND TABLE_SCHEMA='{schema.upper()}' ORDER BY 1").collect()]
    lst_table.insert(0, None)
    return lst_table

@st.cache_data()
def get_columns(db: str, schema: str, table: str):
    snf_session = st.session_state['snowsession']
    lst_column = [columnRow[0] for columnRow in snf_session.sql(
        f"SELECT COLUMN_NAME, DATA_TYPE FROM {db}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG = '{db.upper()}' AND TABLE_SCHEMA='{schema.upper()}' AND TABLE_NAME = '{table.upper()}' ORDER BY 1").collect()]
    return lst_column
```

## `Monte_Carlo_Simulations.py`

The main app file `Monte_Carlo_Simulations.py` is used as input when running Streamlit. The [st.title](https://docs.streamlit.io/library/api-reference/text/st.title?ref=streamlit.ghost.io) object adds the app title. You can even use emoji shortcodes with it! 😄

To add a description, use [st.write](https://docs.streamlit.io/library/api-reference/write-magic/st.write?ref=streamlit.ghost.io):

```
import streamlit as st

st.title("Monte Carlo Simulations :spades:")
st.write(
    """ 
    A demo showing how Monte Carlo simulations can be used to predict the future stock price for P&G.

    A Monte Carlo simulation is a mathematical technique, which is used to estimate the possible outcomes of an uncertain event. 
    A Monte Carlo analysis consists of input variables, output variables, and a mathematical model. 

    This demo is using the following mathematical model:

             Stock Price Today = Stock Price Yesterday * e^r

    To calculate r the geometric Brownian motion (GBM) model is used.

    Start by connecting to your Snowflake account, using the **Snowflake connect** link in the sidebar.

    """
)
```

## `01_Snowflake_connect.py`

The `01_Snowflake_connect.py` file contains the logic for connecting to Snowflake. It begins with the necessary imports and uses the helper functions created in the `snf_functions.py` file.

```
import streamlit as st
from lib.snf_functions import get_databases, get_schemas, get_tables, get_columns, deploy_udf, check_udfs, connect_to_snf, disconnect_snf
```

Define a function that displays the disconnect button along with some information (to display it in multiple places):

```
def dispaly_disconnect():
    st.write("""
    Everything is set up for running Monte Carlo simulations.

    Choose **Run Monte Carlo simulations** in the sidebar to continue.
    """)
    with st.form('Snowflake Connection'):
        st.form_submit_button('Disconnect', on_click=disconnect_snf)
```

Next, build out the structure and logic for your page, starting with a title. This time, use the [st.markdown](https://docs.streamlit.io/library/api-reference/text/st.markdown?ref=streamlit.ghost.io) component, which lets you format strings using markdown.

Check if there is an active connection to Snowflake by looking for the `snowsession` key in the `st.session_state` object. If there isn't one, create an input form using [st.form](https://docs.streamlit.io/library/api-reference/control-flow/st.form?ref=streamlit.ghost.io).

By using the key parameter in the `st.text_input`, you can get the entered values and add them to the `st.session_state` object.

When the [st.form\_submit\_button](https://docs.streamlit.io/library/api-reference/control-flow/st.form_submit_button?ref=streamlit.ghost.io) is clicked, the `connect_to_snf` function is called:

```
st.markdown("# ❄️ Snowflake Connection")
st.sidebar.markdown("# Snowflake Connection ❄️")
# Check if there is a active connection...
if "snowsession" not in st.session_state:
    with st.form('Snowflake Credentials'):
        st.text_input('Snowflake account', key='snow_account')
        st.text_input('Snowflake user', key='snow_user')
        st.text_input('Snowflake password', key='snow_password', type='password')
        st.text_input('Snowflake warehouse', key='snow_wh')
        st.form_submit_button('Connect', on_click=connect_to_snf)
        st.stop()
```

If there is an active connection, the user can specify the database and schema into which they have installed or want to install the UDFs.

Use empty lists to prompt the user to select the values for the database and schema (in that order):

```
else:
    if st.session_state['snowsession']:
				# Assumption is that if a user already have set the install_schema state 
				# then 
        if 'install_schema' not in st.session_state:
            snf_session = st.session_state['snowsession']
            st.write("""
            You are now connected to your Snowflake account!
            
            Select the database and schema where the UDFs for doing Monte Carlo Simulations exists in or to be installed in 
            """)
            lst_databases = get_databases()
            sel_db = st.selectbox("Database", lst_databases)
            if sel_db:
                lst_schemas = get_schemas(sel_db)
                st.session_state['install_db'] = sel_db
                snf_session.use_database(sel_db)
            else:
                lst_schemas = []

            sel_schema = st.selectbox("Schema", options=lst_schemas)
```

After a user selects the schema, a check is performed to determine whether the UDFs exist there.

If they don't, the user is given the option to install them in the selected schema:

```
            if sel_schema:
                st.session_state['install_schema'] = sel_schema
                snf_session.use_schema(sel_schema)
                if check_udfs(sel_db, sel_schema):
                    dispaly_disconnect()
                else:
                    st.write("""
                    The selected database and schema is missing the UDFs needed for doing the Monte Carlo simulations.
                    
                    Set the stage name for the internal stage to be used for deployment, if it does not exists it will be created. 
                    """
                    )
                    with st.form('Deploy UDfs'):
                        stage_nm = st.text_input(label="Stage name", value="MCS_STAGE", key="install_stage")
                        st.form_submit_button('Deploy', on_click=deploy_udf)
                        st.stop()
```

If everything is installed, display the disconnect button:

```
        else:
            dispaly_disconnect()
```

## `02_Run_Monte_Carlo_Simulations.py`

The `02_Run_Monte_Carlo_Simulations.py` file contains the structure and logic for running the simulations.

Import the necessary libraries and check if there is a connection to a Snowflake account:

```
import streamlit as st
import snowflake.snowpark.functions as F
from snowflake.snowpark import Column, Window
from lib.snf_functions import get_databases, get_schemas, get_tables, get_columns, deploy_udf
import plotly.express as px

# Get the current credentials
if "snowsession" in st.session_state:
    snf_session = st.session_state['snowsession']
else:
    st.write("**Please log into you Snowflake account first!**")
    st.stop()
```

In my other [post](https://medium.com/snowflake/doing-monte-carlo-simulations-at-scale-with-snowpark-for-python-5de6b367fdb6?ref=streamlit.ghost.io), I described the function used to run the simulations and outlined all the necessary steps:

```
def run_simulations(df, n_days, n_sim_runs):

    def pct_change(indx_col: Column, val_col: Column):
        return ((val_col - F.lag(val_col, 1).over(Window.orderBy(indx_col))) / F.lag(val_col, 1).over(Window.orderBy(indx_col)))
    
    # Calculate the log return by day
    df_log_returns = df_closing.select(F.col("DATE"), F.col("CLOSE")
                           ,F.call_function("LN", (F.lit(1) + pct_change(F.col("DATE"), F.col("CLOSE")))).as_("log_return"))
    
    # Get the u, var, stddev and last closing price
    df_params = df_log_returns.select(F.mean("LOG_RETURN").as_("u")
                 , F.variance("LOG_RETURN").as_("var")
                 , F.stddev("LOG_RETURN").as_("std_dev")
                ,F.max(F.col("last_close")).as_("LAST_CLOSE"))\\
            .with_column("drift", (F.col("u")-(F.lit(0.5)*F.col("var"))))\\
            .select("std_dev", "drift", "last_close")
    
    # Generates rows for the number of days and simulations by day
    df_days = snf_session.generator(F.row_number().over(Window.order_by(F.seq4())).as_("day_id") ,rowcount=n_days)
    df_sim_runs = snf_session.generator(F.row_number().over(Window.order_by(F.seq4())).as_("sim_run") ,rowcount=n_sim_runs)
	
    df_daily_returns = df_days.join(df_sim_runs).join(df_params)\\
        .select("day_id", "sim_run"
                , F.exp(F.col("drift") + F.col("std_dev") *  F.call_function(f"{data_db}.{data_schema}.norm_ppf", F.uniform(0.0,1.0,F.random()))).as_("daily_return")
               , F.lit(None).as_("SIM_CLOSE"))\\
        .sort(F.col("DAY_ID"), F.col("sim_run"))
	
		# Generate a day 0 row with the last closing price for each simulation run
    last_close = df_params.select("LAST_CLOSE").collect()[0][0]
    df_day_0 = snf_session.generator(F.lit(0).as_("DAY_ID"),  
                                    F.row_number().over(Window.order_by(F.seq4())).as_("SIM_RUN")
                                    , F.lit(1.0).as_("DAILY_RETURN") ,F.lit(last_close).as_("SIM_CLOSE"), rowcount=n_sim_runs)

    # Union the dataframes,
    df_simulations = df_day_0.union_all(df_daily_returns)

    df_simulations_calc_input = df_simulations.with_column("SIM_CLOSE_0", F.first_value(F.col("SIM_CLOSE")).over(Window.partition_by("SIM_RUN").order_by("DAY_ID") ) )\\
                .with_column("L_DAILY_RETURN", F.call_table_function(f"{data_db}.{data_schema}.collect_list", F.col("DAILY_RETURN")).over(partition_by="SIM_RUN", order_by="DAY_ID"))

    df_sim_close = df_simulations_calc_input.with_column("SIM_CLOSE", 
                                                         F.call_function(f"{data_db}.{data_schema}.calc_close"
                                                                    , F.col("SIM_CLOSE_0"),F.col("L_DAILY_RETURN")))
    
    # Cache the returning Snowpark Dataframe so we do not run it multiple times when visulazing etc
    return df_sim_close.select("DAY_ID", "SIM_RUN", "SIM_CLOSE").cache_result()
```

It also has a function for displaying the results of the simulations:

```
def display_sim_result(df):
    pd_simulations = df.sort("DAY_ID", "SIM_RUN").to_pandas()
    
    fig = px.line(pd_simulations, x="DAY_ID", y="SIM_CLOSE", color='SIM_RUN', render_mode='svg')
    st.plotly_chart(fig, use_container_width=True)
    metrics = df.select(F.round(F.mean(F.col("SIM_CLOSE")), 2)
                                       , F.round(F.percentile_cont(0.05).within_group("SIM_CLOSE"), 2)
                                       , F.round(F.percentile_cont(0.95).within_group("SIM_CLOSE"), 2)).collect()
    st.write("Expected price: ", metrics[0][0])
    st.write(f"Quantile (5%): ", metrics[0][1])
    st.write(f"Quantile (95%): ", metrics[0][2])
```

Next, add the GUI components and logic:

```
st.sidebar.markdown("# Simulation Parameters")
st.title("Monte Carlo Simulations :spades:")
st.write("Start by choosing the table and columns with the date and stock prices that is going to be used for the simulations.")
```

To let users change the number of days and simulations per day, create a sidebar with the [st.sidebar](https://docs.streamlit.io/library/api-reference/layout/st.sidebar?ref=streamlit.ghost.io) widget and two sliders—one for days and one for simulations. Whenever the sliders are adjusted, the variables `n_days` and `n_iterations` will be updated.

To track the user clicks on the "Run Simulations" button, use `st.session_state`:

```
with st.sidebar:
    with st.form(key="simulation_param"):
        n_days = st.slider('Number of Days to Generate', 1, 1000, 100)
        n_iterations = st.slider('Number of Simulations by Day', 1, 100, 20)
        st.session_state.start_sim_clicked = st.form_submit_button(label="Run Simulations")
```

Add select boxes to let users select the database, table, and columns. Use the previously defined functions to retrieve the data displayed in the widgets, and use empty lists to ensure that the user selects the value for the database, schema, table, and columns (in that order).

Once the user has selected the date and stock price columns, generate a Snowpark DataFrame and plot the data:

```
lst_databases = get_databases()
col1, col2, col3, col4 = st.columns(4)
sel_db = col1.selectbox("Database", lst_databases)
if sel_db:
    lst_schemas = get_schemas(sel_db)
else:
    lst_schemas = []

sel_schema = col2.selectbox("Schema", options=lst_schemas)

if sel_schema:
    lst_tables = get_tables(sel_db, sel_schema)
else:
    lst_tables = []

sel_table = col3.selectbox("Table", lst_tables)
if sel_table:
    lst_columns = get_columns(sel_db, sel_schema, sel_table)
else:
    lst_columns = []

sel_columns = col4.multiselect("Columns", lst_columns, max_selections=2)
if len(sel_columns) == 2:
    df_closing = snf_session.table(f"{sel_db}.{sel_schema}.{sel_table}").select(F.col(sel_columns[0]).as_("DATE"), F.col(sel_columns[1]).as_("CLOSE"))
    st.line_chart(df_closing.to_pandas(),x="DATE", y="CLOSE")
```

To check if the user has run the simulations after clicking the "Run Simulations" button, use the `display_sim_result` function.

Additionally, store the Snowpark DataFrame containing the results in the session state:

```
if st.session_state.start_sim_clicked:
    with st.spinner('Running simulations...'):
        df_simulations = run_simulations(df_closing, n_days, n_iterations)
        display_sim_result(df_simulations)
        st.session_state["df"] = df_simulations
				st.session_state.start_sim_clicked = False
```

To determine whether to display the "Save Results" button, check if the Snowpark DataFrame containing the simulation results is present in the session state (stored in the variable "df").

To let the user specify the database, schema, and table name, store the result, and display the selection boxes for choosing the database and schema and text input for the table name.

When the user clicks the button, the value of "save" changes to True. The user can then select the database and schema to save the result, along with the table name. The simulation result (stored in `st.session_state["df"]`) is permanently saved to a table.

The "display\_sim\_result" function is called to ensure that the simulation results are displayed after the data has been saved:

```
if "df" in st.session_state:
    st.write("Choose the database and schema to save the data into:")
    save_db = st.selectbox("Database", lst_databases, key="save_db")
    if save_db:
        lst_schemas = get_schemas(save_db)
        snf_session.use_database(save_db)
    else:
        lst_schemas = []
    save_schema = st.selectbox("Schema", options=lst_schemas, key="save_schema")

    if save_schema:
        have_schema = False
    else:
        have_schema = True

    save_tbl = st.text_input(label="Table name", value="STOCK_PRICE_SIMULATIONS", disabled=have_schema)
    save = st.button("❄️ Save results", key="save_sims")
    if save:
        df_simulations = st.session_state["df"]
        display_sim_result(df_simulations)
        with st.spinner("Saving data..."):
            df_simulations.write.mode('overwrite').save_as_table(f"{save_db}.{save_schema}.{save_tbl}")
            st.success(f"✅ Successfully wrote simulations to {save_db}.{save_schema}.{save_tbl}!")
            st.session_state["saved"] = True
```

## Final app

Here is what the final app will look like and how you'd use it step-by-step.

### Step 1

Log in to your Snowflake account:

![sis_mc_connect](https://streamlit.ghost.io/content/images/2023/06/sis_mc_connect.png#browser)

### Step 2

Select the columns and tables to base the simulations on, and set the number of days and simulations per day. Then click on "Run Simulations" to see a chart with the simulations, the expected price (the mean price of all simulations), and the 5% and 95% quantile values:

![mcs_select](https://streamlit.ghost.io/content/images/2023/06/mcs_select.png#browser)

### Step 3

Click on "Save to Snowflake" to save it to a table:

![sis_mc_app_result](https://streamlit.ghost.io/content/images/2023/06/sis_mc_app_result.png#browser)

And you're done! Congratulations! 🎉

## Wrapping up

I hope this post has inspired you to make your own prediction app. To use the code, remember to install the Streamlit library locally using pip. If you have any questions, please post them below or contact me on [LinkedIn](https://www.linkedin.com/in/matsstellwall/?ref=streamlit.ghost.io).

Happy app-building and predicting! 🎲

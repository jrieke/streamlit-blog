---
title: "Instant Insight: Generate data-driven presentations in a snap!"
subtitle: "Create presentations with Streamlit, Snowflake, Plotly, python-pptx, LangChain, and yahooquery"
date: 2023-08-02
authors:
  - "Oleksandr Arsentiev"
category: "LLMs"
---

![Instant Insight: Generate data-driven presentations in a snap!](https://streamlit.ghost.io/content/images/size/w2000/2023/07/instant-insight-app.svg)


Hey there! 👋

I'm Oleksandr, a Data Analyst at [Workday](https://www.workday.com/?ref=streamlit.ghost.io). I wrote my first lines of code four years ago and saw the incredible potential of technology to simplify tasks and enhance productivity.

In this post, I'll tell you about my Instant Insight app, which can generate PowerPoint presentations for company research **instantly**. Forget the hassle of spending hours crafting slides. Now you can create sleek, data-driven presentations in just a few clicks!

I'll show you how to:

1. Connect your Streamlit app to Snowflake
2. Create a UI with dynamic filters and an interactive table
3. Fetch company data from Yahoo Finance
4. Create graphs using Plotly
5. Use Clearbit API to get company logos
6. Use LangChain and GPT 3.5 LLM to write a SWOT analysis and value proposition
7. Extract structured data from the GPT response
8. Generate slides using python-pptx

Let's get cracking!

⚡

TLDR: Here's [the app’s URL](https://arsentievalex-instant-insight-web-app-main-gz753r.streamlit.app/?ref=streamlit.ghost.io) and the [GitHub repo](https://github.com/arsentievalex/instant-insight-web-app/tree/main?ref=streamlit.ghost.io). Enjoy!

## Why Instant Insight?

Imagine working in sales for a B2B SaaS company with hundreds of prospects and offering the following products: Accounting and Planning Software, CRM, Chatbot, and Cloud Data Storage. Your task is to conduct prospect research, including financial and SWOT analysis, explore the competitive landscape, craft value propositions, and share a presentation with your team.

The prospects' data is stored in Snowflake, which feeds your CRM system. You can use the Instant Insight app to quickly filter the prospects by sector, industry, prospect status, and product. Next, select the prospect you want to include in the presentation and click the button to generate the presentation. And... that's it! 🤩 You now have the slides ready to be shared with your team. 🚀

The slides created by the app include the following:

* Basic company overview
* SWOT analysis
* Financial charts
* Value proposition
* Competitor analysis
* Key people
* News and corporate events

### App overview

The high-level architecture of the app looks like this:

![](https://streamlit.ghost.io/content/images/2023/08/app-diagram.png)

And here is a 3-minute video of the app in action:

Now, let's dive into the code!

## 1. Connect your Streamlit app to Snowflake

First, obtain some data. To do this, use the Snowflake Connector:

```
import snowflake.connector

# get Snowflake credentials from Streamlit secrets
SNOWFLAKE_ACCOUNT = st.secrets["snowflake_credentials"]["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = st.secrets["snowflake_credentials"]["SNOWFLAKE_USER"]
SNOWFLAKE_PASSWORD = st.secrets["snowflake_credentials"]["SNOWFLAKE_PASSWORD"]
SNOWFLAKE_DATABASE = st.secrets["snowflake_credentials"]["SNOWFLAKE_DATABASE"]
SNOWFLAKE_SCHEMA = st.secrets["snowflake_credentials"]["SNOWFLAKE_SCHEMA"]

@st.cache_resource
def get_database_session():
    """Returns a database session object."""
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

@st.cache_data
def get_data():
    """Returns a pandas DataFrame with data from Snowflake."""
    query = 'SELECT * FROM us_prospects;'
    cur = conn.cursor()
    cur.execute(query)

    # Fetch the result as a pandas DataFrame
    column_names = [col[0] for col in cur.description]
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=column_names)

    # Close the connection to Snowflake
    cur.close()
    conn.close()
    return df

# get the data from Snowflake
conn = get_database_session()
df = get_data(conn)
```

Sensitive data such as your Snowflake account, username, password, database name, and schema are stored in secrets and retrieved by calling `st.secrets` (read more [here](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management?ref=streamlit.ghost.io#use-secrets-in-your-app)).

Next, define two functions:

1. `get_database_session()` initializes a connection object
2. `get_data()` executes a SQL query and returns a pandas DataFrame

Use a simple `SELECT *` query to retrieve all the data from the `us_prospects` table.

## 2. Create a UI with dynamic filters and an interactive table

Now let's use some Streamlit magic to develop a front end for the app. Create a sidebar panel containing four dynamic multi-select filters and add a checkbox that lets users select all values.

The filters in your app work sequentially. Users are expected to apply them individually, from top to bottom. Once the first filter is applied, the second filter becomes available and contains only relevant labels. After each filter is applied, the underlying DataFrame is pre-filtered, and the `num_of_pros` variable is updated to reflect the number of selected prospects.

See the filters in action:

![](https://streamlit.ghost.io/content/images/2023/08/Instant-Insight---Streamlit--1--2.gif)

Here is the code for the first two filters:

```
# create sidebar filters
st.sidebar.write('**Use filters to select prospects** 👇')
sector_checkbox = st.sidebar.checkbox('All Sectors', help='Check this box to select all sectors')
unique_sector = sorted(df['SECTOR'].unique())

# if select all checkbox is checked then select all sectors
if sector_checkbox:
    selected_sector = st.sidebar.multiselect('Select Sector', unique_sector, unique_sector)
else:
    selected_sector = st.sidebar.multiselect('Select Sector', unique_sector)

# if a user selected sector then allow to check all industries checkbox
if len(selected_sector) > 0:
    industry_checkbox = st.sidebar.checkbox('All Industries', help='Check this box to select all industries')
    # filtering data
    df = df[(df['SECTOR'].isin(selected_sector))]
    # show number of selected prospects
    num_of_pros = str(df.shape[0])
else:
    industry_checkbox = st.sidebar.checkbox('All Industries', help='Check this box to select all industries',
                                           disabled=True)
    # show number of selected prospects
    num_of_pros = str(df.shape[0])

# if select all checkbox is checked then select all industries
unique_industry = sorted(df['INDUSTRY'].loc[df['SECTOR'].isin(selected_sector)].unique())
if industry_checkbox:
    selected_industry = st.sidebar.multiselect('Select Industry', unique_industry, unique_industry)
else:
    selected_industry = st.sidebar.multiselect('Select Industry', unique_industry)

# if a user selected industry then allow them to check all statuses checkbox
if len(selected_industry) > 0:
    status_checkbox = st.sidebar.checkbox('All Prospect Statuses', help='Check this box to select all prospect statuses')
    # filtering data
    df = df[(df['SECTOR'].isin(selected_sector)) & (df['INDUSTRY'].isin(selected_industry))]
    # show number of selected prospects
    num_of_pros = str(df.shape[0])

else:
    status_checkbox = st.sidebar.checkbox('All Prospect Statuses', help='Check this box to select all prospect statuses', disabled=True)
```

Next, use AgGrid to create an interactive table displaying your data, allowing users to select slide-generation prospects (read more [here](https://streamlit-aggrid.readthedocs.io/en/docs/?ref=streamlit.ghost.io)).

Place a checkbox on each table row, allowing users to select only one row. Additionally, set custom column width and table height.

Here is what it'll look like:

![](https://streamlit.ghost.io/content/images/2023/08/table.gif)

Neat, right?

Here is the code to create this table:

```
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode
import pandas as pd

# creating AgGrid dynamic table and setting configurations
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_column(field='Company Name', width=270)
gb.configure_column(field='Sector', width=260)
gb.configure_column(field='Industry', width=350)
gb.configure_column(field='Prospect Status', width=270)
gb.configure_column(field='Product', width=240)

gridOptions = gb.build()

response = AgGrid(
    df,
    gridOptions=gridOptions,
    height=600,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
    theme='alpine',
    allow_unsafe_jscode=True
)

# get selected rows
response_df = pd.DataFrame(response["selected_rows"])
```

## 3. Fetch company data from Yahoo Finance

Let's say the user has selected a company for research, and you need to gather some data on it. Your primary data source is [Yahoo Finance](https://finance.yahoo.com/?ref=streamlit.ghost.io), which you'll access with the [yahooquery library](https://pypi.org/project/yahooquery/?ref=streamlit.ghost.io)—a Python interface to unofficial Yahoo Finance API endpoints. It allows users to retrieve almost all the visible data via the Yahoo Finance front-end.

Here's the overview slide with Yahoo Finance data:

![sample_overview_slide](https://streamlit.ghost.io/content/images/2023/08/sample_overview_slide.png#border)

Use the [Ticker class](https://yahooquery.dpguthrie.com/guide/ticker/intro/?ref=streamlit.ghost.io) of yahooquery to obtain quantitative and qualitative data about a selected company. Just pass the company's ticker symbol as an argument, call the required property, and retrieve the data from the returned dictionary.

Here is the code that retrieves data for the company overview slide:

```
from yahooquery import Ticker

selected_ticker = 'ABC'
ticker = Ticker(selected_ticker)

# get company info
name = ticker.price[selected_ticker]['shortName']
sector = ticker.summary_profile[selected_ticker]['sector']
industry = ticker.summary_profile[selected_ticker]['industry']
employees = ticker.summary_profile[selected_ticker]['fullTimeEmployees']
country = ticker.summary_profile[selected_ticker]['country']
city = ticker.summary_profile[selected_ticker]['city']
website = ticker.summary_profile[selected_ticker]['website']
summary = ticker.summary_profile[selected_ticker]['longBusinessSummary']
```

The app utilizes Yahoo Finance data to create graphs illustrating financial performance over time. One slide displays basic financial metrics such as stock price, total debt, total revenue, and EBITDA over time.

I'll touch on plotting later. For now, let's focus on obtaining financial data from Yahoo Finance. Functions `get_stock()` and `get_financials()` return dataframes with relevant financial metrics. The stock price data is stored separately from other financial metrics, which is why you call two properties:

1. `ticker.history()` to retrieve historical pricing data for given symbol(s) (read docs [here](https://yahooquery.dpguthrie.com/guide/ticker/historical/?ref=streamlit.ghost.io))
2. `ticker.all_financial_data()` to retrieve all financial data, including income statement, balance sheet, cash flow, and valuation measures (read docs [here](https://yahooquery.dpguthrie.com/guide/ticker/financials/?ref=streamlit.ghost.io#all_financial_data))

Here is the code used to generate four dataframes with historical stock price, revenue, total debt, and EBITDA:

```
from yahooquery import Ticker
import pandas as pd

def get_stock(ticker, period, interval):
    """function to get stock data from Yahoo Finance. Takes ticker, period and interval as arguments and returns a DataFrame"""
    hist_df = ticker.history(period=period, interval=interval)
    hist_df = hist_df.reset_index()
    # capitalize column names
    hist_df.columns = [x.capitalize() for x in hist_df.columns]
    return hist_df

def get_financials(df, col_name, metric_name):
    """function to get financial metrics from a DataFrame. Takes DataFrame, column name and metric name as arguments and returns a DataFrame"""
    metric = df.loc[:, ['asOfDate', col_name]]
    metric_df = pd.DataFrame(metric).reset_index()
    metric_df.columns = ['Symbol', 'Year', metric_name]
    return metric_df

selected_ticker = 'ABC'
ticker = Ticker(selected_ticker)

# get all financial data
fin_df = ticker.all_financial_data()

# create df's for each metric
stock_df = get_stock(ticker=ticker, period='5y', interval='1mo')
rev_df = get_financials(df=fin_df, col_name='TotalRevenue', metric_name='Total Revenue')
debt_df = get_financials(df=fin_df, col_name='TotalDebt', metric_name='Total Debt')
ebitda_df = get_financials(df=fin_df, col_name='NormalizedEBITDA', metric_name='EBITDA')
```

The data from Yahoo Finance is also used on another slide for competitor analysis, where a company's performance is compared to its peers. To perform it, use two metrics: total revenue and SG&A % of revenue. They're available in the income statement, so use the `ticker.income_statement()` property which returns a DataFrame (read more [here](https://yahooquery.dpguthrie.com/guide/ticker/financials/?ref=streamlit.ghost.io#income_statement)).

The `extract_comp_financials()` function retrieves the total revenue and selling, general, and administrative expenses (SG&A) from the income statement DataFrame, and only keeps data from 2022. Since the SG&A as a percentage of revenue metric isn't readily available, calculate it manually by dividing SG&A by revenue and multiplying by 100.

The function operates on a nested dictionary with company names as keys and a dictionary with tickers as values, then appends new values to the existing dictionary:

```
from yahooquery import Ticker
import pandas as pd

def extract_comp_financials(tkr, comp_name, comp_dict):
    """Function to extract financial metrics for competitors. 
Takes a ticker, company name and a nested dictionary with 
competitors as arguments and appends financial metrics to dict"""

    ticker = Ticker(tkr)
    income_df = ticker.income_statement(frequency='a', trailing=False)
    subset = income_df.loc[:, ['asOfDate', 'TotalRevenue', 'SellingGeneralAndAdministration']].reset_index()

    # keep only 2022 data
    subset = subset[subset['asOfDate'].dt.year == 2022].sort_values(by='asOfDate', ascending=False).head(1)

    # get values
    total_revenue = subset['TotalRevenue'].values[0]
    sg_and_a = subset['SellingGeneralAndAdministration'].values[0]

    # calculate sg&a as a percentage of total revenue
    sg_and_a_pct = round(sg_and_a / total_revenue * 100, 2)

    # add values to dictionary
    comp_dict[comp_name]['Total Revenue'] = total_revenue
    comp_dict[comp_name]['SG&A % Of Revenue'] = sg_and_a_pct

# sample dict
peers_dict_nested = {'Company 1': {'Ticker': 'ABC'}, 'Company 2': {'Ticker': 'XYZ'}}

# extract financial data for each competitor
for key, value in peers_dict_nested.items():
    try:
        extract_comp_financials(tkr=value['Ticker'], comp_name=key, dict=peers_dict_nested)
    # if ticker is not found in Yahoo Finance, drop it from the peers dict and continue
    except:
        del peers_dict_nested[key]
        continue
```

After running the code above, get a nested dictionary that resembles the following structure:

```
# sample output dict
{'Company 1': {'Ticker': 'ABC', 'Total Revenue': '1234', 'SG&A % Of Revenue': '10'}, 
 'Company 2': {'Ticker': 'XYZ', 'Total Revenue': '5678', 'SG&A % Of Revenue': '20'}}
```

Next, convert the nested dictionary to the DataFrame to pass it to a plotting function:

```
# create a dataframe with peers financial data
peers_df = pd.DataFrame.from_dict(peers_dict_nested, orient='index')
peers_df = peers_df.reset_index().rename(columns={'index': 'Company Name'})
```

The resulting DataFrame should look something like this:

| Company Name | Ticker | Total Revenue | SG&A % Of Revenue |
| --- | --- | --- | --- |
| Company 1 | ABC | 1234 | 10 |
| Company 2 | XYZ | 5678 | 20 |

## 4. Create graphs using Plotly

You've filtered the financial data—now it's time to plot it! Use Plotly Express to create simple yet visually appealing graphs (read more [here](https://plotly.com/python/plotly-express/?ref=streamlit.ghost.io)).

In the previous section, you create a DataFrame and a variable for the company name. Use these in the `plot_graph()` function to take the dataframe, column names for the x and y axes, and the graph title as arguments:

```
import plotly.express as px

def plot_graph(df, x, y, title, name):
    """function to plot a line graph. Takes DataFrame, x and y axis, title and name as arguments and returns a Plotly figure"""
    fig = px.line(df, x=x, y=y, template='simple_white',
                        title='<b>{} {}</b>'.format(name, title))
    fig.update_traces(line_color='#A27D4F')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

stock_fig = plot_graph(df=stock_df, x='Date', y='Open', title='Stock Price USD', name=name)
rev_fig = plot_graph(df=rev_df, x='Year', y='Total Revenue', title='Total Revenue USD', name=name)
debt_fig = plot_graph(df=debt_df, x='Year', y='Total Debt', title='Total Debt USD', name=name)
ebitda_fig = plot_graph(df=ebitda_df, x='Year', y='EBITDA', title='EBITDA USD', name=name)
```

The resulting graphs should look something like this:

![sample_financials_slide-1](https://streamlit.ghost.io/content/images/2023/08/sample_financials_slide-1.png#border)

The app also generates a slide containing a competitor analysis for a given company. To make it, use the `peers_plot()` function along with `peers_df`. This function generates a horizontal bar chart that compares the total revenue and SG&A % of revenue among competitors.

Here is the code:

```
import plotly.express as px
import pandas as pd

def peers_plot(df, name, metric):
    """Function to plot a bar chart with peers. 
Takes DataFrame, name, metric and ticker as arguments and returns a Plotly figure"""

    # drop rows with missing metrics
    df.dropna(subset=[metric], inplace=True)
    df_sorted = df.sort_values(metric, ascending=False)

    # iterate over the labels and add the colors to the color mapping dictionary, hightlight the selected company
    color_map = {}
    for label in df_sorted['Company Name']:
        if label == name:
            color_map[label] = '#A27D4F'
        else:
            color_map[label] = '#D9D9D9'

    fig = px.bar(df_sorted, y='Company Name', x=metric, 
                        template='simple_white', color='Company Name',
                        color_discrete_map=color_map,
                        orientation='h',
                        title='<b>{} {} vs Peers FY22</b>'.format(name, metric))
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, yaxis_title='')
    return fig

# plot peers graphs
rev_peers_fig = peers_plot(df=peers_df, name=name, metric='Total Revenue')
sg_and_a_peers_fig = peers_plot(df=peers_df, name=name, metric='SG&A % Of Revenue')
```

Using custom colors makes your company stand out.

The bar charts should look something like this:

![sample_peers_slide-1](https://streamlit.ghost.io/content/images/2023/08/sample_peers_slide-1.png#border)

## 5. Use Clearbit API to get company logos

As you saw on the company overview slide, there was a logo of the researched company. Logo URLs aren’t available on Yahoo Finance, so use [Clearbit](https://clearbit.com/logo?ref=streamlit.ghost.io) instead. Just connect the company's website to "[https://logo.clearbit.com/](https://logo.clearbit.com/*?ref=streamlit.ghost.io)" with a few lines of code:

```
from yahooquery import Ticker

selected_ticker = 'ABC'
ticker = Ticker(selected_ticker)

# get website of the selected company
website = ticker.summary_profile[selected_ticker]['website']

# get logo url of the selected company
logo_url = '<https://logo.clearbit.com/>' + website
```

Now that you have the logo URL check if it works. If it does, adjust its size and position it on a slide. To do this, use the custom function `resize_image()`, which places a logo image inside a container and adjusts its size while maintaining its aspect ratio. This ensures that all logos look the same despite any initial differences in size.

Then save the image object locally as "logo.png" and retrieve it to place on a slide as a picture. You can place Plotly figures on slides in a similar manner. Use the python-pptx library to manipulate PowerPoint slides and shapes programmatically (read more [here](https://python-pptx.readthedocs.io/en/latest/?ref=streamlit.ghost.io)).

Here is the process:

![](https://streamlit.ghost.io/content/images/2023/08/workflow_instant_insight.jpg)

The code below uses the `logo_url` variable (defined in the previous code snippet):

```
from PIL import Image
import requests
from pptx import Presentation
from pptx.util import Inches
import os

def resize_image(url):
    """function to resize logos while keeping aspect ratio. Accepts URL as an argument and return image object"""
    # open image from url
    image = Image.open(requests.get(url, stream=True).raw)

    # if a logo is too high or too wide then make the background container twice as big
    if image.height > 140:
        container_width = 220 * 2
        container_height = 140 * 2

    elif image.width > 220:
        container_width = 220 * 2
        container_height = 140 * 2
    else:
        container_width = 220
        container_height = 140

    # create a new image with the same aspect ratio as the original image
    new_image = Image.new('RGBA', (container_width, container_height))

    # calculate the position to paste the image so that it is centered
    x = (container_width - image.width) // 2
    y = (container_height - image.height) // 2

    # paste the image onto the new image
    new_image.paste(image, (x, y))
    return new_image

# create presentation object
prs = Presentation('template.pptx')
# select second slide
slide = prs.slides[1]

# check if a logo ulr returns code 200 (working link)
if requests.get(logo_url).status_code == 200:
    # create logo image object
    logo = resize_image(logo_url)
    logo.save('logo.png')
    logo_im = 'logo.png'

    # add logo to the slide
    slide.shapes.add_picture(logo_im, left=Inches(1.2), top=Inches(0.5), width=Inches(2))
    os.remove('logo.png')
```

Running the code above should place a logo on the slide:

![sample_logo_slide-1](https://streamlit.ghost.io/content/images/2023/08/sample_logo_slide-1.png#border)

## 6. Use LangChain and GPT 3.5 LLM to write a SWOT analysis and value proposition

It's time to use AI for your company research! 🤖

You'll use LangChain, a popular framework designed to simplify the creation of applications using ChatOpenAI and Human/System Message LLMs (read more [here](https://python.langchain.com/docs/modules/model_io/models/chat/integrations/openai?ref=streamlit.ghost.io)).

The `generate_gpt_response()` function takes two arguments:

1. `gpt_input`, a prompt that you'll pass to the model
2. `max_tokens`, which limits the number of tokens in the model's response

You'll use the [gpt-3.5-turbo-0613 model](https://platform.openai.com/docs/models/gpt-3-5?ref=streamlit.ghost.io) in the arguments of `ChatOpenAI` and retrieve the OpenAI API key stored in Streamlit secrets. You'll also set the temperature to 0 to get more deterministic responses (read more [here](https://algowriting.medium.com/gpt-3-temperature-setting-101-41200ff0d0be?ref=streamlit.ghost.io)).

To improve the quality of GPT responses, pass the following text to the `SystemMessage` argument: "You are a helpful expert in finance, market, and company research. You also have exceptional skills in selling B2B software products." It'll set the objectives for the AI to follow (read more [here](https://blog.langchain.dev/chat-models/?ref=streamlit.ghost.io)).

```
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def generate_gpt_response(gpt_input, max_tokens):
    """Function to generate a response from GPT-3. Takes input and max tokens as arguments and returns a response"""
    # Create an instance of the OpenAI class
    chat = ChatOpenAI(openai_api_key=st.secrets["openai_credentials"]["API_KEY"], model='gpt-3.5-turbo-0613',
                      temperature=0, max_tokens=max_tokens)

    # Generate a response from the model
    response = chat.predict_messages(
        [SystemMessage(content='You are a helpful expert in finance, market and company research.'
                               'You also have exceptional skills in selling B2B software products.'),
         HumanMessage(
             content=gpt_input)])

    return response.content.strip()
```

Next, let's create a prompt for the model and invoke the `generate_gpt_response()` function.

Prompt the model to create a [SWOT analysis](https://www.investopedia.com/terms/s/swot.asp?ref=streamlit.ghost.io) of a specific company and return the result as a Python dictionary with this code:

```
input_swot = """Create a brief SWOT analysis of {name} company with ticker {ticker}?
Return output as a Python dictionary with the following keys: Strengths, Weaknesses, 
Opportunities, Threats as keys and analysis as values.
Do not return anything else."""

input_swot = input_swot.format(name='Company 1', ticker='ABC')

# return response from GPT-3
gpt_swot = generate_gpt_response(input_swot, 1000)
```

The resulting dictionary should look something like this:

```
{"Strengths": "text", "Weaknesses": "text", 
"Opportunities": "text", "Threats": "text"}
```

Similarly, you can prompt the GPT model to write a value proposition for a specific product for a given company. The app uses the common [value proposition framework](https://www.notion.so/Q2-Business-Review-QBR-reflections-a61e199ae0cb479794acc5b590a6f32f?pvs=21&ref=streamlit.ghost.io) of identifying customer pains and gains, as well as gain creators and pain relievers:

```
input_vp = """"Create a brief value proposition using Value Proposition Canvas framework for {product} for 
{name} company with ticker {ticker} that operates in {industry} industry.
Return output as a Python dictionary with the following keys: Pains, Gains, Gain Creators, 
Pain Relievers as a keys and text as values. Be specific and concise. Do not return anything else."""

input_vp = input_vp.format(product='Accounting software', name='Company 1', ticker='ABC', industry='Retail')

# return response from GPT-3
gpt_value_prop = generate_gpt_response(input_vp, 1000)

# response looks like below: 
# {"Pains": "text", "Gains": "text", "Gain Creators": "text", "Pain Relievers": "text"}
```

## 7. Extract structured data from the GPT response

In the previous step, you asked the GPT model for a Python dictionary of responses. But since LLMs can sometimes produce nonsensical responses, the returned string may not always contain just the necessary dictionary. In such cases, you may need to parse the response string to extract the dictionary and convert it to the Python dictionary type.

To accomplish this, you’ll need two standard libraries: [re](https://docs.python.org/3/library/re.html?ref=streamlit.ghost.io) and [ast](https://docs.python.org/3/library/ast.html?ref=streamlit.ghost.io).

The `dict_from_string()` function takes the response string from the LLM and returns a dictionary in this workflow:

![](https://streamlit.ghost.io/content/images/2023/08/Copy-of-Flowchart-1.jpg)

Here is the code:

```
import re
import ast

def dict_from_string(gpt_response):
    """Function to parse GPT response and convert it to a dict"""
    # Find a substring that starts with '{' and ends with '}', across multiple lines
    match = re.search(r'\\{.*?\\}', gpt_response, re.DOTALL)
    dictionary = None
    if match:
        try:
            # Try to convert substring to dict
            dictionary = ast.literal_eval(match.group())
        except (ValueError, SyntaxError):
            # Not a dictionary
            return None
    return dictionary

swot_dict = dict_from_string(gpt_response=gpt_swot)
vp_dict = dict_from_string(gpt_response=gpt_value_prop)
```

## 8. Generate slides using python-pptx

Now that you have the data, it's time to fill out the slides. Use a PowerPoint template and replace the placeholders with actual values using the [python-pptx library](https://python-pptx.readthedocs.io/en/latest/?ref=streamlit.ghost.io).

Here is what the SWOT slide template should look like:

![sample_swot_slide](https://streamlit.ghost.io/content/images/2023/08/sample_swot_slide.png#border)

To populate the slide with data, use the `replace_text()` function, which takes two arguments:

1. A dictionary with placeholders as keys and replacement text as values
2. A PowerPoint slide object

Use the `swot_dict` variable defined in the previous step:

```
from pptx import Presentation

def replace_text(replacements, slide):
    """function to replace text on a PowerPoint slide. Takes dict of {match: replacement, ... } and replaces all matches"""
    # Iterate through all shapes in the slide
    for shape in slide.shapes:
        for match, replacement in replacements.items():
            if shape.has_text_frame:
                if (shape.text.find(match)) != -1:
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        whole_text = "".join(run.text for run in paragraph.runs)
                        whole_text = whole_text.replace(str(match), str(replacement))
                        for idx, run in enumerate(paragraph.runs):
                            if idx != 0:
                                p = paragraph._p
                                p.remove(run._r)
                        if bool(paragraph.runs):
                            paragraph.runs[0].text = whole_text

prs = Presentation("template.pptx")
swot_slide = prs.slides[2]

# create title for the slide
swot_title = 'SWOT Analysis of {}'.format('Company 1')

# initiate a dictionary of placeholders and values to replace
replaces_dict = {
    '{s}': swot_dict['Strengths'],
    '{w}': swot_dict['Weaknesses'],
    '{o}': swot_dict['Opportunities'],
    '{t}': swot_dict['Threats'],
    '{swot_title}': swot_title}

# run the function to replace placeholders with values
replace_text(replacements=replaces_dict, slide=swot_slide)
```

In short, the `replace_text()` function iterates over all shapes on a slide, looking for placeholder values, and replaces them with values from the dictionary if found.

Once all the slides have been filled with data or images, the presentation object is saved as binary output and passed to `st.download_button()` so that a user can download a PowerPoint file (read more [here](https://docs.streamlit.io/library/api-reference/widgets/st.download_button?ref=streamlit.ghost.io)).

Here's what the download button should look like on the front end:

![sample_downloadbutton](https://streamlit.ghost.io/content/images/2023/08/sample_downloadbutton.png#border)

Download the resulting PPT here:

[NVIDIA Corporation 2023 08 02

NVIDIA Corporation 2023-08-02.pptx

2 MB

download-circle](https://streamlit.ghost.io/content/files/2023/08/NVIDIA-Corporation-2023-08-02.pptx "Download")

And here’s the code:

```
from pptx import Presentation
from io import BytesIO
from datetime import date
import streamlit as st

# create file name
filename = '{name} {date}.pptx'.format(name='Company 1', date=date.today())

# save presentation as binary output
binary_output = BytesIO()
prs.save(binary_output)

# display success message and download button
st.success('The slides have been generated! :tada:')

st.download_button(label='Click to download PowerPoint',
                   data=binary_output.getvalue(),
                   file_name=filename)
```

## Wrapping up

Thank you for reading to the end! Now you can develop a slide automation app for company research using Streamlit, Snowflake, YahooFinance, and LangChain. I hope you found something new and useful in this post.

As you can see, there are some limitations to the app. Firstly, it only generates research on public companies. Secondly, the GPT model uses general knowledge about a product, such as ChatBot or Accounting Software, to write a value proposition. In a more advanced app, the second constraint could be addressed by fine-tuning the model with your product data. This can be done by passing your product details in a prompt or storing this data as embeddings in a vector database (read more [here](https://www.pinecone.io/learn/vector-database/?ref=streamlit.ghost.io)).

If you have any questions or feedback, please post it in the comments below or contact me on [GitHub](https://github.com/arsentievalex?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/oleksandr-arsentiev-5554b3168/?ref=streamlit.ghost.io), or [Twitter](https://twitter.com/alexarsentiev?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

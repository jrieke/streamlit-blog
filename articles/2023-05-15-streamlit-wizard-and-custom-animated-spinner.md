---
title: "Streamlit wizard and custom animated spinner"
subtitle: "Improve user experience with simplified data entry and step-by-step guidance"
date: 2023-05-15
authors:
  - "Andrew Carson"
category: "Snowflake powered \u2744\ufe0f"
---

![Streamlit wizard and custom animated spinner](https://streamlit.ghost.io/content/images/size/w2000/2023/05/Community--1-.svg)


Over the past few months, I’ve had the pleasure of working with [Streamlit](https://streamlit.io/?ref=streamlit.ghost.io) on a variety of projects. For those new to it, Streamlit is an open-source Python framework for building web applications, specifically around visualization and data science.

A recent request - and overall very common use case - was unrelated to data visualization, but automation workflows requiring lengthy and complex user input. To simplify the data entry, I implemented a custom wizard form. Wizards are a great way to break down a complicated process into smaller, manageable steps, providing users with a clear path to follow. While Streamlit doesn't natively offer a wizard component, I easily recreated the functionality using a variety of widgets and session state variables.

In this post, we’ll walk through an example that simulates loading a file into Snowflake. I’ll be using reduced code snippets from [the public GitHub repository located here](https://github.com/acarson510/streamlit-wizard-form?ref=streamlit.ghost.io).

![wizard-form](https://streamlit.ghost.io/content/images/2023/05/wizard-form.gif#browser)

In this post, you will:

1. Build a multi-step wizard form using various components, including a custom spinner (optional).
2. Learn how to manage an application’s views and control flow with session state.
3. Gain exposure to some fantastic open-source libraries being contributed by the Streamlit developer community.

🏂

NOTE: I’ll be using [Streamlit Lottie](https://github.com/andfanilo/streamlit-lottie?ref=streamlit.ghost.io) for the optional animated spinner, which requires [creating a Lottie File account](https://lottiefiles.com/?ref=streamlit.ghost.io). If skipped, check out [the documentation](https://github.com/andfanilo/streamlit-lottie?ref=streamlit.ghost.io) and browse the [Lottie File library](https://lottiefiles.com/featured?ref=streamlit.ghost.io) for future use.

Let's get started!

## Session state variables and callback functions

Create two session state variables and two callback functions that will work together to render views and steps to the user. [Session state](https://docs.streamlit.io/library/api-reference/session-state?ref=streamlit.ghost.io) is Streamlit's way of preserving values across script re-runs, while callback functions are used to manage and update those values (read more on state management [here](https://docs.streamlit.io/library/api-reference/session-state?ref=streamlit.ghost.io)).

For now, let's define them as follows:

```
if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 1

if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'Grid'

### maintains the user's location within the wizard
def set_form_step(action,step=None):
    if action == 'Next':
        st.session_state['current_step'] = st.session_state['current_step'] + 1
    if action == 'Back':
        st.session_state['current_step'] = st.session_state['current_step'] - 1
    if action == 'Jump':
        st.session_state['current_step'] = step

### used to toggle back and forth between Grid View and Form View
def set_page_view(target_view):
    st.session_state['current_view'] = target_view
```

## View rendering

To keep the code modular and render the views, you'll create two simple functions. The `render_grid_view` function uses the [AgGrid custom component](https://github.com/PablocFonseca/streamlit-aggrid?ref=streamlit.ghost.io). If you're not familiar with AgGrid, take a look at [Pablo Fonseca's example page](https://staggrid-examples.streamlit.app/?ref=streamlit.ghost.io). It's an excellent component for DataFrame visualization — and just one of many fantastic open-source libraries built by the Streamlit developer community.

The `render_wizard_view` function uses Streamlit buttons to control movement between steps. To determine whether the buttons should be displayed as primary or secondary, we'll add some ternary logic.

```
def render_grid_view():
    data = {"Table Name": ["Product", "Employee", "Customer"], "Schema": ["Salesforce", "Salesforce", "Salesforce"], "Rows": [200, 300, 400], "Size": ["10 kb", "10 kb", "10 kb"]}
    df = pd.DataFrame(data=data)

    gridOptions = {
		  "rowSelection": "single",        
		        "columnDefs": [
		         { "field": "Table Name", "checkboxSelection": True },
		            { "field": "Schema" },
		            { "field": "Rows" },
		            { "field": "Size" }
		     ]
		 }    

    return AgGrid(
        df,        
        gridOptions=gridOptions,
        theme="balham"
    )
    
def render_wizard_view(): 
    with st.expander('',expanded=True):     
        sf_header_cols = st.columns([1, 1.75, 1])
        
        with sf_header_cols[1]:            
            st.subheader('Load Data to Snowflake')
    
    # determines button color which should be red when user is on that given step
    wh_type = 'primary' if st.session_state['current_step'] == 1 else 'secondary'
    ff_type = 'primary' if st.session_state['current_step'] == 2 else 'secondary'
    lo_type = 'primary' if st.session_state['current_step'] == 3 else 'secondary'
    sf_type = 'primary' if st.session_state['current_step'] == 4 else 'secondary'

    step_cols = st.columns([.5, .85, .85, .85, .85, .5])    
    step_cols[1].button('Warehouses', on_click=set_form_step, args=['Jump', 1], type=wh_type)
    step_cols[2].button('File Format', on_click=set_form_step, args=['Jump', 2], type=ff_type)        
    step_cols[3].button('Load Options', on_click=set_form_step, args=['Jump', 3], type=lo_type)      
    step_cols[4].button('Source Files', on_click=set_form_step, args=['Jump', 4], type=sf_type)                   
        
    st.markdown('---')
    st.write(st.session_state['current_step'])
    st.markdown('---')
    disable_back_button = True if st.session_state['current_step'] == 1 else False
    disable_next_button = True if st.session_state['current_step'] == 4 else False

    form_footer_cols = st.columns([5,1,1,1.75])

    form_footer_cols[0].button('Cancel', on_click=set_page_view, args=['Grid'])
    form_footer_cols[1].button('Back', on_click=set_form_step, args=['Back'], disabled=disable_back_button)
    form_footer_cols[2].button('Next', on_click=set_form_step, args=['Next'], disabled=disable_next_button)
    form_footer_cols[3].button('📤 Load Table', disabled=True)
```

Now, the logic to render the view is a simple "if-else" statement:

```
if st.session_state['current_view'] == 'Grid':
	render_grid_view():
else:
	render_wizard_view()
```

It's that easy! At this point, your app's output should look something like this:

![wizard_frame_2-1-1](https://streamlit.ghost.io/content/images/2023/05/wizard_frame_2-1-1.gif#browser)

If your output is off somewhere, please feel free to reference the Python file located [here](https://github.com/acarson510/streamlit-wizard-form/blob/main/wizard_frame.py?ref=streamlit.ghost.io).

🏂

NOTE: You may need to adjust the column sizes based on your browser size.

## Customize the steps

Feel free to customize the individual steps or use the steps provided in the repository. Once implemented, your fully functional form will look something like this:

![custom_steps-1](https://streamlit.ghost.io/content/images/2023/05/custom_steps-1.gif#browser)

## Custom animated spinner (optional)

Lastly, you can replace the native Streamlit spinner with a custom spinner of your own. You can follow the example using a combination of a [Lottie animation](https://lottiefiles.com/87114-snow-beard?ref=streamlit.ghost.io) and [Streamlit progress bar](https://docs.streamlit.io/library/api-reference/status/st.progress?ref=streamlit.ghost.io) or design your own using the [Lottie file library](https://lottiefiles.com/featured?ref=streamlit.ghost.io). Then, we'll update our imports and add one more function to render the spinner:

```
from streamlit_lottie import st_lottie
import requests

def render_animation():
    animation_response = requests.get('<https://assets1.lottiefiles.com/packages/lf20_vykpwt8b.json>')
    animation_json = dict()
    
    if animation_response.status_code == 200:
        animation_json = animation_response.json()
    else:
        print("Error in the URL")     
                           
    return st_lottie(animation_json, height=200, width=300)
```

Here is our spinner in action:

![custom_spinner-1-1](https://streamlit.ghost.io/content/images/2023/05/custom_spinner-1-1.gif#browser)

## Radio button alternative

In the example above, we used buttons to navigate through the wizard. An alternative approach is to use the [radio button](https://docs.streamlit.io/library/api-reference/widgets/st.radio?ref=streamlit.ghost.io). It offers the same functionality with fewer lines of code since there is no need to worry about button color schemes.

Here is an example within another very common use case, a checkout form:

![checkout_form-1](https://streamlit.ghost.io/content/images/2023/05/checkout_form-1.gif#browser)

For easy reference, here is the [full code repository](https://github.com/acarson510/streamlit-wizard-form?ref=streamlit.ghost.io).

## Conclusion

To conclude, I'd like to thank you very much for taking the time to read my first article. I intend to produce content related to all things data engineering, data science, and any other topic the data community finds relevant and helpful. If you're interested in learning more, please feel free to leave comments.

## My favorite cloud technology resources

### Snowflake

* [Snowflake Quickstarts](https://quickstarts.snowflake.com/?ref=streamlit.ghost.io)
* [Snowflake Labs](https://github.com/Snowflake-Labs?ref=streamlit.ghost.io)
* [Snowflake Developers Youtube Channel](https://www.youtube.com/@snowflakedevelopers?ref=streamlit.ghost.io)
* [Data Engineering Best Practices](https://medium.com/snowflake/top-14-snowflake-data-engineering-best-practices-a3c6c48486f4?ref=streamlit.ghost.io)
* [phData Blog](https://www.phdata.io/snowflake-resources/?ref=streamlit.ghost.io)
* [Data Engineering Simplified](https://www.youtube.com/@DataEngineering?ref=streamlit.ghost.io)
* [Analytics Today Blog](https://www.analytics.today/?ref=streamlit.ghost.io)

### Streamlit

* [Streamlit Custom Component Tracker](https://discuss.streamlit.io/t/streamlit-components-community-tracker/4634?ref=streamlit.ghost.io)
* [Best of Streamlit Examples](https://github.com/jrieke/best-of-streamlit?ref=streamlit.ghost.io)

### AWS

* [AWS Be a Better Dev](https://www.youtube.com/@BeABetterDev?ref=streamlit.ghost.io)
* [Cloud with Raj](https://www.youtube.com/@cloudwithraj?ref=streamlit.ghost.io)

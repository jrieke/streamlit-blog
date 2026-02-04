---
title: "Creating a Time Zone Converter with Streamlit"
subtitle: "6 steps on how to build your own converter"
date: 2023-04-25
authors:
  - "Vin\u00edcius Oviedo"
category: "Advocate Posts"
---

![Creating a Time Zone Converter with Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2023/04/time-zone-converter-streamlit.svg)


Hey, community! 👋

My name is Vinícius, and I’m a Data Analyst and LaTeX Editor.

I love solving problems and assisting customers with technology. When I ask a customer about a delivery deadline, they usually tell me a day and time in a different time zone than mine (e.g., 4 PM PST). Since I’m from Brazil, I have to convert it from PST to UTC+x, where "+x" refers to an offset that can be positive or negative.

There are lots of tools for time zone conversion, but I wanted something simple, intuitive, and ad-free. So I made a Streamlit app that converts a time zone from PST to UTC for any country! 👏

In this post, I’ll show you how to build it in six steps:

1. Import the required Python modules/package
2. Create a set of continents and countries
3. Configure the Streamlit page, header, and dropdown menu
4. Get the corresponding UTC+x time zone
5. Display the resulting time
6. Apply a custom dark theme

👉

You can go straight to the [app](https://time-zone-converter.streamlit.app/?ref=streamlit.ghost.io) and the [GitHub repo](https://github.com/OviedoVR/TimeZoneConverter?ref=streamlit.ghost.io), if you’d like to skip reading.

But first, let’s talk about…

## How does the Time Zone Converter work?

The way it works is super simple:

1. The user selects a continent and a country.
2. The corresponding time zone (in "UTC+x" format) is obtained based on the user's selection.
3. The user enters a PST time to be converted into the associated time obtained from step (2).
4. The resulting time for the selected country is displayed in the app.

![TZC-streamlit](https://streamlit.ghost.io/content/images/2023/04/TZC-streamlit.gif#browser)

Now, let’s help you develop your own converter!

### 1. Import the required Python modules/package

```
# Required Python modules/packages
import streamlit as st         # Streamlit framework 
from datetime import datetime  # For date and time
import pytz                    # For time zones
```

### 2. Create a set of continents and countries in the time zone context

```
# Create a dictionary with country name and corresponding timezone
timezone_dict = {
    "North America": {
        "United States": "America/New_York",
        "Canada": "America/Toronto",
        "Mexico": "America/Mexico_City",
        "Jamaica": "America/Jamaica",
        "Costa Rica": "America/Costa_Rica",
        "Bahamas": "America/Nassau",
        "Honduras": "America/Tegucigalpa",
        "Cuba": "America/Havana",
        "Dominican Republic": "America/Santo_Domingo"
    },
    "South America": {
        "Brazil": "America/Sao_Paulo",
        "Argentina": "America/Argentina/Buenos_Aires",
        "Chile": "America/Santiago",
        "Colombia": "America/Bogota",
        "Peru": "America/Lima",
        "Uruguay": "America/Montevideo",
        "Ecuador": "America/Guayaquil",
        "Bolivia": "America/La_Paz",
        "Paraguay": "America/Asuncion",
        "Venezuela": "America/Caracas"
    },
    "Europe": {
        "United Kingdom": "Europe/London",
        "France": "Europe/Paris",
        "Germany": "Europe/Berlin",
        "Italy": "Europe/Rome",
        "Spain": "Europe/Madrid",
        "Russia": "Europe/Moscow",
        "Turkey": "Europe/Istanbul",
        "Greece": "Europe/Athens",
        "Poland": "Europe/Warsaw",
        "Ukraine": "Europe/Kiev"
    },
    "Asia": {
        "India": "Asia/Kolkata",
        "Japan": "Asia/Tokyo",
        "China": "Asia/Shanghai",
        "Saudi Arabia": "Asia/Riyadh",
        "South Korea": "Asia/Seoul",
        "Indonesia": "Asia/Jakarta",
        "Malaysia": "Asia/Kuala_Lumpur",
        "Vietnam": "Asia/Ho_Chi_Minh",
        "Philippines": "Asia/Manila",
        "Thailand": "Asia/Bangkok"
    },
    "Oceania": {
        "Australia": "Australia/Sydney",
        "New Zealand": "Pacific/Auckland",
        "Fiji": "Pacific/Fiji",
        "Papua New Guinea": "Pacific/Port_Moresby",
        "Samoa": "Pacific/Apia",
        "Tonga": "Pacific/Tongatapu",
        "Solomon Islands": "Pacific/Guadalcanal",
        "Vanuatu": "Pacific/Efate",
        "Kiribati": "Pacific/Tarawa",
        "New Caledonia": "Pacific/Noumea"
    }
}

# Create a list of continents
continents = ["North America", "South America", "Europe", "Asia", "Oceania"]
```

### 3. Configure the Streamlit page, header, and dropdown menu for continent and country selection

```
# Streamlit app page setup
st.set_page_config(
    page_title='Time Zone Coverter', 
    page_icon='🌎',
    layout='centered',
    initial_sidebar_state='expanded',
    menu_items={
        'About': """This app is intended to select a country, get its 
        time zone in UTC format  and have its correspondent result 
        from a user-entered PST time."""
    }  
)

# Main header
st.header('Time Zone Coverter Streamlit app')

# Add some blank space
st.markdown("##")

# Create a dropdown to select a continent
continent = st.sidebar.selectbox("1. Select a continent", continents)

# Create a dropdown to select a country within the selected continent
countries = list(timezone_dict[continent].keys())
country = st.sidebar.selectbox("2. Select a country", countries)
```

### 4. Get the corresponding UTC+x time zone for the user selection

```
# Display the selected UTC offset
st.markdown("### :earth_americas: Corresponding UTC time:")
timezone = timezone_dict[continent][country]
utc_offset = datetime.now(pytz.timezone(timezone)).strftime('%z')
st.markdown(f"> **{country}** time zone is **UTC{utc_offset[:-2]}:{utc_offset[-2:]}**")
```

### 5. Display the resulting time—the informed PST time converted to UTC+x

```
# Add some blank space
st.markdown("##")

# Create input for PST time
st.markdown("### :clock10: PST time to UTC converter:")
pst_input = st.text_input("Enter PST time (e.g., 10:00 AM PST)")

# Convert PST time to UTC+X (where X is the offset)
try:
    pst_time = datetime.strptime(pst_input, "%I:%M %p PST")
    pst_time = pytz.timezone("US/Pacific").localize(pst_time, is_dst=None)
    target_time = pst_time.astimezone(pytz.timezone(timezone)).strftime("%I:%M %p %Z")
    st.markdown(f"> The corresponding time in **{country}** is **{target_time}**")
except:
    st.markdown("""
    :lock: Invalid input format. Please enter PST time in format 
    '<span style="color:#7ef471"><b> 10:00 AM PST </b></span>'
    """, unsafe_allow_html=True)
```

### 6. Apply a custom dark theme by creating a .streamlit folder with this config.toml file

```
[theme]
base="dark"
primaryColor="#54f142"
backgroundColor="#222831"
secondaryBackgroundColor="#393e46"
font="serif"
```

If you want to improve your Time Zone Converter, here are some suggestions:

* Replace the set of time zones for countries/continents with an API. Some alternatives are TimezoneDB and GeoNames, to name a few. This would provide more options for countries and even work with more cities. For example, Brazil has four different time zones.
* Implement more time zone formats, such as GMT, EST, CET, and so on.

Feel free to use your creativity. 😄

## Wrapping up

Thank you for reading my post! Now you know how to create a simple yet useful Time Zone Converter app. It can determine a time zone (in UTC+x format) for a user-selected country and provide a rough estimate for a "PST to UTC+X" time conversion. If you have any questions, please post them in the comments below or contact me via [GitHub](https://github.com/OviedoVR?ref=streamlit.ghost.io), [LinkedIn](https://www.linkedin.com/in/vinicius-oviedo/?ref=streamlit.ghost.io), or [Medium](https://medium.com/@vo.freelancer5?ref=streamlit.ghost.io).

Happy Streamlit-ing! 🎈

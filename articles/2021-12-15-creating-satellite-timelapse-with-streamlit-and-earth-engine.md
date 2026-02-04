---
title: "Creating satellite timelapse with Streamlit and Earth Engine"
subtitle: "How to create a satellite timelapse for any location around the globe in 60 seconds"
date: 2021-12-15
authors:
  - "Qiusheng Wu"
category: "Advocate Posts"
---

![Creating satellite timelapse with Streamlit and Earth Engine](https://streamlit.ghost.io/content/images/size/w2000/2021/12/Timelapse--Original-Res-1452-px----1-.gif)


Want to create a satellite timelapse for any location around the globe to see how the Earth has changed? You've come to the right place. I present to you...

An interactive web app for creating satellite timelapse **without coding!**

In this post, you'll learn how to create a satellite timelapse for any location and to deploy an Earth Engine app to [Streamlit Cloud](https://streamlit.io/cloud?ref=streamlit.ghost.io):

How to create a satellite timelapse without coding:

1. Draw a Region of Interest (ROI) on the map
2. Upload a GeoJSON file to the web app
3. Select a satellite image collection
4. Select a band combination
5. Select an administrative boundary
6. Customize timelapse parameters
7. Download your timelapse in GIF and MP4 formats

How to deploy an Earth Engine app to Streamlit Cloud:

1. Fork the streamlit-geospatial repo
2. Sign up for an Earth Engine account
3. Install GeoPandas, geemap, and Streamlit
4. Get an Earth Engine token
5. Deploy your app to Streamlit Cloud

Want to jump right in? Here's the [web app](https://streamlit.gishub.org/?ref=streamlit.ghost.io) and [repo code](https://github.com/giswqs/streamlit-geospatial?ref=streamlit.ghost.io).

Let's get started!

## How to create a satellite timelapse without coding

### 1. Draw a Region of Interest (ROI) on the map

First, navigate to the web app at [https://streamlit.gishub.org](https://streamlit.gishub.org/?ref=streamlit.ghost.io). Once the app opens in the web browser, click "Create Timelapse" on the left sidebar menu. You should see a map on the left and a list of options on the right. Pan and zoom the map to find your Region of Interest (ROI).

Next, click the rectangle tool to draw a rectangle on the map:

![Draw a Region of Interest (ROI) on the map and export the ROI as a GeoJSON](https://streamlit.ghost.io/content/images/2021/12/1.png)

Draw a Region of Interest (ROI) on the map and export the ROI as a GeoJSON

Due to the limitation of the [folium](https://github.com/python-visualization/folium?ref=streamlit.ghost.io) Python package, there is [no way to retrieve the coordinates](https://github.com/python-visualization/folium/issues/1402?ref=streamlit.ghost.io) of drawn shapes on the map. So you'll need to export the ROI manually and upload it back to the web app for subsequent steps.

Click the "Export" button in the upper-right corner of the map to export the ROI as a GeoJSON file to your computer. The GeoJSON file is a plain text file containing the coordinates of the geometries drawn on the map. Use any Text Editor to open and inspect the file.

### 2. Upload a GeoJSON file to the web app

Click "Browser files" to locate the GeoJSON file exported in the previous step and upload it to the web app. Or you can use other existing GeoJSON. Once you click the "Open" button on the open file dialog, the selected GeoJSON file should be uploaded to the app momentarily with the file name listed under "Browsers files":

![Upload the exported GeoJSON back to the web app](https://streamlit.ghost.io/content/images/2021/12/2.png)

Upload the exported GeoJSON back to the web app

### 3. Select a satellite image collection

Select "Landsat TM-ETM-OLI" from the dropdown list:

![Select a satellite image collection to create timelapse](https://streamlit.ghost.io/content/images/2021/12/3-1.png)

Select a satellite image collection to create timelapse

I chose [Landsat program](https://en.wikipedia.org/wiki/Landsat_program?ref=streamlit.ghost.io) because it's the longest-running enterprise for acquiring satellite imagery of the Earth since 1972. The most recent satellite, [Landsat 9](https://en.wikipedia.org/wiki/Landsat_9?ref=streamlit.ghost.io), was successfully launched on 27 September 2021. The "Landsat TM-ETM-OLI" image collection contains all available Landsat imagery acquired since 1984.

If you want to choose a different image collection from the [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/?ref=streamlit.ghost.io), select "Any Earth Engine ImageCollection."

### 4. Select a band combination

Landsat imagery comes with multi-spectral bands. Here are the common spectral bands produced by Landsat TM, ETM+, and OLI sensors:

![Spectral bands of Landsat satellite imagery](https://streamlit.ghost.io/content/images/2021/12/4.png)

Spectral bands of Landsat satellite imagery

To display and visualize an image on a computer screen, decide which three spectral bands you want to use for the Red, Green, and Blue (RGB) channels. Some of the commonly used band combinations include Natural Color (Red/Green/Blue), Color Infrared (NIR/Red/Green), Short-Wave Infrared (SWIR2/SWIR1/Red), Agriculture (SWIR1/NIR/Blue), and Geology (SWIR2/SWIR1/Blue). Read more about Landsat band combinations [here](https://gisgeography.com/landsat-8-bands-combinations/?ref=streamlit.ghost.io) and [here](https://www.esri.com/arcgis-blog/products/product/imagery/band-combinations-for-landsat-8/?ref=streamlit.ghost.io).

Select a band combination from the dropdown list. Or just enter the title you want to see on the resulting Landsat timelapse:

![Select an RGB band combination](https://streamlit.ghost.io/content/images/2021/12/5.png)

Select an RGB band combination

### 5. Select an administrative boundary

If your timelapse covers a large region, overlay it with an administrative boundary. Select it from the built-in datasets (e.g., Continents, Countries, US States) or select "User-defined," then enter an HTTP URL for the GeoJSON file:

![https://i.imgur.com/heJGmim.png](https://streamlit.ghost.io/content/images/2021/12/6.png)

You can customize the boundary's color, line width, and opacity.

### 6. Customize timelapse parameters

The "Frames per second" parameter controls the speed of the timelapse. The smaller the number, the slower the timelapse, and vice versa.

For example, a timelapse of annual Landsat imagery (1984-2021) has 38 frames. At 5 frames per second, the timelapse would last 7.6 seconds. By default, the app uses all available imagery to create the composite. You can change the start year, the end year, the start month, and the end month if you want a specific time range.

Since Landsat satellites carry optical sensors, you might see clouds in Landsat imagery (especially in the tropics). By default, the app applies the [fmask](https://developers.google.com/earth-engine/apidocs/ee-algorithms-fmask-matchclouds?ref=streamlit.ghost.io) algorithm to remove clouds, shadows, and snow. This can create black spots (nodata) in your timelapse. You can also change the font type, size, and color to customize the animated timestamps.

When finished with all parameters, click "Submit":

![https://i.imgur.com/tkT8ZMg.png](https://streamlit.ghost.io/content/images/2021/12/7.png)

Under the hood, the app will collect the parameters and pass them to the [landsat\_timelapse](https://geemap.org/timelapse/?ref=streamlit.ghost.io#geemap.timelapse.landsat_timelapse) function. It will utilize the GEE cloud computing platform to process the satellite imagery and generate the timelapse. The initial timelapse generated by Earth Engine will be further processed by geemap to add a progress bar, animated timestamps, etc.

### 7. Download your timelapse in GIF and MP4 formats

You can now download your timelapse as a GIF or MP4 animation in 60 seconds. 🚀 Right-click the image/video to save it, then share it with your friends, family, or on social media! 😇

Here are a few timelapse examples:

**River dynamics of Ucayali River, Peru - Created using Landsat imagery (SWIR1/NIR/Red)**

![https://i.imgur.com/xy7A0Yy.gif](https://i.imgur.com/xy7A0Yy.gif)

**Vegetation dynamics in Africa - created using monthly [MODIS NDVI](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2?ref=streamlit.ghost.io) data**

![https://i.imgur.com/k4rn9Vr.gif](https://i.imgur.com/k4rn9Vr.gif)

**Northeast Pacific bomb cyclone in October 2021 - Created using [GOES-17](https://jstnbraaten.medium.com/goes-in-earth-engine-53fbc8783c16?ref=streamlit.ghost.io)**

![https://github.com/giswqs/data/raw/main/timelapse/goes.gif](https://github.com/giswqs/data/raw/main/timelapse/goes.gif)

**Creek Fire in California in September 2020 - Created using [GOES-17](https://jstnbraaten.medium.com/goes-in-earth-engine-53fbc8783c16?ref=streamlit.ghost.io)**

![https://github.com/giswqs/data/raw/main/timelapse/fire.gif](https://github.com/giswqs/data/raw/main/timelapse/fire.gif)

**Temperature dynamics at the global scale - Created using [MODIS Land Surface Temperature](https://samapriya.github.io/awesome-gee-community-datasets/projects/daily_lst/?ref=streamlit.ghost.io)**

![https://i.imgur.com/2XonDcb.gif](https://i.imgur.com/2XonDcb.gif)

Want more examples? Use hashtags [#geemap](https://twitter.com/search?q=%23geemap&f=live&ref=streamlit.ghost.io) and [#streamlit](https://twitter.com/search?q=%23streamlit&src=typed_query&f=live&ref=streamlit.ghost.io) to search on Twitter and LinkedIn.

## How to deploy an Earth Engine app to Streamlit Cloud

### 1. Fork the streamlit-geospatial repo

Fork the [streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial?ref=streamlit.ghost.io) repo to your GitHub account. It contains the source code (>1000 lines) of the multi-page web app for various geospatial applications. You can find it [here](https://github.com/giswqs/streamlit-geospatial/blob/master/apps/timelapse.py?ref=streamlit.ghost.io).

### 2. Sign up for an Earth Engine account

[Sign up](https://earthengine.google.com/signup/?ref=streamlit.ghost.io) for a [Google Earth Engine](https://earthengine.google.com/?ref=streamlit.ghost.io) account. Once you get the email, log in to the [Earth Engine Code Editor](https://code.earthengine.google.com/?ref=streamlit.ghost.io) to verify that your account has been authorized to use Earth Engine.

### 3. Install GeoPandas, geemap, and Streamlit

Install GeoPandas, geemap, and Streamlit Python packages. If you have [Anaconda](https://www.anaconda.com/distribution/?ref=streamlit.ghost.io#download-section) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html?ref=streamlit.ghost.io) installed on your computer, you can create a fresh conda environment to install the required packages using the following commands:

```
conda create -n gee python=3.8
conda activate gee
conda install geopandas
pip install geemap
```

### 4. Get an Earth Engine token

Type `python` into the terminal and press "Enter" to get into the Python interactive shell. Then type `import ee` and `ee.Authenticate()` and press "Enter":

```
import ee
ee.Authenticate()
```

![Authenticate Google Earth Engine](https://streamlit.ghost.io/content/images/2021/12/8-1.png)

Authenticate Google Earth Engine

Log in to your Google account to obtain the authorization code and paste it back into the terminal. Once you press "Enter," an Earth Engine authorization token will be saved to your computer under the following file path (depending on your operating system):

```
Windows: C:\\Users\\USERNAME\\.config\\earthengine\\credentials
Linux: /home/USERNAME/.config/earthengine/credentials
MacOS: /Users/USERNAME/.config/earthengine/credentials
```

Navigate to the above file path and open the `credentials` file using a Text Editor. Copy the token wrapped within the double quotes to the clipboard:

![The Earth Engine token](https://streamlit.ghost.io/content/images/2021/12/9-1.png)

The Earth Engine token

### 5. Deploy your app to Streamlit Cloud

To deploy your app, click the “New app” button in the upper-right corner of your Streamlit workspace at [https://share.streamlit.io](https://share.streamlit.io/?ref=streamlit.ghost.io), then fill in your repo path (e.g., USERNAME/streamlit-geospatial), branch (e.g., master), and main file path (e.g., [app.py](http://app.py/?ref=streamlit.ghost.io)). Go to `App settings - Secrets` and set `EARTHENGINE_TOKEN` as an environment variable for your web app. Click "Save":

![https://i.imgur.com/CSsOMj3.png](https://streamlit.ghost.io/content/images/2021/12/10.png)

Depending on the number of dependencies specified in `requirements.txt`, the app might take a few minutes to install and deploy. Once deployed, you'll see its URL in your Streamlit Cloud workspace. It'll follow a standard structure based on your GitHub repo, such as:

```
<https://share.streamlit.io/>[user name]/[repo name]/[branch name]/[app path]
```

For example, here is the long app URL: [https://share.streamlit.io/giswqs/streamlit-geospatial/app.py](https://share.streamlit.io/giswqs/streamlit-geospatial/app.py?ref=streamlit.ghost.io). And here is the short app URL: [https://streamlit.gishub.org](https://streamlit.gishub.org/?ref=streamlit.ghost.io)

## Wrapping up

Congratulations! 👏 You did it! You have built an interactive web app for creating a satellite timelapse. You're welcome to contribute your comments, questions, resources, and apps as [issues](https://github.com/giswqs/streamlit-geospatial/issues?ref=streamlit.ghost.io) or [pull requests](https://github.com/giswqs/streamlit-geospatial/pulls?ref=streamlit.ghost.io) to the [streamlit-geospatial repo](https://github.com/giswqs/streamlit-geospatial?ref=streamlit.ghost.io).

Want to learn more about GEE and geemap? Check out [https://geemap.org](https://geemap.org/?ref=streamlit.ghost.io) , my [article](https://joss.theoj.org/papers/10.21105/joss.02305?ref=streamlit.ghost.io), and my [YouTube channel](https://www.youtube.com/c/QiushengWu?ref=streamlit.ghost.io) for video tutorials. Or get in touch with me on [Twitter](https://twitter.com/giswqs?ref=streamlit.ghost.io) or [LinkedIn](https://www.linkedin.com/in/qiushengwu?ref=streamlit.ghost.io).

Thanks for reading, and happy coding! 🍺

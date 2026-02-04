---
title: "Sogeti creates an educational Streamlit app for data preprocessing"
subtitle: "Learn how to use Sogeti\u2019s Data Quality Wrapper"
date: 2022-03-08
authors:
  - "Tijana Nikolic"
category: "Advocate Posts"
---

![Sogeti creates an educational Streamlit app for data preprocessing](https://streamlit.ghost.io/content/images/size/w2000/2022/03/Sogeti_feature-GIF.gif)


Trying to find the best approach to improving data quality? We know this pain. That’s why we created an app to automate data preprocessing and educate aspiring and experienced data scientists about improving data quality. We chose Streamlit for its ease of development and called our app Sogeti’s Data Quality Wrapper (DQW).

In this post, you’ll learn how to use DQW to preprocess:

* Structured data
* Text data
* Audio data
* Image data

TL;DR? Go to the [app](https://share.streamlit.io/soft-nougat/dqw-ivves/app.py?ref=streamlit.ghost.io) straight away.🚀  Or jump into the [code!](https://github.com/soft-nougat/dqw-ivves?ref=streamlit.ghost.io) 👩🏽‍💻

But before we dive into the fun stuff, let’s talk about...

## What’s the purpose of DQW?

Sogeti is the Technology and Engineering Services Division of [Capgemini](https://www.capgemini.com/?ref=streamlit.ghost.io). We’re an IT consultancy for testing, cloud, cyber security, and AI. [Sogeti NL’s](https://www.sogeti.nl/?ref=streamlit.ghost.io) data science team (where I work) is always looking for ways to automate our workflow. We made DQW as part of [ITEA IVVES](https://itea4.org/project/ivves.html?ref=streamlit.ghost.io)—a project that focuses on testing AI models in various development phases.

Another product we’re developing is in this project is the [Quality AI Framework](https://www.sogeti.nl/nieuws/artificial-intelligence/blogs/artificial-intelligence-quality-framework?ref=streamlit.ghost.io). To ensure data quality, we use DQW in its initial Data Understanding and Data Preparation phases:

![1_tNZWLX9aUinvjYYCxfih3g](https://streamlit.ghost.io/content/images/2022/03/1_tNZWLX9aUinvjYYCxfih3g.png#browser)

DQW is an accelerator for the Quality AI Framework. It demonstrates the functionality of useful packages and methods around data handling and preprocessing:

| App (sub)section | Description | Visualization | Preprocessing | Package |
| --- | --- | --- | --- | --- |
| Synthetic structured | x | x |  | [table-evaluator](https://github.com/Baukebrenninkmeijer/table-evaluator?ref=streamlit.ghost.io) |
| Structured | x | x |  | [sweetviz](https://github.com/fbdesignpro/sweetviz?ref=streamlit.ghost.io) |
| Structured | x | x |  | [pandas-profiling](https://github.com/ydataai/pandas-profiling?ref=streamlit.ghost.io) |
| Structured, text |  |  | x | [PyCaret](https://github.com/pycaret/pycaret?ref=streamlit.ghost.io) |
| Text | x |  | x | [NLTK](https://github.com/nltk/nltk?ref=streamlit.ghost.io) |
| Text | x |  | x | [spaCy](https://github.com/explosion/spaCy?ref=streamlit.ghost.io) |
| Text | x |  | x | [TextBlob](https://github.com/sloria/TextBlob?ref=streamlit.ghost.io) |
| Text | x | x |  | [word\_cloud](https://github.com/amueller/word_cloud?ref=streamlit.ghost.io) |
| Text | x |  | x | [Textstat](https://github.com/shivam5992/textstat?ref=streamlit.ghost.io) |
| Image | x | x | x | [Pillow](https://github.com/python-pillow/Pillow?ref=streamlit.ghost.io) |
| Audio | x | x |  | [librosa](https://github.com/librosa/librosa?ref=streamlit.ghost.io) |
| Audio | x | x |  | [dtw](https://github.com/pierre-rouanet/dtw?ref=streamlit.ghost.io) |
| Audio |  |  | x | [audiomentations](https://github.com/iver56/audiomentations?ref=streamlit.ghost.io) |
| Audio | x | x |  | [AudioAnalyzer](https://github.com/QED0711/audio_analyzer?ref=streamlit.ghost.io) |
| Report generation | x |  |  | [FPDF](https://github.com/Setasign/FPDF?ref=streamlit.ghost.io) |
| Report generation | x |  |  | [wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf?ref=streamlit.ghost.io) |
| Report generation | x |  |  | [PDFKit](https://github.com/JazzCore/python-pdfkit?ref=streamlit.ghost.io) |

You can use DQW to preprocess structured data (synthetic data included!), text, images, and audio. Use the main selectbox to navigate through these data formats. Follow the **Steps** in the sidebar to navigate through the **subsections**:

![subsections-copy](https://streamlit.ghost.io/content/images/2022/03/subsections-copy.png#browser)

## How to preprocess structured data

The main page of the app offers structured data analysis. Structured data is data in a well-defined format used in various ML applications. The app offers one-file analysis and preprocessing, two-file comparison, and synthetic data evaluation.

### How to analyze one file

Select one file analysis in **Step 1**, upload your file in **Step 2,** and select EDA in **Step 3**. You can also download the report in **Step 4**. Coding this was easy thanks to the [Streamlit pandas-profiling component](https://github.com/okld/streamlit-pandas-profiling?ref=streamlit.ghost.io):

```
import streamlit as st
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

uploaded_data = st.sidebar.file_uploader('Upload dataset', type='csv')
data = pd.read_csv(uploaded_data)

# create the pandas profiling report
pr = data.profile_report()
st_profile_report(pr)
# optional, save to file
pr.to_file('pandas_prof.html')
```

### How to preprocess one file

Select one file analysis in **Step 1**, upload your file in **Step 2,** select Preprocess and compare in **Step 3**. In **Steps 4 and 5** you can download the report, the files, and the pipeline pickle:

![](https://streamlit.ghost.io/content/images/2022/03/Sogeti_preprocess-GIF.gif)

In this subsection, we use [PyCaret](https://github.com/pycaret/pycaret?ref=streamlit.ghost.io)—a workflow automation package. Streamlit widgets make it easy to select which preprocessing steps you want to run. You can display these steps as a diagram, compare the original and the preprocessed file, and download the report, the files, and the pipeline pickle. The pipeline pickle helps you use PyCaret modeling functions, especially in the case of imbalanced class mitigation with [SMOTE](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/?ref=streamlit.ghost.io). The code used is in the [structured\_data.py](https://github.com/soft-nougat/dqw-ivves/blob/master/tabular_eda/structured_data.py?ref=streamlit.ghost.io) script (see [preprocess](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/tabular_eda/structured_data.py?ref=streamlit.ghost.io#L266) and [show\_pp\_file](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/tabular_eda/structured_data.py?ref=streamlit.ghost.io#L376) functions).

### How to compare two files

Select two file comparison in **Step 1**, upload your files in **Step 2,** and download the report in **Step 3**. In this subsection, we use  [Sweetviz](https://github.com/fbdesignpro/sweetviz?ref=streamlit.ghost.io)—an automated EDA library in Python. And to show the report on the app, we use the Streamlit HTML components function:

```
import streamlit as st
import streamlit.components.v1 as components
import sweetviz as sv

uploaded_ref = st.sidebar.file_uploader('Upload reference dataset', type='csv')
ref= pd.read_csv(uploaded_ref)

uploaded_comparison = st.sidebar.file_uploader('Upload comparison dataset', type='csv')
comparison = pd.read_csv(uploaded_comparison)

sw = sv.compare([ref, 'Reference'], [comparison, 'Comparison'])

sw.show_html(open_browser=False, layout='vertical', scale=1.0)

display = open('SWEETVIZ_REPORT.html', 'r', encoding='utf-8')

source_code = display.read()

# you can pass width as well to configure the size of the report
components.html(source_code, height=1200, scrolling=True)
```

### How to evaluate synthetic data

Select synthetic data comparison in **Step 1**, upload your files in **Step 2,** choose one of the two package methods in **Step 3,** and download the report and the files in **Step 4**. Here we use the [table-evaluator](https://github.com/Baukebrenninkmeijer/table-evaluator?ref=streamlit.ghost.io) package. It checks all statistical properties (PCA included) and offers multiple model performance comparisons with the original and synthetic dataset:

![te-copy](https://streamlit.ghost.io/content/images/2022/03/te-copy.png#browser)

The code is in the structured\_data.py ([table\_evaluator\_comparison](https://github.com/soft-nougat/dqw-ivves/blob/7c4a4f0f576ce96cfc54f2f9b2050d4ae8cd2dc6/tabular_eda/structured_data.py?ref=streamlit.ghost.io#L181)), [te.py](https://github.com/soft-nougat/dqw-ivves/blob/7c4a4f0f576ce96cfc54f2f9b2050d4ae8cd2dc6/tabular_eda/te.py?ref=streamlit.ghost.io), [viz.py](https://github.com/soft-nougat/dqw-ivves/blob/7c4a4f0f576ce96cfc54f2f9b2050d4ae8cd2dc6/tabular_eda/viz.py?ref=streamlit.ghost.io), and [metrics.py](https://github.com/soft-nougat/dqw-ivves/blob/7c4a4f0f576ce96cfc54f2f9b2050d4ae8cd2dc6/tabular_eda/metrics.py?ref=streamlit.ghost.io). The report and the files are zipped. Here is the code used in the app:

```
def generate_zip_structured(original, comparison):
    """ A function to write files to disk and zip 'em """
    original.to_csv('pdf_files/synthetic_data/reference_file_dqw.csv', 
               index=False)
    comparison.to_csv('pdf_files/synthetic_data/comparison_file_dqw.csv', 
               index=False)
    # create a ZipFile object
    dirName = "pdf_files/synthetic_data"
    with ZipFile('pdf_files/synthetic_data.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
        	for filename in filenames:
        		#create complete filepath of file in directory
        		filePath = os.path.join(folderName, filename)
        		# Add file to zip
        		zipObj.write(filePath, basename(filePath))

zip = generate_zip_structured(original, comparison)

# sidebar download, you can remove the sidebar api to have the normal download button
with open('pdf_files/synthetic_data/report_files_dqw.zip', 'rb') as fp:
	st.sidebar.download_button(
	'⬇️',
	data=fp,
	file_name='te_compare_files_dqw.zip',
	mime='application/zip'
	)
```

## How to preprocess text data

Text data is unstructured and is used in NLP models. The text data section offers the flexibility of pasting a body of text or uploading a CSV/JSON file for analysis. Currently, it supports only English, but it offers a lot of analysis methods and automated data preprocessing.

### How to preprocess data

Select your data input method in **Step 1** and run preprocessing:

![pp-copy](https://streamlit.ghost.io/content/images/2022/03/pp-copy.png#browser)

This subsection relies on multiple text-preprocessing functions like stemming, lemmatization, de-noising, and stop-word removal. These steps prepare text data in a machine-readable way. You can download the preprocessed file. The code is in the [preprocessor.py](https://github.com/soft-nougat/dqw-ivves/blob/master/text_eda/preprocessor.py?ref=streamlit.ghost.io) script.

### How to do topic analysis with LDA

Select your data input method in **Step 1,** run preprocessing (optional), and select topic modeling in **Step 2**. Choose the topics you want to run or calculate the optimal number of topics based on the u\_mass coherence score. LDA topics are visualized in an interactive plot by using [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/readme.html?ref=streamlit.ghost.io). The code is in the [lda.py](https://github.com/soft-nougat/dqw-ivves/blob/master/text_eda/lda.py?ref=streamlit.ghost.io) script:

![](https://streamlit.ghost.io/content/images/2022/03/Sogeti_topic-GIF-1.gif)

### How to do sentiment analysis

Select your data input method in **Step 1,** run preprocessing (optional) and select sentiment in **Step 2**. You can do sentiment analysis with [Vader](https://github.com/cjhutto/vaderSentiment?ref=streamlit.ghost.io) and [textblob](https://textblob.readthedocs.io/en/dev/?ref=streamlit.ghost.io). It’s an easy way to get the polarity of input text data. The code is in the [polarity.py](https://github.com/soft-nougat/dqw-ivves/blob/master/text_eda/polarity.py?ref=streamlit.ghost.io) script:

![polarity-copy](https://streamlit.ghost.io/content/images/2022/03/polarity-copy.png#browser)

## How to preprocess audio data

Audio data is unstructured and used in audio signal processing algorithms such as music genre recognition and automatic speech recognition. The audio data section offers data augmentation, EDA, and comparison of two audio files.

### How to analyze one file

Upload one file in **Step 1** and select EDA only in **Step 2**. We use plots with [librosa](https://github.com/librosa/librosa?ref=streamlit.ghost.io) to describe the input audio file. The plot descriptions are in the app. The code is in the [audio\_data.py](https://github.com/soft-nougat/dqw-ivves/blob/master/audio_eda/audio_data.py?ref=streamlit.ghost.io) script, function [audio\_eda](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/audio_eda/audio_data.py?ref=streamlit.ghost.io#L264):

![audio-copy](https://streamlit.ghost.io/content/images/2022/03/audio-copy.png#browser)

To upload and display the audio file widget, use this code:

```
import streamlit as st 

audio_file = st.sidebar.file_uploader(label="", 
type=[".wav", ".wave", ".flac", ".mp3", ".ogg"])

st.audio(audio_file , format="audio/wav", start_time=0)
```

### How to augment one file

Upload one file in **Step 1** and select Augmentation in **Step 2**. We use [audiomentations](https://github.com/iver56/audiomentations?ref=streamlit.ghost.io)—a library for the augmentation of audio files. It increases the robustness of the dataset in the case of a lack of training data. The app also runs EDA on the augmented file.

The code is in the [audio\_data.py](https://github.com/soft-nougat/dqw-ivves/blob/master/audio_eda/audio_data.py?ref=streamlit.ghost.io) script, function [augment\_audio](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/audio_eda/audio_data.py?ref=streamlit.ghost.io#L39). Pass the selected augmentation methods to this function with the Streamlit multiselect API, parse the user input as an expression argument, and evaluate it as a Python expression:

```
import streamlit as st 
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift

audio_file = st.sidebar.file_uploader(label="", 
type=[".wav", ".wave", ".flac", ".mp3", ".ogg"])

augmentation_methods = st.multiselect('Select augmentation method:', 
['AddGaussianNoise', 
'TimeStretch', 
'PitchShift', 
'Shift'])  

# add p values to each method and eval parse all list elements
# so they are pushed to global environment as audiomentation methods
augmentation_list = [i + "(p=1.0)" for i in augmentation_methods]
augmentation_final = [eval(i) for i in augmentation_list]

# pass the list to augmentation
augment = Compose(augmentation_list)
```

### How to compare two files

Upload two files in **Step 1** and select Spectrum Compare or DTW in **Step 2**. We compare two files with [Dynamic Time Warping (DTW)](https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd?ref=streamlit.ghost.io), a method for analyzing the maximum path to the similarity of two time-series inputs. The code is in the [audio\_data.py](https://github.com/soft-nougat/dqw-ivves/blob/master/audio_eda/audio_data.py?ref=streamlit.ghost.io) script and the function is [compare\_files](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/audio_eda/audio_data.py?ref=streamlit.ghost.io#L102). Or we compare two files with [audio analyser](https://github.com/QED0711/audio_analyzer/blob/master/main.ipynb?ref=streamlit.ghost.io), a method that compares two spectrums with an applied threshold. The code is in the [audio\_data.py](https://github.com/soft-nougat/dqw-ivves/blob/master/audio_eda/audio_data.py?ref=streamlit.ghost.io) script and the function is [audio\_compare](https://github.com/soft-nougat/dqw-ivves/blob/52a1f1a8f68e561f543d603c7878380175398c7a/audio_eda/audio_data.py?ref=streamlit.ghost.io#L68):

![](https://streamlit.ghost.io/content/images/2022/03/Sogeti_compare-GIF.gif)

## How to preprocess image data

The image data section offers data augmentation and EDA of your images.

### How to augment images

Upload a dataset in **Step 1,** select Augmentations in **Step 2,** and download data in **Step 3**. here we use [Pillow](https://pillow.readthedocs.io/en/stable/?ref=streamlit.ghost.io). It offers image resizing, noise application, and contrast and brightness adjustment. Thanks to session state you can apply multiple augmentations in a sequence and go back to the previous state if you need to. The code is in the [augment.py](http://augment.py/?ref=streamlit.ghost.io) script:

![image-copy](https://streamlit.ghost.io/content/images/2022/03/image-copy.png#browser)

## BONUS: A few handy tricks for app design

You can find a lot of helpful design functions in the [helper\_functions.py](https://github.com/soft-nougat/dqw-ivves/blob/master/helper_functions.py?ref=streamlit.ghost.io) script. Here are a few tricks I use for all my Streamlit apps:

**Local file as a background hack.** This is a lifesaver. Simply use this code to pass a local file and open it as background:

```
def set_bg_hack(main_bg):
	'''
	A function to unpack an image from root folder and set as bg.
	
	Returns
	-------
	The background.
	'''
	# set bg name
	main_bg_ext = "png"
	  
	st.markdown(
	   f"""
	   <style>
	   .stApp {{
	       background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
	       background-size: cover
	   }}
	   </style>
	   """,
	   unsafe_allow_html=True
	)
```

**Custom themes.** Streamlit offers an easy way of secondary app styling through their UI. Check it out [here.](https://share.streamlit.io/streamlit/theming-showcase-blue/main?ref=streamlit.ghost.io)

**The sidebar design.** You can change the width of your sidebar with this simple code:

```
# set sidebar width
st.markdown(
"""
<style>
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 300px;
}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    width: 300px;
    margin-left: -300px;
}
</style>
""",
unsafe_allow_html=True,
)
```

I prefer to move all of the high-level user-defined steps to the sidebar: upload widgets, select boxes, etc. It’s very simple. Just add .sidebar to call the relevant API:

```
import streamlit as st

# add a logo to the sidebar
logo = Image.open("logo.png")
st.sidebar.image(logo, use_column_width=True)

# upload widget
file = st.sidebar.file_uploader("Upload file here")

# selectbox
add_selectbox = st.sidebar.selectbox(
    "What would you like to do?",
    ("EDA", "Preprocess", "Report")
)
```

**Passing HTML code as text.** Since this is a very robust app with a lot of components that need to be explained, in some cases it’s useful to pass HTML code as text. Use this function:

```
def sub_text(text):
    '''
    A function to neatly display text in app.
    Parameters
    ----------
    text : Just plain text.
    Returns
    -------
    Text defined by html5 code below.
    '''
    
    html_temp = f"""
    <p style = "color:#1F4E79; text_align:justify;"> {text} </p>
    </div>
    """
    
    st.markdown(html_temp, unsafe_allow_html = True)
```

**Expanders for more information and references.** The expanders are a space-saver in robust apps with a lot of text:

```
import streamlit as st

info = st.expander("Click here for more info on methods used")
with info:
  st.markdown("More information")
```

## Wrapping up

Use the DQW app to automate your data preprocessing during AI model development. It’ll streamline your workflow and ensure transparency and quality. The app is still in development and is one of the many Streamlit apps we’ve created. We hope it’ll help educate the data science community about data-centric model development and data quality methods.

If you have questions, please leave them in the comments below or reach out to me at [tia.nikolic@sogeti.com](mailto:tia.nikolic@sogeti.com) or on [LinkedIn](https://www.linkedin.com/in/tijana-nikoli%C4%87-99b059110/?ref=streamlit.ghost.io).

Thank you for reading this post, and happy app-building! 🎈

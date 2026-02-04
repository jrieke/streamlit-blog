---
title: "Build an image background remover in Streamlit"
subtitle: "Skip the fees and do it for free! \ud83c\udf88"
date: 2023-01-10
authors:
  - "Tyler Simons"
category: "Tutorials"
---

![Build an image background remover in Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/12/background-image-removal.svg)


You’ve finally found it! 😮

After hours and hours of searching, you’ve found the ********best******** image of a wallaby for your class presentation about Australian wildlife. It’d look great next to your tips on staying safe in the rugged outback (bring lots of water💧).

But there’s one problem. It has a GREEN 🟩 BACKGROUND. Green *totally* doesn’t fit your vibe. So you start searching for web-based image processing services and discount them one by one:

1. $0.25 per image? Nope.
2. I need an account? No, thanks.
3. Won’t let me download my image at full resolution? Absolutely not.

“This will never work”, you think. “But wait! I know some Python and have the magical tools of Streamlit. Can I do this myself?”

Yep, 100%! You can build a high-quality image background remover yourself. In this tutorial, I’ll teach you:

* How to set up your development environment
* How to upload and download images
* How to use the `rembg` package to remove backgrounds from images with Python
* How to put it all together in a neatly formatted Streamlit app 🤯

💡

Want to skip straight to the app? Sure thing! Here’s [the app](https://bgremoval.streamlit.app/?ref=streamlit.ghost.io) and here’s [the code](https://github.com/tyler-simons/BackgroundRemoval?ref=streamlit.ghost.io) on Github.

## How to set up your development environment

In a new folder, make a virtual environment just for this project. Pull out your handy-dandy terminal and run the following:

```
# Set up our folder
cd ~/Documents
mkdir Streamlit-Image-Remover
cd Streamlit-Image-Remover

# Create and source our virtual environment
python3 -m venv venv
source venv/bin/activate
```

This will let you separate your local packages from the rest of your ecosystem—the standard best practice. Once it’s set up, install the following packages (to use everything available in Streamlit and the awesome Python library [rembg](https://github.com/danielgatis/rembg?ref=streamlit.ghost.io)):

```
pip install streamlit
pip install rembg
```

Next, download the [source image](https://upload.wikimedia.org/wikipedia/commons/7/74/Red_necked_wallaby444.jpg?ref=streamlit.ghost.io), save it in the same folder as the app, and call it `wallaby.png`.

## How to upload and download images

Streamlit makes uploading and downloading files easy. Just define the file types you’d like to accept in the arguments and give the functions some labels:

* `st.file_uploader()` accepts a label and allowed file types.
* `st.download_button()` accepts a label, a Python object, a file name, and a file type.

For your new folder `Streamlit-Image-Remover/`, open a code editor (VSCode or PyCharm), make a new file, and add the following:

```
import streamlit as st

st.title("Hello Upload!")

# Upload the image
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Now, you can download the same file!
if image_upload:
	st.download_button("Download your file here", image_upload, "my_image.png", "image/png")
```

Save the Python file as `bg_remove.py` and run the app to try it out:

```
streamlit run bg_remove.py
```

![hello-upload-1](https://streamlit.ghost.io/content/images/2022/12/hello-upload-1.png#border)

You did it!

Now upload the `wallaby.png` image and download it again if you want to try it out. 💥

## How to use the rembg package to remove backgrounds from images with Python

You want your app to work in 3 steps:

1. A user uploads an image
2. The `rembg` package transforms it
3. The user downloads the transformed image

Steps 1 and 3 are done. For step 2, change the code to:

```
# We need a few more packages
from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove

st.title("Hello Upload!")

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Convert the image to BytesIO so we can download it
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# If we've uploaded an image, open it and remove the background!
if image_upload:
    image = Image.open(image_upload)
    fixed = remove(image)
    downloadable_image = convert_image(fixed)
    st.download_button(
        "Download fixed image", downloadable_image, "fixed.png", "image/png"
    )
```

Here is what you just did:

1. You imported three more packages:

* `io.BytesIO` and `PIL.Image` to help with file types and memory management;
* `rembg.remove` to remove the backgrounds;

1. You added a  `convert_image()` function to manage the file types for downloading.

That’s it! Upload your `wallaby.png` image and take a look at the app…

![hello-upload-2](https://streamlit.ghost.io/content/images/2022/12/hello-upload-2.png#border)

Download your image. The background has been removed like magic! 🪄

Awesome job. Your picture looks *so* good. 👍

## How to put it all together in a neatly formatted Streamlit app 🤯

Wouldn’t it be nice to see the before-and-after image in the app? Streamlit makes it easy! Just add a few calls to `st.image`:

```
from io import BytesIO

import streamlit as st
from PIL import Image
from rembg import remove

st.title("Hello Upload!")

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Convert the image to BytesIO so we can download it!
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# If we've uploaded an image, open it and remove the background!
if image_upload:
    # SHOW the uploaded image!
    st.image(image_upload)
    image = Image.open(image_upload)
    fixed = remove(image)
    downloadable_image = convert_image(fixed)
    # SHOW the improved image!
    st.image(downloadable_image)
    st.download_button(
        "Download fixed image", downloadable_image, "fixed.png", "image/png"
    )
```

You can see the images now, but it’s a bit clunky to scroll down.

![hello-upload-3](https://streamlit.ghost.io/content/images/2022/12/hello-upload-3.png#border)

What if they were next to each other in columns? Let’s move some components around so it looks more professional:

1. Put upload and download on `st.sidebar`.
2. Use `st.columns` to arrange the pre- and post-images side-by-side.
3. Use `st.set_page_config` to set a widescreen layout and `st.write` for commentary.
4. Add **a default image** to get a quick preview of the app every time you open it and save `wallaby.png` in the same folder.

```
from io import BytesIO

import streamlit as st
from PIL import Image
from rembg import remove

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](<https://github.com/tyler-simons/BackgroundRemoval>) on GitHub. Special thanks to the [rembg library](<https://github.com/danielgatis/rembg>) :grin:"
)
st.sidebar.write("## Upload and download :gear:")

# Create the columns
col1, col2 = st.columns(2)

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Package the transform into a function
def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\\n")
    st.sidebar.download_button(
        "Download fixed image", convert_image(fixed), "fixed.png", "image/png"
    )

# Create the file uploader
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Fix the image!
if my_upload is not None:
    fix_image(upload=my_upload)
else:
    fix_image("./wallaby.png")
```

Here’s how it looks:

![remove-background-from-your-image](https://streamlit.ghost.io/content/images/2022/12/remove-background-from-your-image.png#border)

Your image is ready for your class presentation and your app is ready for showtime! Don’t forget to add your app to a GitHub repo (follow [these steps](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app?ref=streamlit.ghost.io)), then post it on Twitter, and tag @streamlit. 🎈

## Wrapping up 🎁

Congratulations! You can now remove backgrounds from images whenever you want to—for free. And if you want to make your app even better, you can add:

1. Support for videos and GIFs.
2. File type conversion (to pick the file output type).
3. Image sizing (how about making tiny images and turning them into emojis?).

That’s it. You’ve earned it. Grab some ice cream 🍦 and take the rest of the day off.

Happy Streamlit-ing! 🎈

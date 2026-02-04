---
title: "How to Create Automated Visual Tests [SeleniumBase Tutorial]"
subtitle: "How to create automated visual tests"
date: 2020-11-23
authors:
  - "Randy Zwitch"
category: "Tutorials"
---

![Testing Streamlit apps using SeleniumBase](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--21-.svg)


In the time I’ve worked at Streamlit, I’ve seen hundreds of impressive data apps ranging from computer vision applications to public health [tracking of COVID-19](https://discuss.streamlit.io/t/data-apps-regarding-covid-19/2203?ref=streamlit.ghost.io) and even simple [children’s games](https://joelgrus.com/2020/10/02/creating-games-in-streamlit/?ref=streamlit.ghost.io). I believe the growing popularity of Streamlit comes from the fast, iterative workflows through the [Streamlit “magic”](https://docs.streamlit.io/en/stable/api.html?highlight=magic&ref=streamlit.ghost.io#magic-commands) functionality and auto-reloading the front-end upon saving your Python script. Write some code, hit ‘Save’ in your editor, then visually inspect the correctness of each code change. And with the unveiling of [Streamlit sharing](https://www.streamlit.io/sharing?ref=streamlit.ghost.io) for easy deployment of Streamlit apps, you can go from idea to coding to deploying your app in just minutes!

Once you've created a Streamlit app, you can use automated testing to future-proof it against regressions. In this post, I'll be showing how to programmatically validate that a Streamlit app is unchanged visually using the Python package [SeleniumBase](https://seleniumbase.io/?ref=streamlit.ghost.io).

## Case Study: streamlit-folium

To demonstrate how to create automated visual tests, I’m going to use the [streamlit-folium GitHub repo](https://github.com/randyzwitch/streamlit-folium?ref=streamlit.ghost.io), a Streamlit Component I created for the [Folium Python library for leaflet.js](https://python-visualization.github.io/folium/?ref=streamlit.ghost.io). [Visual regression tests](https://baseweb.design/blog/visual-regression-testing/?ref=streamlit.ghost.io) help detect when the layout or content of an app changes, without requiring the developer to manually visually inspect the output each time a line of code changes in their Python library. Visual regression tests also help with cross-browser compatibility of your Streamlit apps and provide advanced warning about new browser versions affecting how your app is displayed.

![5-7](https://streamlit.ghost.io/content/images/2021/08/5-7.png#browser)

### Setting up a test harness

The streamlit-folium test harness has three files:

* [`tests/requirements.txt`](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/requirements.txt?ref=streamlit.ghost.io): the Python packages only needed for testing
* [`tests/app_to_test.py`](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/app_to_test.py?ref=streamlit.ghost.io): the reference Streamlit app to test
* [`tests/test_package.py`](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/test_package.py?ref=streamlit.ghost.io): the tests to demonstrate the package works as intended

The first step is to create a Streamlit app using the package to be tested and use that to set the baseline. We can then use SeleniumBase to validate that the structure and visual appearance of the app remains unchanged relative to the baseline.

This post focuses on describing `test_package.py` since it’s the file that covers how to use SeleniumBase and OpenCV for Streamlit testing.

### Defining test success

There are several ways to think about what constitutes looking *the same* in terms of testing. I chose the following three principles for testing my streamlit-folium package:

1. The [Document Object Model (DOM) structure](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction?ref=streamlit.ghost.io) (but not necessarily the values) of the page should remain the same
2. For values such as headings, test that those values are exactly equal
3. Visually, the app should look the same

I decided to take these less strict definitions of “unchanged” for testing streamlit-folium, as the internals of the Folium package itself appear to be non-deterministic. Meaning, the same Python code will create the same *looking* image, but the generated HTML will be different.

## Testing using SeleniumBase

SeleniumBase is an all-in-one framework written in Python that wraps the [Selenium WebDriver](https://www.selenium.dev/?ref=streamlit.ghost.io) project for browser automation. SeleniumBase has two functions that we can use for the first and second testing principles listed above: [check\_window](https://seleniumbase.io/examples/visual_testing/ReadMe/?ref=streamlit.ghost.io#automated-visual-regression-testing), which tests the DOM structure and [assert\_text](https://seleniumbase.io/help_docs/method_summary/?ref=streamlit.ghost.io), to ensure a specific piece of text is shown on the page.

To check the DOM structure, we first need a baseline, which we can generate using the `check_window` function. The `check_window` has two behaviors, based on the required `name` argument:

* If a folder <**name>** within the `visual_baseline/<Python file>.<test function name>` path does not exist, this folder will be created with all of the baseline files
* If the folder *does exist*, then SeleniumBase will compare the current page against the baseline at the specified accuracy level

You can see an example of calling [check\_window](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/test_package.py?ref=streamlit.ghost.io#L19) and the resulting [baseline files](https://github.com/randyzwitch/streamlit-folium/tree/master/tests/visual_baseline/test_package.test_basic/first_test?ref=streamlit.ghost.io) in the streamlit-folium repo. In order to keep the baseline constant between runs, I committed these files to the repo; if I were to make any substantive changes to the app I am testing (`app_to_test.py`), I would need to remember to set the new baseline or the tests would fail.

With the baseline folder now present, running check\_window runs the comparison test. I chose to run the test at **Level 2**, with the level definitions as follows:

* **Level 1 (least strict)**: HTML tags are compared to [tags\_level1.txt](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/visual_baseline/test_package.test_basic/first_test/tags_level_1.txt?ref=streamlit.ghost.io)
* **Level 2**: HTML tags and attribute names are compared to [tags\_level2.txt](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/visual_baseline/test_package.test_basic/first_test/tags_level_2.txt?ref=streamlit.ghost.io)
* **Level 3 (most strict)**: HTML tags, attribute names and attribute values are compared to [tags\_level3.txt](https://github.com/randyzwitch/streamlit-folium/blob/master/tests/visual_baseline/test_package.test_basic/first_test/tags_level_3.txt?ref=streamlit.ghost.io)

As mentioned in the “Defining Test Success” section, I run the `check_window` function at Level 2, because the Folium library adds an GUID-like id value to the attribute values in the HTML, so the tests will never pass at Level 3 because the attribute values are always different between runs.

For the second test principle (“check certain values are equal”), the `assert_text` method is very easy to run:

`self.assert_text("streamlit-folium")`

This function checks that the exact text “streamlit-folium” is present in the app, and the test passes because it’s the value of the H1 heading in this example.

## Testing using OpenCV

While checking the DOM structure and presence of a piece of text provides some useful information, my true acceptance criterion is that the visual appearance of the app doesn’t change from the baseline. In order to test that the app is visually the same *down to the pixel*, we can use the `save_screenshot` method from SeleniumBase to capture the current visual state of the app and compare to the baseline using the OpenCV package:

Using OpenCV, the first step is to read in the baseline image and the current snapshot, then compare that the size of the pictures are identical (the `shape` comparison checks that the NumPy ndarrays of pixels have the same dimensions). Assuming the pictures are both the same size, we can then use the `subtract` function from OpenCV to calculate the per-element difference between pixels by channel (blue, green and red). If all three channels have no differences, then we know that the visual representation of the Streamlit app is identical between runs.

## Automating tests using GitHub actions

With our SeleniumBase and OpenCV code set up, we can now feel free to make changes to our Streamlit Component (or other Streamlit apps) and not worry about things breaking unintentionally. In my single-contributor project, it’s easy to enforce running the tests locally, but with tools such as [GitHub Actions available for free for open-source projects](https://github.blog/2019-08-08-github-actions-now-supports-ci-cd/?ref=streamlit.ghost.io), setting up a [Continuous Integration pipeline](https://www.infoworld.com/article/3271126/what-is-cicd-continuous-integration-and-continuous-delivery-explained.html?ref=streamlit.ghost.io) guarantees the tests are run for each commit.

The streamlit-folium has a workflow [`run_tests_each_PR.yml`](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io) defined that does the following:

* Sets up a [test matrix for Python 3.6, 3.7, 3.8](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L18)
* Installs the [package dependencies](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L30) and [test dependencies](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L31)
* [Lints the code](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L35-L37) with flake8
* [Install Chrome with seleniumbase](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L40)
* [Run the Streamlit app](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L43) to test in the background
* Run the [SeleniumBase and OpenCV tests in Python](https://github.com/randyzwitch/streamlit-folium/blob/master/.github/workflows/run_tests_each_PR.yml?ref=streamlit.ghost.io#L46)

By having this workflow defined in your repo, and [required status checks enabled on GitHub](https://docs.github.com/en/github/administering-a-repository/enabling-required-status-checks?ref=streamlit.ghost.io), every pull request will now have the following status check appended to the bottom, letting you know the status of your changes:

![6-5](https://streamlit.ghost.io/content/images/2021/08/6-5.png#border)

## Writing tests saves work in the long run

Having tests in your codebase has numerous benefits. As explained above, automating visual regression tests allows you to maintain an app without having to have a human in the loop looking for changes. Writing tests is also a great signal to potential users that you care about stability and long-term maintainability of your projects. It’s not only easy to write tests for a Streamlit app and have them automatically run on each GitHub commit, but that the extra work of adding tests to your Streamlit project will save you time in the long run.

*Have questions about this post or Streamlit in general? Stop by the [Streamlit Community forum](https://discuss.streamlit.io/?ref=streamlit.ghost.io), start a discussion, meet other Streamlit enthusiasts, find a collaborator in the [Streamlit Component tracker](https://discuss.streamlit.io/t/streamlit-components-community-tracker/4634?ref=streamlit.ghost.io) or [share your Streamlit project](https://discuss.streamlit.io/c/streamlit-examples/9?ref=streamlit.ghost.io)! There are plenty of ways to get involved in the Streamlit community and we look forward to welcoming you 🎈*

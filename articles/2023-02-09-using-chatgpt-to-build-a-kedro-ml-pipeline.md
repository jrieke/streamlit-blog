---
title: "Using ChatGPT to build a Kedro ML pipeline"
subtitle: "Talk with ChatGPT to build feature-rich solutions with a Streamlit frontend"
date: 2023-02-09
authors:
  - "Arvindra Sehmi"
category: "LLMs"
---

![Using ChatGPT to build a Kedro ML pipeline](https://streamlit.ghost.io/content/images/size/w2000/2023/02/Announcement--2--1.svg)


Hi, community! 👋

My name is Arvindra Sehmi. I've been a life-long learner with too many degrees and far too many years of research and work in academia and the tech industry - 35 years and counting! I’m on a career break (advising [Auth0.com](http://auth0.com/?ref=streamlit.ghost.io), [Macrometa.com](http://macrometa.com/?ref=streamlit.ghost.io), [Tangle.io](http://tangle.io/?ref=streamlit.ghost.io), [Crowdsense.ai](https://crowdsense.ai/?ref=streamlit.ghost.io), and [DNX ventures](https://www.dnx.vc/?ref=streamlit.ghost.io)) and am taking the opportunity to learn new software development tools and enjoy being an active member of the Streamlit Creators group.

I recently came across an open-source Python DevOps framework [Kedro](https://kedro.org/?ref=streamlit.ghost.io) and thought, “Why not have [ChatGPT](https://chat.openai.com/chat?ref=streamlit.ghost.io) teach me how to use it to build some ML/DevOps automation?” The idea was to write my questions with hints that encouraged explanations of advanced Kedro features (to evolve incrementally as if a teacher taught me).

I planned to ask ChatGPT how to:

1. Use basic Kedro.
2. Use more advanced features in the Kedro framework.
3. Display pipeline graphs in Streamlit.
4. Build an example ML model and explicitly refer to it in the Kedro pipeline.
5. Scale the pipeline and perform pipeline logging, monitoring, and error handling.
6. Connect Kedro logs to a cloud-based logging service.
7. Contrast Kedro with similar (competing) products and services and show me how the earlier-developed pipeline could be implemented in one of them.

What follows are the annotated responses. I was super impressed. Will you be? (This is a long post, so if you want, dive right into [the app](https://kedro-ml-pipeline.streamlit.app/?ref=streamlit.ghost.io) and [the repo](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app?ref=streamlit.ghost.io).)

⛔

The generated Kedro code was simplistic and in some cases wrong, but perfectly okay to work with. My app is original, with small parts of it taken from Kedro's code template, so it can be used without any recourse under my MIT license. As to ChatGPT, though it's powerful, be aware of its potential limitations (see [here](https://www.theregister.com/2022/12/05/stack_overflow_bans_chatgpt/?ref=streamlit.ghost.io) and [here](https://www.theregister.com/2023/01/06/chatgpt_cybercriminals_malicious_code?ref=streamlit.ghost.io)).

## A guided chat in 25 questions

Try replicating my Q&A and see if you get better results, as ChatGPT should be getting smarter from millions of conversations. My opening prompt mentioned the technology I’m interested in learning about.

### Question 1

**Can you show me how to build a Kedro application to ingest data, train an ML model, evaluate the model, and visualize the model evaluation metrics?**

Certainly! Here's an example of how you can build a Kedro application to ingest data, train a machine learning model, evaluate the model, and visualize the model evaluation metrics:

**1. Ingest the data:**

First, you'll need to ingest the data that you want to use for training and evaluating your model. You can use the `DataCatalog` to load your data from a variety of sources, such as a CSV file, a database, or a cloud storage bucket.

For example, you can use the load method of the `DataCatalog` to load data from a CSV file and save it to a data node in your Kedro pipeline:

```
from kedro.io import DataCatalog

# Create a DataCatalog to manage the data for your project
catalog = DataCatalog()

# Load the data from a CSV file and save it to a data node
data = catalog.load("my_data", "./data/my_data.csv")
```

**2. Train the model:**

Next, you'll need to define a function that trains your machine learning model. This function should take the training data as input, and should return the trained model.

Here's an example of how you can define a function to train a simple linear regression model:

```
from sklearn.linear_model import LinearRegression

def train_model(data):
	# Split the data into features and targets
	X = data.drop("target", axis=1)
	y = data["target"]
	# Create a LinearRegression model and fit it to the data
	model = LinearRegression()
	model.fit(X, y)
	return model
```

**3. Evaluate the model:**

After training the model, you'll need to evaluate its performance on a separate test dataset. You can use a variety of evaluation metrics, such as accuracy, precision, and recall, to measure the performance of your model.

Here's an example of how you can define a function to evaluate a model using the mean squared error metric:

```
from sklearn.metrics import mean_squared_error

def evaluate_model(model, data):
	# Split the data into features and targets
	X = data.drop("target", axis=1)
	y = data["target"]
	# Make predictions using the model and calculate the mean squared error
	y_pred = model.predict(X)
	mse = mean_squared_error(y, y_pred)
	return mse
```

**4. Visualize the model evaluation metrics:**

Finally, you can use a library like Matplotlib to visualize the model evaluation metrics. This can help you understand how well your model is performing and identify areas for improvement.

Here's an example of how you can use Matplotlib to visualize the mean squared error for a model:

```
import matplotlib.pyplot as plt

def plot_metric(metric_values):
	# Plot the metric values
	plt.plot(metric_values)
	plt.ylabel("Mean Squared Error")
	plt.xlabel("Iteration")
	plt.show()
```

I hope this helps! Let me know if you have any other questions.

***Comment:*** *That’s a great start. I know decent DevOps frameworks will provide a way to abstract and manage activities in a process. This is called orchestration, so let’s ask about that and implicitly refer to the steps described in the answer above.*

🐛

***Code comment**: [The subsequent implementation](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/crypto_fc/data.py?ref=streamlit.ghost.io#L50) of the above data ingest code didn't work as intended. Kedro has a concept of datasets, and you must first create datasets from source data and then add them to the Kedro DataCatalog, which acts as a central data store for your application. Visualizing evaluation metrics as they are written can also be a problem when integrating with Streamlit because it conflates visualization with processing logic. Personally, I prefer to have these two concerns of any reasonably large application as separate logical layers. In my application, I [save metrics results to a file](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/crypto_fc/nodes.py?ref=streamlit.ghost.io#L53) (but it could be any persistence mechanism) that is [independently accessed](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/streamlit_app.py?ref=streamlit.ghost.io#L259) by my Streamlit presentation layer.*

### Question 2

**Can you use Kedro to orchestrate this series of steps?**

Yes, you can use Kedro to orchestrate the series of steps for ingesting data, training a machine learning model, evaluating the model, and visualizing the model evaluation metrics.

To do this, you can define your steps as Kedro nodes in a pipeline, and use the run method of the `Pipeline` to execute the pipeline.

Here's an example of how you can use Kedro to orchestrate the series of steps that I described in the previous message:

```
from kedro.pipeline import Pipeline, node

# Define the pipeline nodes
def train_model(data):
	# Train the model (as described in the previous message)
	return model
	
def evaluate_model(model, data):
	# Evaluate the model (as described in the previous message)
	return mse
	
def plot_metric(metric_values):
	# Plot the metric values (as described in the previous message)

# Create a pipeline to orchestrate the steps
pipeline = Pipeline([
	node(
		train_model,
		inputs="data",
		outputs="model",
	),
	node(
		evaluate_model,
		inputs=["model", "data"],
		outputs="mse",
	),
	node(
		plot_metric,
		inputs="mse",
	),
])
	
# Execute the pipeline
pipeline.run(catalog)
```

This will execute the pipeline, which will ingest the data, train the model, evaluate the model, and visualize the model evaluation metrics.

I hope this helps! Let me know if you have any other questions.

***Comment:** ChatGPT introduced the concept of a pipeline, which is nice. The steps are now encapsulated. An essential part of any ML experiment is tuning model parameters, so let’s ask to include a hyperparameter tuning step in the pipeline.*

🐛

***Code comment***: *It makes sense that a pipeline should be run as shown by ChatGPT above. However, it turns out that Kedro requires a pipeline runner to orchestrate pipeline node execution. There are several kinds of runners, and I [chose to use the simplest](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/crypto_fc/pipeline.py?ref=streamlit.ghost.io#L52) SequentialRunner. This ChatGPT mistake appeared in several of it's subsequent responses, so please take note.*  
  
*Since Kedro pipelines need to be command-line executable so that they can be included in CI (continuous integration) processes, pipelines and data catalogs need to be discoverable by Kedro's CLI (command-line interface) tool chain. To enable this, Kedro requires various [externalized configurations](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/main/pyproject.toml?ref=streamlit.ghost.io) and pipeline registration patterns to be defined (see [here](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/crypto_fc/pipeline_registry.py?ref=streamlit.ghost.io#L8) and [here](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/crypto_fc/pipeline.py?ref=streamlit.ghost.io#L8)). It wasn't complicated to replicate these in my application from Kedro's [example template projects](https://kedro.readthedocs.io/en/stable/get_started/new_project.html?ref=streamlit.ghost.io).*  
  
*So while ChatGPT gave me a head start, there was still some work to be done.*

### Question 3

**Can you add hyperparameter tuning to the steps and the Kedro orchestration pipeline?**

Yes, you can add hyperparameter tuning to the steps for training a machine learning model and the Kedro orchestration pipeline.

To do this, you can use a library like scikit-learn's `GridSearchCV` to search for the best hyperparameter values for your model. `GridSearchCV` performs an exhaustive search over a specified parameter grid, and returns the best set of hyperparameters based on cross-validated performance.

Here's an example of how you can use `GridSearchCV` to add hyperparameter tuning to the training step of your pipeline:

```
from sklearn.model_selection import GridSearchCV

def train_model(data, hyperparams):
	# Split the data into features and targets
	X = data.drop("target", axis=1)
	y = data["target"]
	# Create a LinearRegression model
	model = LinearRegression()
	# Create a parameter grid for the hyperparameters
	param_grid = {
		"fit_intercept": [True, False],
		"normalize": [True, False],
	}
	# Use GridSearchCV to search for the best hyperparameters
	grid_search = GridSearchCV(model, param_grid, cv=5)
	grid_search.fit(X, y)
	# Return the best model
	return grid_search.best_estimator_
	
# Define the pipeline nodes
pipeline = Pipeline([
	node(
		train_model,
		inputs="data",
		outputs="model",
		hyperparams=Hyperparameters(param_grid),
	),
	# ... other nodes ...
])
```

This will use `GridSearchCV` to search for the best values for the `fit_intercept` and normalize hyperparameters of the linear regression model, using 5-fold cross-validation.

You can then pass the best set of hyperparameters to the `train_model` function as a Hyperparameters object, and use them to train the model.

I hope this helps! Let me know if you have any other questions.

***Comment:** I like that. It’s what I do in my experiments. I secretly hope that by saying the answer is interesting, my chat session will remain live a little longer (as ChatGPT Preview is prone to terminating sessions without warning). After all I just started and human moderators might be snooping in on the conversation—I want to show them I’m serious. My LSTM ML model is implemented in Keras, and it happens to be a regressor too…a happy coincidence. My regressor has quite a few parameters that require tuning, so I’ll name them for ChatGPT and ask it to use GridSearchCV with those named parameters.*

### Question 4

**Interesting! How can GridSearchCV be used to tune the parameters for a multilayer Tensorflow (Keras) LSTM network with parameters for the lookback, batch size, learning rate, epochs, optimizer, and loss function, and a number of nodes in each network layer, including the output layer?**

You can use `GridSearchCV` to tune the hyperparameters for a multilayer TensorFlow (Keras) Long Short-Term Memory (LSTM) network by defining a custom `KerasClassifier` or `KerasRegressor` model, and passing it to `GridSearchCV` as the estimator.

Here's an example of how you can use `GridSearchCV` to tune the hyperparameters for a multilayer LSTM network for time series forecasting:

```
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_model(lookback, batch_size, learning_rate, optimizer, loss, units):
	# Create a Sequential model
	model = Sequential()
	# Add an LSTM layer with the specified number of units
	model.add(LSTM(units, input_shape=(lookback, 1)))
	# Add a dense output layer
	model.add(Dense(1))
	# Compile the model with the specified optimizer and loss function
	model.compile(optimizer=optimizer, loss=loss, metrics=["mae"])
	return model

# Define the hyperparameter grid
param_grid = {
	"lookback": [10, 20, 30],
	"batch_size": [32, 64, 128],
	"learning_rate": [0.001, 0.01, 0.1],
	"optimizer": ["adam", "sgd"],
	"loss": ["mse", "mae"],
	"units": [32, 64, 128],
}

# Create the KerasClassifier model
model = KerasClassifier(create_model)

# Use GridSearchCV to search for the best hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X, y)

# Print the best set of hyperparameters
print(grid_search.best_params_)
```

This will use `GridSearchCV` to search for the best values for the `lookback`, `batch_size`, `learning_rate`, `optimizer`, `loss`, and `units` hyperparameters of the LSTM network, using 5-fold cross-validation.

You can then use the best set of hyperparameters to train the LSTM network and make forecasts.

I hope this helps! Let me know if you have any other questions.

***Comment:** Great, ChatGPT knows that LSTM regression models are used to create forecasts. However, it probably should’ve wrapped `create_model` in `KerasRegressor`, not `KerasClassifier`. That’s something I’ll check when I try to run the code. Now I want to steer my Q&A in the direction of model evaluation to gain a better understanding of cross-validation.*

### Question 5

**What does cross-validation do?**

Cross-validation is a technique for evaluating the performance of a machine learning model by training and testing the model on different subsets of the data. It helps to reduce the variance of the model's performance estimates and can give you a more accurate picture of how the model will perform on unseen data.

There are several different types of cross-validation, but the most common is k-fold cross-validation. In k-fold cross-validation, the data is split into k folds, and the model is trained and evaluated k times, with a different fold being used as the test set each time.

For example, in 5-fold cross-validation, the data is split into 5 folds, and the model is trained and evaluated 5 times, with a different fold being used as the test set each time. The model's performance is then averaged across the 5 folds to give a final performance estimate.

Cross-validation is useful for hyperparameter tuning because it allows you to evaluate the model's performance on different subsets of the data, which can help you identify the best set of hyperparameters for the model.

I hope this helps! Let me know if you have any other questions.

***Comment:** Let’s ask for more detail on evaluation metrics.*

### Question 6

**What are the different ways of evaluating an LSTM, such as mae, confusion matrix, etc.? How do you implement or visualize these?**

There are several different ways to evaluate the performance of a Long Short-Term Memory (LSTM) network, depending on the type of problem you are trying to solve. Some common evaluation metrics for LSTM networks include:

* **Mean Absolute Error (MAE)**: This metric measures the average magnitude of the errors in the predictions, without considering their direction. It is calculated as the sum of the absolute differences between the predicted values and the true values, divided by the number of predictions.
* **Mean Squared Error (MSE)**: This metric measures the average squared difference between the predicted values and the true values. It is calculated as the sum of the squared differences between the predicted values and the true values, divided by the number of predictions.
* **Confusion Matrix**: This is a matrix that shows the number of correct and incorrect predictions made by the model for each class. It is often used for classification tasks, and can help you understand the types of errors that the model is making.

To implement or visualize these evaluation metrics, you can use a library like scikit-learn. Here's an example of how you can use scikit-learn to calculate and visualize the MAE and MSE for an LSTM network:

```
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Make predictions using the LSTM network
y_pred = model.predict(X_test)

# Calculate the MAE and MSE
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
# Print the results
print(f"MAE: {mae:.3f}")
print(f"MSE: {mse:.3f}")
```

To visualize the confusion matrix, you can use the `confusion_matrix` function from scikit-learn, and use a library like Matplotlib to plot the matrix:

```
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Make predictions using the LSTM network
y_pred = model.predict(X_test)

# Calculate the confusion matrix
confusion_mat = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix
plt.imshow(confusion_mat, cmap="Blues")
plt.colorbar()
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.title("Confusion Matrix")
plt.show()
```

This will plot the confusion matrix as a color-coded matrix, with the predicted classes on the x-axis and the true classes on the y-axis. The color of each cell in the matrix represents the number of predictions made by the model for each class.

I hope this helps! Let me know if you have any other questions.

***Comment:*** *Oops! I made the mistake of mentioning the confusion matrix above, which made ChatGPT lose its context on regression models as confusion matrices don’t apply. I’m going to steer it back on track.*

### Question 7

**What evaluation metrics and visualizations are used for Time Series Regression LSTMs?**

For time series regression tasks, some common evaluation metrics and visualizations for Long Short-Term Memory (LSTM) networks include:

* **Mean Absolute Error (MAE)**: This metric measures the average magnitude of the errors in the predictions, without considering their direction. It is calculated as the sum of the absolute differences between the predicted values and the true values, divided by the number of predictions.
* **Mean Squared Error (MSE)**: This metric measures the average squared difference between the predicted values and the true values. It is calculated as the sum of the squared differences between the predicted values and the true values, divided by the number of predictions.
* **Root Mean Squared Error (RMSE)**: This metric is the square root of the MSE, and is often used to report the performance of a time series model. It is interpreted in the same units as the original time series data, which can make it easier to understand the magnitude of the errors.
* **Time Series Plot**: A time series plot can help you visualize the predicted values and the true values for the time series. You can plot the predicted values and the true values on the same plot, and use the plot to identify trends, patterns, and anomalies in the data.

To calculate these evaluation metrics and create a time series plot, you can use a library like Matplotlib. Here's an example of how you can use Matplotlib to calculate and visualize the MAE, MSE, and RMSE for an LSTM network:

```
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Make predictions using the LSTM network
y_pred = model.predict(X_test)

# Calculate the MAE, MSE, and RMSE
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Print the results
print(f"MAE: {mae:.3f}")
print(f"MSE: {mse:.3f}")
print(f"RMSE: {rmse:.3f}")

# Create a time series plot
plt.plot(y_test, label="True Values")
plt.plot(y_pred, label="Predicted Values")
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Time Series Prediction")
plt.legend()
plt.show()
```

This will calculate the MAE, MSE, and RMSE for the LSTM network, and plot the predicted values and the true values for the time series on the same plot.

I hope this helps! Let me know if you have any other questions.

***Comment:** Fab! When I build Streamlit apps, I never use Matplotlib for charting, so let’s ask ChatGPT to use Plotly Express instead for interactive charts.*

### Question 8

**Can you show this using Plotly Express instead of Matplotlib?**

Certainly! Here's an example of how you can use Plotly Express to calculate and visualize the MAE, MSE, and RMSE for an LSTM network:

```
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Make predictions using the LSTM network
y_pred = model.predict(X_test)

# Calculate the MAE, MSE, and RMSE
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Print the results
print(f"MAE: {mae:.3f}")
print(f"MSE: {mse:.3f}")
print(f"RMSE: {rmse:.3f}")

# Create a time series plot
fig = px.scatter(x=range(len(y_test)), y=y_test, title="Time Series Prediction")
fig.add_scatter(x=range(len(y_pred)), y=y_pred, mode="markers", name="Predicted Values")
fig.show()
```

This will calculate the MAE, MSE, and RMSE

***Comment:*** *That looks promising. My time series forecasting LSTM is part of an algorithmic trading system that outputs trade entry and exit signals for a trading bot. It’d be nice to plot these signals on a chart. Let’s ask.*

### Question 9

**I want to add "enter" and "exit" marks at certain times on a time series plot. These marks are derived from another data set. How do I do this using Plotly Express?**

You can add "enter" and "exit" marks to a time series plot using Plotly Express by creating a separate scatter plot trace for the marks and adding it to the figure.

Here's an example of how you can do this:

```
import plotly.express as px

# Load the data
df = pd.read_csv("data.csv")

# Split the data into features and targets
X = df.drop("target", axis=1)
y = df["target"]

# Make predictions using the LSTM network
y_pred = model.predict(X)

# Create a time series plot
fig = px.scatter(x=range(len(y)), y=y, title="Time Series Prediction")
fig.add_scatter(x=range(len(y_pred)), y=y_pred, mode="markers", name="Predicted Values")

# Load the marks data
marks = pd.read_csv("marks.csv")

# Add a scatter plot trace for the marks
fig.add_scatter(x=marks["time"], y=marks["value"], mode="markers", name="Marks")
fig.show()
```

This will create a time series plot with the predicted values and the true values, and a separate scatter plot trace for the marks. The marks will be plotted as markers at the specified times on the x-axis.

I hope this helps!

***Comment:** That’s reasonable. In the past, I’ve done something similar using `fig.add_trace` and not `fig.add_scatter`, so I learned something new. However, ChatGPT didn’t quite nail the answer as `marks.csv` doesn’t distinguish between trade entry (buy) and trade exit (sell) marks. Let’s ask for some detail.*

### Question 10

**What is the format of the marks.csv data file?**

The format of the `marks.csv` data file will depend on the data that you want to include in the marks.

Here's an example of a simple `marks.csv` file that contains two columns:

| `time` | `value` |
| --- | --- |
| `5` | `10` |
| `15` | `20` |
|  |  |
| --- | --- |
| `30` | `50` |

In this example, the `time` column contains the time (in some unit) at which the mark should be displayed on the x-axis, and the `value` column contains the value (in some unit) at which the mark should be displayed on the y-axis.

You can include additional columns in the `marks.csv` file if you want to include more data in the marks. For example, you might want to include a `label` column to specify a label for each mark, or a `color` column to specify a color for each mark.

I hope this helps! Let me know if you have any other questions.

***Comment:*** *Lovely! The answer elaborates on the basic file layout and suggests adding a* `label` *column to distinguish between different kinds of marks. I’ll coax it into showing me what it looks like.*

### Question 11

**If I have a label column of "buy" and "sell" values in marks.csv, then how will the Plotly Express chart be written to show the marks in "green" and "red" respectively?**

To show the marks in "green" and "red" based on the values in the label column of the `marks.csv` file, you can use the color parameter of the `add_scatter` function to specify a color for each mark.

Here's an example of how you can do this:

```
import plotly.express as px

# Load the data
df = pd.read_csv("data.csv")

# Split the data into features and targets
X = df.drop("target", axis=1)
y = df["target"]

# Make predictions using the LSTM network
y_pred = model.predict(X)

# Create a time series plot
fig = px.scatter(x=range(len(y)), y=y, title="Time Series Prediction")
fig.add_scatter(x=range(len(y_pred)), y=y_pred, mode="markers", name="Predicted Values")

# Load the marks data
marks = pd.read_csv("marks.csv")

# Add a scatter plot trace for the marks
fig.add_scatter(x=marks["time"], y=marks["value"], mode="markers", name="Marks", color=marks["label"])
fig.show()
```

This will create a scatter plot trace for the marks, with the color of each mark determined by the corresponding value in the `label` column. The color parameter can accept a list of colors, a list of color names (as strings), or a list of color codes (as strings).

I hope this helps! Let me know if you have any other questions.

***Comment:*** *I could’ve asked for more detail on how the* `color` *parameter uses a list of colors, but I wanted to get back to the Kedro pipeline and use it to tune multiple different models. My algo-trading system has one model per financial instrument, so I wanted to easily manage all of them. I asked ChatGPT to tell me what* changes *are required to the pipeline to achieve this.*

### Question 12

**Going back to the Kedro pipeline...say, I have several LSTM models and want to tune each one and visualize their evaluation results. How does the pipeline change?**

To build a Kedro pipeline that tunes multiple LSTM models and visualizes their evaluation results, you can follow these steps:

1. Create a function that takes in a set of hyperparameters and returns a trained LSTM model. This function should take care of preprocessing the data, training the model, and evaluating the model on a test set.
2. Create a list of dictionaries, where each dictionary contains a set of hyperparameters to be passed to the model training function.
3. Use the `Pipeline` class from Kedro to define a pipeline that loops through the list of hyperparameters, trains a model for each set of hyperparameters, and stores the trained models in a pipeline output.
4. Use the `Visualizer` class from Kedro to define a visualization function that takes in the trained models and generates evaluation plots for each model.
5. Add the visualization function as a final node in the pipeline.

Here's an example of how you can define the pipeline:

```
from kedro.pipeline import Pipeline, node

# Define the model training function
def train_model(hyperparameters, data):
	# Preprocess the data
	X_train, X_test, y_train, y_test = preprocess_data(data)
	# Create the LSTM model
	model = create_lstm_model(hyperparameters)
	# Train the model
	model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=hyperparameters["epochs"])
	# Evaluate the model
	evaluation = model.evaluate(X_test, y_test, return_dict=True)
	return model, evaluation
	
# Define the list of hyperparameters to try
hyperparameters_list = [
	{"lookback": 10, "batch_size": 32, "learning_rate": 0.1, "epochs": 10, "optimizer": "Adam", "loss":
	"mean_absolute_error"},
	{"lookback": 20, "batch_size": 64, "learning_rate": 0.01, "epochs": 20, "optimizer": "SGD", "loss":
	"mean_squared_error"},
	{"lookback": 5, "batch_size": 16, "learning_rate": 0.001, "epochs": 5, "optimizer": "RMSprop", "loss":
	"mean_absolute_percentage_error"},
]

# Define the pipeline
pipeline = Pipeline(
	[
		node(
			train_model,
			inputs=["hyperparameters", "data"],
			outputs=["model", "evaluation"],
			iterable=hyperparameters_list,
		),
		node(
			visualize_results,
			inputs=["model", "evaluation"],
			iterable=hyperparameters_list,
		),
	]
)
```

This pipeline defines a node that trains a model for each set of hyperparameters in the `hyperparameters_list`, and stores the trained models and their evaluation results in the pipeline output. The pipeline also defines a final node that visualizes the evaluation results for each model.

I hope this helps! Let me know if you have any other questions.

***Comment:** I think this gives me a good handle on how to manage multiple models. I can add additional parameters for each model, and the `Pipeline` and `node` objects warrant further investigation since the results stored in `Pipeline` and `node` can take hyperparameter iterables! Now, what would a `visualize_results` implementation look like?*

### Question 13

**Great, so can `visualize_results` be implemented using similar Plotly Express examples you gave earlier, in the Kedro Visualizer class?**

Yes, you can use Plotly Express to visualize the evaluation results for each LSTM model in the `Visualizer` class of Kedro.

Here's an example of how you can define the `visualize_results` function using Plotly Express:

```
import plotly.express as px

def visualize_results(model, evaluation):
	# Extract the evaluation metrics from the evaluation dictionary
	mae = evaluation["mae"]
	mse = evaluation["mse"]
	rmse = evaluation["rmse"]
	# Create a bar chart to visualize the evaluation metrics
	fig = px.bar(x=["MAE", "MSE", "RMSE"], y=[mae, mse, rmse])
	fig.show()
```

This function creates a bar chart that displays the MAE, MSE, and RMSE evaluation metrics for the model.

You can then use this function as a node in the Kedro pipeline, as shown in the previous example.

I hope this helps! Let me know if you have any other questions.

***Comment:** I saw a YouTube video on Kedro. The speaker showed a graphical representation of the Kedro pipeline. I was intrigued to learn how that was done.*

### Question 14

**Amazing, thanks. How can I see a graphical representation of the Kedro pipeline?**

To see a graphical representation of a Kedro pipeline, you can use the `draw` method of the `Pipeline` class.

Here's an example of how you can use the draw method to draw a graphical representation of the pipeline:

```
# Import the necessary modules
from kedro.pipeline import Pipeline
from kedro.io import KedroCliKernel

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml", KedroCliKernel())

# Draw the pipeline
pipeline.draw()
```

This will open a graphical representation of the pipeline in your default web browser. The graph will show the nodes of the pipeline as boxes, with the input and output nodes connected by arrows.

You can also use the `show_graph` method of the `Pipeline` class to draw the pipeline and save it to a file:

```
# Import the necessary modules
from kedro.pipeline import Pipeline
from kedro.io import KedroCliKernel

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml", KedroCliKernel())

# Draw the pipeline and save it to a file
pipeline.show_graph(format="png", filename="pipeline.png")
```

This will save the graphical representation of the pipeline to a file called `pipeline.png` in the current working directory.

I hope this helps! Let me know if you have any other questions.

***Comment:** I was right. This Pipeline object is very powerful. I wonder if it can be used to distribute model training jobs across several machines or CPU/GPU cores.*

🐛

***Code comment:*** *There are no such pipeline APIs like draw() and show\_graph(). Maybe ChatGPT was partially replaying someone's pipeline wrapper object with those interfaces, or maybe it was telling me about another framework's pipeline API. I will never know!*  
  
*Kedro has a separate application "kedro viz" to visualize pipelines. This command is run in your application's root folder and it uses the project's configuration, data catalog, and pipeline registration conventions to start a web server that displays your pipeline graph in a browser window. Much like Streamlit does. My Streamlit application* [*runs the "kedro viz" command in a sub-process*](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/streamlit_app.py?ref=streamlit.ghost.io#L104) *and* [*visualizes the output in Streamlit's component.html widget*](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app/blob/796ddc10d6de4a96f723105050c719610357f014/src/streamlit_app.py?ref=streamlit.ghost.io#L413)*.*

### Question 15

**Can the Pipeline class be used to distribute the jobs in each node across several machines or run them in parallel?**

Yes, the `Pipeline` class in Kedro can be used to distribute the jobs in each node across several machines or run them in parallel.

To do this, you can use the `Executor` class from Kedro to create an executor that manages the parallel execution of the pipeline nodes. The `Executor` class supports several different execution modes, including:

* **SequentialExecutor**: This executor runs the nodes of the pipeline sequentially, one after the other. This is the default executor.
* **ThreadedExecutor**: This executor runs the nodes of the pipeline in separate threads, allowing them to run in parallel.
* **MultiprocessingExecutor**: This executor runs the nodes of the pipeline in separate processes, allowing them to run in parallel across multiple CPU cores or machines.

To use one of these executors, you can pass it as an argument to the run method of the `Pipeline` class. For example, to run the pipeline using the `ThreadedExecutor`, you can do the following:

```
from kedro.pipeline import Pipeline
from kedro.executor import ThreadedExecutor

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Create the executor
executor = ThreadedExecutor()

# Run the pipeline using the executor
pipeline.run(executor=executor)
```

This will run the nodes of the pipeline in separate threads, allowing them to run in parallel.

I hope this helps! Let me know if you have any other questions.

***Comment:*** *Really? That’s awesome, and it looks so easy. I know from many years of experience with distributed systems that job instrumentation, logging, and failure management are critical. Does the pipeline support these capabilities too?*

### Question 16

**Awesome! Does kedro.executor allow the jobs (log outputs) to be monitored and restarted if they fail?**

Yes, the `Executor` class in Kedro allows you to monitor the jobs and restart them if they fail.

To do this, you can use the `RetryingExecutor` class, which wraps another executor and automatically retries failed jobs.

Here's an example of how you can use the `RetryingExecutor` to monitor and restart the jobs in a pipeline:

```
from kedro.pipeline import Pipeline
from kedro.executor import MultiprocessingExecutor, RetryingExecutor

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Create the executor
executor = MultiprocessingExecutor()

# Wrap the executor in a RetryingExecutor
retrying_executor = RetryingExecutor(executor, retries=3)

# Run the pipeline using the retrying executor
pipeline.run(executor=retrying_executor)
```

This will run the pipeline using the `MultiprocessingExecutor`, which will distribute the jobs across multiple CPU cores or machines. If a job fails, the `RetryingExecutor` will automatically retry it up to 3 times before giving up.

You can also specify a delay between retries by setting the delay parameter of the `RetryingExecutor`. For example, to specify a delay of 1 second between retries, you can do the following:

```
retrying_executor = RetryingExecutor(executor, retries=3, delay=1.0)
```

I hope this helps! Let me know if you have any other questions.

***Comment:** Wow, there is a `RetryingExecutor` out of the box. Nice. When it comes to logging, it’s best to have some log persistence, on top of which analytics and insights can be implemented. Let’s explore that line of thought a little. In particular, I want to know about log sinks.*

### Question 17

**How is the output of executors redirected to files or custom log sinks?**

To redirect the output of the executors to files or custom log sinks, you can use the `LogSink` class from Kedro.

The `LogSink` class allows you to specify a logging handler that will be used to redirect the output of the executors to a specific location. Kedro provides several built-in log sinks, including:

* **TeeSink**: This log sink redirects the output to both the console and a file.
* **FileSink**: This log sink redirects the output to a file.
* **NullSink**: This log sink discards all output.

You can use these log sinks by passing them as an argument to the run method of the `Pipeline` class. For example, to redirect the output of the pipeline to a file called `output.log`, you can do the following:

```
from kedro.pipeline import Pipeline
from kedro.io import FileSink

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Create the log sink
sink = FileSink("output.log")

# Run the pipeline using the log sink
pipeline.run(log_sink=sink)
```

This will redirect the output of the pipeline to the file `output.log`.

You can also use a custom logging handler by subclassing the `LogSink` class and overriding the `_setup_logging` method. For example, to redirect the output to a custom log sink called `CustomSink`, you can do the following:

```
from kedro.pipeline import Pipeline
from kedro.io import LogSink
import logging

class CustomSink(LogSink):
	def _setup_logging(self):
		# Set up the custom log sink
		self.custom_logger = logging.getLogger("CustomLogger")
		self.custom_logger.setLevel(logging.INFO)
		# Add a handler to the custom logger
		handler = logging.StreamHandler()
		handler.setFormatter(logging.Formatter("%(message)s"))
		self.custom_logger.addHandler(handler)
		# Set the root logger to use the custom logger
		logging.root.handlers = [handler]
	
# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Create the log sink
sink = CustomSink()

# Run the pipeline using the log sink
pipeline.run(log_sink=sink)
```

This will redirect the output of the pipeline to the custom log sink `CustomLogger`. You can then use the `custom_logger` object to log messages to the custom sink.

I hope this helps! Let me know if you have any other questions.

***Comment:** At this point, I don’t know if I should be more impressed with Kedro or that ChatGPT “knows”. From what I’ve learned so far, I’m itching to get started with Kedro straight away, but I want to ask one more question.*

🐛

***Code comment****: Unfortunately, the latest version of Kedro doesn't have these sinks out-of-the-box. ChatGPT was trained on pre-2021 web knowledge, so this information may be outdated or incorrect. Instead, Kedro uses* [*configuration-driven logging*](https://kedro.readthedocs.io/en/stable/logging/logging.html?ref=streamlit.ghost.io) *which I haven't figured out yet.*

### Question 18

**Can you make a custom sink that sends logs to Kibana?**

Yes, you can use the `ElasticsearchHandler` from the `elasticsearch-logger` package to create a custom log sink that sends logs to Kibana.

Here's an example of how you can define the `KibanaSink` class to redirect the output of the executors to Kibana:

```
from kedro.pipeline import Pipeline
from kedro.io import LogSink
import logging
from elasticsearch_logger import ElasticsearchHandler

class KibanaSink(LogSink):
	def _setup_logging(self):
		# Set up the Elasticsearch handler
		self.handler = ElasticsearchHandler(
			hosts=[{"host": "localhost", "port": 9200}]
		)
		# Set the root logger to use the Elasticsearch handler
		logging.root.handlers = [self.handler]

# Load the pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Create the log sink
sink = KibanaSink()

# Run the pipeline using the log sink
pipeline.run(log_sink=sink)
```

This will redirect the output of the pipeline to Kibana, which can be used to visualize and analyze the logs.

You will need to have Elasticsearch and Kibana installed and running on your machine to use this sink. You can find more information on how to install and configure Elasticsearch and Kibana in the Elasticsearch documentation.

I hope this helps! Let me know if you have any other questions.

***Comment:*** *I know ChatGPT is cleverly replaying canned Kedro knowledge, but when it’s revealed elegantly like this, the conversation is very satisfying. Kedro appears to be very powerful and well-designed, making ChatGPT’s answers look trivial. I want to see a contrast between Kedro and alternatives.*

🐛

***Code comment**: This looks like it could work, except for the reference to pipeline.run() again, and is worth investigating further.*

### Question 19

**What are the alternatives to using Kedro?**

There are several alternatives to Kedro that you can use for building and managing machine learning pipelines. Some of the popular alternatives include:

* **Airflow**: Airflow is a platform to programmatically author, schedule, and monitor workflows. It was originally developed by Airbnb, and is now a popular open-source project. Airflow provides a flexible and powerful platform for building and managing ML pipelines, and has a large user base and community.
* **Kubeflow**: Kubeflow is an open-source project that aims to make it easy to deploy and manage machine learning workflows on Kubernetes. It provides a range of tools and frameworks for building, deploying, and managing ML pipelines, including Jupyter notebooks, TensorFlow, and PyTorch.
* **Prefect**: Prefect is an open-source platform for building, scheduling, and monitoring data pipelines. It is designed to be highly scalable and resilient, and provides a range of features for building and managing ML pipelines, including support for distributed execution and automatic retries.
* **Luigi**: Luigi is an open-source Python library for building complex pipelines of batch jobs. It was developed by Spotify and is designed to be easy to use and flexible. Luigi provides a range of features for building and managing ML pipelines, including support for dependencies, parallel execution, and error handling.

These are just a few examples of the alternatives to Kedro that you can consider. Each platform has its own strengths and weaknesses, and the right choice will depend on your specific needs and requirements.

I hope this helps! Let me know if you have any other questions.

***Comment:** Let’s dig deeper into this contrast and see how the Kedro pipeline is done in another framework.*

### Question 20

**How would you implement our Kedro pipeline in Airflow?**

To implement the Kedro pipeline in Airflow, you can define a series of tasks and dependencies using the `DAG` (directed acyclic graph) and `Operator` classes in Airflow.

Here's an example of how you can define the Kedro pipeline in Airflow:

Here's the complete example of how you can define the Kedro pipeline in Airflow:

```
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define the default_args dictionary to specify the default parameters of the DAG
default_args = {
	"owner": "me",
	"start_date": "2022-01-01",
	"depends_on_past": False,
	"retries": 1,
	"retry_delay": timedelta(minutes=5),
}

# Create the DAG object
dag = DAG(
	"kedro_pipeline",
	default_args=default_args,
	description="Example Kedro pipeline in Airflow",
	schedule_interval=timedelta(hours=1),
	catchup=False,
)

# Define the data ingestion task
def ingest_data_task():
	# Call the data ingestion function
	module.ingest_data()
	ingest_data = PythonOperator(
		task_id="ingest_data",
		python_callable=ingest_data_task,
		dag=dag,
	)

# Define the preprocessing task
def preprocess_data_task():
	# Call the preprocessing function
	module.preprocess_data()
	preprocess_data = PythonOperator(
		task_id="preprocess_data",
		python_callable=preprocess_data_task,
		dag=dag,
	)

# Define the hyperparameter tuning task
def tune_model_task():
	# Call the hyperparameter tuning function
	module.tune_model()
	tune_model = PythonOperator(
		task_id="tune_model",
		python_callable=tune_model_task,
		dag=dag,
	)

# Define the model evaluation task
def evaluate_model_task():
# Call the model evaluation function
module.evaluate_model()
evaluate_model = PythonOperator(
	task_id="evaluate_model",
	python_callable=evaluate_model_task,
	dag=dag,
)

# Define the model visualization task
def visualize_results_task():
	# Call the model visualization function
	module.visualize_results()
	visualize_results = PythonOperator(
		task_id="visualize_results",
		python_callable=visualize_results_task,
		dag=dag,
	)

# Set the dependencies between tasks
ingest_data >> preprocess_data >> tune_model >> evaluate_model >> visualize_results
```

In this example, the Kedro pipeline is implemented as a series of tasks defined using the `PythonOperator` class in Airflow. The tasks are connected by dependencies using the `>>` operator in Airflow, which specifies dependencies between tasks in a DAG. It specifies that the task on the left-hand side of the operator must be completed before the task on the right-hand side can start.

For example, in the following code snippet:

```
ingest_data >> preprocess_data >> tune_model >> evaluate_model >> visualize_results
```

The `>>` operator specifies that the `ingest_data` task must be completed before the `preprocess_data` task can start, the `preprocess_data` task must be completed before the `tune_model` task can start, and so on.

This ensures that the tasks are run in the correct order, and that the necessary data and resources are available when each task is run.

I hope this helps! Let me know if you have any other questions.

***Comment:** That looks like a lot of imperative code. I’m not sure if Airflow has a declarative syntax like Kedro’s or any of Kedro’s other features. Still, I want to dig into this opaque “module” reference that’s in the Airflow code above.*

### Question 21

**What is the variable "module"?**

In the example code I provided, `module` is a placeholder for the Python module that contains the functions or methods that are called by the tasks in the Airflow DAG.

For example, in the following code snippet:

```
# Define the data ingestion task
def ingest_data_task():
	# Call the data ingestion function
	module.ingest_data()
```

The `ingest_data_task` function calls the `ingest_data` function, which is assumed to be defined in the module Python module.

You would need to replace `module` with the actual name of the Python module that contains the functions or methods you want to call. For example, if the `ingest_data` function is defined in a module called `data_ingestion`, you would replace `module` with `data_ingestion`.

I hope this helps! Let me know if you have any other questions.

***Comment:** Ah, so there’s more to it than initially implied. It pays to read the code ChatGPT produces and ask for clarification when you don’t understand.*

### Question 22

**Can you provide me with a skeleton implementation for the Python "module"?**

Certainly! Here's a skeleton implementation of the Python "module" that contains the functions or methods that are called by the tasks in the Airflow DAG:

```
# Import required libraries
import pandas as pd

def ingest_data():
	"""Ingest raw data from a file or database"""
	# Load the raw data
	raw_data = pd.read_csv("raw_data.csv")
	# Save the data to a file or database
	raw_data.to_csv("data.csv", index=False)

def preprocess_data():
	"""Preprocess the data"""
	# Load the data
	data = pd.read_csv("data.csv")
	# Perform preprocessing steps, such as cleaning and feature engineering
	processed_data = data.clean()
	# Save the processed data to a file or database
	processed_data.to_csv("processed_data.csv", index=False)

def tune_model():
	"""Tune the hyperparameters of the model"""
	# Load the processed data
	processed_data = pd.read_csv("processed_data.csv")
	# Create and tune the model
	model = Model(processed_data)
	model.tune_hyperparameters()
	# Save the tuned model to a file or database
	model.save("tuned_model.pkl")

def evaluate_model():
	"""Evaluate the model"""
	# Load the processed data and tuned model
	processed_data = pd.read_csv("processed_data.csv")
	model = Model.load("tuned_model.pkl")
	# Evaluate the model
	evaluation_metrics = model.evaluate(processed_data)
	# Save the evaluation metrics to a file or database
	pd.DataFrame(evaluation_metrics).to_csv("evaluation_metrics.csv", index=False)

def visualize_results():
	# TODO: Implement the model visualization logic here
	pass
```

In this example, the module contains five functions: `ingest_data`, `preprocess_data`, `tune_model`, `evaluate_model`, and `visualize_results`. These functions correspond to the tasks in the Airflow DAG.

You would need to replace the TODO comment(s) with the actual code for the function(s). The code should implement the logic for the corresponding task in the pipeline.

I hope this helps! Let me know if you have any other questions.

***Comment:** I’m comfortable displaying my LSTM model data and forecasts in tables and charts in Streamlit. But I’m not sure how to display a Kedro pipeline graph. So, let’s ask…*

### Question 23

**How would you display the Kedro pipeline graph in Streamlit?**

To display the Kedro pipeline graph in a Streamlit application, you can use the `Pipeline.to_dot_graph` method to generate a dot graph representation of the pipeline, and then to display a dot graph in a Streamlit app, you can use the `pyvis.network.Network.from_dot` method from the Pyvis library to generate a network object from the dot graph representation, and then use the `st.pyplot` function to display the network object in the Streamlit app.

Here's an example of how you can do this:

```
import streamlit as st
from kedro.pipeline import Pipeline
from pyvis import network as net

# Load the Kedro pipeline
pipeline = Pipeline.load("path/to/pipeline.yml")

# Generate the dot graph representation of the pipeline
dot_graph = pipeline.to_dot_graph()

# Generate a network object from the dot graph
graph = net.Network.from_dot(dot_graph)

# Display the network object in the Streamlit app
st.pyplot(graph.show)
```

This will display the Kedro pipeline graph in the Streamlit app, using the dot graph representation generated by the `Pipeline.to_dot_graph` method and the pyvis library.

You can customize the appearance of the graph by modifying the properties of the graph object. For example, you can use the `set_edge_color` method to change the color of the edges, or the `set_node_color` method to change the color of the nodes.

***Comment:** I’m not certain that `st.pyplot` can display `dot_graph`, so let’s regenerate the answer.*

🐛

***Code comment**: Kedro's pipeline doesn't have a to\_dot\_graph() API! See my earlier code comment about "kedro viz".*

### Question 24

**[Regenerate!]**

To display the Kedro pipeline graph in a Streamlit application, you can use the `st.graphviz_chart` function to render the graph using Graphviz.

Here's an example of how you can do this:

```
import streamlit as st
from kedro.pipeline import Pipeline

# Create the Kedro pipeline
pipeline = Pipeline([
	# Add the pipeline nodes here
])

# Generate the Graphviz representation of the pipeline
pipeline_graph = pipeline.to_graph()

# Render the pipeline graph using st.graphviz_chart
st.graphviz_chart(pipeline_graph)
```

In this example, the `Pipeline` class is used to create a Kedro pipeline, and the `to_graph` method is used to generate a Graphviz representation of the pipeline. The `st.graphviz_chart` function is then used to render the graph in a Streamlit application.

***Comment:** I didn’t know about `st.graphviz_chart`. Let’s try another.*

🐛

***Code comment**: Kedro's pipeline doesn't have a to\_graph() API! See my earlier code comment about "kedro viz".*

### Question 25

**[Regenerate!]**

To display the Kedro pipeline graph in Streamlit, you can use the `kedro.pipeline.Pipeline.graph` method to generate the graph, and then use the `st.graphviz_chart` function to render the graph in a Streamlit app.

Here's an example of how you can do this:

```
import streamlit as st
from kedro.pipeline import Pipeline

# Load the Kedro pipeline
pipeline = Pipeline.load("/path/to/pipeline.yml")

# Generate the pipeline graph
graph = pipeline.graph

# Render the graph in a Streamlit app
st.graphviz_chart(graph)
```

In this example, the `Pipeline.load` method is used to load the Kedro pipeline from a `pipeline.yml` file. The `pipeline.graph` method is then used to generate the graph of the pipeline, and the `st.graphviz_chart` function is used to render the graph in a Streamlit app.

You can customize the appearance of the graph using the various options provided by the `st.graphviz_chart` function. For example, you can specify the font, color, and size of the nodes and edges in the graph.

I hope this helps! Let me know if you have any other questions.

***Comment:** By this point, I’m overwhelmed with ideas, but I’ve learned enough. Since ChatGPT saves previous conversations, I can come back to fill in the gaps or make corrections. Now I’m going to take the provided code and build the Kedro pipeline and the Streamlit front end. I’ll start with a simple LSTM model for the purposes of this post and build upon it for my real-world solution.*

🐛

***Code comment**: If only it were true, I'd still be overwhelmed. Kedro's pipeline doesn't have a graph attribute! See my earlier code comment about "kedro viz".*

## Wrapping up

ChatGPT helped me develop a decent solution for deploying and managing my ML models using Kedro. I did this in less time and with less effort than I could’ve done without it. I learned a lot about Kedro and can now run an ML pipeline manually or orchestrated by the Kedro framework, and display a pipeline visualization.

![Screenshot-2023-02-08-at-6.45.33-AM](https://streamlit.ghost.io/content/images/2023/02/Screenshot-2023-02-08-at-6.45.33-AM.png#browser)

I built [the app](https://kedro-ml-pipeline.streamlit.app/?ref=streamlit.ghost.io) over the weekend. I didn't have time to implement hyperparameter tuning or an LSTM model in my pipeline. I'll do that in the coming weeks, so if you find this useful, follow [my repo](https://github.com/asehmi/using_chatgpt_kedro_streamlit_app?ref=streamlit.ghost.io) and consider giving it a star! ⭐

In the future, as the field of "prompt engineering" matures, maybe chatbots using LLMs will be smart enough to clarify user intent. I believe for now you'll get better results if you write prompts with a clear context and goal in mind. Make a conversation plan to take ChatGPT through a series of small Q&A steps of increasing detail on your desired outcome. If you’re fortunate, you’ll tease out more features and capabilities in your answers. Finally, thoroughly check and test the code ChatGPT generates and use it only as a springboard for your own creativity.

If you want to create your own conversation plan and prompts, read [How to write an effective GPT-3 prompt](https://zapier.com/blog/gpt-3-prompt/?ref=streamlit.ghost.io). And if you have any questions, contact me on [LinkedIn](https://www.linkedin.com/in/asehmi/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3B8ZTM7%2BaCQHiM0HRipxj%2Bkw%3D%3D&ref=streamlit.ghost.io) or [Twitter](https://twitter.com/asehmi?ref=streamlit.ghost.io).

Happy chatting and Streamlit-ing! 🎈

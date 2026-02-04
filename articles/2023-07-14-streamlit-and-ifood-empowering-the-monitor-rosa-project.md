---
title: "Streamlit and iFood: Empowering the Monitor Rosa project"
subtitle: "Harnessing technology and corporate support for social impact"
date: 2023-07-14
authors:
  - "Heber Augusto Scachetti"
category: "Advocate Posts"
---

![Streamlit and iFood: Empowering the Monitor Rosa project](https://streamlit.ghost.io/content/images/size/w2000/2023/07/monitor-rasa-app.svg)


Hey, Streamlit community! 👋

My name is Heber A. Scachetti, and I'm a Data Squad Lead at iFood.

I joined iFood in 2020 after participating in a hackathon that introduced me to the Monitor Rosa project, a volunteer initiative aimed at helping the Brazilian Association of Lymphoma and Leukemia (Abrale) to address the challenges faced by patients with breast cancer.

In this post, I'll share with you how I used GitHub Actions, Google Storage, and Streamlit to create an app for the Monitor Rosa project.

## What is the Monitor Rosa project?

Before we dive into the app, I want to share with you a little background on the Monitor Rosa project and how iFood, Abrale, and Streamlit helped make it happen:

* **iFood.** iFood has been instrumental in supporting my involvement in the Monitor Rosa project through its unique employee engagement program called "Minha Quarta" (" My Wednesday"). This initiative allows iFood employees, including myself, to dedicate every Wednesday to personal development, learning, and volunteering. By providing this dedicated time, iFood indirectly contributes to the project's success by enabling its employees to invest their skills and expertise in initiatives that make a meaningful impact on society.
* **Abrale.** Abrale is a non-profit organization created in 2002 by patients and their families with the mission of offering help and mobilizing partners so that all people with cancer and blood diseases have access to the best treatment. Abrale is the leader of the TJCC Movement (Movimento Todos Juntos Contra o Câncer—"All Together against Cancer"), developing projects related to breast cancer, such as Monitor Rosa.
* **Streamlit.** Streamlit helped me create interactive data visualizations for the Monitor Rosa project.

The support from iFood has been invaluable, as it has allowed me to balance my professional responsibilities with my passion for making a difference in the lives of patients and their families. This partnership showcases the potential for technology companies to positively impact society by supporting initiatives that aim to improve the lives of those in need. It also highlights the importance of fostering a culture of learning and social responsibility within the corporate environment.

And now, let's dive into the app!

## App overview

The app consolidates data from different sources, including the Brazilian public health system (SUS) and other data providers. It helps you explore key performance indicators (KPIs) and gain insights into Brazil's current state of cancer and blood disease treatment.

There are three repositories:

1. [devops-pysus-get-files](https://github.com/heber-augusto/devops-pysus-get-files?ref=streamlit.ghost.io) automates the data collection from SUS and other sources, ensuring the project has access to the most up-to-date information.
2. [sus-kpis-analysis](https://github.com/heber-augusto/sus-kpis-analysis?ref=streamlit.ghost.io) consolidates the collected data, maintains analyses of the KPIs, and will eventually contain models and other data artifacts that can be consumed by dashboards and other data visualization tools.
3. [streamlit-monitor-rosa](https://github.com/heber-augusto/streamlit-monitor-rosa?ref=streamlit.ghost.io) contains the Streamlit app (deployed on Streamlit Community Cloud) and serves as the main interface for users to interact with the data.

The following cutting-edge technologies ensure efficient data collection, storage, and visualization:

1. **GitHub Actions.** At regular intervals, GitHub Actions automatically fetch data from the SUS FTP server and other sources for the project to have the most up-to-date information.
2. **Google Storage.** Once collected, the data is stored in a Google Storage bucket—a centralized repository. This allows for easy access and management of the data by the project's various components. The data is then read and processed by the code in the `sus-kpis-analysis` repo, which consolidates the data and maintains analyses of the KPIs.
3. **Streamlit.** The Streamlit application in the `streamlit-monitor-rosa` repo also accesses the data directly from the Google Storage bucket, ensuring that the dashboard displays the most recent information.

To protect sensitive information, such as Google Storage access keys, I used Streamlit Cloud secrets. This allows the team to securely store and manage sensitive data, ensuring that only authorized users can access the necessary resources.

## How was the app developed?

I wanted to create an app that could visualize data collected from SUS and accommodate additional features as the project progressed.

I have previously used Streamlit and deployed apps to the Streamlit Community Cloud, so I knew it'd help me achieve my goal quickly. But I'd never connected it to a Google Cloud Storage bucket that housed the files collected and transformed by two other repositories. So I followed [this Streamlit doc](https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs?ref=streamlit.ghost.io) to set it up.

Here is the code:

```
from google.oauth2 import service_account
from google.cloud import storage
import pandas as pd

#Create API client
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

client = storage.Client(credentials=credentials)
bucket = client.bucket(bucket_name)
content = bucket.blob(file_path).download_as_bytes()
bytes_io = BytesIO(content)
dados_estad_mensal = pd.read_parquet(bytes_io)
```

The whole app is just over 130 lines of code, 30 of which read the file from the Google Storage bucket and perform additional calculations. I used:

* Streamlit Cloud secrets and the "google-cloud-storage" Python library to access the file content—a parquet file containing indicators for one of Brazil's states
* pandas library to manage date filters, date transformations, and calculated column creation (such as a 6-month moving average)

The collected file already organizes indicators by date and cancer staging, which is a measure of cancer severity at the time of diagnosis. Early diagnoses are considered to be stages 0, 1, and 2, while late diagnoses are considered to be stages 3 and 4.

Once the file was collected, I created an app interface using a few Streamlit components and the Plotly library (for line charts). I used two components to filter the staging and metric displayed on the chart and a checkbox for the users to choose between using the data as a moving average or without any calculations.

Here is the complete code:

```
import streamlit as st
import pandas as pd

metrics = {
 'Número de pacientes em tratamento': 'numero_pacientes',   
 'Óbitos':'obtitos',
 'Custo':'custo_estadiamento',
 'Custo por paciente': 'custo_por_paciente',
 'Número de diagnosticos': 'numero_diagnosticos'      
}

# cancer stage filter
all_symbols = dados_estad_mensal.estadiamento.unique()
symbols = st.multiselect("Estadiamentos", all_symbols, all_symbols)

# metric filter
metrics_selector = st.selectbox(
    "Métrica",
    list(metrics.keys())
)
y_column_name = metrics[metrics_selector]

# enable/disable moving average values
ma_option = st.checkbox('Média móvel (6 meses)')
if ma_option:
    y_column_name = f'{metrics[metrics_selector]}_ma'

# get data by column name
dataset = dados_estad_mensal[dados_estad_mensal.primeiro_estadiamento.isin(symbols)]

# create figure to plotly chart
fig = px.line(
    dataset, 
    x='data', 
    y=y_column_name, 
    color='estadiamento', 
    symbol="estadiamento")

# Update layout (yaxis title and responsive legend)
fig.update_layout(
    yaxis_title=metrics_selector,
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="left",
            x=0.01
            )    
)

# shows chat using streamlit magic :) 
st.plotly_chart(
    fig, 
    use_container_width=True)
```

And here is what the final app looks like:

Key insights gained from this app include:

* The cost per patient is higher for late-stage diagnoses (stages 3 or 4)
* The number of monthly deaths among patients with late-stage diagnoses is more than double that of early-stage diagnoses
* The number of patients diagnosed with stage 4 cancer has been increasing over the past six months

## Wrapping up

I hope I was able to show you how the power of technology and data-driven solutions can address social issues. Using Streamlit, GitHub Actions, and Google Storage, I created a valuable tool for the Monitor Rosa project. This tool can aid healthcare managers in understanding and addressing the challenges faced by patients with breast cancer in Brazil.

If you have any questions, please leave them in the comments below or contact me on [LinkedIn](https://www.linkedin.com/in/heberscachetti/?ref=streamlit.ghost.io).

Thank you, and happy Streamlit-ing! 🎈

# Fake News Detection Using AI

A web-based Fake News Detection System developed as a CS619 Final Year Project. The project combines a Django web application with Natural Language Processing (NLP) and supervised machine learning to classify submitted news text as Real or Fake.

## Project Overview

The application allows users to submit news text and receive a predicted classification with a confidence score. It also provides user-facing functionality and administrative features for managing the application and machine learning workflow.

**Important:** Predictions are model classifications, not independent verification of factual claims.

## Machine Learning Approach

- **Task:** Binary text classification
- **Learning type:** Supervised learning
- **Feature extraction:** TF-IDF (Term Frequency–Inverse Document Frequency)
- **Model:** Logistic Regression
- **Input:** English news text
- **Output:** Real or Fake classification with a model confidence score
- **Reported accuracy:** 91.44%

See the final project report for the methodology and evaluation details.

## Technologies Used

- Python
- Django
- Scikit-learn
- Pandas and NumPy
- NLTK
- Joblib
- SQLite
- HTML, CSS and JavaScript
- Chart.js
- Jupyter Notebook

## Repository Structure

```text
CS619-Final-Year-Project-Fake-News-Detection-Using-AI/
├── Application/
│   ├── config/
│   ├── detector/
│   ├── templates/
│   ├── manage.py
│   ├── requirements.txt
│   └── trained model and vectorizer files
├── Machine-Learning/
│   ├── DataPreprocessing_2.ipynb
│   ├── Model_Change_EDA.ipynb
│   └── README.md
├── Documentation/
│   ├── Final project report
│   ├── Final presentation
│   └── Supporting university document
└── README.md
```

## Machine Learning and Datasets

The machine learning work includes data preprocessing, exploratory data analysis (EDA), and model experimentation.

The project uses publicly available datasets, including:

- [WELFake Dataset — Kaggle](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification)
- [FakeNewsNet Dataset — Kaggle](https://www.kaggle.com/datasets/algord/fake-news)

Raw and processed datasets are not included in this repository because of their size. Refer to the Machine-Learning directory for the available notebooks and dataset information.

## Evaluation

The final project report records the following model results:

| Metric | Result |
|---|---:|
| Accuracy | 91.44% |
| Precision | 91.55% |
| Recall | 91.44% |
| F1-score | 91.42% |

These are the reported evaluation results from the project documentation.

## Running the Application Locally

The Django application is located in the `Application/` directory.

For Windows setup instructions, see [`Application/README.md`](Application/README.md).

The application requires Python and its listed dependencies. Dataset files are not included, so any functionality that requires uploading a dataset will need an appropriate dataset supplied separately.

## Project Documentation

The `Documentation/` directory contains the final report, presentation slides, and supporting university documentation.

## Current Status

- Django application and trained model files uploaded
- Data preprocessing and model experimentation notebooks uploaded
- Final project documentation uploaded
- Live deployment: not yet configured

## Limitations

- Supports English text only
- Uses classical machine learning rather than deep learning
- Does not independently verify claims against live sources
- Dataset coverage may not represent every region or type of news

## Author

**Muhammad Tayyar Hussain**

CS619 — Final Year Project  
Fake News Detection Using AI

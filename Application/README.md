# Fake News Detection System using AI

## Overview

This project is a web-based Fake News Detection System developed using Django and AI.
It allows users to input news text and receive a prediction indicating whether the news is **Real** or **Fake**.

---

## Please use these credentials if you want to check the complete application.

Admin can do everything which a simple user can with extra privileges.

* Username: admin
* Password: 12345678@

## Technologies Used

* Python
* Django
* SQLite
* Scikit-learn
* Pandas
* NumPy
* Joblib
* NLTK
* Chart.js

---

## Project Final Deliverables

The final submission folder includes:

* Final Project Report
* Presentation Slides (PPT)
* Preprocessing and Model Experimentation folder (Jupyter Notebook work)

---

## Installation and Setup

> Note: Virtual environment (venv) is not included.

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate environment (Windows)

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run server

```bash
python manage.py runserver
```

### 6. Open in browser

http://127.0.0.1:8000/

---

## Dataset

* The system was trained using publicly available fake news datasets (e.g., WELFake dataset).
* Large dataset files are not included in the submission due to size limitations on LMS.

---

## Notes

* Only English text is supported for analysis
* Minimum text length validation is applied
* The system handles invalid input and displays appropriate error messages

---

## Python Version

Python 3.x

## Operating System

Windows

---

## Author

Final Year Project: Fake News Detection System using AI
Muhammad Tayyar Hussain

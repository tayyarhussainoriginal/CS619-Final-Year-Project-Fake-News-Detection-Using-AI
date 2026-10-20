import joblib
import numpy as np
import pandas as pd
import os
import datetime
import csv
import re
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.functions import TruncDate

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from .models import NewsAnalysis, Dataset, MLModel, PerformanceMetrics, UsageReport


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LABEL_MAP = {
    0: "Fake",
    1: "Real",
    "0": "Fake",
    "1": "Real"
}


# LOGIN

class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.is_staff:
            return reverse_lazy("admin:index")

        return reverse_lazy("home")



# LANDING PAGE

def landing(request):

    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "landing.html")




# HOME


def home(request):

    sample_text = (
        "u n seeks humanitarian pause in sanaa where streets battlegrounds geneva "
        "reuters the united nations called on monday for a humanitarian pause in "
        "the yemeni capital of sanaa on tuesday to allow civilians to leave their "
        "homes aid workers to reach them and the wounded to get medical care jamie "
        "mcgoldrick u n humanitarian coordinator in yemen said in a statement that "
        "the streets of sanaa had become battlegrounds and that aid workers remain "
        "in lockdown thus i call on all parties to the conflict to urgently enable "
        "a humanitarian pause on tuesday 5 december between 10 00 a m and 16 00 p m "
        "to allow civilians to leave their homes and seek assistance and protection "
        "and to facilitate the movement of aid workers to ensure the continuity of "
        "life saving programs he said mcgoldrick warned the warring parties that any "
        "deliberate attacks against civilians and against civilian and medical "
        "infrastructure are clear violations of international humanitarian law and "
        "may constitute war crimes"
    )

    prefill_text = request.GET.get("sample", "")

    if request.method == "POST":

        text = request.POST.get("news", "").strip()

        # input validation

        if not text:
            return render(request, "home.html", {
                "error": "Please enter text.",
                "prefill_text": prefill_text
            })

        if not re.search(r"[A-Za-z]", text):
            return render(request, "home.html", {
                "error": "Only English text is supported.",
                "prefill_text": prefill_text
            })

        if re.search(r"[@#$%^*_+=<>~`{}[\]|\\]{4,}", text):
            return render(request, "home.html", {
                "error": "Only English text is supported.",
                "prefill_text": prefill_text
            })

        if not request.user.is_authenticated:
            if text != sample_text:
                return render(request, "home.html", {
                    "error": "Demo users can analyze only the provided sample text. Please login or register for custom analysis.",
                    "prefill_text": sample_text
                })

        words = text.split()

        if len(words) < 15:
            return render(request, "home.html", {
                "error": f"Minimum 15 words required. Currently {len(words)} words.",
                "prefill_text": prefill_text
            })

        label, confidence = predict_news(text)

        if request.user.is_authenticated:

            latest_model = MLModel.objects.filter(status="active").first()

            NewsAnalysis.objects.create(
                user=request.user,
                input_text=text,
                prediction_result=label,
                confidence_score=confidence,
                model=latest_model
            )

        return render(request, "home.html", {
            "result": label,
            "confidence": confidence,
            "prefill_text": text
        })

    return render(request, "home.html", {
        "prefill_text": prefill_text
    })



# PREDICTION FUNCTION

def predict_news(text):

    active_model = MLModel.objects.filter(status="active").first()

    if not active_model:
        raise Exception("No active model found")

    model_path = os.path.join(BASE_DIR, active_model.model_file)
    vectorizer_path = os.path.join(BASE_DIR, active_model.vectorizer_file)

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]
    probability = model.predict_proba(text_vector)

    confidence = np.max(probability)
    label = LABEL_MAP.get(str(prediction), prediction)

    return label, float(confidence)



# REGISTER

def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})



# HISTORY

@login_required
def history(request):

    data = NewsAnalysis.objects.filter(
        user=request.user
    ).order_by("-analysis_date")

    return render(request, "history.html", {
        "predictions": data
    })



# HISTORY CHART

@login_required
def history_chart(request):

    fake_count = NewsAnalysis.objects.filter(
        user=request.user,
        prediction_result="Fake"
    ).count()

    real_count = NewsAnalysis.objects.filter(
        user=request.user,
        prediction_result="Real"
    ).count()

    import json

    chart_data = json.dumps({
        "real": real_count,
        "fake": fake_count
    })

    return render(request, "history_chart.html", {
        "fake_count": fake_count,
        "real_count": real_count,
        "chart_data": chart_data
    })

# EXPORT HISTORY

@login_required
def export_history(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="history.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Text", "Prediction", "Confidence"])

    data = NewsAnalysis.objects.filter(user=request.user)

    for item in data:
        writer.writerow([
            item.analysis_date,
            item.input_text,
            item.prediction_result,
            item.confidence_score
        ])

    return response



# PROFILE

@login_required
def profile(request):

    if request.method == "POST":

        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "profile.html")



# CHANGE PASSWORD

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password updated successfully!")
            return redirect("profile")

    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {
        "form": form
    })


# ADMIN METRICS

@staff_member_required
def admin_metrics(request):

    active_model = MLModel.objects.filter(status="active").first()

    if active_model:
        metrics = PerformanceMetrics.objects.filter(
            model=active_model
        ).first()
    else:
        metrics = None

    return render(request, "admin_metrics.html", {
        "metrics": metrics
    })



# FIXED RETRAIN MODEL

@staff_member_required
def retrain_model(request):

    if request.method != "POST":
        return redirect("home")

    dataset = Dataset.objects.order_by("-uploaded_at").first()

    if not dataset:
        messages.error(request, "No dataset found.")
        return redirect("admin_metrics")

    try:
        df = pd.read_csv(dataset.file.path)

    except Exception:
        messages.error(request, "Unable to read CSV file.")
        return redirect("admin_metrics")

    #dataset validation

    df.columns = df.columns.str.strip().str.lower()

    if "news" not in df.columns or "label" not in df.columns:
        messages.error(request, "Dataset must contain news and label columns.")
        return redirect("admin_metrics")

    df = df.dropna(subset=["news", "label"])

    df["news"] = df["news"].astype(str).str.strip()
    df = df[df["news"] != ""]

    df = df.drop_duplicates(subset=["news"])

    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df = df[df["label"].isin([0, 1])]

    if len(df) < 10:
        messages.error(request, "Dataset too small.")
        return redirect("admin_metrics")

    X = df["news"]
    y = df["label"]

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=7000,
    min_df=2,
    max_df=0.90,
    sublinear_tf=True,
    ngram_range=(1, 2)
)

    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    model = LogisticRegression(
        max_iter=2000,
        solver="liblinear"
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")

    model_filename = f"model_{timestamp}.pkl"
    vectorizer_filename = f"vectorizer_{timestamp}.pkl"

    model_path = os.path.join(BASE_DIR, model_filename)
    vectorizer_path = os.path.join(BASE_DIR, vectorizer_filename)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    MLModel.objects.all().update(status="inactive")

    ml_model = MLModel.objects.create(
        model_name="LogisticRegression",
        version=timestamp,
        status="active",
        dataset=dataset,
        model_file=model_filename,
        vectorizer_file=vectorizer_filename
    )

    PerformanceMetrics.objects.create(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1,
        model=ml_model
    )

    messages.success(request, "Model retrained successfully!")

    return redirect("admin_metrics")



# USAGE REPORT

@staff_member_required
def usage_report(request):

    total_users = User.objects.count()
    total_predictions = NewsAnalysis.objects.count()

    fake_count = NewsAnalysis.objects.filter(
        prediction_result="Fake"
    ).count()

    real_count = NewsAnalysis.objects.filter(
        prediction_result="Real"
    ).count()

    predictions_per_user = (
        NewsAnalysis.objects
        .values("user__username")
        .annotate(total=Count("id"))
    )

    daily_stats = (
        NewsAnalysis.objects
        .annotate(date=TruncDate("analysis_date"))
        .values("date")
        .annotate(total=Count("id"))
        .order_by("date")
    )

    return render(request, "usage_report.html", {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "fake_count": fake_count,
        "real_count": real_count,
        "predictions_per_user": predictions_per_user,
        "daily_stats": daily_stats
    })



# DOWNLOAD USAGE REPORT

@staff_member_required
def download_usage_report(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="usage_report.csv"'

    writer = csv.writer(response)

    total_users = User.objects.count()
    total_predictions = NewsAnalysis.objects.count()

    fake_count = NewsAnalysis.objects.filter(
        prediction_result="Fake"
    ).count()

    real_count = NewsAnalysis.objects.filter(
        prediction_result="Real"
    ).count()

    writer.writerow(["System Usage Report"])
    writer.writerow([])
    writer.writerow(["Total Users", total_users])
    writer.writerow(["Total Predictions", total_predictions])
    writer.writerow(["Fake Predictions", fake_count])
    writer.writerow(["Real Predictions", real_count])
    writer.writerow([])

    writer.writerow(["Analyses Per Day"])
    writer.writerow(["Date", "Total"])

    daily_stats = (
        NewsAnalysis.objects
        .annotate(date=TruncDate("analysis_date"))
        .values("date")
        .annotate(total=Count("id"))
        .order_by("date")
    )

    for row in daily_stats:
        writer.writerow([row["date"], row["total"]])

    writer.writerow([])
    writer.writerow(["Predictions Per User"])
    writer.writerow(["Username", "Total"])

    predictions_per_user = (
        NewsAnalysis.objects
        .values("user__username")
        .annotate(total=Count("id"))
    )

    for row in predictions_per_user:
        writer.writerow([row["user__username"], row["total"]])

    UsageReport.objects.create(
        report_type="CSV",
        file_path="usage_report.csv",
        user=request.user
    )

    return response
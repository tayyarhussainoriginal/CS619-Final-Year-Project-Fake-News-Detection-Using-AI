from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Landing / Public Pages
    path("", views.landing, name="landing"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="landing"), name="logout"),
    path("register/", views.register, name="register"),

    # User Features
    path("home/", views.home, name="home"),
    path("history/", views.history, name="history"),
    path("export-history/", views.export_history, name="export_history"),
    path("history-chart/", views.history_chart, name="history_chart"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),

    # Admin Features
    path("admin-metrics/", views.admin_metrics, name="admin_metrics"),
    path("retrain/", views.retrain_model, name="retrain_model"),
    path("usage-report/", views.usage_report, name="usage_report"),
    path("download-report/", views.download_usage_report, name="download_report"),
    

]
from django.contrib import admin
from .models import NewsAnalysis, Dataset, MLModel, PerformanceMetrics, UsageReport


# ---------------------------
# NEWS ANALYSIS ADMIN
# ---------------------------
@admin.register(NewsAnalysis)
class NewsAnalysisAdmin(admin.ModelAdmin):
    list_display = ("user", "prediction_result", "confidence_score", "analysis_date", "model")
    list_filter = ("prediction_result", "analysis_date")
    search_fields = ("user__username", "input_text")


# ---------------------------
# DATASET ADMIN
# ---------------------------
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("file_name", "uploaded_at", "is_active", "user")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


# ---------------------------
# ML MODEL ADMIN
# ---------------------------
@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "version", "trained_date", "status", "dataset")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
# ---------------------------
# PERFORMANCE METRICS ADMIN
# ---------------------------
@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ("accuracy", "precision", "recall", "f1_score", "generated_at", "model")


# ---------------------------
# USAGE REPORT ADMIN
# ---------------------------
@admin.register(UsageReport)
class UsageReportAdmin(admin.ModelAdmin):
    list_display = ("report_type", "generated_date", "file_path", "user")
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os



# DATASET TABLE

class Dataset(models.Model):
    file = models.FileField(upload_to="datasets/")

    file_name = models.CharField(max_length=250, null=True, blank=True)   
    file_path = models.CharField(max_length=255, null=True, blank=True)  

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            try:
                self.file_path = self.file.path
            except:
                self.file_path = ""
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)
    
    def clean(self):
        if not self.file.name.endswith('.csv'):
            raise ValidationError("Only CSV files are allowed.")

    def __str__(self):
        return self.file_name if self.file_name else "Dataset"



# ML MODEL TABLE

from django.conf import settings
import os


class MLModel(models.Model):
    model_name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    trained_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")

    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True)

    model_file = models.CharField(max_length=255, null=True, blank=True)
    vectorizer_file = models.CharField(max_length=255, null=True, blank=True)

    def delete(self, *args, **kwargs):

        
        if self.status == "active":
            raise Exception("Cannot delete active model")

       
        if self.model_file:
            model_path = os.path.join(settings.BASE_DIR, self.model_file)
            if os.path.exists(model_path):
                os.remove(model_path)

        
        if self.vectorizer_file:
            vectorizer_path = os.path.join(settings.BASE_DIR, self.vectorizer_file)
            if os.path.exists(vectorizer_path):
                os.remove(vectorizer_path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.model_name} ({self.version})"


# PERFORMANCE METRICS TABLE

class PerformanceMetrics(models.Model):
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()

    generated_at = models.DateTimeField(auto_now_add=True)

    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Metrics - {self.model}"



# NEWS ANALYSIS TABLE

class NewsAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    input_text = models.TextField()
    prediction_result = models.CharField(max_length=20)
    confidence_score = models.FloatField()

    analysis_date = models.DateTimeField(auto_now_add=True)

    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return f"{self.user.username} - {self.prediction_result}"



# USAGE REPORT TABLE

class UsageReport(models.Model):
    report_type = models.CharField(max_length=50)
    generated_date = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.report_type} - {self.generated_date}"
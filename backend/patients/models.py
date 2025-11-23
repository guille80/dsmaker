from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.patient_id})"

class Study(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='studies')
    study_instance_uid = models.CharField(max_length=64, unique=True)
    study_date = models.DateField(null=True, blank=True)
    study_time = models.TimeField(null=True, blank=True)
    modality = models.CharField(max_length=16, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Study {self.study_instance_uid} - {self.modality}"

class Series(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='series')
    series_instance_uid = models.CharField(max_length=64, unique=True)
    modality = models.CharField(max_length=16, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    series_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Series {self.series_number} - {self.modality}"

class ImageInstance(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='images')
    sop_instance_uid = models.CharField(max_length=64, unique=True)
    file_path = models.CharField(max_length=1024)
    instance_number = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.instance_number}"

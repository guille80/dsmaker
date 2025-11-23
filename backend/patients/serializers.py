from rest_framework import serializers
from .models import Patient, Study, Series, ImageInstance

class ImageInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageInstance
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    images = ImageInstanceSerializer(many=True, read_only=True)
    class Meta:
        model = Series
        fields = '__all__'

class StudySerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=True, read_only=True)
    class Meta:
        model = Study
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    studies = StudySerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = '__all__'

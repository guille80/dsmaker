from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Patient, Study, Series, ImageInstance
from .serializers import PatientSerializer, StudySerializer, SeriesSerializer, ImageInstanceSerializer
from .utils import import_study_from_folder
import os

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class ImageInstanceViewSet(viewsets.ModelViewSet):
    queryset = ImageInstance.objects.all()
    serializer_class = ImageInstanceSerializer

class ImportStudyView(APIView):
    def post(self, request):
        folder_path = request.data.get('folder_path')
        if not folder_path:
            return Response({"error": "folder_path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.exists(folder_path):
            return Response({"error": "Folder does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            count, errors = import_study_from_folder(folder_path)
            return Response({
                "message": f"Successfully processed {count} DICOM files.",
                "errors": errors
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


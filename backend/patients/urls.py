from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, StudyViewSet, SeriesViewSet, ImageInstanceViewSet, ImportStudyView

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'studies', StudyViewSet)
router.register(r'series', SeriesViewSet)
router.register(r'images', ImageInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import_study/', ImportStudyView.as_view(), name='import_study'),
]

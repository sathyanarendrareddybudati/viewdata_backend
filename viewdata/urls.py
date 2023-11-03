from django.urls import path
from .views import DatasetListAPI, DatasetComputeView, DatasetPlotView

urlpatterns = [
    path('dataset/', DatasetListAPI.as_view()),
    path('dataset/<str:name>/compute/', DatasetComputeView.as_view(), name='dataset-compute'),
    path('dataset/<str:name>/plot/', DatasetPlotView.as_view(), name='dataset-plot'),
]

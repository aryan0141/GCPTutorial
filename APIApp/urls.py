from django.urls import path
from .views import sentimentAnalysis, englishToFrench, index
urlpatterns = [
    path('sentimentAnalysis', sentimentAnalysis, name="sentimentAnalysis"),
    path('englishToFrench', englishToFrench, name="englishToFrench"),
    path('', index, name="index"),
]
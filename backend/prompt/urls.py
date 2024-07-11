from django.urls import path
from .views import TextProcessView

urlpatterns = [
    path('process-text/', TextProcessView.as_view(), name='process_text'),
]

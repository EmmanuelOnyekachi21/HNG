from django.urls import path
from .views import HandleViews

urlpatterns = [
    path('hello/', HandleViews.as_view(), name='handleViews'),
]

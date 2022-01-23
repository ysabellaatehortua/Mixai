from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('genetic_algorithm/', views.genetic_alg, name='genetic-algorithm'),
]
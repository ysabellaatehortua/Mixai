from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('genetic_algorithm/', views.genetic_alg, name='genetic-algorithm'),
    path("register/", views.register_request, name="register"),
    path("about/", views.register_request, name="about")
]
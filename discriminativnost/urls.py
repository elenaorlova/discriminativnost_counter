from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dc', views.Discr.as_view()),
]
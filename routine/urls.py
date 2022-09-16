
from django.urls import path
from . import views

urlpatterns = [
    path('',views.RoutineApiView.as_view()),
]
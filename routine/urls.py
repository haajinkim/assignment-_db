
from django.urls import path
from . import views

urlpatterns = [
    path('',views.RoutineApiView.as_view()),
    path('result',views.RoutineResultApiView.as_view())
]
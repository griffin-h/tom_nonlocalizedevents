from django.urls import path

from . import views

urlpatterns = [
    path('', views.SupereventListView.as_view(), name='index'),
    path('<int:pk>/', views.SupereventDetailView.as_view(), name='detail'),
]
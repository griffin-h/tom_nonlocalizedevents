from django.urls import path

from . import views

# app_name provides namespace in {% url %} template tag
# (i.e. {% url 'superevents:detail' <pk> %}
app_name = 'superevents'

urlpatterns = [
    path('', views.SupereventListView.as_view(), name='index'),
    path('<int:pk>/', views.SupereventDetailView.as_view(), name='detail'),
]
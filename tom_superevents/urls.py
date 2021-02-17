from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'superevents', views.SupereventViewSet)
router.register(r'eventlocalizations', views.EventLocalizationViewSet)

# app_name provides namespace in {% url %} template tag
# (i.e. {% url 'superevents:detail' <pk> %}
app_name = 'superevents'

urlpatterns = [
    path('', views.SupereventListView.as_view(), name='index'),
    path('<int:pk>/', views.SupereventDetailView.as_view(), name='detail'),
    # django restframework URLConf
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
from django.views import generic

from rest_framework import viewsets
from rest_framework import permissions

from .models import Superevent, EventLocalization
from .serializers import SupereventSerializer, EventLocalizationSerializer

class SupereventListView(generic.ListView):
    model = Superevent
    template_name = 'tom_superevents/index.html'


class SupereventDetailView(generic.DetailView):
    model = Superevent
    template_name = 'tom_superevents/detail.html'


# Django Rest Framework Views


class SupereventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Superevents to be viewed or edited.
    """
    queryset = Superevent.objects.all()
    serializer_class = SupereventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventLocalizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EventLocalizations to be viewed or edited.
    """
    queryset = EventLocalization.objects.all()
    serializer_class = EventLocalizationSerializer
    permission_classes = [permissions.IsAuthenticated]

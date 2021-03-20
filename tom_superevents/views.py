from importlib import import_module

from django.conf import settings
from django.views.generic import DetailView, ListView
from rest_framework import viewsets
from rest_framework import permissions

from .models import Superevent, EventLocalization
from .serializers import SupereventSerializer, EventLocalizationSerializer


class SupereventListView(ListView):
    model = Superevent
    template_name = 'tom_superevents/index.html'


class SupereventDetailView(DetailView):
    """
    Requires the following setting:

    SUPEREVENT_CLASSES = {
        'gravitational_wave_event': 'tom_superevents.superevent_clients.gracedb.GraceDBClient',
        'gamma_ray_burst': None
    }
    """
    model = Superevent
    template_name = 'tom_superevents/detail.html'

    # TODO: Discuss w/David: adding SupereventTypes (via settings.py) is not supported at the moment
    template_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE: 'tom_superevents/superevent_detail/gravitational_wave.html',
        Superevent.SupereventType.GAMMA_RAY_BURST: 'tom_superevents/superevent_detail/gamma_ray_burst.html',
        Superevent.SupereventType.NEUTRINO: 'tom_superevents/superevent_detail/neutrino.html',
    }
    client_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE: 'tom_superevents.superevent_clients.gracedb.GraceDBClient',
        Superevent.SupereventType.GAMMA_RAY_BURST: None,
        Superevent.SupereventType.NEUTRINO: None,
        Superevent.SupereventType.UNKNOWN: None,
    }

    def get_template_names(self):
        obj = self.get_object()
        if obj.superevent_type is None or obj.superevent_type not in [choice[0] for choice in Superevent.SupereventType.choices]:
            return super().get_template_names()
        return [self.template_mapping[obj.superevent_type]]

    # TODO: error handling
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module_name, class_name = self.client_mapping[self.object.superevent_type].rsplit('.', 1)
        module = import_module(module_name)
        superevent_client_class = getattr(module, class_name)
        superevent_client = superevent_client_class()
        context['superevent_data'] = superevent_client.get_superevent_data(self.object.superevent_id)
        return context


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

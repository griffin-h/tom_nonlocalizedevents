from django.views import generic

from .models import Superevent


class SupereventListView(generic.ListView):
    model = Superevent
    template_name = 'tom_superevents/index.html'


class SupereventDetailView(generic.DetailView):
    model = Superevent
    template_name = 'tom_superevents/detail.html'

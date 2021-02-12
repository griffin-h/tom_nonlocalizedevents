from django.views import generic

from .models import Superevent


class SupereventListView(generic.ListView):
    model = Superevent
    template_name = 'tom_superevent/index.html'


class SupereventDetailView(generic.DetailView):
    model = Superevent
    template_name = 'tom_superevent/detail.html'

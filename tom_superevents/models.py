from django.conf import settings
from django.db import models


class Superevent(models.Model):
    """Represents a Superevent being followed-up upon by this TOM.
    For the moment, this is rather GraceDB specific, but sh/could be generalized to work
    with gamma-ray bursts et al
    """
    # TODO: ask Curtis/Rachel/Andy about generalized use cases.
    superevent_id = models.CharField(max_length=64)  # GraceDB superevent_id reference
    superevent_url = models.URLField()  # TODO: this should instead be constructed via superevent_id
    superevent_type = models.CharField(max_length=50)  # Should eventually be ChoiceField

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.superevent_id


class EventLocalization(models.Model):
    """Represents a region of the sky in which a superevent may have taken place.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


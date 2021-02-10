from django.db import models

import tom_targets.models

# Create your models here.


class CandidateTarget(tom_targets.models.Target):
    """This is an experiment to see if it makes sense to extend
    the tom_targets.models.Target with a subclass.
    """
    pass


class EventLocalization(models.Model):
    """Represents a region of the sky in which a superevent may have taken place.
    """
    pass

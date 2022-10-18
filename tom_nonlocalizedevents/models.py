from django.db import models

from tom_targets.models import Target


class NonLocalizedEvent(models.Model):
    """Represents a NonLocalizedEvent being followed-up upon by this TOM.

    A NonLocalizedEvent is distinguished from a Target in that it is localized to a region of the sky
    (vs. a specific RA,DEC). The potential Targets in the localization region must be identified,
    prioritized, and categorized (retired, of-interest, etc) for follow-up EM observations

    For the moment, this is rather GraceDB (GW) specific, but sh/could be generalized to work
    with gamma-ray burst and neutrino events.
    """

    class NonLocalizedEventType(models.TextChoices):
        GRAVITATIONAL_WAVE = 'GW', 'Gravitational Wave'
        GAMMA_RAY_BURST = 'GRB', 'Gamma-ray Burst'
        NEUTRINO = 'NU', 'Neutrino'
        UNKNOWN = 'UNK', 'Unknown'

    event_type = models.CharField(
        max_length=3,
        choices=NonLocalizedEventType.choices,
        default=NonLocalizedEventType.GRAVITATIONAL_WAVE,
        help_text='The type of NonLocalizedEvent, used for determining how to ingest and display it'
    )
    event_subtype = models.CharField(
        max_length=256,
        default='',
        help_text='The subtype of the event. Options are type specific, i.e. GW events have initial, '
                  'preliminary, update types.'
    )

    # TODO: ask Curtis/Rachel/Andy about generalized use cases.
    event_id = models.CharField(
        max_length=64,
        help_text='Unique identifer for the event. I.E. the TRIGGER_NUM for a GW event.'
    )
    sequence_id = models.PositiveIntegerField(
        default=1,
        help_text='The version / update number of this event. I.E. the SEQUENCE_NUM for a GW event.'
    )
    skymap_file_url = models.URLField(
        default='',
        help_text='The URL to a file containing skymap details for the event.'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['event_id', 'sequence_id']

    @property
    def gracedb_url(self):
        """Construct and return the GraceDB URL for this nonlocalizedevent from the event_id Field.

        for example, https://gracedb.ligo.org/superevents/S200316bj/
        """
        # TODO: add check that superevent_type is GRAVITATIONAL_WAVE
        return f"https://gracedb.ligo.org/superevents/{self.event_id}/"

    @property
    def treasuremap_url(self):
        """Construct and return the Treasure Map (treasuremap.space) URL for this nonlocalizedevent
        from the event_id Field.

        for example: http://treasuremap.space/alerts?graceids=S200219ac
        """
        # TODO: add check that superevent_type is GRAVITATIONAL_WAVE
        return f"http://treasuremap.space/alerts?graceids={self.event_id}"

    def __str__(self):
        return f"{self.event_id}_{self.sequence_id}"


class EventCandidate(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    nonlocalizedevent = models.ForeignKey(NonLocalizedEvent, related_name='candidates', on_delete=models.CASCADE)

    viable = models.BooleanField(
        default=True,
        help_text='Whether this event candidate is actively being considered or not'
    )
    viability_reason = models.TextField(
        default='',
        help_text='Reason why this candidates viability is set the way it is.'
    )
    priority = models.IntegerField(
        default=1,
        # TODO: add description, etc
    )

    class Meta:
        constraints = [  # TODO: this constraint isn't working
            models.UniqueConstraint(fields=['target', 'nonlocalizedevent'], name='Unique Target/NonLocalizedEvent')
        ]

    def __str__(self):
        return f'EventCandidate({self.id}) NonLocalizedEvent: {self.nonlocalizedevent} Target: {self.target}'


class EventLocalization(models.Model):
    """Represents a region of the sky in which a nonlocalizedevent may have taken place.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

from django.dispatch import receiver
from django.db.models.signals import post_save

from tom_nonlocalizedevents.models import NonLocalizedEvent

@receiver(post_save, sender=NonLocalizedEvent)
def cb_nonlocalizedevent_add_candidates(sender, instance, *args, **kwargs):
    # If this is not the first sequence in an event, attempt to find the previous
    # sequence and copy over its candidate event list
    if instance.sequence_id > 1:
        previous_sequence = instance.sequence_id - 1
        previous_instance = NonLocalizedEvent.objects.filter(
            event_id=instance.event_id).exclude(sequence_id=instance.sequence_id).order_by('-sequence_id').first()

        if previous_instance:
            candidates = previous_instance.candidates.all()
            for candidate in candidates:
                candidate.pk = None
                candidate.nonlocalizedevent = instance
                candidate._state.adding = True
                candidate.save()

import factory

from tom_nonlocalizedevents.models import NonLocalizedEvent, EventLocalization


class NonLocalizedEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NonLocalizedEvent

    event_id = factory.Faker('pystr')
    skymap_file_url = factory.Faker('pystr')


class EventLocalizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventLocalization

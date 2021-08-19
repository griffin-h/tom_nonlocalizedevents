from rest_framework import serializers
from tom_targets.models import Target
from tom_targets.serializers import TargetSerializer

from tom_superevents.models import EventCandidate, EventLocalization, Superevent


class SupereventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Superevent
        fields = ['superevent_id', 'superevent_url',
                  'id', 'created', 'modified']


class EventCandidateSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ``EventCandidate``. ``PrimaryKeyRelatedField``s are used in order to allow creating an
    ``EventCandidate`` with just a primary key, and ``to_representation`` is then overridden for proper display values.
    See: https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    """
    superevent = serializers.PrimaryKeyRelatedField(queryset=Superevent.objects.all())
    target = serializers.PrimaryKeyRelatedField(queryset=Target.objects.all())

    class Meta:
        model = EventCandidate
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['target'] = TargetSerializer(Target.objects.get(pk=representation['target'])).data
        representation['superevent'] = SupereventSerializer(
            Superevent.objects.get(pk=representation['superevent'])
        ).data
        return representation


class EventLocalizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventLocalization
        fields = [
            'id', 'created', 'modified']

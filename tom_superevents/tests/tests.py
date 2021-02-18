from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from tom_superevents.tests.factories import SupereventFactory, EventLocalizationFactory


class SupereventAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.superevent1 = SupereventFactory.create(superevent_id='superevent1')
        self.superevent2 = SupereventFactory.create(superevent_id='superevent2')
        self.eventlocalization1 = EventLocalizationFactory.create()
        self.eventlocalization2 = EventLocalizationFactory.create()

        # TODO: sort out django-guardian permissions
        # assign_perm('tom_targets.view_target', self.user, self.st2)

        self.client.force_login(self.user)


class TestSupereventViewSet(SupereventAPITestCase):
    def test_01(self):
        pass


class TestEventLocalizationViewSet(SupereventAPITestCase):
    pass

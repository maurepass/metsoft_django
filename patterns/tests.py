import factory
from django.contrib.auth.models import Group, User, Permission

from django.test import TestCase
from django.urls import reverse

from .models import Pattern, PatternStatus


class PatternStatusFactory(factory.DjangoModelFactory):
    class Meta:
        model = PatternStatus


class PatternsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # users
        cls.user1 = User.objects.create_user(username='modelarnia', password='test_password')
        cls.user2 = User.objects.create_user(username='noname', password='nopass')
        cls.group_model = Group.objects.create(name='modelarnia')
        cls.user1.groups.add(cls.group_model)

        # patterns
        cls.pattern1 = Pattern.objects.create(status=PatternStatusFactory())
        cls.perm_add_pattern = Permission.objects.get(codename='add_pattern')
        cls.perm_change_pattern = Permission.objects.get(codename='change_pattern')

    def test_url_patterns(self):
        response = self.client.get(reverse('patterns:patterns'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/patterns/api/patterns/')
        self.assertEqual(response.status_code, 200)

    def test_url_pattern_card(self):
        response = self.client.get(reverse('patterns:pattern-card', args=[self.pattern1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_url_pattern_create(self):
        response = self.client.get(reverse('patterns:pattern-create'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='noname', password='nopass')
        response = self.client.get(reverse('patterns:pattern-create'))
        self.assertEqual(response.status_code, 403)
        # self.user1.user_permissions.add(self.perm_add_pattern)
        # self.client.login(username='modelarnia', password='test_password')
        # self.assertEqual(response.status_code, 200)

    def test_url_pattern_report(self):
        response = self.client.get(reverse('patterns:pattern-report'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('patterns:pattern-report'), {'customer1': 'test'})
        self.assertEqual(response.status_code, 200)





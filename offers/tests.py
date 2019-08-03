from django.test import TestCase

from .models import Offer


class OfferTestCase(TestCase):

    def setUp(self):
        Offer.objects.create(offer_no='777/77', client='Noreva')

    def tearDown(self):
        Offer.objects.filter(offer_no='777/77').delete()

    def test_offer_exist(self):
        of = Offer.objects.get(offer_no='777/77')
        self.assertEqual(of.client, 'Noreva')

from django.test import TestCase, RequestFactory
from unittest.mock import patch
from datetime import datetime, timedelta
from django.shortcuts import reverse
from django.contrib.auth.models import User, Permission, ContentType


from .models import (Offer, OfferStatus, Detail, MaterialGroup, Material, MachiningType, HeatTreatment, PatternTaper,
                     AtestType, OfferPatternStatus, Notice)
from .views import OfferCreateView, DetailCreateView


class OffersModelsTest(TestCase):
    """ Unit Tests for Models"""

    def test_string_from_list(self):
        test_list = ['test1', 'test1', 'test1', 'test2', 'test2']
        results = 'test1: 1,2,3,; test2: 4,5,; '
        self.assertEqual(Offer.string_from_list(test_list), results)


class OffersViewsTests(TestCase):
    """Unit Tests for Views"""

    @patch('offers.views.Offer.objects.last')
    def test_offer_create_view_get_initial_try(self, mock_objects_last):

        class NewOffer:
            offer_no = '100/17'

        mock_objects_last.return_value = NewOffer()
        view = OfferCreateView()
        initial = view.get_initial()
        self.assertEqual(initial['offer_no'], '101/17')

    @patch('offers.views.Offer.objects.last')
    def test_offer_create_view_get_initial_except(self, mock_offer_objects_last):

        class NewOffer:
            offer_no = 'a100/17'

        mock_offer_objects_last.return_value = NewOffer()
        view = OfferCreateView()
        initial = view.get_initial()
        self.assertEqual(initial['offer_no'], 'a100/17')

    # @patch('offers.view.Offer.objects.get')
    # def test_detail_create_view_form_valid(self, mock_offer_objects_get):
    #     class NewOffer:
    #         positions_amount = 0
    #
    #     mock_offer_objects_get.return_value = NewOffer()
    #     view = DetailCreateView()
    #     view.form_valid()


class OffersIntegrationTest(TestCase):
    """ Integration Tests for Offers"""

    @classmethod
    def setUpTestData(cls):
        # users
        cls.user1 = User.objects.create_user(username='test_user1', password='test_password')
        cls.user2 = User.objects.create_user('test_user2')

        # offers
        cls.of_stat_id1 = OfferStatus.objects.create(id=1, offer_status='test status id 1')
        cls.of_stat_id2 = OfferStatus.objects.create(id=2, offer_status='test status id 2')
        cls.notice = Notice.objects.create(content='test_notices')
        cls.perm_add_offer = Permission.objects.get(codename='add_offer')
        cls.perm_change_offer = Permission.objects.get(codename='change_offer')

        cls.offer1 = Offer.objects.create(
            offer_no='0/00',
            client='test_client1',
            user_mark=cls.user1,
            user_tech=cls.user2,
            status=cls.of_stat_id1,
            date_tech_in=datetime.today() - timedelta(days=5)
        )
        cls.offer2 = Offer.objects.create(
            offer_no='0/00',
            client='test_client2',
            user_mark=cls.user1,
            user_tech=cls.user2,
            status=cls.of_stat_id2,
            date_tech_in=datetime.today() - timedelta(days=5)
        )

        # materials
        cls.content_type_offers_material = ContentType.objects.get(app_label='offers', model='material')
        cls.perm_add_material = Permission.objects.get(
            codename='add_material',
            content_type=cls.content_type_offers_material
        )
        cls.perm_change_material = Permission.objects.get(
            codename='change_material',
            content_type_id=cls.content_type_offers_material
        )
        MaterialGroup.objects.create(id=1, mat_group=21, description='test_material_group')
        cls.mat1 = Material.objects.create(
            material='test_material_test_1',
            mat_group=MaterialGroup.objects.get(id=1)
        )

        # details
        cls.perm_add_detail = Permission.objects.get(codename='add_detail')
        cls.perm_change_detail = Permission.objects.get(codename='change_detail')
        cls.perm_delete_detail = Permission.objects.get(codename='delete_detail')
        cls.mach1 = MachiningType.objects.create(machining='test_machining_1')
        HeatTreatment.objects.create(term='test_heat_treatment_1')
        PatternTaper.objects.create(taper='test_pattern_taper_1')
        AtestType.objects.create(atest='test_atest_type_1')
        OfferPatternStatus.objects.create(status='offer_pattern_status_1')
        cls.detail1 = Detail.objects.create(
            offer=cls.offer1,
            mat=cls.mat1,
            machining=cls.mach1,
            tolerances='test_tolerances_1',
            tapers='test_tapers_1',
            atest='test_atest_1',
        )
        cls.detail2 = Detail.objects.create(
            offer=cls.offer1,
            mat=cls.mat1,
            machining=cls.mach1,
            tolerances='test_tolerances_1',
            tapers='test_tapers_2',
            atest='test_atest_2',
        )

    def user1_logged(self):
        return self.client.login(username='test_user1', password='test_password')

    def test_url_offers(self):
        response = self.client.get(reverse('offers'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/offers/api/offers/')
        self.assertEqual(response.status_code, 200)

    def test_url_offer_create(self):
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 302)
        self.user1_logged()
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_add_offer)
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 200)

    def test_url_offer_update(self):
        self.user1_logged()
        response = self.client.get(reverse('offer-update', args=[self.offer1.pk]))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_change_offer)
        response = self.client.get(reverse('offer-update', args=[self.offer1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_url_offer_print(self):
        response = self.client.get('/offers/{}/print/'.format(self.offer1.pk))
        self.assertEqual(response.status_code, 200)

    def test_url_offer_details(self):
        response = self.client.get(reverse('offer-details', args=[self.offer1.pk]))
        self.assertEqual(response.status_code, 302)
        self.user1_logged()
        response = self.client.get(reverse('offer-details', args=[self.offer1.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('offer-details', args=[self.offer1.pk]), {'status': '1'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('offer-details', args=[self.offer1.pk]), {'new_notices': 'updated notices'})
        self.assertEqual(response.status_code, 200)

    def test_url_offer_notices_get(self):
        self.user1_logged()
        response = self.client.get('/offers/notices/')
        self.assertEqual(response.status_code, 200)

    def test_url_offer_notice_post(self):
        self.user1_logged()
        response = self.client.post('/offers/notices/', {'notices': 'new_notices'})
        self.assertEqual(response.status_code, 200)

    def test_url_offer_detail_create(self):
        self.user1_logged()
        response = self.client.get('/offers/{}/details/create/?steel'.format(self.offer1.pk))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_add_detail)
        response = self.client.get('/offers/{}/details/create/?steel'.format(self.offer1.pk))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/offers/{}/details/create/?iron'.format(self.offer1.pk))
        self.assertEqual(response.status_code, 200)

    def test_url_offer_detail_update(self):
        self.user1_logged()
        response = self.client.get(reverse('detail-update', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_change_detail)
        response = self.client.get(reverse('detail-update', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('detail-update', args=[self.offer1.pk, self.detail1.pk]),
            {'new-detail': ''}
        )
        self.assertEqual(response.status_code, 200)

    def test_url_offer_detail_delete(self):
        self.user1_logged()
        response = self.client.get(reverse('detail-delete', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_delete_detail)
        response = self.client.get(reverse('detail-delete', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_url_details(self):
        response = self.client.get('/offers/details/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/offers/api/details/')
        self.assertEqual(response.status_code, 200)

    def test_url_details_searching(self):
        response = self.client.get(reverse('details-searching'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('details-searching'),
            {'cast_name': 'Body', 'drawing_no': '', 'offer_no': ''}
        )
        self.assertEqual(response.status_code, 200)

    def test_url_materials(self):
        response = self.client.get(reverse('materials'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/offers/api/materials/')
        self.assertEqual(response.status_code, 200)

    def test_url_material_create(self):
        response = self.client.get(reverse('material-create'))
        self.assertEqual(response.status_code, 302)
        self.user1_logged()
        response = self.client.get(reverse('material-create'))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_add_material)
        response = self.client.get(reverse('material-create'))
        self.assertEqual(response.status_code, 200)

    def test_url_material_update(self):
        response = self.client.get(reverse('material-update', args=[self.mat1.pk]))
        self.assertEqual(response.status_code, 302)
        self.user1_logged()
        response = self.client.get(reverse('material-update', args=[self.mat1.pk]))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_change_material)
        response = self.client.get(reverse('material-update', args=[self.mat1.pk]))
        self.assertEqual(response.status_code, 200)



    #
    # def test_get_days_amount(self):
    #     self.assertEqual(self.offer1.get_days_amount(), 5)
    #     self.assertIsNone(self.offer2.get_days_amount())
    #
    # def test_offer_status_creation(self):
    #     self.assertTrue(isinstance(self.of_stat1, OfferStatus))
    #     self.assertEqual(self.of_stat1.__str__(), self.of_stat1.offer_status)
    #

    # def test_prepare_details(self):
    #     results = {
    #         'machining': 'test_machining_1: 1,2,; ',
    #         'tolerances': 'test_tolerances_1: 1,2,; ',
    #         'tapers': 'test_tapers_1: 1,; test_tapers_2: 2,; ',
    #         'atest': 'test_atest_1: 1,; test_atest_2: 2,; ',
    #     }
    #     self.assertEqual(self.offer1.prepare_details(), results)
    #












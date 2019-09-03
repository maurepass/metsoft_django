from django.test import TestCase
from unittest.mock import patch
from django.shortcuts import reverse

from django.contrib.auth.models import User, Group, Permission, PermissionManager, PermissionsMixin, ContentType

import datetime

from .models import (Offer, OfferStatus, Detail, MaterialGroup, Material, MachiningType, HeatTreatment, PatternTaper,
                     AtestType, OfferPatternStatus, Notice)

from .views import OfferCreateView


class OfferTest(TestCase):

    @patch.object(OfferCreateView, 'get_last_offer')
    def test_offer_create_view_try(self, mock_get_last_offer):

        class NewOffer:
            offer_no = '100/17'

        mock_get_last_offer.return_value = NewOffer()
        view = OfferCreateView()
        initial = view.get_initial()
        self.assertEqual(initial['offer_no'], '101/17')

    @patch.object(OfferCreateView, 'get_last_offer')
    def test_offer_create_view_except(self, mock_get_last_offer):
        class NewOffer:
            offer_no = 'a100/17'

        mock_get_last_offer.return_value = NewOffer()
        view = OfferCreateView()
        initial = view.get_initial()
        self.assertEqual(initial['offer_no'], 'a100/17')


    # @classmethod
    # def setUpTestData(cls):
    #     cls.notice = Notice.objects.create(content='test_notices')
    #     cls.of_stat1 = OfferStatus.objects.create(id=1, offer_status='test status 1')
    #     cls.of_stat2 = OfferStatus.objects.create(id=2, offer_status='test status 2')
    #     cls.perm_add_offer = Permission.objects.get(codename='add_offer')
    #     cls.perm_change_offer = Permission.objects.get(codename='change_offer')
    #     cls.perm_add_detail = Permission.objects.get(codename='add_detail')
    #     cls.perm_change_detail = Permission.objects.get(codename='change_detail')
    #     cls.perm_delete_detail = Permission.objects.get(codename='delete_detail')
    #     cls.content_type_offers_material = ContentType.objects.get(app_label='offers', model='material')
    #     cls.perm_add_material = Permission.objects.get(
    #         codename='add_material',
    #         content_type=cls.content_type_offers_material
    #     )
    #     cls.perm_change_material = Permission.objects.get(
    #         codename='change_material',
    #         content_type_id=cls.content_type_offers_material
    #     )
    #     cls.user1 = User.objects.create_user(username='test_user1', password='test_password')
    #     cls.user1.user_permissions.add(cls.perm_add_offer.id)
    #     cls.user1.user_permissions.add(cls.perm_change_offer.id)
    #     cls.user1.user_permissions.add(cls.perm_add_detail.id)
    #     cls.user1.user_permissions.add(cls.perm_change_detail)
    #     cls.user1.user_permissions.add(cls.perm_delete_detail)
    #     cls.user1.user_permissions.add(cls.perm_add_material)
    #     cls.user1.user_permissions.add(cls.perm_change_material)
    #     cls.user2 = User.objects.create_user('test_user2')
    #     cls.group1 = Group.objects.create(name='test_group_1')
    #     cls.group2 = Group.objects.create(name='test_group_2')
    #     cls.offer1 = Offer.objects.create(
    #         offer_no='0/00',
    #         client='test_client',
    #         user_mark=cls.user1,
    #         user_tech=cls.user2,
    #         status=cls.of_stat1,
    #         date_tech_in=datetime.date.today() - datetime.timedelta(days=5)
    #     )
    #     cls.offer2 = Offer.objects.create(
    #         offer_no='0/00',
    #         client='test_client',
    #         user_mark=cls.user1,
    #         user_tech=cls.user2,
    #         status=cls.of_stat2,
    #         date_tech_in=datetime.date.today() - datetime.timedelta(days=5)
    #     )
    #     MaterialGroup.objects.create(
    #         id=1,
    #         mat_group=21,
    #         description='test_material_group'
    #     )
    #     cls.mat1 = Material.objects.create(
    #         material='test_material_test_1',
    #         mat_group=MaterialGroup.objects.get(id=1)
    #     )
    #     HeatTreatment.objects.create(term='test_heat_treatment_1')
    #     cls.mach1 = MachiningType.objects.create(machining='test_machining_1')
    #     PatternTaper.objects.create(taper='test_pattern_taper_1')
    #     AtestType.objects.create(atest='test_atest_type_1')
    #     OfferPatternStatus.objects.create(status='offer_pattern_status_1')
    #     Detail.objects.create(
    #         offer=cls.offer1,
    #         mat=cls.mat1,
    #         machining=cls.mach1,
    #         tolerances='test_tolerances_1',
    #         tapers='test_tapers_1',
    #         atest='test_atest_1',
    #     )
    #     Detail.objects.create(
    #         offer=cls.offer1,
    #         mat=cls.mat1,
    #         machining=cls.mach1,
    #         tolerances='test_tolerances_1',
    #         tapers='test_tapers_2',
    #         atest='test_atest_2',
    #     )
    #
    # def user1_login(self):
    #     return self.client.login(username='test_user1', password='test_password')
    #
    # def test_get_days_amount(self):
    #     self.assertEqual(self.offer1.get_days_amount(), 5)
    #     self.assertIsNone(self.offer2.get_days_amount())
    #
    # def test_offer_status_creation(self):
    #     self.assertTrue(isinstance(self.of_stat1, OfferStatus))
    #     self.assertEqual(self.of_stat1.__str__(), self.of_stat1.offer_status)
    #
    # def test_string_from_list(self):
    #     list1 = ['test1', 'test1', 'test1', 'test2', 'test2']
    #     self.assertEqual(Offer.string_from_list(list1), 'test1: 1,2,3,; test2: 4,5,; ')
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
    # def test_url_offers(self):
    #     response = self.client.get('/offers/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_create(self):
    #     self.user1_login()
    #
    #     response = self.client.get('/offers/create/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_offer_update(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/1/update/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_print(self):
    #     response = self.client.get('/offers/1/print/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_details(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/1/details/')
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post('/offers/1/details/', {'status': '1'})
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post('/offers/1/details/', {'new_notices': 'updated notices'})
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_notices_get(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/notices/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_notice_post(self):
    #     self.user1_login()
    #     response = self.client.post('/offers/notices/', {'notices': 'new_notices'})
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_detail_create(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/1/details/create/?steel')
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.get('/offers/1/details/create/?iron')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_detail_update(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/1/details/1/update/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_offer_detail_delete(self):
    #     self.user1_login()
    #     response = self.client.get('/offers/1/details/1/delete/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_details(self):
    #     response = self.client.get(reverse('details-index'))
    #     self.assertEqual(response.status_code, 200)
    #
    # # def test_url_details_searching(self):
    # #     response = self.client.get('/offers/details/searching')
    # #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_materials(self):
    #     response = self.client.get(reverse('materials'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_material_create(self):
    #     self.user1_login()
    #     response = self.client.get(reverse('material-create'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_material_update(self):
    #     self.user1_login()
    #     response = self.client.get(reverse('material-update', args=[1]))
    #     self.assertEqual(response.status_code, 200)
    #
    #
    #
    #
    #













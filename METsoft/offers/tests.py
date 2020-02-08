import factory
import pytest

from django.test import TestCase
from unittest.mock import patch
from datetime import datetime, timedelta
from django.shortcuts import reverse
from django.contrib.auth.models import User, Permission, ContentType, Group

from . import models


class OfferStatusFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.OfferStatus


def test_offer_string_from_list():
    test_list = ['test1', 'test1', 'test1', 'test2', 'test2']
    results = 'test1: 1,2,3; test2: 4,5; '
    assert models.Offer.string_from_list(test_list) == results


@patch('offers.models.reverse')
def test_offer_get_absolute_url(mock_reverse):
    mock_reverse.return_value = 'test'
    assert models.Offer.get_absolute_url() == 'test'
    mock_reverse.assert_called()


@patch('offers.models.reverse')
def test_material_get_absolute_url(mock_reverse):
    mock_reverse.return_value = 'test'
    assert models.Offer.get_absolute_url() == 'test'
    mock_reverse.assert_called()


@pytest.mark.django_db
class OffersViewsTests(TestCase):
    """Unit Tests for Views"""

    def offer_create_view(self):
        from . import views
        return views.OfferCreateView()

    @patch('offers.views.Offer.objects.last')
    def test_offer_create_view_get_initial_try(self, mock_objects_last):
        class NewOffer:
            offer_no = '100/17'

        mock_objects_last.return_value = NewOffer()
        initial = self.offer_create_view().get_initial()
        self.assertEqual(initial['offer_no'], '101/17')

    @patch('offers.views.Offer.objects.last')
    def test_offer_create_view_get_initial_except(self, mock_offer_objects_last):
        class NewOffer:
            offer_no = 'a100/17'

        mock_offer_objects_last.return_value = NewOffer()
        initial = self.offer_create_view().get_initial()
        self.assertEqual(initial['offer_no'], 'a100/17')


@pytest.mark.django_db
class OffersIntegrationTest(TestCase):
    """ Integration Tests for Offers"""

    databases = {'kokila', 'default'}

    @classmethod
    def setUpTestData(cls):
        # users
        cls.user1 = User.objects.create_user(username='test_user1', password='test_password')
        cls.user2 = User.objects.create_user('test_user2')
        cls.group_mark = Group.objects.create(name='marketing')
        cls.user1.groups.add(cls.group_mark)
        cls.group_tech = Group.objects.create(name='technologia')
        cls.user2.groups.add(cls.group_tech)

        # offers
        cls.of_stat_id1 = models.OfferStatus.objects.create(id=1, offer_status='test status id 1')
        cls.of_stat_id2 = models.OfferStatus.objects.create(id=2, offer_status='test status id 2')
        cls.notice = models.Notice.objects.create(content=u'test_notices')

        models.Notice.objects.create(content=r'a')
        cls.perm_add_offer = Permission.objects.get(codename='add_offer')
        cls.perm_change_offer = Permission.objects.get(codename='change_offer')

        cls.offer1 = models.Offer.objects.create(
            offer_no='0/00',
            client='test_client1',
            user_mark=cls.user1,
            user_tech=cls.user2,
            status=cls.of_stat_id1,
            date_tech_in=datetime.today() - timedelta(days=5),
            positions_amount=2,
        )
        cls.offer2 = models.Offer.objects.create(
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
        models.MaterialGroup.objects.create(id=1, mat_group=21, description='test_material_group')
        cls.mat1 = models.Material.objects.create(
            material='test_material_test_1',
            mat_group=models.MaterialGroup.objects.get(id=1)
        )

        # details
        cls.perm_add_detail = Permission.objects.get(codename='add_detail')
        cls.perm_change_detail = Permission.objects.get(codename='change_detail')
        cls.perm_delete_detail = Permission.objects.get(codename='delete_detail')
        cls.mach1 = models.MachiningType.objects.create(machining='test_machining_1')
        cls.heat_treat1 = models.HeatTreatment.objects.create(term='test_heat_treatment_1')
        cls.pat_taper_1 = models.PatternTaper.objects.create(taper='test_pattern_taper_1')
        cls.atest_type1 = models.AtestType.objects.create(atest='test_atest_type_1')
        cls.of_pat_status1 = models.OfferPatternStatus.objects.create(status='offer_pattern_status_1')
        cls.detail1 = models.Detail.objects.create(
            offer=cls.offer1,
            mat=cls.mat1,
            machining=cls.mach1,
            tolerances='test_tolerances_1',
            tapers='test_tapers_1',
            atest='test_atest_1',
        )
        cls.detail2 = models.Detail.objects.create(
            offer=cls.offer1,
            mat=cls.mat1,
            machining=cls.mach1,
            tolerances='test_tolerances_1',
            tapers='test_tapers_2',
            atest='test_atest_2',
        )
        cls.detail_data_form = {
            'new-detail': '',
            'steel': '',
            'cast_name': 'test',
            'drawing_no': 'test',
            'mat': cls.mat1.id,
            'draw_weight': 1,
            'cast_weight': 10,
            'pieces_amount': '10',
            'detail_yield': 50,
            'pattern': 'wg wyceny',
            'heat_treat': 'brak',
            'tolerances': 'test',
            'tapers': 'wg uwag',
            'atest': '3.2 (DNV) wg PN-EN 10204',
            'required': 'test',
            'quality_class': 'test',
            'boxes': 'test',
            'others': 'test',
            'fr_chromite': 2,
            'machining': cls.mach1.id,
        }

    def user1_logged(self):
        return self.client.login(username='test_user1', password='test_password')

    def test_offer_str(self):
        self.assertEqual(
            self.offer1.__str__(),
            '{} -- {} -- {}'.format(self.offer1.offer_no, self.offer1.client, self.offer1.positions_amount)
        )

    def test_heat_treatment_str(self):
        self.assertEqual(self.heat_treat1.__str__(), self.heat_treat1.term)

    def test_pattern_taper_str(self):
        self.assertEqual(self.pat_taper_1.__str__(), self.pat_taper_1.taper)

    def test_atest_type_str(self):
        self.assertEqual(self.atest_type1.__str__(), self.atest_type1.atest)

    def test_offer_pattern_status_str(self):
        self.assertEqual(self.of_pat_status1.__str__(), self.of_pat_status1.status)

    def test_detail_str(self):
        self.assertEqual(
            self.detail1.__str__(),
            '{} {} {}'.format(self.detail1.cast_name, self.detail1.drawing_no, self.detail1.cast_weight)
        )

    def test_url_test(self):
        response = self.client.get(reverse('test'))
        self.assertEqual(response.status_code, 200)

    def test_url_offers(self):
        response = self.client.get(reverse('offers'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/offers/api/offers/')
        self.assertEqual(response.status_code, 200)

    def test_url_offer_create(self):
        from . import forms

        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 302)
        self.user1_logged()
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_add_offer)
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 200)
        form_data = {
            'offer_no': '100/17',
            'client': 'test',
            'user_mark': self.user1.id,
            'user_tech': self.user2.id,
            'date_tech_in': datetime.today(),
            'data_tech_out': datetime.today(),
            'date_mark_out': datetime.today(),
            'positions_amount': 0,
            'status': self.of_stat_id2,
            'days_amount': 0,
            # 'notices': 'test',
        }
        form = forms.OfferCreateUpdateForm(form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('offer-create'), form_data, follow=True)
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
        #     response = self.client.get(reverse('offer-details', args=[self.offer1.pk]))
        #     self.assertEqual(response.status_code, 302)
        self.user1_logged()
    #     response = self.client.get(reverse('offer-details', args=[self.offer1.pk]))
    #     self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('offer-details', args=[self.offer1.pk]), {'status': '1'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('offer-details', args=[self.offer1.pk]),
            {'new_notices': 'updated notices'}
        )
        self.assertEqual(response.status_code, 200)

    def test_url_offer_notices_get(self):
        self.user1_logged()
        response = self.client.get(reverse('notices'))
        self.assertEqual(response.status_code, 200)

    def test_url_offer_notices_post(self):
        self.user1_logged()
        response = self.client.post(reverse('notices'), {'content': 'new_notices'}, follow=True)
        self.assertEqual(response.redirect_chain, [(reverse('offers'), 302)])
        self.assertEqual(response.status_code, 200)

    def test_url_offer_detail_create(self):
        self.user1_logged()
        response = self.client.get(reverse('detail-create', args=[self.offer1.pk]), {'steel': ''})
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_add_detail)
        response = self.client.get(reverse('detail-create', args=[self.offer1.pk]), {'steel': ''})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('detail-create', args=[self.offer1.pk]), {'iron': ''})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('detail-create', args=[self.offer1.pk]), self.detail_data_form, follow=True)
        # self.assertEqual(response.redirect_chain, [(reverse('offer-details', args=[self.offer1.pk]), 302)])
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
            self.detail_data_form,
            follow=True
        )
        self.assertEqual(response.redirect_chain, [(reverse('offer-details', args=[self.offer1.pk]), 302)])
        self.assertEqual(response.status_code, 200)

    def test_url_offer_detail_delete(self):
        self.user1_logged()
        response = self.client.get(reverse('detail-delete', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 403)
        self.user1.user_permissions.add(self.perm_delete_detail)
        response = self.client.get(reverse('detail-delete', args=[self.offer1.pk, self.detail1.pk]))
        self.assertEqual(response.status_code, 200)

        """ Redirect to offers-details after delete """
        response = self.client.delete(reverse('detail-delete', args=[self.offer1.pk, self.detail1.pk]), follow=True)
        self.assertEqual(response.redirect_chain, [(reverse('offer-details', args=[self.offer1.pk]), 302)])
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

    # def test_url_stats(self):
    #     response = self.client.get(reverse('offers-stats'))
    #     self.assertEqual(response.status_code, 302)
    #     self.user1_logged()
    #     response = self.client.get(reverse('offers-stats'))
    #     self.assertEqual(response.status_code, 403)
    #     self.user1.user_permissions.add(self.perm_add_offer)
    #     response = self.client.get(reverse('offers-stats'))
    #     self.assertEqual(response.status_code, 200)

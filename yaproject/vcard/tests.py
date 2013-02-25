from django.test import TestCase
from django.core.urlresolvers import reverse

from yaproject.vcard.models import VCard, RequestStore


class BaseTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': '1',
        }
        self.vcard = VCard.objects.get(pk=1)


class VcardModelsTest(BaseTest):
    def test_vcard_with_data(self):
        self.assertTrue(self.vcard.name)
        self.assertTrue(self.vcard.surname)
        self.assertTrue(self.vcard.birth_date)
        self.assertTrue(self.vcard.bio)
        self.assertTrue(self.vcard.e_mail)

    def test_vcard_with_unicode(self):
        self.assertEqual('Yaroslav Tsarevsky', self.vcard.__unicode__())


class AdminTest(BaseTest):
    def test_admin_with_vcard(self):
        link = reverse('admin:vcard_vcard_change', args=[self.vcard.pk])
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)


class VcardViewsTest(BaseTest):
    def test_views_with_contacts(self):
        link = reverse('home')
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)
        self.assertTrue(self.resp.context['contacts'])
        self.vcard = self.resp.context['contacts']
        self.assertTrue(self.vcard.name)
        self.assertTrue(self.vcard.surname)
        self.assertTrue(self.vcard.birth_date)
        self.assertTrue(self.vcard.bio)
        self.assertTrue(self.vcard.e_mail)


class RequestStoreTest(TestCase):
    def test_middleware_with_store(self):
        link = reverse('home')
        while RequestStore.objects.all().count() != 10:
            self.resp = self.client.get(link)
        self.resp = self.client.get('/request_store/')
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(len(self.resp.context['requests']), 10)
        self.req_store = RequestStore.objects.latest('id')
        self.assertNotIn(self.req_store, self.resp.context['requests'])
        self.assertTrue(self.req_store)
        self.assertEqual(self.req_store.host, 'testserver')
        self.assertEqual(self.req_store.path, '/request_store/')
        self.assertTrue(self.req_store.date)

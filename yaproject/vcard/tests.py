from django.test import TestCase
from django.template import RequestContext, Template, Context,\
                            TemplateSyntaxError
from django.test.client import RequestFactory
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from yaproject.vcard.context_processor import add_settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.core import management
from cStringIO import StringIO

import sys

from yaproject.vcard.models import VCard, RequestStore, EntryLog
from yaproject.vcard.forms import MemberAccountForm


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

    def test_views_with_login(self):
        link = reverse('login')
        User.objects.create_user(**self.user_data)
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsInstance(self.resp.context['form'], AuthenticationForm)
        link = reverse('login')
        self.resp = self.client.post(link, self.user_data, follow=True)
        self.assertIn('http://testserver/',
            dict(self.resp.redirect_chain))

    def test_edit_page(self):
        link = reverse('edit_page')
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.resp.context['form'].instance, self.vcard)
        self.data = {
            'name': 'test',
            'surname': 'test',
            'birth_date': '1980-10-10',
            'bio': 'test test',
            'e_mail': 'test@test.com',
            'skype': 'test',
            'mob': '1111111',
            'jid': 'test'
        }
        self.resp = self.client.post(link, self.data, follow=True)
        self.assertEqual(self.resp.status_code, 200)
        self.vcard = VCard.objects.get(pk=1)
        self.assertEqual(self.vcard.name, 'test')
        self.assertEqual(self.vcard.surname, 'test')
        self.assertEqual(str(self.vcard.birth_date), '1980-10-10')
        self.assertEqual(self.vcard.bio, 'test test')
        self.assertEqual(self.vcard.e_mail, 'test@test.com')
        self.assertEqual(self.vcard.skype, 'test')
        self.assertEqual(self.vcard.mob, '1111111')
        self.assertEqual(self.vcard.jid, 'test')

    def test_login_wrong_password(self):
        link = reverse('login')
        User.objects.create_user(**self.user_data)
        self.user_data['password'] = '2'
        self.resp = self.client.post(link, self.user_data)
        self.assertEqual(len(self.resp.context['form'].errors), 1)

    def test_views_with_registration_form_clean_email(self):
        link = reverse('sign-up')
        self.user_data = {
            'username': 'test3',
            'email': 'a@a.ru',
            'password': '1',
            'r_password': '1'
        }
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsInstance(self.resp.context['form'], MemberAccountForm)
        self.resp = self.client.post(link, self.user_data)
        self.assertEqual(self.resp.context['form'].errors['email'],
            ['User with this email already exists'])
        self.user_data['email'] = 'b@b.ru'
        self.resp = self.client.post(link, self.user_data, follow=True)
        self.assertIn('http://testserver/', dict(self.resp.redirect_chain))

    def test_registration_passwords_dont_match(self):
        link = reverse('sign-up')
        self.user_data = {
            'username': 'test4',
            'email': 'test4@test.com',
            'password': '1',
            'r_password': '2'
        }
        self.resp = self.client.post(link,
            self.user_data)
        self.assertEqual(self.resp.context['form'].errors['r_password'],
            ['Passwords should match'])

    def test_views_with_logout(self):
        link = reverse('home')
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.context['user'].username, 'admin')
        link = reverse('logout')
        self.resp = self.client.get(link, follow=True)
        self.assertEqual(self.resp.context['user'].username, '')

    def test_views_with_edit_incorrect_data(self):
        link = reverse('edit_page')
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get(link)
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.resp.context['form'].instance, self.vcard)
        self.resp = self.client.post(link, {'name': ''}, follow=True)
        self.assertEqual(self.resp.context['form'].errors['name'][0],
            'This field is required.')
        self.resp = self.client.post(link,
            {'name': 'test', 'birth_date': '1980'}, follow=True)
        self.assertEqual(self.resp.context['form'].errors['birth_date'][0],
            'Enter a valid date.')

    def test_form_json(self):
        self.client.login(username='admin', password='admin')
        self.data = {
            'name': 'test',
            'surname': 'test',
            'birth_date': '1980-10-10',
            'bio': 'test test',
            'e_mail': 'test@test.com',
            'skype': 'test',
            'mob': '1111111',
            'jid': 'test'
        }
        import json
        self.json = json.dumps({'resource': self.data})
        self.resp = self.client.post(reverse('edit_page'),
            self.data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.data['name'] = 'test2'
        self.resp = self.client.post(reverse('edit_page'),
            self.data, follow=True)
        self.vcard = VCard.objects.get(pk=1)
        self.assertEqual(self.vcard.name, 'test2')


class RequestStoreTest(TestCase):
    def test_middleware_with_store(self):
        link = reverse('home')
        while RequestStore.objects.all().count() != 10:
            self.resp = self.client.get(link)
        self.resp = self.client.get('/request_store/')
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(len(self.resp.context['requests']), 11)
        self.req_store = RequestStore.objects.latest('id')
        self.assertEqual(self.req_store, self.resp.context['requests'][10])
        self.form = self.resp.context['formset'][10]
        self.assertEqual(self.form.initial['priority'], 0)
        self.assertTrue(self.req_store)
        self.assertEqual(self.req_store.host, 'testserver')
        self.assertEqual(self.req_store.path, '/request_store/')
        self.assertTrue(self.req_store.date)


class ContextProcessorTest(TestCase):
    def test_context_processor_with_settings(self):
        link = reverse('home')
        factory = RequestFactory()
        request = factory.get(link)
        c = RequestContext(request, {'foo': 'bar'}, [add_settings])
        self.assertTrue('settings' in c)
        self.assertEquals(c['settings'], django_settings)


class TemplateTagTest(BaseTest):
    def render_template(self, t, c):
        c = Context(c)
        return Template(t).render(c)

    def test_template_tag(self):
        link = reverse('home')
        pattern = 'admin:{0}_{1}_change'.format(self.vcard._meta.app_label,
            self.vcard._meta.module_name)
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get(link)
        self.assertIn(reverse(pattern, args=[self.vcard.id]),
            self.resp.content)

    def test_template_tag_error(self):
        t = '{% load edit_link %}{% get_edit_link my_vcard %}'
        c = {"my_vcard": self.vcard}
        self.assertEqual(self.render_template(t, c),
            '<a href="/admin/vcard/vcard/1/">Edit(admin)</a>')
        self.assertRaisesRegexp(TemplateSyntaxError,
            "'get_edit_link' tag requires only one arguments",
            self.render_template,
            '{% load edit_link %}{% get_edit_link my_vcard "some" %}',
            {})


class EntryLogTest(BaseTest):
    def setUp(self):
        self.data = {
            'name': 'test',
            'surname': 'test',
            'birth_date': '1980-10-10',
            'bio': 'test test',
            'e_mail': 'test@test.com',
            'skype': 'test',
            'mob': '1111111',
            'jid': 'test'
        }

    def test_log_with_vcard_created(self):
        VCard.objects.create(**self.data)
        entry = EntryLog.objects.latest('id')
        self.assertEquals(entry.get_action_display(), 'Created')

    def test_log_with_vcard_changed(self):
        self.client.login(username='admin', password='admin')
        self.resp = self.client.post(reverse('edit_page'),
            self.data, follow=True)
        entry = EntryLog.objects.latest('id')
        self.assertEquals(entry.get_action_display(), 'Changed')

    def test_log_with_vcard_delete(self):
        vcard = VCard.objects.create(**self.data)
        vcard.delete()
        entry = EntryLog.objects.latest('id')
        self.assertEquals(entry.get_action_display(), 'Deleted')

    def test_log_with_req_store_create(self):
        self.client.post(reverse('home'), follow=True)
        entry = EntryLog.objects.latest('id')
        self.assertEquals(entry.get_action_display(), 'Created')
        self.assertEquals(str(entry.content_type), 'request store')

    def test_log_with_req_store_delete(self):
        self.client.post(reverse('home'), follow=True)
        req_store = RequestStore.objects.latest('id')
        req_store.delete()
        entry = EntryLog.objects.latest('id')
        self.assertEquals(entry.get_action_display(), 'Deleted')


class ShowModelsCommandTest(TestCase):
    def out(self, model):
        cnt = model.objects.count()
        out = '[error]%s(%d)' % (model.__name__, cnt)
        return out

    def call(self):
        orig_stdout = sys.stderr
        sys.stderr = content = StringIO()
        management.call_command('show_models', db_dry_run=True)
        sys.stdout = orig_stdout
        content.seek(0)
        return content.read()

    def test_command_call(self):
        self.assertIn('show_models',
            str(management.get_commands()))
        self.assertIn(self.out(VCard), self.call())
        self.assertIn(self.out(RequestStore), self.call())
        self.assertIn(self.out(EntryLog), self.call())

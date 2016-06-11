from django.test import TestCase, RequestFactory
from django.contrib import admin
from pony_admin.tests.utils import IntModel, IntsAdmin


class RegisterAdminTest(TestCase):
    def setUp(self):
        admin.site._registry = {}

    def test_register(self):
        admin.site.register([IntModel], IntsAdmin)
        self.assertIn(IntModel, admin.site._registry)
        self.assertIsInstance(admin.site._registry[IntModel], IntsAdmin)


class BaseAdminGetFieldValueTest(TestCase):
    def test_get_from_admin(self):
        modeladmin = IntsAdmin(IntModel, admin.site)
        result = modeladmin._get_field_value('as_float_from_admin', 1)
        self.assertEqual(result, 1.0)
        result = modeladmin._get_field_value('as_float_from_admin', 2)
        self.assertEqual(result, 2.0)


class BaseAdminGetFieldNameTest(TestCase):
    def test_get_from_admin(self):
        modeladmin = IntsAdmin(IntModel, admin.site)
        result = modeladmin._get_field_name('as_float_from_admin')
        self.assertEqual(result, 'as_float_from_admin')
        result = modeladmin._get_field_name('as_float_described')
        self.assertEqual(result, 'Description')


class BaseAdminGetResultsTest(TestCase):
    def test_get_results(self):
        modeladmin = IntsAdmin(IntModel, admin.site)
        results = modeladmin.get_results('FOO')
        self.assertEqual(results['names'], ['as_float_from_admin', 'Description'])
        self.assertEqual(results['rows'][0], [1, 1.0, 1.0])


class BaseAdminChangeListViewTest(TestCase):
    def test_changelist_view(self):
        req_factory = RequestFactory()
        request = req_factory.get('/')
        modeladmin = IntsAdmin(IntModel, admin.site)
        response = modeladmin.changelist_view(request)
        self.assertEqual(response.status_code, 200)

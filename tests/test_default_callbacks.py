from django.test.utils import override_settings

from debug_toolbar.middleware import (
    default_allow_toolbar, default_show_toolbar,
)

from .base import BaseTestCase


@override_settings(DEBUG=True)
class DefaultAllowToolbarTestCase(BaseTestCase):
    def test_defaults(self):
        self.assertTrue(default_allow_toolbar(self.request))

    def test_DEBUG_False(self):
        with self.settings(DEBUG=False):
            self.assertFalse(default_allow_toolbar(self.request))

    def test_empty_INTERNAL_IPS(self):
        with self.settings(INTERNAL_IPS=[]):
            self.assertFalse(default_allow_toolbar(self.request))


@override_settings(DEBUG=True)
class DefaultShowToolbarTestCase(BaseTestCase):
    def test_defaults(self):
        self.assertTrue(default_show_toolbar(self.request))

    def test_with_ALLOW_TOOLBAR_CALLBACK(self):
        with self.settings(DEBUG_TOOLBAR_CONFIG={
            'ALLOW_TOOLBAR_CALLBACK': lambda request: False,
        }):
            self.assertFalse(default_show_toolbar(self.request))

    def test_ajax_request(self):
        request = self.rf.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(default_show_toolbar(request))

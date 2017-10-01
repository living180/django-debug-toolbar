from django.test.utils import override_settings

from debug_toolbar.middleware import default_show_toolbar

from .base import BaseTestCase


@override_settings(DEBUG=True)
class DefaultShowToolbarTestCase(BaseTestCase):
    def test_defaults(self):
        self.assertTrue(default_show_toolbar(self.request))

    def test_DEBUG_False(self):
        with self.settings(DEBUG=False):
            self.assertFalse(default_show_toolbar(self.request))

    def test_empty_INTERNAL_IPS(self):
        with self.settings(INTERNAL_IPS=[]):
            self.assertFalse(default_show_toolbar(self.request))

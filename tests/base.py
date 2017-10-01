from __future__ import absolute_import, unicode_literals

import threading

import html5lib
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from debug_toolbar.middleware import DebugToolbarMiddleware
from debug_toolbar.toolbar import DebugToolbar


class BaseTestCase(TestCase):
    def setUp(self):
        rf = RequestFactory()

        request = rf.get("/")
        response = HttpResponse()
        toolbar = DebugToolbar(request)

        DebugToolbarMiddleware.debug_toolbars[
            threading.current_thread().ident
        ] = toolbar

        self.rf = rf
        self.request = request
        self.response = response
        self.toolbar = toolbar
        self.toolbar.stats = {}

    def assertValidHTML(self, content, msg=None):
        parser = html5lib.HTMLParser()
        parser.parseFragment(self.panel.content)
        if parser.errors:
            default_msg = ["Content is invalid HTML:"]
            lines = content.split("\n")
            for position, errorcode, datavars in parser.errors:
                default_msg.append("  %s" % html5lib.constants.E[errorcode] % datavars)
                default_msg.append("    %s" % lines[position[0] - 1])

            msg = self._formatMessage(msg, "\n".join(default_msg))
            raise self.failureException(msg)

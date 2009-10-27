__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

import unittest

from zope.component import getMultiAdapter, getUtility

from Products.CMFCore.utils import getToolByName

from gomobile.convergence.interfaces import IOverrider
from gomobile.convergence.overrider.base import IOverrideStorage

from base import BaseTestCase

class TestMobileOverrides(BaseTestCase):

    def create_doc(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document", "doc")

    def create_event(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Event", "event")

    def test_has_overrides(self):
        """ Document object overrides are enabled by default
        """
        self.create_doc()
        doc = self.portal.doc
        overrider = IOverrider(doc)
        assert overrider != None

        assert overrider.schema != None
        self.assertEqual(overrider._getOverrideFieldNames(), ["Title", "Description", "getText"])

        # Set one override enabled and check it is read properly
        storage = IOverrideStorage(doc)
        storage.enabled_overrides = ["Title"]
        self.assertEqual(overrider._isOverrideEnabled("Title", storage), True)

        # Set overriden title
        storage.Title = "Foobar"

        # Call title accessor
        self.assertEqual(overrider._getOverrideOrOrignal("Title")(), "Foobar")

        assert overrider.Title() == u"Foobar"

    def test_has_no_overrides(self):
        """ Event object does not have default overrides
        """
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Event", "event")
        event = self.portal.event

        try:
            overrider = IOverrider(event)
            raise AssertionError("Should not be never reached")
        except TypeError:
            pass

    def test_traverse_checker(self):
        """ Check that condition view works """
        self.create_doc()
        self.create_event()


        result = self.portal.doc.restrictedTraverse("@@supports_mobile_overrides")
        result = result()
        self.assertEqual(result, True)


        result = self.portal.event.restrictedTraverse("@@supports_mobile_overrides")
        result = result()
        self.assertEqual(result, False)

    def test_render_form(self):
        self.create_doc()

        result = self.portal.doc.restrictedTraverse("@@edit_mobile_overrides")
        result()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMobileOverrides))
    return suite




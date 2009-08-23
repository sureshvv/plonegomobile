__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

import unittest

from zope.component import getMultiAdapter, getUtility

from Products.CMFCore.utils import getToolByName

from gomobile.mobile.interfaces import IMobileContentish

from gomobile.convergence.tests.base import ViewTestCase
from gomobile.convergence.browser import tabs
from gomobile.convergence.behaviors import IMultiChannelBehavior
from gomobile.convergence.interfaces import ContentMediaOption

from zope.schema.interfaces import ConstraintNotSatisfied

class TestBehavior(ViewTestCase):

    def test_has_behavior(self):
        """ Test behavior and assignable works nicely.
        """

        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document", "doc")
        doc = self.portal.doc

        # Check assignable works
        from plone.behavior.interfaces import IBehaviorAssignable
        assignable = IBehaviorAssignable(doc, None)

        self.assertTrue(assignable.supports(IMultiChannelBehavior))
        self.assertNotEqual(assignable, None)


        # Check behavior works
        self.assertTrue(IMobileContentish.providedBy(doc))
        behavior = IMultiChannelBehavior(doc)

        self.assertNotEquals(behavior, None)

    def test_set_media(self):
        """ Try behavior properties """
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document", "doc")
        doc = self.portal.doc

        self.assertTrue(IMobileContentish.providedBy(doc))
        behavior = IMultiChannelBehavior(doc)

        self.assertEqual(behavior.contentMedias, ContentMediaOption.USE_PARENT)

        behavior.contentMedias = ContentMediaOption.WEB

        # Recreate behavior
        behavior = IMultiChannelBehavior(doc)
        self.assertEqual(behavior.contentMedias, ContentMediaOption.WEB)

    def test_check_registration(self):
        """ Check that our behavior is correctly adapting to IContentish
        """

        from zope.component import getGlobalSiteManager
        sm = getGlobalSiteManager()

        registrations = [a for a in sm.registeredAdapters() if a.provided == IMultiChannelBehavior ]
        self.assertEqual(len(registrations), 1)


    def test_shit_input(self):
        """ Try put in bad data """


        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document", "doc")
        doc = self.portal.doc
        behavior = IMultiChannelBehavior(doc)
        try:
            behavior.contentMedias = "xxx"
            raise AssertionError("Should not be never reached")
        except ConstraintNotSatisfied:
            pass

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBehavior))
    return suite

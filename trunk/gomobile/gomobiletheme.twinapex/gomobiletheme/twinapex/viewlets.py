"""

   Twinapex theme specific new viewlets and viewlet overrides for mobile theme.


"""

from Acquisition import aq_inner
from zope.component import getMultiAdapter

from zope.interface import Interface

from five import grok
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from plone.app.layout.viewlets.interfaces import IPortalHeader
from Products.CMFCore.interfaces._content import IFolderish
from Products.statusmessages.interfaces import IStatusMessage

from gomobile.mobile.behaviors import IMobileBehavior
from gomobile.mobile.utilities import getCachedMobileProperties
from gomobile.mobile.browser.resizer import getUserAgentBasedResizedImageURL

from gomobiletheme.basic.viewlets import MainViewletManager, getView, gomobiletheme_basic_templatedir
from gomobiletheme.basic import viewlets as base

# Layer for which against all our viewlets are registered
from interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)

grok.viewletmanager(MainViewletManager)

class Head(base.Head):
    """ Render <head> section for every page.

    This stub is to override a template
    """

    def resource_url(self):
        return self.portal_url + "/" + "++resource++gomobiletheme.twinapex"

class Logo(base.Logo):
    """ Render site logo with link back to the site root.

    Logo will be automatically resized in the case of
    the mobile screen is very small.
    """

    def getLogoPath(self):
        return "++resource++gomobiletheme.twinapex/logo.png"

class HeaderImage(grok.Viewlet):
    """
    Viewlet which renders the header image shown on some sections.
    """

    def hasHeaderImage(self):
        """ Check whether context has AT field headerImage present and file uploaded """

        # Check for Archetypes field accessor
        context = self.context
        if not hasattr(context, "getField"):
            return False

        # Check for presence of AT field
        field = context.getField("headerImage")
        if field is not None:
            data = field.get(self.context)
        else:
            return False

        # Check whether file field has any data
        if data != None and data != '' and data.getSize() > 0:
            return True

    def update(self):

        portal_state = getView(self.context, self.request, "plone_portal_state")
        self.portal_url = portal_state.portal_url()

        if self.hasHeaderImage():
            # Get Zope traversing path for the image
            #
            image_path = self.context.getPhysicalPath() + "/headerImage"

            # Generate user-agent based resized image download URL
            # for the header image
            self.image_url = getUserAgentBasedResizedImageURL(self.context, self.request,
                                                         path=image_path,
                                                         width="auto",
                                                         height="auto",
                                                         padding_width=10)

        else:
            self.image_url = None






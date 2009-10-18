"""

    Various reusable page parts used in main_template.pt and elsewhere.

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

from gomobiletheme.basic.viewlets import MainViewletManager, getView
from gomobiletheme.basic import viewlets as base

from interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)


def getView(context, request, name):
    context = aq_inner(context)
    # Will raise ComponentLookUpError
    view = getMultiAdapter((context, request), name=name)
    view = view.__of__(context)
    return view


class Head(base.Head):
    """ Render <head> section for every page.

    This stub is to override a template
    """

class Logo(base.Logo):
    """ Render site logo with link back to the site root.

    Logo will be automatically resized in the case of
    the mobile screen is very small.
    """

    def getLogoPath(self):
        return "++resource++gomobiletheme.twinapex/logo.png"


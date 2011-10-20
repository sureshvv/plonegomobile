"""

   This module contains all viewlet overrides and new viewlets
   for the mobile theme. 
   
   For more information about how to deal with Grok viewlets see
   
   * http://vincentfretin.ecreall.com/articles/creating-a-viewlet-with-grok
   
   * http://grok.zope.org/doc/current/reference/directives.html

"""

__docformat__ = "epytext"
__license__ = "GPL"

from Acquisition import aq_inner, aq_parent

from zope.component import getMultiAdapter

from zope.interface import Interface

from five import grok
from Products.CMFCore.interfaces import IFolderish

from gomobiletheme.basic import viewlets as base
from gomobiletheme.basic.viewlets import getView
from gomobile.mobile.interfaces import IMobileImageProcessor

from gomobiletheme.mobipublic import MessageFactory as _

# Layer for which against all our viewlets are registered
from interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)

# All viewlets are registered against this dummy viewlet manager
grok.viewletmanager(base.MainViewletManager)

class Head(base.Head):
    
    def favicon_url(self):
        """ Get url for favicon
        """
        portal_state = getView(self.context, self.request, "plone_portal_state")
        self.portal_url = portal_state.portal_url()
        return self.portal_url + "/favicon.ico"

class Logo(base.Logo):
    """ Render site logo with link back to the site root.

    Logo will be automatically resized in the case of
    the mobile screen is very small.
    """

    def getLogoPath(self):
        """ Use Zope 3 resource directory mechanism to pick up the logo file from the static media folder registered by Grok """
        return "++resource++gomobiletheme.mobipublic/logo.png"
    
    def update(self):
        self.portal_state = portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")        
        self.portal_url = portal_state.portal_url()
        self.logo_url = self.portal_url + "/" + self.getLogoPath()
        
    def getSections(self):
        portal = self.portal_state.portal()
        items = portal.getFolderContents()
        for brain in items:
            obj = brain.getObject()
            if IFolderish.providedBy(obj):
                yield obj
        
class AdditionalHead(base.AdditionalHead):
    """ Include our custom CSS and JS in the theme.
    
    If you want to override the base versions, please consider customizing base.Head instead.
    """
    
    def update(self):
        
        base.AdditionalHead.update(self)
        
        context = self.context.aq_inner
        
        portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        self.portal_url = portal_state.portal_url()
        
        # Absolute URL refering to the static media folder
        self.resource_url = self.portal_url + "/" + "++resource++gomobiletheme.mobipublic"


class MobileTracker(base.MobileTracker):
    """ Site visitors tracking code for mobile analytics """

class FooterText(base.FooterText):
    """
    Override footer text, set by templates/footertext.pt.
    """

class TopActions(base.TopActions):
    """ """

class Sections(base.Sections):
    """ """
    
class SearchBoxBottom(base.Sections):
    """ """    
        
class ActionsHeader(base.ActionsHeader):
    """ """

class Back(base.Back):
    """ """
    
    def update(self):
        context= aq_inner(self.context)
        
        context_helper = getMultiAdapter((context, self.request), name="plone_context_state")
        
        portal_helper = getMultiAdapter((context, self.request), name="plone_portal_state")
        
        canonical = context_helper.canonical_object()
        
        parent = aq_parent(canonical)
        
        breadcrumbs_view = getView(self.context, self.request, 'breadcrumbs_view')
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        
        if (len(breadcrumbs)==1):
            self.backTitle = _(u"Home")
        else:
            if hasattr(parent, "Title"):
                self.backTitle = parent.Title()
            else:
                self.backTitle = _(u"Back")
        
        if hasattr(parent, "absolute_url"):
            self.backUrl = parent.absolute_url()
        else:
            self.backUrl = portal_helper.portal_url()
            
        self.isHome = len(breadcrumbs)==0    
        
        self.homeUrl = portal_helper.portal_url()
"""

    Views for accessing and editing convergence options.

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

from AccessControl import Unauthorized

from zope.interface import implements, Interface
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.component import getUtility, queryUtility

from five import grok
from zope.component import queryAdapter, getUtility

from Products.Five import BrowserView
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import IContentish

from gomobile.mobile.interfaces import IMobileUtility, IMobileRequestDiscriminator, IMobileSiteLocationManager, MobileRequestType
from gomobile.convergence.interfaces import ContentMediaOption, IConvergenceMediaFilter
from gomobile.convergence.interfaces import IOverrider

class ChangeMediaStrategyView(BrowserView):
    """
    Handle change media strategy portlet form posts.
    """

    def __call__(self):

        strategy = self.request["media_option"]

        # We reallly want to edit folder settings,
        # this magic this juts work (tm)
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        isDefaultPage = self.context_state.is_default_page()

        if isDefaultPage:
            # Use parent folder, no point of changing the
            # folder front page setting
            instance = self.context.aq_inner.aq_parent
        else:
            instance = self.context

        filter = getUtility(IConvergenceMediaFilter)

        filter.setContentMedia(instance, strategy)


        # Update portal_catalog to reflect new changes
        #self.context.reindexObject(idxs=["getContentMedias"])

        # Go back to the object front page
        self.request.response.redirect(self.context.absolute_url())



class OverriderView(BrowserView):
    """  Helper views to allow easy access to overridden data from templates.

    Enable converged proxy object if we are in mobile mode.

    How to traverse to find mobile overrides and redefine context in safe way::

        context context/@@multichannel_overrider|nocall:context; here nocall:context;

    This will give you context unmodified if convergence is not installed.
    """

    def __call__(self):
        """
        """

        util = getUtility(IMobileRequestDiscriminator)
        flags = util.discriminate(self.context, self.request)

        if MobileRequestType.MOBILE in flags:

            overrider = queryAdapter(self.context, IOverrider)
            if overrider is not None:
                return overrider

        # No overrides, use context as is
        return self.context

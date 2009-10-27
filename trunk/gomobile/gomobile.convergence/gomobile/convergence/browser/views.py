__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

from zope.interface import implements, Interface
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.component import getUtility, queryUtility

from Products.Five import BrowserView
from five import grok
from Products.CMFCore.utils import getToolByName

from AccessControl import Unauthorized

from gomobile.convergence.interfaces import ContentMediaOption, IConvergenceMediaFilter

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



class MasterForm(form.Form):



class PropertiesView(grok.View):
    """ Allow user to edit convergence options and mobile overrides.

    """

    settings_form =


    def getForms(self):
        """ Get all forms on this view
        """
        r

    def constructForm(self):


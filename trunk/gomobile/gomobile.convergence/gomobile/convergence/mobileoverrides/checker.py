"""


"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

from zope.interface import implements, Interface
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.component import getUtility, queryUtility

from gomobile.convergence.interfaces import IMobileOverrider

from Products.Five import BrowserView

class MobileOverrideSupportCheckerView(BrowserView):
    """
    View to allow easily check whether the context object supports mobile overrides.
    """

    def __call__(self):
        return IMobileOverrider.providedBy(self.context)


from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.invoice import invoiceMessageFactory as _

from getpaid.invoice.browser.baseinvoiceview import BaseInvoiceView

class IPDFInvoiceView(Interface):
    """
    PDFInvoice view interface
    """

    def test():
        """ test method"""


class PDFInvoiceView(BaseInvoiceView):
    """
    PDFInvoice browser view
    """
    implements(IPDFInvoiceView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

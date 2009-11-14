
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.invoice import invoiceMessageFactory as _

from getpaid.invoice import IInvoiceView

class BaseInvoiceView(BrowserView):
    """
    BaseInvoice browser view
    """
    implements(IInvoiceView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cart = None

    def setCart(self, cart):
        self.cart = cart

    def assertHasCart(self):
        """
        """
        if self.cart is None:
            raise AssertionError("Call setCart() before calling other InvoiceView methods")


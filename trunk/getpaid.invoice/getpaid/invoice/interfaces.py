from zope.interface import implements, Interface
from zope import schema

from getpaid.invoice import invoiceMessageFactory as _

class IInvoiceView(Interface):
    """ Invoice generator view.

    Generates invoice report for the customer.

    This view *does not* respond to HTTP requests directly,
    but is used as utility view from other views and viewlets.

    You must call setCart() before calling other methods.
    """

    def setCart(cart):
        """
        Set the shopping cart where we have invoice data.
        """

    def download():
        """ Downloads the current invoice.

        The called method generates necessary HTTP
        """

    def generateInvoice():
        """ Generate the invoice body data.

        The actual return format depends on the invoice.

        @return: File contents or Python string
        """

class IInvoiceData(Interface):
    """ Shop specific data appearing in voices.

    """

    terms_oy_payment = schema.TextLine(title=_(u"Terms of payment"), description=_(u"E.g. due in 14 days"))

    running_counter = schema.Int(title=_(u"Next reference number id"), description=_(u"Running counter for the next reference number. This is not the actual number, but running counte used to generate the id."))


class IReferenceNumberGenerator(Interface):
    """ Generate reference numbers.

    Reference number generation method depends on the country
    and used accounting system. This utility class
    can be overridden in site specific manner.

    """

    def getReferenceNumber(running_counter):
        """
        @param running_counter: Integer, Usually matches order number.
        """




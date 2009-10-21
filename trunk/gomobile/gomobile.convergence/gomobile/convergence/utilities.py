"""

     Misc. helper functions

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

import zope.schema
from zope.schema.vocabulary import SimpleTerm

def make_terms(items):
    """ Create zope.schema terms objects based on tuples of (value, Title) """
    terms = [ c(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
    return terms



def addSchema(target, source):
    """ Combine zope.schema fields from another class.

    @param source: Class having zope.schema fields

    @param target: any Class
    """
    for name, field in zope.schema.getFieldsInOrder(source):
        setattr(target, name, field)




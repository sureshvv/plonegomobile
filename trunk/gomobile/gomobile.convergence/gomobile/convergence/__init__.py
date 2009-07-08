from zope.component import getUtility, queryUtility

import monkeypatch # Run navtree monkey patches
import indexing
import Missing

from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from interfaces import IConvergenceSupport


def getContentMedias(object, portal, **kw):
    """ Provide indexing hooksk for portal_catalog """
    if IConvergenceSupport.providedBy(object):
        
        schema = object.Schema()

        if not "contentMedias" in schema:        
            # Not real AT object - e.g. criteria
            # TODO: Do we need to use different marker interface?
            return Missing.Value
        else:
            val = schema["contentMedias"].get(object)
            return val
        

registerIndexableAttribute('getContentMedias', getContentMedias)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

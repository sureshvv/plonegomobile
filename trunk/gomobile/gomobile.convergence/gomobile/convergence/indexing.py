"""
    Include content media information in portal_catalog indexing and search output.

"""

__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"


from zope.component import getUtility, queryUtility

import Missing

from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from interfaces import IConvergenceSupport, IConvergenceMediaFilter

from plone.indexer.decorator import indexer
  
@indexer(IConvergenceSupport)
def getContentMedias(object, portal, **kw):
    """ Provide indexing hooksk for portal_catalog """

    if IConvergenceSupport.providedBy(object):
        
        schema = object.Schema()

        if not "contentMedias" in schema:        
            # Not real AT object - e.g. criteria
            # TODO: Do we need to use different marker interface?
            return Missing.Value
        else:
            filter = getUtility(IConvergenceMediaFilter)
            return filter.getContentMedia(object)
                    

# Plone 3.2.x code
#registerIndexableAttribute('getContentMedias', getContentMedias)

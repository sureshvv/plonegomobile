"""
    Include content media information in portal_catalog indexing and search output.

"""

__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"


from zope.component import getUtility, queryUtility

import Missing

from interfaces import IConvergenceSupport, IConvergenceMediaFilter

from gomobile.convergence.behaviors import IMultiChannelBehavior

try:
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

except ImportError:
    # Plone 3.2.x code

    from Products.CMFPlone.CatalogTool import registerIndexableAttribute

    def getContentMedias(object, portal, **kw):
        """ Provide indexing hooksk for portal_catalog """

        try:
            behavior = IMultiChannelBehavior(object)
        except TypeError:
            # OBject is not type which supports behavior adaptions
            return Missing.Value

        if behavior == None:
            # Multichannel behavior has been disabled for the object by
            # behavior assignable
            return Missing.Value

        return behavior.contentMedias


        if IConvergenceSupport.providedBy(object):

            schema = object.Schema()

            if not "contentMedias" in schema:
                # Not real AT object - e.g. criteria
                # TODO: Do we need to use different marker interface?
                return Missing.Value
            else:
                filter = getUtility(IConvergenceMediaFilter)
                return filter.getContentMedia(object)

    registerIndexableAttribute('getContentMedias', getContentMedias)

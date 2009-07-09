from zope.component import getUtility, queryUtility

import monkeypatch # Run navtree monkey patches
import indexing
import Missing

from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from interfaces import IConvergenceSupport


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

"""

    Use mobile.sniffer for prepare browser information

"""

import os

import zope.thread
from zope.component import getUtility
from zope.app.component.hooks import getSite

import traceback

# We need to store site as thread local (request local)
# since getSite() is cleared by its own EndRequestEvent
# before our hook is called

#_site_memorizer = zope.thread.local()


black_list = [ ".js", ".css" ]


def incoming(site, event):
    """ Sniff browser from the database.
    
    Do all in special Django transaction context.
    """
    
    # TODO: Not implemented yet
    
    pass 

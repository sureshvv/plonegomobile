import logging

import zope.interface
from zope.component import getMultiAdapter

from collective.easytemplate.interfaces import ITag

from five import grok

from plone.app.discussion.interfaces import IConversation

# Viewlets are on all content by default.
grok.context(zope.interface.Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

logger = logging.getLogger("mobipublic")

class FrontPageBlock(object):
    """ """
    zope.interface.implements(ITag)
    
    def getName(self):
        return "front_page_block"
    
    def render(self, scriptingContext, path, portalType, title, count):
        """ """
        
        # Look up the view by name
        
        view = getMultiAdapter((scriptingContext.context. scriptingContext.request), name="front_page_block")
        
        view.path = path
        view.portalType = portalType
        view.title = title
        view.count = count
        return view()
        
        
class BlockView(grok.View):
    """
    """
    
    grok.name("front_page_block")        
                
    def getItems(self):
        """
        """
        #folder = self.context.unrestrictedTraverse(self.path)
        #listing = folder.getFolderListing()        
        
        if self.count > 0:
            return self.context.portal_catalog(path={ "query": self.path }, portal_type=self.portalType,  sort_on="created", sort_order="reverse")[0:self.count]
        
    def getSlots(self):
        """
        """
        folder = self.context.unrestrictedTraverse(self.path)
        return self.folder.listFolderContents()
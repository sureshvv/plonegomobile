import logging

import zope.interface
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite 

from collective.templateengines.interfaces import ITag

from five import grok

from plone.app.discussion.interfaces import IConversation

# Viewlets are on all content by default.
grok.context(zope.interface.Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

logger = logging.getLogger("mobipublic")

class FrontPageBlockTag(object):
    """ """
    zope.interface.implements(ITag)
    
    def getName(self):
        return "front_page_block"
    
    def render(self, scriptingContext, path, itemPortalType, itemPortalType2, folderPortalType,  title, slotTitle, count):
        """ """
        
        # Look up the view by name
        
        mappings = scriptingContext.getMappings()
        context = mappings['context']
        request = mappings['request']
        view = getMultiAdapter((context, request), name="front_page_block")
        
        view.path = path
        view.itemPortalType = itemPortalType
        view.itemPortalType2 = itemPortalType2
        view.folderPortalType = folderPortalType
        view.title = title
        view.slotTitle = slotTitle
        view.count = count
        return view()
        
        
class BlockView(grok.View):
    """
    Define a view which is called thru script tag, with special parameters 
    set up by the tag class.
    """
    
    grok.name("front_page_block")        
    grok.template("front_page_block")
    
    def getMasterItem(self):
        folder = self.context.unrestrictedTraverse(self.path)
        return folder 
                
    def getItems(self):
        """
        Get X amount of nested item from folder hierarchy by portal type, sorted by creation.
        """        
        if self.count > 0:
            
            site = getSite()
            
            
            # Make string path relative to the site root
            # E.g. string path "news" becomes "/yoursiteid/news"
            site_path = site.getPhysicalPath();
            
            path = "/".join(site_path) + "/" + self.path         
            
            types = [self.itemPortalType]
            
            items = []
                                
            if self.itemPortalType2 != None:
                types.append(self.itemPortalType2) 
            
            #print "Querying by:" + type + " " + path
            content_by_type = self.context.portal_catalog(path={ "query": path, "depth" :9 }, 
                                                portal_type=types,  
                                                sort_on="created", 
                                                sort_order="reverse")[0:self.count]
            items += list(content_by_type)
        else:
            items = []
                    
        return items
        
    def getSlots(self):
        """
        """
        
        site = getSite()
        
        if self.path != "":
            folder = site.unrestrictedTraverse(self.path)
            items = folder.listFolderContents()
        else:
            items = []
        
        return items
        
        
from collective.easytemplate.tagconfig import tags as tag_list
from collective.easytemplate.engine import setDefaultEngine 

tag_list.append(FrontPageBlockTag())        
setDefaultEngine() # Refresh tag list        
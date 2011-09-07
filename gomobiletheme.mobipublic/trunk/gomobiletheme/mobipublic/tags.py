import logging
import datetime

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
    
    def render(self, scriptingContext, path, itemPortalType, itemPortalType2, folderPortalType,  title, slotTitle, itemCount, slotCount):
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
        view.itemCount = itemCount
        view.slotCount = slotCount
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
        if self.itemCount > 0:
            
            site = getSite()
            
            
            # Make string path relative to the site root
            # E.g. string path "news" becomes "/yoursiteid/news"
            site_path = site.getPhysicalPath();
            
            path = "/".join(site_path) + "/" + self.path         
            
            types = [self.itemPortalType]
            
            items = []
                                
            #if self.itemPortalType2 != None:
            #    types.append(self.itemPortalType2) 
            
            #print "Querying by:" + type + " " + path
            content_by_type = self.context.portal_catalog(path={ "query": path, "depth" :9 }, 
                                                portal_type=self.itemPortalType,  
                                                sort_on="created", 
                                                sort_order="reverse")[0:self.itemCount]

            content_by_type = list(content_by_type)
            
            if self.itemPortalType2 != None:
                content_by_type2 = self.context.portal_catalog(path={ "query": path, "depth" :9 }, 
                                                    portal_type=self.itemPortalType2,  
                                                    sort_on="created", 
                                                    sort_order="reverse")[0:self.itemCount]

                content_by_type += list(content_by_type2)

            
            items += [ brain.getObject() for brain in content_by_type ]
        else:
            items = []
            
        #if self.title == "Daily deals":
        #    import pdb ; pdb.set_trace()
            
        # XXX: custom hack for deals
        def is_expired_deal(i):
            """
            """
            if hasattr(i, "validUntil"):
                now = datetime.datetime.utcnow()
                if now > i.validUntil:
                    return True
                
            return False
        
        items = [ i for i in items if not is_expired_deal(i) ]
                    
        return items
        
    def getSlots(self):
        """
        """
        
        site = getSite()
        
        if self.path != "":
            folder = site.unrestrictedTraverse(self.path)
            items = folder.listFolderContents(contentFilter={"portal_type" : self.folderPortalType})
        else:
            items = []
        
        return items
        
        
from collective.easytemplate.tagconfig import tags as tag_list
from collective.easytemplate.engine import setDefaultEngine 

class LatestPickTag(object):
    """ """
    zope.interface.implements(ITag)
    
    def getName(self):
        return "latest_pick"
    
    def render(self, scriptingContext, path, itemCount):
        """ """
        
        # Look up the view by name
        
        mappings = scriptingContext.getMappings()
        context = mappings['context']
        request = mappings['request']
        view = getMultiAdapter((context, request), name="latest_pick")
        
        view.path = path
        view.itemCount = itemCount
        return view()
    
class LatestPickView(grok.View):
    """
    Define a view which is called thru script tag, with special parameters 
    set up by the tag class.
    """
    
    grok.name("latest_pick")        
    grok.template("latest_pick")    
    
    def getItems(self):
        """
        Get X amount of nested item from folder hierarchy by portal type, sorted by creation.
        """        
        items = []
        if self.itemCount > 0:
            
            site = getSite()
            
            
            # Make string path relative to the site root
            # E.g. string path "news" becomes "/yoursiteid/news"
            site_path = site.getPhysicalPath();
            
            path = "/".join(site_path) + "/" + self.path         
                                            
            #if self.itemPortalType2 != None:
            #    types.append(self.itemPortalType2) 
            
            #print "Querying by:" + type + " " + path
            content_by_type = self.context.portal_catalog(path={ "query": path, "depth" :9 }, 
                                                sort_on="created", 
                                                sort_order="reverse")[0:self.itemCount]

                   
            items += [ brain.getObject() for brain in content_by_type ]

        return items    
    
        
        
class DealsTag(object):
    """ """
    zope.interface.implements(ITag)
    
    def getName(self):
        return "deals"
    
    def render(self, scriptingContext):
        """ """
        
        # Look up the view by name
        mappings = scriptingContext.getMappings()
        context = mappings['context']
        request = mappings['request']
        view = getMultiAdapter((context, request), name="deals_tag")
        return view()
    
class DealsTagView(grok.View):
    """
    Define a view which is called thru script tag, with special parameters 
    set up by the tag class.
    """
    
    grok.name("deals_tag")        
    grok.template("deals_tag")    
    
    def getItems(self):
        """
        Get X amount of nested item from folder hierarchy by portal type, sorted by creation.
        """        
        from frontpage import get_deals
        items = get_deals(self.context, self.request)
        return items    
    
    def getMasterItem(self):
        return self.context.portal_url.getPortalObject()["deals-discounts"]
        

tag_list += [FrontPageBlockTag(), LatestPickTag(), DealsTag()]
setDefaultEngine() # Refresh tag list        
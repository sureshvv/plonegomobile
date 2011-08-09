"""

    Front page special views.
    
    Can be called from collective.easytemplate templates by putting in the following template code::
    
        {{ view("hotnow") }}

    http://mfabrik.com

"""


__author__ = "Mikko Ohtamaa <mikko@mfabrik.com>"
__copyright__ = "2010-2011 mFabrik Research Oy"
__docformat__ = "epytext"
__license__ = "GPL 2"

import math
import datetime
import DateTime
from DateTime import DateTime as DateTimeClass
import logging

import pytz  # 3rd party

from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
from zope.interface import Interface
from five import grok
 
from Products.ATContentTypes.utils import DT2dt, dt2DT

from gomobiletheme.mobipublic.utils import shorten_description

# Use templates directory to search for templates.
grok.templatedir("templates")

logger = logging.getLogger("mobipublic")

class HotNewsToday(grok.View):    
    """  
    This view is used on the front page.
    It is rendered through collective.easytemplate tag.
    """
    

    # Viewlets are on all content by default.
    grok.context(Interface)
    
    def update(self):
        """
        """
        
        portal_catalog = self.context.portal_catalog
        
        count = 5
        
        #end = datetime.datetime.utcnow() + datetime.timedelta(3600)
        #start = datetime.datetime.utcnow()- datetime.timedelta(3600*24)
        
        #end = dt2DT(end)
        #start = dt2DT(start)
        
        # DateTime deltas are days as floating points
        end = DateTime.DateTime() + 0.1 # If we have some clock skew peek a little to the future
        start = DateTime.DateTime() - 1
        
        date_range_query = { 'query':(start,end), 'range': 'min:max'} 
                
        items = portal_catalog.queryCatalog({"portal_type":"FeedFeederItem",
                                             "created" : date_range_query,
                                             "sort_on":"positive_ratings",
                                             "sort_order":"reverse",
                                             "sort_limit":count,
                                             "review_state":"published"})
        
        #print "Got items:" + str(items)
        #import pdb ; pdb.set_trace()
        variables = ["getFeedItemUpdated", "Title", "Description", "getLink", "getFeedItemAuthor"]
        
        # Convert brain objects to dictionaries and stuff in some custom variables
        result = []
        for i in items:
            t = {}
            for v in variables:
                t[v] = i[v]
            
            t["friendlyTime"] = format_datetime_friendly_ago(i["getFeedItemUpdated"])
            t["link"] = i.getURL()
            t["object"] = i.getObject()
            try:
                t["socialbar"] = getMultiAdapter((t["object"].aq_inner, self.request), name="socialbar")
            except:
                # Web mode
                t["socialbar"] = None
                
            result.append(t)
            
        self.items = result
        


class Deals(grok.View):    
    """  
    Show 1 automatic deal (RSS) + all manual deals
    """
    

    # Viewlets are on all content by default.
    grok.context(Interface)
    
    def update(self):
        """
        """
        
        portal_catalog = self.context.portal_catalog
        
        count = 1
        
        #end = datetime.datetime.utcnow() + datetime.timedelta(3600)
        #start = datetime.datetime.utcnow()- datetime.timedelta(3600*24)
        
        #end = dt2DT(end)
        #start = dt2DT(start)
              
                
        items = portal_catalog.queryCatalog({"portal_type":"FeedFeederItem",
                                             "path" : {"query" : "/mobipublic/deals-discounts" },
                                             "sort_on":"created",
                                             "sort_order":"reverse",
                                             "sort_limit":1,
                                             "review_state":"published"})
        
        
        # Convert brain objects to dictionaries and stuff in some custom variables
        result = []
        variables = ["getFeedItemUpdated", "Title", "Description", "getLink", "getFeedItemAuthor"]


        for i in items:
            t = {}
            for v in variables:
                t[v] = i[v]
            
            t["friendlyTime"] = format_datetime_friendly_ago(i["getFeedItemUpdated"])
            t["link"] = i.getURL()
            t["object"] = i.getObject()
            t["Description"] = shorten_description(i.Description)
            try:
                t["socialbar"] = getMultiAdapter((t["object"].aq_inner, self.request), name="socialbar")
            except:
                # Web mode
                t["socialbar"] = None
                
            result.append(t)
            
            
        now = datetime.datetime.utcnow()
            
        # Add manual pages
        try:
            deals = getSite().unrestrictedTraverse("deals-discounts")
            
            pages = deals.listFolderContents(contentFilter={"portal_type" : "mobipublic.content.deal"})


    
            for i in pages:
                t = {}
            
                #t["friendlyTime"] = format_datetime_friendly_ago(i["getFeedItemUpdated"])
                t["link"] = i.absolute_url()
                t["Title"] = i.Title()
                t["Description"] = i.Description()
                t["object"] = i

                                    
                if hasattr(i, "validUntil") and i.validUntil is not None:

                    if now > i.validUntil:
                        # No longer valid
                        continue 

                    t["validUntil"] =  format_datetime_friendly_ago(i.validUntil)
                else:
                    t["validUntil"] = None

                
                try:
                    t["socialbar"] = getMultiAdapter((t["object"].aq_inner, self.request), name="socialbar")
                except:
                    # Web mode
                    t["socialbar"] = None

                result.append(t)
            
        except Exception, e:
            logger.exception(e)
            
                                                                    
        self.items = result
                    

def format_datetime_friendly_ago(date):
    """ Format date & time using site specific settings.

    @param date: datetime object
    """
    
    if date == None:
        return ""
    
    
    if isinstance(date, DateTimeClass):
        date = DT2dt(date) # zope DateTime -> python datetime

    # How long ago the timestamp is
    # See timedelta doc http://docs.python.org/lib/datetime-timedelta.html
    #since = datetime.datetime.utcnow() - date

    from pytz import timezone
    helsinki = timezone('Europe/Helsinki')
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=helsinki)

    date = date.replace(tzinfo=helsinki)
    since = now - date
      
    seconds = since.seconds + since.microseconds / 1E6 + since.days * 86400

    days = math.floor(seconds / (3600*24))

    if days < 0:
        # Timezone confusion, is in future
        return date.strftime("%d.%m.%Y %H:%M")

    if days > 7:
        # Full date
        return date.strftime("%d.%m.%Y %H:%M")
    elif days >= 1:
        # Week day format
        return date.strftime("%A %H:%M")
    else:
        hours = math.floor(seconds/3600.0)
        minutes = math.floor((seconds % 3600) /60)
        if hours > 0:
            return "%d hours %d minutes ago" % (hours, minutes)
        else:
            if minutes > 0:
                return "%d minutes ago" % minutes
            else:
                return "few seconds ago"        
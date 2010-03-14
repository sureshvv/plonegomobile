"""

    Front page special views.
    
    Can be called from collective.easytemplate templates by putting in the following template code::
    
        {{ view("hotnow") }}

    http://mfabrik.com

"""


__author__ = "Mikko Ohtamaa <mikko@mfabrik.com>"
__copyright__ = "2010 mFabrik Research Oy"
__docformat__ = "epytext"
__license__ = "GPL 2"

import math
import datetime

from zope.interface import Interface
from five import grok
 
from Products.ATContentTypes.utils import DT2dt, dt2DT

# Use templates directory to search for templates.
grok.templatedir("templates")

class HotNow(grok.View):    
    """  
    This view is used on the front page.
    It is rendered through collective.easytemplate tag.
    """
    

    # Viewlets are on all content by default.
    grok.context(Interface)

    
    def __call__(self):
        """
        """
        
        portal_catalog = self.context.portal_catalog
        
        count = 5
        
        items = portal_catalog.queryCatalog({"portal_type":"FeedFeederItem",
                                             "sort_on":"getFeedItemUpdated",
                                             "sort_order":"reverse",
                                             "sort_limit":count,
                                             "review_state":"published"})
        
        print "Got items:" + str(items)
        
        variables = ["getFeedItemUpdated", "Title", "Description", "getLink", "getFeedItemAuthor"]
        
        # Convert brain objects to dictionaries and stuff in some custom variables
        result = []
        for i in items:
            t = {}
            for v in variables:
                t[v] = i[v]
            
            t["friendlyTime"] = format_datetime_friendly_ago(i["getFeedItemUpdated"])
            t["link"] = i.getURL()
            
            result.append(t)
            
        self.items = result
        
        print "Rendering:" + str(self.items)
        
        return self.template()
            

def format_datetime_friendly_ago(date):
    """ Format date & time using site specific settings.

    @param date: datetime object
    """
    
    if date == None:
        return ""
    
    date = DT2dt(date) # zope DateTime -> python datetime

    # How long ago the timestamp is
    # See timedelta doc http://docs.python.org/lib/datetime-timedelta.html
    #since = datetime.datetime.utcnow() - date

    since = datetime.datetime.now() - date
      
    seconds = since.seconds + since.microseconds / 1E6 + since.days * 86400

    days = math.floor(seconds / (3600*24))

    if days <= 0 and seconds <= 0:
        # Timezone confusion, is in future
        return "moment ago"

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
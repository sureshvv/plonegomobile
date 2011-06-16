from zope.interface import Interface
import urllib
from zope.component import getMultiAdapter

from five import grok

# Layer for which against all our viewlets are registered
from interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

# Viewlets are active only when gomobiletheme.basic theme layer is activated
#grok.layer(IThemeLayer)

from plone.app.discussion.interfaces import IConversation

class SocialBar(grok.View):
    """
    Render a bar with Facebook, Twitter and mobile thumb rating.
    """
    
    grok.context(Interface)
    
    def setTargetContent(self, targetContent):
        """
        Which item we use as Facebook et. al. link target
        """
        self.targetContent = targetContent
    
    def getOutgoingURL(self):        
        """ What we share in social media """
        return self.targetContent.absolute_url()

    def getOrignalURL(self):        
        """ RSS feed link """
        
        remote_url = getattr(self.targetContent, "remote_url", None)
        if remote_url:
            return remote_url()
        
        return self.targetContent.absolute_url()


    def getFacebookSharingLink(self):
        link = self.getOutgoingURL()
        # http://m.facebook.com/sharer.php?u=http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229&t=Eduskuntaryhm%C3%A4t+koolle+hallitusneuvotteluista+tiistaina
        return "http://m.facebook.com/sharer.php?u=" + urllib.quote(link)
        #return "http://m.facebook.com/sharer.php?u=" + link

    # http://mobile.twitter.com/home?status=Lukee%20nyt%20http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229
    def getTwitterSharingLink(self):
        link = self.getOutgoingURL()
        # http://mobile.twitter.com/home?status=Lukee%20nyt%20http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229
        return "http://mobile.twitter.com/home?status=" + urllib.quote(link)

    def getDiscussionLink(self):
        link = "foobar"
        # http://mobile.twitter.com/home?status=Lukee%20nyt%20http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229
        return self.targetContent.absolute_url() + "#discussion"

    def getDiscussionCount(self):
        try:
            # plone.app.discussion.conversation object 
            # fetched via IConversation adapter
            conversation = IConversation(self.targetContent)
        except:
            return 0
        
        return conversation.total_comments
        
    def getVoteFormLink(self):
        link = self.targetContent.absolute_url()
        return link + "/@@vote"
    
    def getThumbsForm(self):
        view = getMultiAdapter((self.context, self.request), name="thumbs")
        
        #import pdb ;pdb.set_trace()
        return view
    
    def update(self):
        if not hasattr(self, "targetContent"):
            self.targetContent = self.context
    
    
class Vote(grok.CodeView):
    """
    Custom vote manager.
    """

    def render(self, REQUEST, RESPONSE):
        form = self.request.form
        if form.get('form.lovinit', False):
            rate.loveIt(self.context)
        elif form.get('form.hatedit', False):
            rate.hateIt(self.context)
            
            
class Empty(grok.View):
    """
    Empty folder listing
    """
    
    grok.context(Interface)

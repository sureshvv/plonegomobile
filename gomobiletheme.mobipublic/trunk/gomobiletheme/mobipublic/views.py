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
grok.layer(IThemeLayer)


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
        return self.targetContent.absolute_url()

    def getFacebookSharingLink(self):
        link = self.getOutgoingURL()
        # http://m.facebook.com/sharer.php?u=http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229&t=Eduskuntaryhm%C3%A4t+koolle+hallitusneuvotteluista+tiistaina
        return "http://m.facebook.com/sharer.php?u=" + urllib.quote(link)

    # http://mobile.twitter.com/home?status=Lukee%20nyt%20http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229
    def getTwitterSharingLink(self):
        link = self.getOutgoingURL()
        # http://mobile.twitter.com/home?status=Lukee%20nyt%20http%3A%2F%2Fm.yle.fi%2Fw%2Fuutiset%2Ftalous%2Fns-yduu-3-2638229
        return "http://mobile.twitter.com/home?status=" + urllib.quote(link)

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
            
            
    
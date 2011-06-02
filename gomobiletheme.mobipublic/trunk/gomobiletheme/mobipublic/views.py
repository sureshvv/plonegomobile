from zope.interface import Interface

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
    
    def update(self):
        if not hasattr(self, "targetContent"):
            self.targetContent = self.context
    
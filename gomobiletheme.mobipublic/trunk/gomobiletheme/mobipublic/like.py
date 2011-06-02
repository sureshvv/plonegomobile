
from zope.interface import Interface
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from cioppino.twothumbs import _
from cioppino.twothumbs import rate

from five import grok

# Layer for which against all our viewlets are registered
from interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')


class Thumbs(grok.View):
    """ Display the like/unlike widget. """

    grok.context(Interface)
    
    def canRate(self):
        return True
    
    def getStats(self):
        """
        Look up the annotation on the object and return the number of
        likes and hates
        """
        return rate.getTally(self.context)

    def myVote(self):
        if not self.canRate():
            return 0

        return rate.getMyVote(self.context)

    def getTwoThumbsAlt(self):
        if self.canRate():
            return _(u'I like this')
        return _(u'Please log in to rate this')

    def update(self):
        self.annotations = rate.setupAnnotations(self.context)

class LikeForm(grok.CodeView):
    """ Update the like/unlike status of a product via AJAX """

    def render(self):
        form = self.request.form

        if 'form.lovinit' in form:
            rate.loveIt(self.context)
            msg = u"You like it!"
        elif "form.hatedit" in form:
            rate.hateIt(self.context)
            msg = u"You don't like it!"
        else:
            msg = "Like fail"
            print self.request.form.items()
        
        from Products.statusmessages.interfaces import IStatusMessage
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(msg, type="info")

        self.request.response.redirect(self.context.absolute_url())
        return ""
        
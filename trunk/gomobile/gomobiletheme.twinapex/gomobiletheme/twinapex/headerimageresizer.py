"""

    Special handler for images stored in context annotations

"""

from StringIO import StringIO
import PIL

from five import grok
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter

from interfaces import IThemeLayer
from collective.fastview.template import PageTemplate

from gomobile.mobile.browser.resizer import getRecommendedDimensions
from gomobile.imageinfo.interfaces import IImageInfoUtility
from gomobile.mobile.interfaces import IUserAgentSniffer


# Use templates directory to search for templates.
grok.templatedir('templates')

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)

class MobileHeaderImageResizer(grok.CodeView):
    """ A special mobile-resize aware renderer for header images.

    We cannot use gomobile.mobile stock resizer as images
    are stored in annotation storage which is untraversable.
    """
    grok.context(Interface)
    grok.require('zope2.View')


    def getImage(self):
        """
        @return: PIL object for Archetypes image
        """
        field = self.context.getField("headerImage")
        value = field.get(self.context)
        data = value.data
        io = StringIO(data)
        return PIL.Image.open(io)

    def render(self):
        """
        """

        # Try sniffing device maximum image dimensions if supported
        device_size = None
        ua = getMultiAdapter((self.context, self.request), IUserAgentSniffer)

        if ua:
            width = ua.get("usableDisplayWidth")
            height = ua.get("usableDisplayHeight")
            if width and height:
                device_size = (width, height)
                print "Got device size: " + str(device_size)

        dimensions = getRecommendedDimensions(device_size, ("auto", "auto"), padding=(10, 10), fallback_size=(256,256))

        field = self.context.getField("headerImage")
        value = field.get(self.context)

        print "Resizing:" + str(dimensions)

        image = self.getImage()

        tool = getUtility(IImageInfoUtility)
        data, format = tool.performResize(image, dimensions[0], dimensions[1], conserve_aspect_ration=True)

        self.request.response.setHeader("Content-type", "image/" + format)

        if isinstance(data, StringIO):
            # Looks like ZMedusa server cannot stream data to the client...
            return data.getvalue()

        return data



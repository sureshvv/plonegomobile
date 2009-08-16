__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

from plone.browserlayer.interfaces import ILocalBrowserLayerType

#from collective.contentleadimage import LayoutImageMessageFactory as _

class ContentMediaOption:
    """ Pseudo-constants defining on which medias content should apper """
    WEB = "web"
    MOBILE = "mobile"
    USE_PARENT = "parent"    
    BOTH = "both" # default
    
class IConvergenceSupport(Interface):
    """ The content supports convergence options """


class IConvergenceMediaFilter(Interface):
    """ Utility to deal with the media state of content objects and catalog brains. """
    
class IConvergenceBrowserLayer(Interface):
    """ This layer is applied on the request when Plone Mobile product has been quick installed.
    
    It will have effects on sitemap etc.
    """


# -*- extra stuff goes here -*-
import zope.interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager


from gomobile.mobile.interfaces import IMobileLayer

class IThemeLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    
    This layer is applied on HTTPRequest when mobile rendering 
    is on.    
    """
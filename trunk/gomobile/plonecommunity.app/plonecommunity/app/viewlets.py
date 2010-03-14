"""

    Override theme viewlets for Plone Community mobile site.
    
    Inherit viewlets from the base theme package and add in needed 
    customizations.
    
    See http://code.google.com/p/plonegomobile/source/browse/trunk/gomobile/gomobiletheme.basic/gomobiletheme/basic/viewlets.py
    for available viewlets.
    

"""

__author__ = "Mikko Ohtamaa <mikko@mfabrik.com>"
__copyright__ = "2010 mFabrik Research Oy"
__docformat__ = "epytext"
__license__ = "GPL 2"

from gomobiletheme.basic import viewlets as base

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir("templates")

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)

class Head(base.Head):
    """
    Override <head> generation so that we use CSS files 
    and static resources specific to this skin.
    """
    
class Logo(base.Logo):    
    """ Mobile site logo """
    
    def getLogoName(self):
        return "++resource++plonecommunity.app/plone-logo-white-on-blue.png"


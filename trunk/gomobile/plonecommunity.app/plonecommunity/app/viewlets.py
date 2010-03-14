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

from zope.interface import Interface
from five import grok

from collective.fastview.utilities import fix_grok_template_inheritance
from gomobiletheme.basic import viewlets as base
from gomobiletheme.basic.viewlets import MainViewletManager
from plonecommunity.app.interfaces import IThemeLayer

# Viewlets are on all content by default.
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir("templates")

# Viewlets are active only when gomobiletheme.basic theme layer is activated
grok.layer(IThemeLayer)

grok.viewletmanager(MainViewletManager)


class AdditionalHead(base.AdditionalHead):
    """ Include some more service  specific CSS files.
    """
    
    def resource_url(self):
        """ Get static resource URL.
        
        See gomobiletheme.basic.viewlets.Head for more information.
        """
        return self.portal_url + "/" + "++resource++plonecommunity.app" 
        

class Logo(base.Logo):    
    """ Mobile site logo """
    
    def getLogoName(self):
        return "++resource++plonecommunity.app/plone-logo-white-on-blue.png"

# Fix for grok 1.0 template inheritance
# https://bugs.launchpad.net/grok/+bug/255005
fix_grok_template_inheritance(Logo, base.Logo)



class FooterText(base.FooterText):
    """
    Override footer text in footertext.pt.
    """



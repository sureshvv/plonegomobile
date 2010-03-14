from gomobile.mobile.browser.viewlets import common as base

class LogoViewlet(base.LogoViewlet):    
    """ Mobile site logo """
    
    def getLogoName(self):
        return "++resource++plonecommunity.app/plone-logo-white-on-blue.png"

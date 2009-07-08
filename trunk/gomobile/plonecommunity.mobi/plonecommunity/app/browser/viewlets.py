from gomobile.mobile.browser.viewlets import common as base

class LogoViewlet(base.LogoViewlet):    
    """ Mobile site logo """
    
    def update(self):
        common.LogoViewlet.update(self)
        self.portal = self.portal_state.portal()        
        logoName = "++resource++plonecommunity.app/logo-small.gif"

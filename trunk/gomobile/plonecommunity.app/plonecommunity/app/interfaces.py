from five import grok

import gomobiletheme.basic.interfaces as base

class IThemeLayer(base.IThemeLayer):
    """ Declare mobile theme layer.

    All views and viewlets registered against this layer are enabled
    only when site is in mobile mode and your theme is active.
    """
    
    grok.skin("plonecommunity.mobi theme")



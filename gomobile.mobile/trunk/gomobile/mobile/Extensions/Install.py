"""


    Old-fashioned uninstall script.
    
"""


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from gomobile.mobile.setuphandlers import clean_up_content_annotations

def uninstall(portal, reinstall=False):

    output = StringIO()
    if not reinstall:

        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-gomobile.mobile:uninstall')
      
        report = clean_up_content_annotations(portal, ["mobile"])
        print >> output, report
        
        print >> output, "Ran all uninstall steps."
        return output

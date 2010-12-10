__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"


def importFinalSteps(context):
    """
    The last bit of code that runs as part of this setup profile.
    """
    # Only run step if a flag file is present, otherwise this step
    # also gets run when applying a totally unrelated profile.
    if context.readDataFile('gomobile_convergence-default.txt') is None:
        return
    site = context.getSite()

    # GenericProfiles nukes catalog indexes on each quick installer run
    # work around this "feature" by reindexing the whole site
    # after the quick installer has been run
    site.portal_catalog.manage_reindexIndex(ids=['getContentMedias'])

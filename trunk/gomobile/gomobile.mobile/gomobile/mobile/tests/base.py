__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import utils

@onsetup
def setup_zcml():

    fiveconfigure.debug_mode = True
    import gomobile.convergence
    zcml.load_config('configure.zcml', gomobile.convergence)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.

    ztc.installPackage('gomobile.mobile')
    #ztc.installPackage('gomobile.convergence')



# The order here is important.
setup_zcml()
ptc.setupPloneSite(products=['gomobile.mobile'])

class BaseTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def setUp(self):
        ptc.PloneTestCase.setUp(self)

    def setDiscriminateMode(self, mode):
        utils.setDiscriminateMode(self.portal.REQUEST, mode)

from Products.Five.testbrowser import Browser

class BaseFunctionalTestCase(ptc.FunctionalTestCase):
    """ This is a base class for functional test cases for your custom product.
    """

    def afterSetUp(self):
        """
        Show errors in console by monkey patching site error_log service
        """

        ptc.FunctionalTestCase.afterSetUp(self)

        self.browser = Browser()
        self.browser.handleErrors = False # Don't get HTTP 500 pages


        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising


    def loginAsAdmin(self):
        """ Perform through-the-web login.

        Simulate going to the login form and logging in.

        We use username and password provided by PloneTestCase.

        This sets session cookie for testbrowser.
        """
        from Products.PloneTestCase.setup import portal_owner, default_password

        # Go admin
        browser = self.browser
        browser.open(self.portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()

    def setUA(self, user_agent):
        """
        Create zope.testbrowser Browser with a specific user agent.
        """

        # Be sure to use Products.Five.testbrowser here
        self.browser = UABrowser(user_agent)
        self.browser.handleErrors = False # Don't get HTTP 500 pages

from zope.testbrowser import browser
from Products.Five.testbrowser import PublisherHTTPHandler
from Products.Five.testbrowser import PublisherMechanizeBrowser

class UABrowser(browser.Browser):
    """A Zope ``testbrowser` Browser that uses the Zope Publisher.

    The instance must set a custom user agent string.
    """

    def __init__(self, user_agent, url=None):

        mech_browser = PublisherMechanizeBrowser()
        mech_browser.addheaders = [("User-agent", user_agent),]

        # override the http handler class
        mech_browser.handler_classes["http"] = PublisherHTTPHandler
        browser.Browser.__init__(self, url=url, mech_browser=mech_browser)


"""

    See also http://codespeak.net/svn/lxml/trunk/src/lxml/html/clean.py

"""

__license__ = "GPL 2"
__copyright__ = "2009 Twinapex Research"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__author_url__ = "http://www.twinapex.com"
__docformat__ = "epytext"

import re
import copy

try:
    import lxml
except ImportError:
    raise RuntimeError("Please install lxml: http://pypi.python.org/pypi/lxml/")

from lxml.html import defs
from lxml.html import fromstring, tostring, XHTML_NAMESPACE
from lxml.html import _nons, _transform_result

from lxml.html.clean import Cleaner

class XHTMLMPCleaner(Cleaner):
    """ Clean incoming HTML to be valid XHTML mobile profile without any nastiness """
    
    def add_alt_tags(self, doc):
        """ Alt tags are needed for every image.
        
        If not ALT tag is present, put in an empty string.
        """
        
        for el in doc.iter('img'):
            if not "alt" in el.attrib:
                el.attrib["alt"] = ""
        
    def clean_mobile(self, doc):
        """ Run XHTML-MP specific cleaners for the document.
        """        
        self.add_alt_tags(doc)
        
    def clean(self, html):
        """ Run XHTML mobile profile cleaner for HTML code.
        
        @param html: HTML as a strinrg or lxml Document        
        @return: XHTML, utf-8 encoded string
        """ 
        result_type = type(html)
        
        if isinstance(html, basestring):
            doc = fromstring(html)
        else:
            doc = copy.deepcopy(html)
        
        # Run normal cleaning
        self(doc)
        
        # Run XHTML MP specific cleaning
        self.clean_mobile(doc)
        
        return tostring(doc, method="xml", encoding='UTF-8')

cleaner = XHTMLMPCleaner()

clean_xhtml_mp = cleaner.clean  

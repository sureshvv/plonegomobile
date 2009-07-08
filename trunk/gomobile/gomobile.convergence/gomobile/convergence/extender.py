"""


"""

__license__ = "GPL 2.1"
__copyright__ = "2009 Twinapex Research"

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.Archetypes.public import ImageField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes import public as atapi
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.configuration import zconf
from Products.Archetypes.Registry import registerWidget

from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from ZPublisher import NotFound
from Products.validation import V_REQUIRED

from Products.Archetypes.interfaces import IBaseObject

from gomobile.convergence.interfaces import IConvergenceSupport, ContentMediaOption
from gomobile.convergence.filter import media_options_vocabulary

IMAGE_SIZE = (730,210)
    
class ExtentedImageField(ExtensionField, ImageField):
    """A Image field. """

    @property
    def sizes(self):
        sizes = {}
        sizes['leadimage'] = IMAGE_SIZE
        return sizes

class ExtentedAnimationField(ExtensionField, atapi.FileField):
    """A Image field. """
    
    
class ExtentedBooleanField(ExtensionField, atapi.BooleanField):
    pass

class ExtentedStringField(ExtensionField, atapi.StringField):
    pass
        
        
class ConvergenceSchemaModifier(object):
    """ Override Title renderer with a custom version. """
    implements(ISchemaModifier)
    adapts(IConvergenceSupport)
    
    def __init__(self, context):
        self.context = context
    
    def fiddle(self, schema):
        pass
        
class ConvergenceExtender(object):
    adapts(IConvergenceSupport)
    implements(IOrderableSchemaExtender)

    fields = [
              
        ExtentedStringField("contentMedias",
          schemata="mobile",
          required = False,          
          languageIndependent = True,
          default="parent",
          enforceVocabulary = True,
          vocabulary = media_options_vocabulary,
          widget = atapi.SelectionWidget(
                         format="radio",
                         label="Content media",
                         description=u"Does this content appear on web, mobile or both",
                         
            ),       
        ),
        
        
        ExtentedBooleanField("mobileFolderListing",
          schemata="mobile",
          required = False,          
          languageIndependent = True,
          default=False,          
          widget = atapi.BooleanWidget(
                         label="Mobile folder listing",
                         description=u"List folder contents as touch screen buttons below content",
                         
            ),       
        ),
        
        ExtentedImageField("mobileButtonImage",
          schemata="mobile",
          required = False,
          storage = AnnotationStorage(migrate=True),
          languageIndependent = False,
          validators = (('isNonEmptyFile', V_REQUIRED),),
          widget = ImageWidget(
                         label="Mobile button",
                         description=u"Upload image which will be used as a link image for this page",
                         show_content_type=False,
                 ),
            )
    ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
        return self.fields
    
    def getOrder(self, original):
        """
        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.
        
        Move leadImage field just after the Description
        """        
        return original
    

class ExtenterTraverser(DefaultPublishTraverse):
    implements(IPublishTraverse)
    adapts(IConvergenceSupport, IHTTPRequest)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def publishTraverse(self, request, name):
        
        fileFields = ["mobileButtonImage"]

        # Check whether content exist
        for check in fileFields:

            if name.startswith("has_" + check):
                field = self.context.getField(check)
                file = field.get(self.context)
                if file is not None and not isinstance(file, basestring):
                    # image might be None or '' for empty images
                    return True
        
        # Return actual content
        for check in fileFields:
            
            if name.startswith(check):
                field = self.context.getField(check)
                file = field.get(self.context)

                if file is not None and not isinstance(file, basestring):
                    # image might be None or '' for empty images
                    return file
                    
        return super(ExtenterTraverser, self).publishTraverse(request, name)



"""
    Suppoer behavior assignments for non-dexerity objects.

    Define default mechanism to determine whether thr header animation
    is enabled (the header is editable) on content.

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

import zope.interface
import zope.component
import zope.schema

from zope.annotation.interfaces import IAnnotations

from five import grok

from Products.CMFCore.interfaces import IContentish
from persistent import Persistent

from plone.directives import form
from zope.schema.interfaces import IContextSourceBinder

from gomobile.convergence.interfaces import IOverrider, IOverrideEditView, IOverrideForm
from gomobile.convergence.utilities import make_terms

class IOverrideStorage(zope.interface.Interface):
    """
    Adapter to store mobile overrides on context objects.

    You can override this adapter to
    store data in different database, for example.
    """

class OverrideStorage(Persistent):
    """
    Persistent object storing z3c.form field values for mobile overrides.

    Field values are attributes of this.

    - Attribute name is the name of the overriden field (like description)

    - Attribute value is the overriden value for the field
    """

    KEY = "mobile_override_values"

def getOverrideStorage(context):
    """ Default implementation how to store mobile overridden values for context objects.

    Use zope.annotations package to stick data on __annotations__ attribute on the object.
    """

    annotations = IAnnotations(context)

    value = annotations.get(OverrideStorage.KEY, None)
    if value is None:
        # Compute value and store it on request object for further look-ups
        value = annotations[OverrideStorage.KEY] = OverrideStorage()

    return value

class Overrider(object):
    """
    Base class for mobile overrides.

    Checks if

    - The field is on "enabled overrides" list

    - Read the field value from mobile overrides instead of the proxyed real object

    The adapter look up uses standard view properties.

    We use underscore to mark functions and attributes which are not proxied
    from the orignal object in any scenario.
    """

    zope.interface.implements(IOverrider)

    # zope.schema object describing overriden fields
    _schema = None

    def __init__(self, context):
        self.context = context

    def _getOverrideFieldNames(self):
        return zope.schema.getFieldNamesInOrder(self._schema)

    def _isOverride(self, fieldName):
        """
        @return True: If the field is overridable field
        """
        return fieldName in self._getOverrideFieldNames()

    def _isOverrideEnabled(self, fieldName, storage):
        """
        Check whether the fieldName appears in "overrided fields list"
        """
        overrides = getattr(storage, "enabled_overrides", [])
        return fieldName in overrides

    def _fixCallable(self, fieldName, value):

        # Check whether the orignal accessed attribute
        # was callable or not

        def callable_proxy():
            """ Faux generated function to return the overridden value when accessed as function """
            return value

        orignal = getattr(self.context, fieldName)
        if callable(orignal):
            return callable_proxy
        else:
            return value

    def _getOverrideOrOrignal(self, fieldName):
        """
        """
        if self._isOverride(fieldName):

            storage = IOverrideStorage(self.context)

            if self._isOverrideEnabled(fieldName, storage):
                value = getattr(storage, fieldName)
                if value != None:
                    return self._fixCallable(fieldName, value)

        # Fall back to orignal field value
        return getattr(self.context, fieldName)

    def __str__(self):
        return "Mobile overrides proxy object for %s" % str(self.context)



    def __getattr__(self, name):
        """ Proxy magic.
        """
        if name.startswith("_"):
            return self.__dict__[name]
        else:
            return self._getOverrideOrOrignal(name)

@grok.provider(IContextSourceBinder)
def get_field_list(context):
    """ Return available overridable fields for mobile
    """
    overrider = IMobileOverride(context)

    assert overrider._schema is not None, "Context overrider not sane:" + str(context)

    fields = zope.schema.getFieldsInOrder(overrider._schema)

    terms = [ SimpleTerm(value=field.name, token=field.name, title=field.title) for field in fields ]

    return SimpleVocabulary(terms)


class IOverrideFormSchema(form.Schema):
    """ Base class for editable override forms """

    form.widget(enable_overrides='z3c.form.browser.checkbox.CheckboxWidget')
    enabled_overrides = zope.schema.Choice(source=get_field_list, title=u"Overridden fields", required=False)

class OverrideForm(form.EditForm):
    """ Site editor interface for mobile override attributes.
    """
    ignoreContext = False

    grok.baseclass()
    grok.context(IContentish)

    zope.interface.implements(IOverrideForm)

    schema = IOverrideFormSchema

    def getContents(self):
        storage = IOverrideStorage(self.context)
        assert storage is not None
        return storage
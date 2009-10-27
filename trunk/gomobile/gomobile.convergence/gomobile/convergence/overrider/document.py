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
from zope import schema

from gomobile.convergence.overrider import base
from gomobile.convergence.utilities import addSchema

from plone.directives import form
from plone.app.z3cform.layout import wrap_form
from z3c.form import field

class Schema(form.Schema):
    """ Schema for overriden accessors.

    Correspond AT accessor names for  Products.ATContentTypes.content.document.ATDocumentSchema.
    """

    Title = schema.TextLine(title=u"Title")

    Description = schema.Text(title=u"Description")

    form.widget(getText='plone.app.z3cform.wysiwyg.WysiwygFieldWidget')
    getText = schema.Text(title=u"Text")


class DocumentOverrider(base.Overrider):
    """ Provide mobile specific versions for title, description and text Document.

    Document is Products.ATContentTypes.content.document.ATDocument object.
    """

    _schema = Schema

class IFormSchema(form.Schema):
    """ Schema for "edit mobile overrides" form """


addSchema(IFormSchema, base.IOverrideFormSchema)
addSchema(IFormSchema, Schema)

class DocumentOverriderForm(base.OverrideForm):
    """ Edit mobile overrides for the document
    """

    fields = field.Fields(IFormSchema)


DocumentOverriderFormView = wrap_form(DocumentOverriderForm)

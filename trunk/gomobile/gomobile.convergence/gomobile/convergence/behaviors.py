"""
    Multi-channel behavior for content.

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

from persistent import Persistent

from zope import schema
from zope.interface import implements, alsoProvides
from zope.component import adapts
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema import getFields
from zope.annotation.interfaces import IAnnotations

from plone.directives import form

from gomobile.mobile.behaviors import FieldPropertyDelegate

from gomobile.convergence.interfaces import ContentMediaOption


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

items = (
    (u"User parent folder setting", ContentMediaOption.USE_PARENT),
    (u"Both", ContentMediaOption.BOTH),
    (u"Web", ContentMediaOption.WEB),
    (u"Mobile", ContentMediaOption.MOBILE)
    )

terms = [ SimpleTerm(value=pair[1], token=pair[1], title=pair[0]) for pair in items ]

contentMediasVocabury = SimpleVocabulary(terms)

class IMultiChannelBehavior(form.Schema):
    """ How content and its children react to differt medias """

    form.fieldset(
        'multichannel',
        label=('Multichanne'),
        fields=('contentMedias'),
    )

    contentMedias = schema.Choice(vocabulary=contentMediasVocabury,
                                  title=u"Content medias",
                                  description=u"Does this content appear on web, mobile or both",
                                  default=ContentMediaOption.USE_PARENT,
                                  required=True)

alsoProvides(IMultiChannelBehavior, form.IFormFieldProvider)

#
class MultiChannelBehaviorStorage(Persistent):
    """Set IMultiChannelBehavior specific field properties on the context object and return the context object itself.#

    This allows to use attribute storage with schema input validation.
    """

    implements(IMultiChannelBehavior)

    contentMedias = FieldPropertyDelegate(IMultiChannelBehavior["contentMedias"])

    def __init__(self, context):
        self.context = context


def behavior_factory(context):

    annotations = IAnnotations(context)
    if not "multichannel" in annotations:
        annotations["multichannel"] = MultiChannelBehaviorStorage(context)

    object = annotations["multichannel"]

    return object





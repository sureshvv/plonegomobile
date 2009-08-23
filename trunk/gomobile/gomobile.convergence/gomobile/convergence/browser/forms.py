"""
    Convergence related forms and form views.

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2009 Twinapex Research"
__license__ = "GPL v2"

import zope.interface
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
import zope.app.pagetemplate.viewpagetemplatefile
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

import z3c.form
import z3c.form.interfaces
from z3c.form import field

from plone.directives import form
from plone.z3cform.layout import FormWrapper, wrap_form
from plone.z3cform.crud import crud

import plone.z3cform.interfaces
import plone.z3cform.templates

from gomobile.convergence.behaviors import IMultiChannelBehavior

class MultiChannelForm(form.EditForm):
    """ Form which displays options to edit header animation.

    """
    fields = field.Fields(IMultiChannelBehavior)

    label = u"Multichannel publishing settings"

    def getContent(self):
        """ @return: Persistent data to edit by form machinery """
        return IMultiChannelBehavior(self.context)

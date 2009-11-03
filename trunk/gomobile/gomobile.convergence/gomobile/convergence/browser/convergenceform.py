"""

    Convergence options edit forms

"""

import zope.interface
from zope import schema
from zope.component import getUtility, queryUtility
from zope.component import getMultiAdapter, queryMultiAdapter

import z3c.form.form
from z3c.form import subform
from z3c.form import field
from z3c.form import group

from gomobile.convergence.interfaces import IOverrideForm, IOverrider
from plone.z3cform.layout import FormWrapper, wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

from gomobile.convergence.behaviors import contentMediasVocabury, IMultiChannelBehavior
from gomobile.convergence.interfaces import ContentMediaOption, IConvergenceMediaFilter, IConvergenceBrowserLayer
from gomobile.convergence.filter import media_options_vocabulary

from gomobile.convergence.overrider.base import IOverrideStorage

class PublishingForm(group.Group):
    """ Folder/page specific convergence options """
    
    fields = field.Fields(IMultiChannelBehavior)

    label = u"Media options"

    def update(self):
        return group.Group.update(self)

    def getContent(self):
        """ @return: Persistent data to edit by form machinery """
        return IMultiChannelBehavior(self.context)

class OverrideForm(group.Group):
    """ Fielde specific convergence options """

    label = u"Field overrides"

    def update(self):
        return group.Group.update(self)

    def getContent(self):
        storage = IOverrideStorage(self.context)
        assert storage is not None
        
        # Make sure that z3c.form.datamanager
        # accepts our storage as input
        #form = getMultiAdapter((self.context, self.request), IOverrideForm)
        #zope.interface.directlyProvides(storage, form._schema)
    
        return storage
    
    def update(self):
        """ Dynamically load fields.
        
        Form.update() is correct place to fiddle
        with fields information, before proceeding
        to parent update() and widget creation.
        """

        self.fields = self.getOverriderFields()
        group.Group.update(self)
        
    def getOverriderFields(self):
        """ Recycle fields dynamically from another form instance """
    
        # Get the mobile overrider form for the context
        form = getMultiAdapter((self.context, self.request), IOverrideForm)
        
        # Read its Fields instance
        fields = form.fields
        # Fields could be mofified in this point
        # (need to duplicate it first though)
        
        return fields

class MasterForm(group.GroupForm, z3c.form.form.EditForm):
    """ Multi-form orchestaring the convergence as a whole """
    
    groups = (PublishingForm, OverrideForm)
    
    def update(self):
        import pdb ; pdb.set_trace()
        return super(MasterForm, self).update()
       
       #self.publishing = PublishingForm(self.context, self.request, self)
       #self.override = OverrideForm(self.context, self.request, self)

       #self.publishing.update()
       #self.override.update()
       
       
class MasterFormView(FormWrapper):
 
    form = MasterForm
    
    label = u"Multichannel management"
    
    index = FiveViewPageTemplateFile("convergenceformview.pt")

    #def render(self):
        #import pdb ; pdb.set_trace()
    #    z3c.form.form.EditForm.render(self)

    
    def media_status(self):
        """ Get human-readable text on which medias the context is available  """
        filter = getUtility(IConvergenceMediaFilter)
        context = self.context.aq_inner
        media = filter.solveContentMedia(context)
        
        # Translate
        for id, text in media_options_vocabulary:
            if id == media:
                return text
        
        return None
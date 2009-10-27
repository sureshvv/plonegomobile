"""


"""

import z3c.form.form
from z3c.form import subform

class PublishingForm(subform.EditSubFrom):

    fields = field.Fields(IMultiChannelBehavior)

    label = u"Publishing settings"

    def getContent(self):
        """ @return: Persistent data to edit by form machinery """
        return IMultiChannelBehavior(self.context)

class OverrideForm(subform.EditSubForm):

    def getContents(self):
        storage = IOverrideStorage(self.context)
        assert storage is not None
        return storage

    def constructFields(self):
        """ Construct fields dynamically as they depent on the content type """


class MasterForm(z3c.form.form.Form):

   def update(self):
       super(MasterForm, self).update()
       self.publishing = PublishingForm(self.context, self.request, self)
       self.override = OverrideForm(self.context, self.request, self)

       self.publishing.update()
       self.override.update()
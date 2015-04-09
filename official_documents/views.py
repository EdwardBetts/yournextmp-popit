from django.views.generic import CreateView, DetailView

from candidates.static_data import MapItData
from auth_helpers.views import GroupRequiredMixin

from .forms import UploadDocumentForm
from .models import DOCUMENT_UPLOADERS_GROUP_NAME, OfficialDocument

class DocumentView(DetailView):
    model = OfficialDocument

    def get_context_data(self, **kwargs):
        context = {}
        context['constituency'] = \
            MapItData.constituencies_2010[self.object.mapit_id]
        context.update(kwargs)
        return context

class CreateDocumentView(GroupRequiredMixin, CreateView):
    required_group_name = DOCUMENT_UPLOADERS_GROUP_NAME

    form_class = UploadDocumentForm
    template_name = "official_documents/upload_document_form.html"

    def get_initial(self):
        return {
            'mapit_id': self.kwargs['mapit_id'],
            'document_type': OfficialDocument.NOMINATION_PAPER
        }

    def get_context_data(self, **kwargs):
        context = {}
        context['constituency'] = \
            MapItData.constituencies_2010[self.kwargs['mapit_id']]
        context.update(kwargs)
        return context

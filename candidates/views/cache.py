import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.views.generic import View

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from candidates.cache import invalidate_person, invalidate_posts


# class InvalidatePersonView(LoginRequiredMixin, StaffuserRequiredMixin, View):
class InvalidatePersonView(View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        person_id = request.POST['person_id']
        if re.search(r'^\d+$', person_id):
            invalidate_person(person_id)
        return HttpResponseRedirect(
            reverse('person-view', kwargs={
                'person_id': person_id
            })
        )


class InvalidatePostView(LoginRequiredMixin, StaffuserRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post_id = request.POST['mapit_area_id']
        if re.search(r'^\d+$', post_id):
            invalidate_posts([post_id])
        return HttpResponseRedirect(
            reverse('constituency', kwargs={
                'mapit_area_id': post_id,
                'ignored_slug': ''
            })
        )

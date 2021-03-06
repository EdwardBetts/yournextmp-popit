import re

from django import forms
from django.core.exceptions import ValidationError

from .models import QueuedImage

class UploadPersonPhotoForm(forms.ModelForm):

    class Meta:
        model = QueuedImage
        fields = [
            'image', 'why_allowed',
            'justification_for_use', 'popit_person_id', 'decision'
        ]
        widgets = {
            'popit_person_id': forms.HiddenInput(),
            'decision': forms.HiddenInput(),
            'why_allowed': forms.RadioSelect(),
            'justification_for_use': forms.Textarea(
                attrs={'rows': 1, 'columns': 72}
            )
        }

    def clean_popit_person_id(self):
        popit_person_id = self.cleaned_data['popit_person_id']
        if not re.search(r'^\d+$', popit_person_id):
            raise ValidationError("The popit_person_id must be all digits")
        return popit_person_id

    def clean(self):
        cleaned_data = super(UploadPersonPhotoForm, self).clean()
        justification_for_use = cleaned_data.get(
            'justification_for_use', ''
        ).strip()
        why_allowed = cleaned_data.get('why_allowed')
        if why_allowed == 'other' and not justification_for_use:
            message = "If you checked 'Other' then you must provide a " + \
                "justification for why we can use it."
            raise ValidationError(message)
        return cleaned_data


class PhotoReviewForm(forms.Form):

    queued_image_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
    )
    x_min = forms.IntegerField(min_value=0)
    x_max = forms.IntegerField(min_value=1)
    y_min = forms.IntegerField(min_value=0)
    y_max = forms.IntegerField(min_value=1)
    decision = forms.ChoiceField(choices=QueuedImage.DECISION_CHOICES)
    make_primary = forms.BooleanField(required=False)
    rejection_reason = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    justification_for_use = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    moderator_why_allowed = forms.ChoiceField(
        choices=QueuedImage.WHY_ALLOWED_CHOICES
    )

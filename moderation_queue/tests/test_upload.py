from mock import patch
from os.path import join, realpath, dirname
from urlparse import urlsplit

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from django_webtest import WebTest
from webtest import Upload

from ..models import QueuedImage
from candidates.tests.fake_popit import FakePersonCollection

TEST_MEDIA_ROOT=realpath(join(dirname(__file__), 'media'))

class PhotoUploadTests(WebTest):

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUp(self):
        self.test_upload_user = User.objects.create_user(
            'john',
            'john@example.com',
            'notagoodpassword',
        )
        self.test_upload_user.terms_agreement.assigned_to_dc = True
        self.test_upload_user.terms_agreement.save()

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    @patch('candidates.popit.PopIt')
    def test_photo_upload(self, mock_popit):
        mock_popit.return_value.persons = FakePersonCollection
        image_filename = join(TEST_MEDIA_ROOT, 'pilot.jpg')
        upload_form_url = reverse(
            'photo-upload',
            kwargs={'popit_person_id': '2009'}
        )
        form_page_response = self.app.get(
            upload_form_url,
            user=self.test_upload_user
        )
        form = form_page_response.forms['person-upload-photo']
        with open(image_filename) as f:
            form['image'] = Upload('pilot.jpg', f.read())
        form['why_allowed'] = 'copyright-assigned'
        form['justification_for_use'] = 'I took this photo'
        upload_response = form.submit()
        self.assertEqual(upload_response.status_code, 302)
        split_location = urlsplit(upload_response.location)
        self.assertEqual('/moderation/photo/upload/2009/success', split_location.path)
        queued_images = QueuedImage.objects.all()
        self.assertEqual(1, queued_images.count())
        queued_image = list(queued_images)[0]
        self.assertEqual(queued_image.decision, 'undecided')
        self.assertEqual(queued_image.why_allowed, 'copyright-assigned')
        self.assertEqual(
            queued_image.justification_for_use,
            'I took this photo'
        )
        self.assertEqual(queued_image.popit_person_id, '2009')
        self.assertEqual(queued_image.user, self.test_upload_user)

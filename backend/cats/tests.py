import base64
import tempfile
from http import HTTPStatus
from io import BytesIO

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient


class CatsAPITestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='auth_user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_exists(self):
        """Проверка доступности списка задач."""
        response = self.client.get('/api/cats/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_and_replace_image(self):
        with tempfile.TemporaryDirectory() as media:
            with override_settings(MEDIA_ROOT=media):
                for image_format in ('JPEG', 'PNG'):
                    stream = BytesIO()
                    Image.new('RGB', (2, 2), 'red').save(stream, image_format)
                    encoded = base64.b64encode(stream.getvalue()).decode()
                    data = {
                        'name': 'Demo cat', 'birth_year': 2020,
                        'color': '#FFFFFF',
                        'image': f'data:image/{image_format.lower()};base64,'
                                 f'{encoded}',
                    }
                    response = self.client.post(
                        '/api/cats/', data, format='json'
                    )
                    self.assertEqual(response.status_code, HTTPStatus.CREATED)
                    url = f'/api/cats/{response.data["id"]}/'
                    response = self.client.patch(
                        url, {'image': data['image']}, format='json'
                    )
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    self.assertTrue(response.data['image_url'])
                    response = self.client.patch(
                        url, {'image': None}, format='json'
                    )
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    self.assertIsNone(response.data['image_url'])

    def test_invalid_image_returns_validation_error(self):
        response = self.client.post('/api/cats/', {
            'name': 'Demo cat', 'birth_year': 2020, 'color': '#FFFFFF',
            'image': 'data:image/png;base64,bm90IGFuIGltYWdl',
        }, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn('image', response.data)

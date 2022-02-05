from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """Test the public available tags API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test the authorized user tags API."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'snape@hogwarts.com',
            'imserious'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        for tag in ['Vegan', 'Meal']:
            Tag.objects.create(user=self.user, name=tag)

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """Test that tags returned are for the authenticated user."""
        user2 = get_user_model().objects.create_user(
            'rony@hogsmeade.com',
            'weasleyF'
        )
        Tag.objects.create(user=user2, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Meal')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

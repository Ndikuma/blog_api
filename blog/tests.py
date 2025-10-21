from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Post, Category


class BlogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.category = Category.objects.create(name="Tech")
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {
            "title": "API Auth Post",
            "content": "Protected route test",
            "category": self.category.id,
        }
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, 201)

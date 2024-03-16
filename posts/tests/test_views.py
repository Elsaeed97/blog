from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from posts.views import PostViewSet
from rest_framework.authtoken.models import Token
from posts.models import Post
from posts.serializers import PostSerializer
from .factories import PostFactory, UserFactory


class PostViewSetTestCase(APITestCase):
    """
    Test case class for testing the PostViewSet.
    """

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.post = PostFactory(author=self.user)
        self.token = Token.objects.create(user=self.user)
        self.another_token = Token.objects.create(user=self.user2)
        self.factory = APIRequestFactory()
        self.view = PostViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.url = "/api/posts/"
        self.post_url = f"/api/posts/{self.post.pk}/"

    def test_create_post(self):
        post_data = PostSerializer(PostFactory.build()).data

        request = self.factory.post(self.url, post_data, format="json")
        request.user = self.user
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token.key
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Post.objects.exists())
        post = Post.objects.first()
        self.assertEqual(post.title, post_data["title"])
        self.assertEqual(post.content, post_data["content"])
        self.assertEqual(post.author, self.user)

    def test_create_post_with_long_title(self):
        post_data = PostFactory.build(title="Title" * 50)

        post_data_json = PostSerializer(post_data).data
        request = self.factory.post(self.url, post_data_json, format="json")
        request.user = self.user
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token.key
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_error_message = ["Ensure this field has no more than 200 characters."]
        self.assertEqual(response.data["title"], expected_error_message)

    def test_update_post_with_post_author(self):
        data = {"title": "Updated Title", "content": "Updated Content"}
        request = self.factory.put(self.post_url, data, format="json")
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token.key
        response = self.view(request, pk=self.post.pk)

        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated Content")

    def test_update_post_with_another_user(self):
        data = {"title": "Updated Title", "content": "Updated Content"}
        request = self.factory.put(self.url, data, format="json")
        request.user = self.user2
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.another_token.key
        response = self.view(request, pk=self.post.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, "Updated Title")
        self.assertNotEqual(self.post.content, "Updated Content")

    def test_delete_post_with_post_author(self):
        request = self.factory.delete(self.post_url)
        request.user = self.user
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token.key
        response = self.view(request, pk=self.post.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_post_with_another_user(self):
        request = self.factory.delete(self.post_url)
        request.user = self.user2
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + self.another_token.key
        response = self.view(request, pk=self.post.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

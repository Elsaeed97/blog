from django.test import TestCase
from posts.models import Post
from .factories import PostFactory


class PostModelTestCase(TestCase):
    """
    Test case class for testing the Post Model.
    """
    def test_create_post(self):
        post_factory = PostFactory()

        post = Post.objects.get(pk=post_factory.pk)

        self.assertEqual(post_factory.title, post.title)
        self.assertEqual(post_factory.content, post.content)
        self.assertEqual(post_factory.author, post.author)

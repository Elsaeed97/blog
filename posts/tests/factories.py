import factory
from factory.django import DjangoModelFactory
from faker import Faker
from posts.models import Post
from django.contrib.auth import get_user_model

fake = Faker()

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
    content = fake.paragraph()
    author = factory.SubFactory(UserFactory)

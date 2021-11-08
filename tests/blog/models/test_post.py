"""
Testing Post
"""

from model_mommy import mommy
import pytest

from blog.models import Post

def test_get_authors_returns_users_who_have_authored_a_post(django_user_model):
    # Create a user
    author = mommy.make(django_user_model)
    # Create a post that is authored by the user
    mommy.make('blog.Post', author=author, _quantity=3)
    # Create another user – but this one won't have any posts
    mommy.make(django_user_model)

    assert list(Post.objects.get_authors()) == [author]

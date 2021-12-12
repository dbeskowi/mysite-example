# tests/blog/models/test_post.py
import datetime as dt
from model_mommy import mommy
import pytest

from blog.models import Post


pytestmark = pytest.mark.django_db


def test_get_absolute_url_for_post_with_published_date():
    post = mommy.make(
        'blog.Post',
        published=dt.datetime(2014, 12, 20, tzinfo=dt.timezone.utc),
        slug='model-instances',
    )
    assert post.get_absolute_url() == '/posts/2014/12/20/model-instances/'


def test_get_absolute_url_for_post_without_published_date_or_slug():
    post = mommy.make(
        'blog.Post',
        published=None,
    )

    assert post.get_absolute_url() == f'/posts/{post.pk}/'


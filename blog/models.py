"""
    blog.models
"""

from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.

class Topic(models.Model):
    """
    Topic
    """
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Meta for ordering
        """
        ordering = ['name']


class PostQuerySet(models.QuerySet):
    """
    Extra frequently used queries
    """

    def published(self):
        """
        Returns all published posts
        """
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """
        Returns all draft posts
        """
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        """
        returns all authors
        """
        User = get_user_model()
        return User.objects.filter(blog_posts__in=self).distinct()


class Post(models.Model):
    """
        Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',  # Slug is unique for publication date
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        if self.published:
            return reverse(
                'post-detail',
                kwargs={
                    'year': self.published.year,
                    'month': self.published.month,
                    'day': self.published.day,
                    'slug': self.slug
                }
            )

        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        """
            Post.Meta
        """
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']

    def __str__(self):
        return str(self.title)


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'

"""
html templates here
"""

from django.shortcuts import render
from . import models
from django.views.generic import TemplateView


# Create your views here.


def home(request):
    """
    home blog
    """
    # Get last 3 pos    ts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    # Add as context variable "latest_posts"
    context = {
        'authors': authors,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/home.html', context)


def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class ContextMixin:
    """
    Provides common context variables for blog views
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Post.objects.published() \
            .get_authors() \
            .order_by('first_name')

        return context


class AboutView(ContextMixin, TemplateView):
    template_name = 'blog/about.html'
    """
    # Not needed using ContextMixin
    def get_context_data(self, **kwargs):
        # get context from parent
        context = super().get_context_data(**kwargs)

        # Define "authors" context variable
        context['authors'] = models.Post.objects.published() \
            .get_authors() \
            .order_by('first_name')

        return context
    """


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
                           .order_by('-published')[:3]

        # Update the context with our context variables
        context.update({
            'latest_posts': latest_posts
        })

        return context

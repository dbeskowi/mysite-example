"""
html templates here
"""

from django.shortcuts import render
from . import models

# Create your views here.

def home(request):
    """
    home blog
    """
    # Get last 3 pos    ts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    # Add as context variable "latest_posts"
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/home.html', context)

"""
html templates here
"""

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, CreateView, ListView
#FormView,


from . import forms, models

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


def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})


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


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class PostDetailView(DetailView):
    model = models.Post
    context_object_name = 'post'

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset().published().order_by('-published')

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)

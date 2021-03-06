"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog import views  # Import the views module

urlpatterns = [
    # path('', views.index),  # Add our index view to the URL patterns
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('terms/', views.terms_and_conditions, name='terms-and-conditions'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('form-example/', views.form_example, name='form-example'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
]

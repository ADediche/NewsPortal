from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostsList (ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
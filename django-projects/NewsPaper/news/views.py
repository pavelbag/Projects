from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post

class NewsList(ListView):
    model = Post

    ordering = '-date'

    template_name = 'news_list.html'
    context_object_name = 'news_list'

class NewsDetail(DetailView):
    model = Post

    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
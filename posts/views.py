from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from comentarios.models import Comment


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 3


class PostSearch(PostIndex):
    pass


class PostCategory(PostIndex):
    pass


class PostDetails(UpdateView):
    pass

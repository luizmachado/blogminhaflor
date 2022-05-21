from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from comentarios.models import Comment
from django.db.models import Q, Count, Case, When


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(post_published=True)
        # Count only comments published
        qs = qs.annotate(
            comment_count=Count(
                Case(
                    When(comment__comment_published=True, then=1)
                )
            )
        )
        return qs


class PostSearch(PostIndex):
    pass


class PostCategory(PostIndex):
    pass


class PostDetails(UpdateView):
    pass

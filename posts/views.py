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
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')
        qs = qs.filter(
            Q(post_title__icontains=termo) |
            Q(post_author__first_name__icontains=termo) |
            Q(post_brief__icontains=termo) |
            Q(post_content__icontains=termo) |
            Q(post_category__cat_name__icontains=termo)
        )
        return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)
        if not category:
            return qs
        qs = qs.filter(post_category__cat_name__iexact=category)
        return qs


class PostDetails(UpdateView):
    pass

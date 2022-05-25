from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Post
from comentarios.models import Comment
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComment
from django.views import View
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('post_category')
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


class PostDetails(View):
    template_name = 'posts/post_detail.html'

    # Method used to share attributes between this views methods
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, post_published=True)
        self.context = {
            'post': post,
            'comments': Comment.objects.filter(comment_post=post, comment_published=True),
            'form': FormComment(request.POST or None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.context['form']

        if not form.is_valid():
            return render(request, self.template_name, self.context)
        comment = form.save(commit=False)

        if request.user.is_authenticated:
            comment.comment_user = request.user

        comment.comment_post = self.context['post']
        comment.save()
        messages.success(request, 'Seu comentário foi enviado para moderação.')
        return redirect('post_details', pk=self.kwargs.get('pk'))

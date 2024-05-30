from django.contrib.auth.models import User
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from django.views.generic.edit import FormView

from notatki.models import Post, Comment
from . import models
from .forms import CommentForm, PostForm
from taggit.models import Tag


# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request, "notatki/post/list.html", context={"posts": posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3  # ile elementow ma byc na jednej stronie
    template_name = "notatki/post/list.html"


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    comment_form = CommentForm()
    return render(request, 'notatki/post/detail.html',
                  context={"post": post, "comments": comments, "comment_form": comment_form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('notatki/post/detail.html', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'notatki/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('notatki/post_detail.html', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'notatki/post_edit.html', {'form': form})

# class CreateNewPost(FormView):
#     form_class = PostForm
#     template_name = "notatki/create.html"
#     success_url = "/"
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         new_object = Post.objects.create(
#             title=form.cleaned_data['title'],
#             text=form.cleaned_data['text']
#         )
#
#         return super().form_valid(form)


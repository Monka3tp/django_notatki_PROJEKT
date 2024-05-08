from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from notatki.models import Post


# Create your views here.
# def post_list(request):
#     posts = Post.published.all()
#     return render(request, "notatki/post/list.html", context={"posts": posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3 #ile elementow ma byc na jednej stronie
    template_name = "notatki/post/list.html"

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post , slug=slug, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'notatki/post/detail.html', context={"post": post})
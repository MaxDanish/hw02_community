from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.http import HttpResponse, HttpRequest


POSTS_LIMIT: int = 10


def index(request: HttpResponse) -> HttpRequest:
    """
    Передаёт в шаблон posts/index.html десять последних объектов модели Post.
    """
    template = 'posts/index.html'
    posts = Post.objects.select_related('author')[:POSTS_LIMIT]
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Передаёт в шаблон posts/group_list.html десять последних объектов модели
    Post, отфильтрованных по полю group, и содержимое для тега <title>.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    # Нижняя строка не подсвечивается и при наведении на posts/all() выдает ANY
    posts = group.posts.all()[:POSTS_LIMIT]
    context = {
        'slug': slug,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)

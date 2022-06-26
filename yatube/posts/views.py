from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest


POSTS_LIMIT: int = 10


def index(request: HttpResponse) -> HttpRequest:
    """
    Извлекает из URL номер страницы с постами. Передаёт в шаблон
    posts/index.html набор записей для запрошенной страницы.
    """
    template = 'posts/index.html'

    posts = Post.objects.select_related('author')
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Передаёт в шаблон posts/group_list.html десять последних объектов модели
    Post, отфильтрованных по полю group, и содержимое для тега <title>.
    """
    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'slug': slug,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)

from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.http import HttpResponse, HttpRequest


def index(request: HttpResponse) -> HttpRequest:
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'slug': slug,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)

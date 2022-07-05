from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import PostForm


POSTS_LIMIT: int = 10


def index(request):
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


def profile(request, username):

    template = 'posts/profile.html'

    author = get_object_or_404(User, username=username)

    posts = author.posts.all()
    posts_count = posts.count()
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'username': username,
        'posts_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):

    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()

    context = {
        'post_id': post_id,
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, template, context)


def post_create(request):

    template = 'posts/post_create.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)

        context = {
            'form': form,
        }
        return render(request, template, context)

    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, template, context)


def post_edit(request, post_id):

    template = 'posts/post_create.html'

    post = get_object_or_404(Post, pk=post_id)
    context = {
        'is_edit': True,
        'post': post
    }
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)

        context['form'] = form
        return render(request, template, context)

    form = PostForm()
    context['form'] = form
    return render(request, template, context)

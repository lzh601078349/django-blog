import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown

# 首页文章列表视图


def index(request):
    post_list = Post.objects.all()
    return render(request, "blog/index.html", context={
        # "title": "钊华的601小屋首页",
        # "welcome": "欢迎访问我的小屋首页",
        "post_list": post_list
    })


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.body = markdown.markdown(post.body, extensions=[
#         # extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，
#         # 这为后面的实现代码高亮功能提供基础，而 toc 则允许自动生成目录
#         "markdown.extensions.extra", "markdown.extensions.codehilite", "markdown.extensions.toc"
#     ])

#     return render(request, "blog/detail.html", context={
#         # "title": "钊华的601小屋首页",
#         # "welcome": "欢迎访问我的小屋首页",
#         "post": post
#     })

# 点击进入文章后文章详细视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    # print(post.body)
    # 这里可以上百度多查查用法
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})

# 点击边栏时间后，进入当前时间下所属文章页面列表


def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month)
    return render(request, "blog/index.html", context={
        "post_list": post_list
    })

# 点击边栏文章分类后，进入当前分类下所属文章页面列表


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, "blog/index.html", context={
        "post_list": post_list
    })

# 点击边栏文章标签后，进入当前标签下所属文章页面列表


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, "blog/index.html", context={
        "post_list": post_list
    })
# Create your views here.
# print(__name__)

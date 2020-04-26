import re

import markdown
import requests
from beem import Hive
from beem.account import Account
from beem.comment import Comment
from beem.discussions import (Discussions_by_blog, Discussions_by_created,
                              Discussions_by_hot, Discussions_by_trending,
                              Query)
from beem.instance import set_shared_blockchain_instance
from beem.utils import construct_authorperm
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import cache_page
from markupsafe import Markup

#nodes = ["https://api.hive.blog", "https://anyx.io"]
q = Query(limit=10)
hv = Hive()  # node=nodes)
set_shared_blockchain_instance(hv)
image_proxy = "https://images.hive.blog/640x0/"

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def strip(text):
    text['body'] = re.sub(r"(^https?:[^)''\"]+\.(?:jpg|jpeg|gif|png))", rf'![](\1) >', text['body'])
    text['body'] = markdown.markdown(text['body'], extensions=[
                                     'nl2br', 'codehilite', 'pymdownx.extra', 'pymdownx.magiclink', 'pymdownx.betterem', 'pymdownx.inlinehilite'])
    #text['body'] = re.sub("(<h1>|<h2>)", "<h3>", text['body'])
    text['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                          rf'<img src={image_proxy}\1 >', text['body'])
    text['body'] = Markup(text['body'])
    return text

@cache_page(CACHE_TTL)
def trending(request):
    posts = Discussions_by_trending(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

@cache_page(CACHE_TTL)
def hot(request):
    posts = Discussions_by_hot(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

@cache_page(CACHE_TTL)
def latest(request):
    posts = Discussions_by_created(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

@cache_page(CACHE_TTL)
def tag(request, tag):
    tag_q = Query(limit=10, tag=tag)
    posts = Discussions_by_trending(tag_q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {"posts": posts})

@cache_page(CACHE_TTL)
def blog_posts(request, author):
    author = re.sub(r'(\/)', '', author)
    account = Account(author)
    posts = account.get_blog(limit=10)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

@cache_page(CACHE_TTL)
def post_detail(request, author, permlink, **args):
    author_perm = construct_authorperm(author, permlink)
    post = Comment(author_perm)
    if post:
        replies = post.get_all_replies()
        post = strip(post)
        for reply in replies:
            reply = strip(reply)
    return render(request, 'blog/post_detail.html', {'post': post, 'replies': replies})

@cache_page(CACHE_TTL)
def followers(request, author):
    account = Account(author)
    followers = account.get_followers(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})

@cache_page(CACHE_TTL)
def following(request, author):
    account = Account(author)
    followers = account.get_following(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})

@cache_page(CACHE_TTL)
def request_author(request, *args, **kwargs):
    if(request.GET.get('req_author')):
        author = str(request.GET.get('author'))
    else:
        if 'author' in kwargs:
            author = kwargs['author']
    account = Account(author)
    return render(request, 'blog/account.html', {'account': account})


def market(request):
    return render(request, 'blog/market.html')


def post_new(request):
    """    if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', permlink=post.permlink)
        else:
            form = PostForm()"""
    return render(request, 'blog/post_edit.html', {'form': ""})


def post_edit(request, author, permlink):
    """
        author_perm = construct_authorperm(author, permlink)
        post = Comment(author_perm, steem_instance=steem)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', permlink=post.permlink)
        else:
            form = PostForm(instance=post)
    """
    return render(request, 'blog/post_edit.html', {'form': ""})

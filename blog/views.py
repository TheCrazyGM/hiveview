import re

import markdown
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from beem import Hive
from beem.nodelist import NodeList
from beem.account import Account
from beem.comment import Comment
from beem.discussions import Query
from beem.discussions import Discussions
from beem.instance import set_shared_blockchain_instance
from beem.utils import construct_authorperm
from markupsafe import Markup

nodelist = NodeList()
nodelist.update_nodes()
#nodes = ["https://api.hive.blog", "https://anyx.io"]
q = Query(limit=10)

hv = Hive(node=nodelist.get_hive_nodes())
set_shared_blockchain_instance(hv)
d = Discussions(blockchain_instance=hv)
image_proxy = "https://images.hive.blog/480x0/"


def strip(text):
    text['body'] = markdown.markdown(text['body'], extensions=[
                                     'nl2br', 'codehilite', 'pymdownx.extra', 'pymdownx.magiclink', 'pymdownx.betterem', 'pymdownx.inlinehilite', 'pymdownx.snippets',
                                     'pymdownx.striphtml'])
    text['body'] = re.sub("(<h1>|<h2>)", "<h3>", text['body'])
    text['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                          rf'<img src={image_proxy}\1 >', text['body'])
    text['body'] = Markup(text['body'])
    return text


def trending(request):
    posts = []
    for post in d.get_discussions("trending", q, limit=10, raw_data=True):
        if post:
            post = strip(post)
            posts.append(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def hot(request):
    posts = []
    for post in d.get_discussions("hot", q, limit=10, raw_data=True):
        if post:
            post = strip(post)
            posts.append(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def latest(request):
    posts = []
    for post in d.get_discussions("created", q, limit=10, raw_data=True):
        if post:
            post = strip(post)
            posts.append(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def tag(request, tag):
    tag_q = Query(limit=10, tag=tag)
    posts = []
    for post in d.get_discussions("trending", tag_q, limit=10, raw_data=True):
        if post:
            post = strip(post)
            posts.append(post)
    return render(request, 'blog/post_list.html', {"posts": posts})


def blog_posts(request, author):
    author = re.sub(r'(\/)', '', author)
    account = Account(author, blockchain_instance=hv)
    posts = account.get_blog()
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, author, permlink, **args):
    author_perm = construct_authorperm(author, permlink)
    post = Comment(author_perm, blockchain_instance=hv)
    if post:
        replies = post.get_replies(raw_data=True)
        post = strip(post)
        for reply in replies:
            reply = strip(reply)
    return render(request, 'blog/post_detail.html', {'post': post, 'replies': replies})


def followers(request, author):
    account = Account(author, blockchain_instance=hv)
    followers = account.get_followers(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})


def following(request, author):
    account = Account(author, blockchain_instance=hv)
    followers = account.get_following(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})


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
        post = Comment(author_perm, blockchain_instance=steem)
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

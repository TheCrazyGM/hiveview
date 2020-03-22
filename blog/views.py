import re

import markdown
import requests
from bhive import Hive
from bhive.account import Account
from bhive.comment import Comment
from bhive.discussions import Query
from bhive.instance import set_shared_hive_instance
from bhive.utils import construct_authorperm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from html_sanitizer import Sanitizer
from hive import Hive as Hivepy

#nodes = ["https://api.hive.blog", "https://anyx.io"]
q = Query(limit=10)
hvpy = Hivepy()#nodes=nodes)
hv = Hive()#node=nodes)
set_shared_hive_instance(hv)
options = {
    "tags": {
        "a", "h1", "h2", "h3", "strong", "em", "p", "ul", "ol",
        "li", "br", "sub", "sup", "hr", "img"
    },
    "attributes": {"a": ("href", "name", "target", "title", "id", "rel"), 'img': ('src', )},
    "empty": {"hr", "a", "br", "img"},
    "separate": {"a", "p", "li"},
    "whitespace": {"br"},
    "keep_typographic_whitespace": False,
    "add_nofollow": False,
    "autolink": True,
    "is_mergeable": lambda e1, e2: True,
}
sanitizer = Sanitizer(settings=options)
image_proxy = "https://images.hive.blog/640x0/"


def strip(text):
    text['body'] = markdown.markdown(text['body'])
    text['body'] = sanitizer.sanitize(text['body'])
    #x['body'] = re.sub("(<h1>|<h2>)", "<h3>", x['body'])
    text['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                          rf'<img src={image_proxy}\1 >', text['body'])
    return text


def trending(request):
    posts = hvpy.get_discussions_by_trending(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def hot(request):
    posts = hvpy.get_discussions_by_hot(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

def latest(request):
    posts = hvpy.get_discussions_by_created(q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})

def tag(request, tag):
    tag_q = Query(limit=10, tag=tag)
    posts = hvpy.get_discussions_by_trending(tag_q)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {"posts": posts})

def blog_posts(request, author):
    author = re.sub(r'(\/)', '', author)
    account = Account(author, hive_instance=hv)
    posts = account.get_blog()
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, author, permlink, **args):
    author_perm = construct_authorperm(author, permlink)
    post = Comment(author_perm, hive_instance=hv)
    if post:
        replies = hvpy.get_content_replies(author, permlink)
        post = strip(post)
        for reply in replies:
            reply = strip(reply)
    return render(request, 'blog/post_detail.html', {'post': post, 'replies': replies})


def followers(request, author):
    account = Account(author, hive_instance=hv)
    followers = account.get_followers(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})


def following(request, author):
    account = Account(author, hive_instance=hv)
    followers = account.get_following(raw_name_list=True, limit=100)
    return render(request, 'blog/follower.html', {'followers': followers})

def request_author(request):
  if(request.GET.get('req_author')):
    author =str(request.GET.get('author'))
    account = Account(author)
    return render(request, 'blog/account.html', {'account': account})


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

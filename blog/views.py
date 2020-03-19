import re

import markdown
import requests
from beem import Steem
from beem.account import Account
from beem.comment import Comment
from beem.discussions import Query
from beem.utils import construct_authorperm
from beemapi.steemnoderpc import SteemNodeRPC
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from html_sanitizer import Sanitizer
from steem import Steem as Steempy

nodes = ["https://api.steemit.com", "https://anyx.io"]
q = Query(limit=10)
stm = Steempy(nodes=nodes)
steem = Steem(node=nodes)
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
image_proxy = "https://steemitimages.com/640x0/"


def strip(text):
    text['body'] = markdown.markdown(text['body'])
    text['body'] = sanitizer.sanitize(text['body'])
    #x['body'] = re.sub("(<h1>|<h2>)", "<h3>", x['body'])
    text['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                          rf'<img src={image_proxy}\1 >', text['body'])
    return text


def trending(request):
    posts = stm.get_discussions_by_trending(q)
    return render(request, 'blog/post_list.html', {'posts': posts})


def hot(request):
    posts = stm.get_discussions_by_hot(q)
    return render(request, 'blog/post_list.html', {'posts': posts})


def promoted(request):
    posts = stm.get_discussions_by_promoted(q)
    return render(request, 'blog/post_list.html', {'posts': posts})


def latest(request):
    posts = stm.get_discussions_by_created(q)
    return render(request, 'blog/post_list.html', {'posts': posts})

def tag(request, tag):
    tag_q = Query(limit=10, tag=tag)
    posts = stm.get_discussions_by_trending(tag_q)
    return render(request, 'blog/post_list.html', {"posts": posts})

def blog_posts(request, author):
    author = re.sub(r'\/', '', author)
    account = Account(author, steem_instance=steem)
    posts = account.get_blog(start_entry_id=0, limit=10)
    for post in posts:
        if post:
            post = strip(post)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, author, permlink, **args):
    author_perm = construct_authorperm(author, permlink)
    post = Comment(author_perm, steem_instance=steem)
    if post:
        replies = stm.get_content_replies(author, permlink)
        post = strip(post)
        for reply in replies:
            reply = strip(reply)
    return render(request, 'blog/post_detail.html', {'post': post, 'replies': replies})


def followers(request, author):
    account = Account(author, steem_instance=steem)
    followers = account.get_followers(raw_name_list=True, limit=100)
    return render(request, 'blog/userlist.html', {'followers': followers})


def following(request, author):
    account = Account(author, steem_instance=steem)
    followers = account.get_following(raw_name_list=True, limit=100)
    return render(request, 'blog/userlist.html', {'followers': followers})


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

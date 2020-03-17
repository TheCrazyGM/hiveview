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


def blog_posts(request, author):
    account = Account(author, steem_instance=steem)
    posts = account.get_blog(start_entry_id=0, limit=10)
    for x in posts:
        x['body'] = markdown.markdown(x['body'])
        x['body'] = sanitizer.sanitize(x['body'])
        x['body'] = re.sub("(<h1>|<h2>)", "<h3>", x['body'])
        x['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                           r'<img src=https://steemitimages.com/640x0/\1 >', x['body'])

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, author, pk,):
    author_perm = construct_authorperm(author, pk)
    post = Comment(author_perm, steem_instance=steem)
    replies = stm.get_content_replies(author, pk)
    post['body'] = markdown.markdown(post.body)
    post['body'] = sanitizer.sanitize(post['body'])
    post['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                          r'<img src=https://steemitimages.com/640x0/\1 >', post['body'])

    for x in replies:
        x['body'] = markdown.markdown(x['body'])
        x['body'] = sanitizer.sanitize(x['body'])
        x['body'] = re.sub("(<h1>|<h2>)", "<h3>", x['body'])
        x['body'] = re.sub(r"<img\b(?=\s)(?=(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*?\ssrc=['\"]([^\"]*)['\"]?)(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"\s]*)*\"\s?\/?>",
                           r'<img src=https://steemitimages.com/640x0/\1 >', x['body'])


    #post = Comment(pk).permlink
    return render(request, 'blog/post_detail.html', {'post': post, 'replies': replies})


def post_detail_url(request, tag, author, pk,):
    tags = tag
    author_perm = construct_authorperm(author, pk)
    post = Comment(author_perm, steem_instance=steem)
    post['body'] = markdown.markdown(post.body)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    """    if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()"""
    return render(request, 'blog/post_edit.html', {'form': ""})


def post_edit(request, author, pk):
    """
        author_perm = construct_authorperm(author, pk)
        post = Comment(author_perm, steem_instance=steem)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
    """
    return render(request, 'blog/post_edit.html', {'form': ""})

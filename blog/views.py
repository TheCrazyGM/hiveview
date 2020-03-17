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
from steem import Steem as Steempy

q = Query(limit=10)
stm = Steempy()
steem = Steem(node="https://api.steemit.com")


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
    posts = account.get_blog(start_entry_id=0, limit=10, short_entries=True)
    for x in posts:
        x['body'] = markdown.markdown(x['body'])
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, author, pk,):
    author_perm = construct_authorperm(author, pk)
    post = Comment(author_perm, steem_instance=steem)
    replies = stm.get_content_replies(author, pk)
    post['body'] = markdown.markdown(post.body)
    for x in replies:
        x['body'] = markdown.markdown(x['body'])
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

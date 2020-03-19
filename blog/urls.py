from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.trending, name='home'),
    path('trending/', views.trending, name='trending'),
    path('hot/', views.hot, name='hot'),
    path('latest/', views.latest, name='latest'),
    path('request_account/', views.request_author, name='account'),
    re_path(r'^@(?P<author>[^~,]+)\/followers/?$',
            views.followers, name='followers'),
    re_path(r'^@(?P<author>[^~,]+)\/following/?$',
            views.following, name='following'),
    re_path(r'^@(?P<author>[^~,]+)\/(?P<permlink>[^~,]+/?$)',
            views.post_detail, name='post_detail'),
    re_path(r'^@(?P<author>[^~,]+/?$)', views.blog_posts, name='blog_posts'),
    re_path(r'^(?P<tag>[^~,]+)\/\@(?P<author>[^~,]+)/(?P<permlink>[^~,]+/?$)',
            views.post_detail, name='post_detail'),
    #    path('post/new/', views.post_new, name='post_new'),
    #path('@<slug:author>/<slug:permlink>/edit/',
    #     views.post_edit, name='post_edit'),
    re_path(r'^(?P<tag>[^~,]+/?$)', views.tag, name='tag'),

]

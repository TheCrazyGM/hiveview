from django.urls import path
from . import views

urlpatterns = [
    path('', views.trending, name='trending'),
    path('trending', views.trending, name='trending'),
    path('hot', views.hot, name='hot'),
    path('promoted', views.promoted, name='promoted'),
    path('latest', views.latest, name='latest'),
    path('@<slug:author>', views.blog_posts, name='blog_posts'),
    path('@<slug:author>/<slug:pk>', views.post_detail, name='post_detail'),
    path('<slug:tag>/@<slug:author>/<slug:pk>', views.post_detail_url, name='post_detail_url'),
    path('post/new/', views.post_new, name='post_new'),
    path('@<slug:author>/<slug:pk>/edit/', views.post_edit, name='post_edit'),

]

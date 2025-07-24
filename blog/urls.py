from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('arama/', views.search_view, name='search_view'),
    path('kategori/<slug:category_slug>/', views.PostListView.as_view(), name='category_posts'),
    path('yazar/<str:username>/', views.AuthorPostListView.as_view(), name='author_posts'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

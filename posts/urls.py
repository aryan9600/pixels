from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
	path('create/', views.create_post, name='create'),
	path('detail/<int:id>/<slug:slug>/', views.post_detail_view, name='detail'),
	path('like/', views.like_post, name='like'),
	path('list/', views.posts_list, name='list'),
]
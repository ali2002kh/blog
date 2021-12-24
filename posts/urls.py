from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<int:post_id>', views.post_detail ,name='detail'),
    path('create/', views.post_create, name='create'),
]

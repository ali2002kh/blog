from django.urls import path
from . import views


app_name = 'management'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:post_id>/edit', views.edit, name='edit'),
    path('<int:post_id>/delete', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/comments/', views.comments, name='comments'),
    path('<int:comment_id>/confirm', views.confirm, name='confirm'),
    path('<int:comment_id>/reject', views.reject, name='reject'),
]
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'management'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:pk>/edit', login_required(views.edit.as_view()), name='edit'),
    path('<int:post_id>/delete', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/comments/', views.comments, name='comments'),
    path('<int:comment_id>/confirm', views.confirm, name='confirm'),
    path('<int:comment_id>/reject', views.reject, name='reject'),
]
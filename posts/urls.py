from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<int:post_id>', views.post_detail ,name='detail'),
    path('<int:post_id>/addComment', views.addComment ,name='addComment'),
    path('<int:comment_id>/replyComment', views.replyComment ,name='replyComment'),
]

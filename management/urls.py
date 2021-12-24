from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:post_id>/edit', views.edit ,name='edit'),
    path('<int:post_id>/delete', views.delete ,name='delete'),
    path('create/', views.create, name='create'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall),
    path('/add_message', views.post_msg),
    path('/add_comment', views.post_cmt),
    path('/destroy_message', views.destroy_msg),
    path('/destroy_comment', views.destroy_cmt),
]

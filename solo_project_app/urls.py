from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('register_process', views.register_process),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('post_process', views.post_process),
    path('like/<int:id>', views.like),
    path('unlike/<int:id>', views.unlike),
    path('view_post/<int:id>', views.post),
    path('comment_process', views.comment_process),
    path('profile', views.profile),
    path('favorite_post/<int:id>', views.favorite_post),
    path('confirm_edit', views.confirm_edit),
    path('edit_auth', views.edit_auth),
    path('edit_profile', views.edit_profile),
    path('edit_process', views.edit_process),
    path('profile_ml', views.profile_ml),
    path('profile_faves', views.profile_faves),
    path('confirm_delete/<int:id>', views.confirm_delete),
    path('like_prof/<int:id>', views.like_prof),
    path('unlike_prof/<int:id>', views.unlike_prof),
    path('like_post/<int:id>', views.like_post),
    path('unlike_post/<int:id>', views.unlike_post),
    path('confirm_delete_prof/<int:id>', views.confirm_delete_prof),
    path('delete/<int:id>', views.delete),
    path('delete_prof/<int:id>', views.delete_prof)
]
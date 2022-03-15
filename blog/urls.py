from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:post_id>/', views.detail, name = 'detail'),
    path('login/', views.login_user, name = 'login'),
    path('signup/', views.signup_user, name = 'signup'),
    path('logout/', views.logout_user, name = 'logout'),
    path('contact/', views.contact_view, name = 'contact'),
    path('<int:post_id>/<int:comment_id>/edit_comment/', views.edit_comment, name = 'edit_comment'),
    path('<int:post_id>/<int:comment_id>/update_comment/', views.update_comment, name = 'update_comment'),
    path('<int:post_id>/<int:comment_id>/delete_comment/', views.delete_comment, name = 'delete_comment'),
    path('<int:post_id>/post_comment/', views.post_comment, name = 'post_comment'),
]

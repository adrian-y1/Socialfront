
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('post/<int:post_id>', views.single_post_view, name='post'),
    path('profile/<int:user_id>/followings', views.followings_page, name='followings_page'),
    path('profile/<int:user_id>/followers', views.followers_page, name='followers_page'),
    path('suggestions', views.suggestions, name='suggestions'),


    # APIs
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('edit/<int:post_id>', views.editPost, name='edit'),
    path('like/<int:post_id>', views.likePost, name="like"),
    path('comment/like/<int:comment_id>', views.likeComment, name="like-comment"),
    path('search_followings/<int:user_id>', views.followings_page_api, name='followings_page_api'),
    path('search_followers/<int:user_id>', views.followers_page_api, name='followers_page_api'),
    path('suggestions_api', views.suggestions_api, name='suggestions_api'),
    
    # Authentication
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='net/password_reset.html'), name="reset_password"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='net/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='net/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='net/password_reset_complete.html'), name="password_reset_complete"),

    # Error
    path('error', views.error_handling, name="error")

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
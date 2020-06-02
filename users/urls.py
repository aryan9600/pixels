from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),

        path('change_password/',
             auth_views.PasswordChangeView.as_view(template_name="users/password_change.html"),
             name='password-change'),
        path('change_password_done/',
             auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
             name='password-change-done'),

        path('password_reset/',
             auth_views.PasswordResetView.as_view(
                   email_template_name="users/password_reset_email.html", template_name="users/password_reset.html"),
             name='password_reset'),
        path('password_reset/done/',
             auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_email_sent.html"),
             name='password_reset_done'),
        path('reset/<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
             name='password_reset_confirm'),
        path('reset/done/',
             auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
             name='password_reset_complete'),

        path('', views.dashboard, name='dashboard'),
        path('users/', views.user_list, name='user_list'),
        path('users/<username>/', views.user_detail, name='user_detail'),
        path('users/follow/', views.user_follow, name='user_follow'),
]

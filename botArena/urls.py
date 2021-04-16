from django.urls import path, reverse, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'botArena'
urlpatterns = [
    # ex: /botArena/
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='botArena/login.html', get_success_url=lambda: reverse('botArena:home', args=())), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('game/<str:name>', views.game, name='game'),
    path('new_game/', views.creating_game_view, name='new_game'),
    path('game/<str:name>/new_bot', views.creating_bot_view, name='new_bot'),
    path('game/<str:game_name>/bot/<str:creator_name>_<int:id>', views.bot_view, name='bot'),
    path('game/<str:game_name>/<int:bot_id>', views.playground_bot, name='playground'),
    path('sign-s3/', views.sign_s3, name='s3-sign'),
    path('about/', views.about_view, name='about'),
    path('game/<str:game_name>/play', views.playing_game_view, name='play_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='botArena/password_reset.html', email_template_name='botArena/email_template.html',
        success_url=reverse_lazy('botArena:password_reset_done')), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='botArena/password_reset_confirm.html', success_url=
        reverse_lazy('botArena:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='botArena/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='botArena/password_reset_complete.html'), name='password_reset_complete'),

]

# password_reset_confirm

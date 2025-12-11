from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  # <-- ajout du dashboard
    path('books/', views.books_list, name='books_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrow/history/', views.borrow_history, name='borrow_history'),
    path('profile/', views.profile_view, name='profile'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('signup/', views.signup_view, name='signup'),

       # ... tes autres urls
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    


    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

   ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
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

   ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Loan, Quiz, Question, Choice, QuizAttempt, Profile, Category
from .forms import SignUpForm, BorrowForm
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required



@never_cache
@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    loans = Loan.objects.filter(user=request.user)
    all_books = Book.objects.all()  # <-- récupérer tous les livres

    monthly_loans = [0, 2, 1, 3, 0, 2]
    monthly_quiz = [1, 0, 2, 1, 1, 0]

    context = {
        'profile': profile,
        'loans': loans,
        'all_books': all_books,  # <-- ajouter dans le contexte
        'monthly_loans': mark_safe(json.dumps(monthly_loans)),
        'monthly_quiz': mark_safe(json.dumps(monthly_quiz)),
    }
    return render(request, 'core/dashboard.html', context)

def home(request):
    latest_books = Book.objects.all()[:6]
    return render(request, 'core/home.html', {'latest_books': latest_books})


def books_list(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')  # récupérer la catégorie filtrée

    books = Book.objects.all()

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__icontains=q)

    if category_id:
        books = books.filter(category_id=category_id)

    # Récupérer toutes les catégories créées
    categories = Category.objects.all()

    context = {
        'books': books,
        'q': q,
        'categories': categories,
        'selected_category': category_id,  # pour mettre le filtre actif en surbrillance
    }
    return render(request, 'core/books_list.html', context)



def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    can_borrow = True
    if request.user.is_authenticated:
        # Vérifie si l'utilisateur a déjà emprunté ce livre et que l'emprunt n'est pas expiré
        active_loan = book.loan_set.filter(
            user=request.user,
            returned=False,
            due_date__gte=timezone.now()
        ).exists()
        if active_loan:
            can_borrow = False

    return render(request, 'core/book_detail.html', {
        'book': book,
        'can_borrow': can_borrow,
    })


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.available_copies <= 0:
        messages.error(request, "Aucune copie disponible pour le moment.")
        return redirect('core:book_detail', pk=pk)

    Loan.objects.create(
        user=request.user,
        book=book,
        due_date=timezone.now() + timezone.timedelta(seconds=20)  # 20 secondes pour le test
    )

    messages.success(
        request,
        f"Vous avez emprunté '{book.title}' pour 20 secondes."
    )
    return redirect('core:books_list')

@never_cache
@never_cache
@login_required
def borrow_history(request):
    now = timezone.now()
    loans = Loan.objects.filter(user=request.user).order_by('-borrowed_at')

    # Met à jour automatiquement les prêts dépassés
    for loan in loans:
        if not loan.returned and loan.due_date and loan.due_date <= now:
            loan.returned = True
            loan.returned_at = now
            loan.status = "retourné"
            loan.save()

    return render(request, 'core/borrow_history.html', {
        'loans': loans,
        'now': now
    })


@never_cache
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html', {'profile': profile})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            # Ne pas loguer automatiquement
            messages.success(request, 'Compte créé ! Vous pouvez maintenant vous connecter.')
            return redirect('login')  # redirige vers la page de connexion
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


# ---------------- QUIZ VIEWS ---------------- #

def quiz_list(request):
    quizzes = Quiz.objects.all()  # On récupère tous les quiz
    show_login_alert = not request.user.is_authenticated  # Affiche l'alerte si pas connecté
    return render(request, 'core/quiz_list.html', {
        'quizzes': quizzes,
        'show_login_alert': show_login_alert
    })


@never_cache
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    previous_attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz
    ).order_by('-taken_at').first()

    already_passed = False
    if previous_attempt:
        total_questions = quiz.questions.count()
        if total_questions > 0 and previous_attempt.score >= total_questions / 2:
            already_passed = True

    if request.method == 'POST':
        score = 0

        for question in quiz.questions.all():
            selected = request.POST.get(str(question.id))
            if selected:
                try:
                    choice = Choice.objects.get(id=int(selected))
                    if choice.correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass

        profile, _ = Profile.objects.get_or_create(user=request.user)

        # Si pas encore réussi → enregistrer score
        if not previous_attempt or (previous_attempt.score < quiz.questions.count() / 2):
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score
            )

            profile.points += score * 10

            # Gestion des badges par niveaux
            if profile.points >= 100 and "Expert Reader" not in profile.badges:
                profile.badges.append("Expert Reader")
            elif profile.points >= 50 and "Lecteur Confirmé" not in profile.badges:
                profile.badges.append("Lecteur Confirmé")
            elif profile.points < 50 and "Débutant Lecteur" not in profile.badges:
                profile.badges.append("Débutant Lecteur")

            profile.save()
            messages.success(request, f"Quiz terminé — score : {score}")

        else:
            messages.info(
                request,
                f"Vous avez déjà réussi ce quiz. Vous pouvez le refaire, mais le score ne sera pas enregistré. Score actuel : {score}"
            )

        return redirect('core:profile')

    return render(request, 'core/take_quiz.html', {
        'quiz': quiz,
        'already_passed': already_passed
    })


# ---------------- CHATBOT VIEW ---------------- #

def chatbot_view(request):
    return render(request, 'core/chatbot.html')
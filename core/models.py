from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    copies = models.PositiveIntegerField(default=1)
    cover = models.URLField(blank=True)
    image = models.ImageField(upload_to='covers/', blank=True, null=True)


    @property
    def available_copies(self):
        """Retourne le nombre de copies disponibles"""
        borrowed = Loan.objects.filter(book=self, returned=False).count()
        return max(0, self.copies - borrowed)

    @property
    def is_available(self):
        return self.available_copies() > 0

    def __str__(self):
        return f"{self.title} — {self.author}"


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=30,
        default="en cours",  # "en cours", "en train de retourner", "retourné"
    )

    def mark_returned(self):
        """Marquer le prêt comme retourné"""
        if not self.returned:
            self.returned = True
            self.status = "retourné"
            self.returned_at = timezone.now()
            self.save()
            # NE PAS toucher à book.copies ! 
            # available_copies() gère dynamiquement le stock

    def __str__(self):
        return f"Loan({self.user.username}, {self.book.title}, status={self.status})"

# ------- QUIZ SYSTEM -------- #

class Quiz(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz({self.title})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f"Question({self.text[:50]})"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice({self.text[:30]}{'✔' if self.correct else ''})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt({self.user.username} - {self.quiz.title} = {self.score})"

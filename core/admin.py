from django.contrib import admin
from .models import Profile, Category, Book, Loan, Quiz, Question, Choice, QuizAttempt


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author' , 'category', 'copies')
    list_filter = ('category',)
    search_fields = ('title', 'author', 'isbn')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned')


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(QuizAttempt)

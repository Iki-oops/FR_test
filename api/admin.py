from django.contrib import admin

from .models import Question, Poll, PollQuestion, Answer, UserAnswer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')


@admin.register(PollQuestion)
class PollQuestionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'question')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'type')
    search_fields = ('text', 'type')
    list_filter = ('type',)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_date', 'end_date', 'description')
    search_fields = ('name',)

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    TYPES = (
        ('text', 'Ответ текстом'),
        ('one', 'Выбор одного варианта'),
        ('several', 'Выбор нескольких вариантов'),
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст вопроса'
    )
    type = models.CharField(
        max_length=20,
        verbose_name='Тип вопроса',
        choices=TYPES,
        default='text'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'


class Poll(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    start_date = models.DateTimeField(verbose_name='Дата старта')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')
    questions = models.ManyToManyField(Question, through='PollQuestion')

    def __str__(self):
        if len(self.name) > 50:
            return f"{self.name[:50]}..."
        return self.name

    class Meta:
        verbose_name_plural = 'Опросы'
        verbose_name = 'Опрос'


class PollQuestion(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions_in',
        verbose_name='Опрос'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='questions_in',
        verbose_name='Вопрос'
    )

    def __str__(self):
        return f"{self.poll.name} - {self.question.text}"

    class Meta:
        verbose_name_plural = 'Вопросы к опросам'
        verbose_name = 'Вопрос к опросу'
        constraints = [
            models.UniqueConstraint(
                fields=['poll', 'question'],
                name='unique_poll_question',
            )
        ]


class Answer(models.Model):
    question = models.ForeignKey(
        PollQuestion,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )
    answer = models.CharField(
        max_length=200,
        verbose_name='Ответ',
    )

    def __str__(self):
        return f"{self.question} - {self.answer}"

    class Meta:
        verbose_name_plural = 'Ответы на вопросы'
        verbose_name = 'Ответ на вопрос'
        constraints = [
            models.UniqueConstraint(
                fields=('question', 'answer'),
                name='unique_question_answer',
            )
        ]


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='Ответ пользователя'
    )

    class Meta:
        verbose_name_plural = 'Ответы на вопросы от пользователя'
        verbose_name = 'Ответ от пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'answer'),
                name='unique_user_answer',
            )
        ]

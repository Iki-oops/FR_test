from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import IntegrityError

from .models import Answer, Poll, PollQuestion, Question, User, UserAnswer
from .serializers import (
    PollSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserAnswerSerializer
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        poll = get_object_or_404(Poll, id=self.kwargs.get('poll_id'))
        queryset = Question.objects.filter(questions_in__poll=poll)
        return queryset

    def perform_create(self, serializer):
        serializer.save()
        poll = get_object_or_404(Poll, id=self.kwargs.get('poll_id'))
        question = Question.objects.get(pk=serializer.data['pk'])
        PollQuestion.objects.create(poll=poll, question=question)
        return serializer

    @action(methods=['POST'], detail=True)
    def answer(self, request, poll_id, pk):
        question = get_object_or_404(Question, id=pk)
        pollquestion = get_object_or_404(
            PollQuestion,
            question=question,
            poll=get_object_or_404(Poll, id=poll_id),
        )
        answers = request.data.get('answer')
        result = []
        if isinstance(answers, str):
            answers = [answers,]
        for answer in answers:
            try:
                answer, is_created = Answer.objects.get_or_create(
                    question=pollquestion,
                    answer=answer,
                )
                result.append(answer)
                # После того как переделаю user доделать ЭТО
                # UserAnswer.objects.create(user=request.user, answer=answer)
            except IntegrityError:
                return Response(
                    data={'message': 'Необходимо поле answer'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = AnswerSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(
        #     data={'message': 'Такой ответ от вас уже существует'},
        #     status=status.HTTP_400_BAD_REQUEST
        # )


class AnswersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAnswerSerializer

    # Переделать user
    def get_queryset(self):
        user = User.objects.get(id=1)
        # user = self.request.user
        answers = user.answers.all()
        return answers

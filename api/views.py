from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.utils import IntegrityError

from api_user_poll.settings import USER_ID
from .models import Answer, Poll, PollQuestion, Question, UserAnswer
from .permissions import AnonWithCookie, AnonymousPermission
from .serializers import (
    LoginSerializer,
    PollSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserAnswerSerializer
)


@api_view(['GET'])
def start_polling(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    request.session.set_test_cookie()
    request.session['user_id'] = next(USER_ID)
    print(request.session['user_id'])
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AnonWithCookie,])
def delete_test_cookie(request):
    request.session.delete_test_cookie()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AnonWithCookie,])
def get_answers(request):
    user_id = request.session['user_id']
    user_answers = UserAnswer.objects.filter(user=user_id)
    serializer = UserAnswerSerializer(user_answers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_auth = authenticate(
        username=serializer.data['username'],
        password=serializer.data['password']
    )
    if user_auth:
        token, is_created = Token.objects.get_or_create(user=user_auth)
        return Response({'token': token.key})
    return Response({'message': 'Неправильный username или password'})


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (AnonymousPermission,)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (AnonymousPermission,)

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

    @action(methods=['GET'], detail=True, permission_classes=[AnonWithCookie])
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
                user_id = request.session['user_id']
                UserAnswer.objects.create(user=user_id, answer=answer)
            except IntegrityError:
                return Response(
                    data={'message': 'Необходимо поле answer'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = AnswerSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

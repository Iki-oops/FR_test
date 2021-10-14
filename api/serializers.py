from rest_framework import serializers

from .models import Answer, Poll, PollQuestion, Question, User, UserAnswer


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ('pk', 'text', 'type',)


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('name', 'start_date', 'end_date', 'description', 'questions')

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        poll, status = Poll.objects.get_or_create(**validated_data)
        for question in questions:
            current_question, status = Question.objects.get_or_create(**question)
            PollQuestion.objects.create(poll=poll, question=current_question)
        return poll

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        questions = validated_data.get('questions')
        if questions:
            questions = [
                Question.objects.get_or_create(**question)[0]
                for question in questions
            ]
            instance.questions.set(questions)
        return instance


class ShortPollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('name', 'description')


class AnswerSerializer(serializers.ModelSerializer):
    poll = ShortPollSerializer(read_only=True, source='question.poll')
    question = QuestionSerializer(read_only=True, source='question.question')

    class Meta:
        model = Answer
        fields = ('poll', 'question', 'answer')

    def create(self, validated_data):
        question = validated_data.pop('question')
        poll = validated_data.pop('poll')
        pollquestion = PollQuestion.objects.create(question=question, poll=poll)
        answer = Answer.objects.create(
            question=pollquestion, answer=validated_data.pop('answer')
        )
        return answer


class UserAnswerSerializer(serializers.ModelSerializer):
    poll = ShortPollSerializer(source='answer.question.poll')
    question = QuestionSerializer(source='answer.question.question')
    answer = serializers.CharField(source='answer.answer')

    class Meta:
        model = UserAnswer
        fields = ('pk', 'poll', 'question', 'answer')

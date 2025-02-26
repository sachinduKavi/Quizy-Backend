from rest_framework import serializers
from .models import User, Quiz, Question, Answers, Submission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'


class SubmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
from json.decoder import JSONArray
from logging import exception

from django.forms import Form
from django.shortcuts import render, get_object_or_404
from django.utils.regex_helper import Choice
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .middleware import encrypt, decrypt

from .models import User, Quiz, Question, Answers
from .serializers import UserSerializer, QuizSerializer, QuestionSerializers

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    # def create(self, request, *args, **kwargs):
    #     print('running this post function...')
    #     return Response({
    #         'proceed': True,
    #         'content': None,
    #         'message': None
    #     })


    @action(detail=False, methods=['post'], url_path='authorize')
    def authorize(self, request, *args, **kwargs):
        proceed = False
        encrypt_id = "0"

        try:
            db_user = User.objects.filter(username=request.data['username'])[0]
            proceed = db_user.password == request.data['password']
            message = "Authorized" if proceed else 'Invalid credentials'
            encrypt_id = encrypt(str(db_user.id)) if proceed else "0"
            print(encrypt_id)

        except Exception as e:
            print('exception occured', e)
            message = 'Invalid credentials'

        response = Response({
            'proceed': proceed,
            'content': db_user.extract_json() if proceed else None,
            'message': message
        })
        response.set_cookie(key='quiz_token', value=encrypt_id, max_age=3600*24*365, httponly=True, secure=False, samesite='Lax', path="/")
        return response


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class =  QuizSerializer


    # This function will create new
    @action(detail=False, methods=['post'], url_path='createQuiz')
    def createQuiz(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            quiz_name = request.data.get('name')
            user_id = request.data.get('userID')
            question_list = request.data.get('questionList', [])

            # Validate required fields
            if not quiz_name or not user_id:
                return Response(
                    {'message': 'Quiz name and user ID are required'},
                    status=400
                )

            # Create Quiz entry
            quiz = Quiz.objects.create(
                user_id=user_id,
                quiz_name=quiz_name,
                access_link=f"http://example.com/quizzes/"  # Generate access link
            )
            quiz.save()



            # Create Question and Answer entries
            for question_data in question_list:
                question_instance = Question.objects.create(
                    quiz=quiz,
                    title=question_data.get('title'),
                    description=question_data.get('description', ''),
                    multiple=question_data.get('multiple', False),
                    required=question_data.get('required', False)
                )

                # Create Answer entries for the question
                for choice in question_data.get('choices', []):
                    Answers.objects.create(
                        question=question_instance,
                        answer=choice.get('answer', ''),
                        state=choice.get('selected', False)
                    )

            return Response(
                {'message': 'Quiz and questions created successfully', 'quiz_id': quiz.quiz_id, 'proceed': True, 'quiz_data': QuizSerializer(quiz).data},
                status=201
            )

        except Exception as e:
            return Response(
                {'message': 'An error occurred', 'error': str(e), 'proceed': False},
                status=500
            )


    @action(detail=False, methods=['post'], url_path='updateQuiz')
    def updateQuiz(self, request, *args, **kwargs):
        try:
            # Fetch the quiz using its primary key `quiz_id`
            quiz_id = request.data.get('id')
            quiz = get_object_or_404(Quiz, quiz_id=quiz_id)

            # Update quiz fields
            quiz.quiz_name = request.data.get('name', quiz.quiz_name)
            quiz.save()

            # Process questions in the quiz
            for question_data in request.data.get('questionList', []):
                question_id = question_data.get('id')  # Primary key for the Question model
                if question_id:
                    # Update existing question
                    question = get_object_or_404(Question, question_id=question_id, quiz=quiz)
                    question.title = question_data.get('title', question.title)
                    question.description = question_data.get('description', question.description)
                    question.type = question_data.get('type', question.type)
                    question.answer = question_data.get('answer', question.answer)
                    question.multiple = question_data.get('multiple', question.multiple)
                    question.required = question_data.get('required', question.required)
                    question.save()

                    # Process answers (choices) for the question
                    for choice_data in question_data.get('choices', []):
                        choice_id = choice_data.get('id')  # Primary key for the Answers model
                        if choice_id:
                            # Update existing answer
                            choice = get_object_or_404(Answers, ans_id=choice_id, question=question)
                            choice.answer = choice_data.get('answer', choice.answer)
                            choice.state = choice_data.get('selected', choice.state)
                            choice.save()
                        else:
                            # Create a new answer
                            Answers.objects.create(
                                question=question,
                                answer=choice_data['answer'],
                                state=choice_data['selected']
                            )
                else:
                    # Create a new question
                    new_question = Question.objects.create(
                        quiz=quiz,
                        title=question_data['title'],
                        description=question_data['description'],
                        type=question_data.get('type', 'text'),
                        answer=question_data.get('answer', ''),
                        multiple=question_data.get('multiple', False),
                        required=question_data.get('required', False)
                    )
                    # Add answers (choices) for the new question
                    for choice_data in question_data.get('choices', []):
                        Answers.objects.create(
                            question=new_question,
                            answer=choice_data['answer'],
                            state=choice_data['selected']
                        )

            return Response({'message': 'Quiz updated successfully.', 'proceed': True, 'quiz_data': quiz}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e), 'proceed': False}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['get'], url_path='getQuiz')
    def getAllQuizes(self, request, *args, **kwargs):
        # Fetch the quiz using its primary key `quiz_id`
        quiz_id = request.data.get('id')
        quiz = get_object_or_404(Quiz, quiz_id=quiz_id)



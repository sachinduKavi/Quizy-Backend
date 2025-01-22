from logging import exception

from django.forms import Form
from django.shortcuts import render, get_object_or_404
from django.utils.regex_helper import Choice
from rest_framework import viewsets, status
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
                {'message': 'Quiz and questions created successfully', 'quiz_id': quiz.quiz_id, 'proceed': True},
                status=201
            )

        except Exception as e:
            return Response(
                {'message': 'An error occurred', 'error': str(e), 'proceed': False},
                status=500
            )


    @action(detail=False, methods=['post'], url_path='updateQuiz')
    def updateQuiz(self, request, *args, **kwargs):
        data = request.data

        try:
            # Fetch the form using its ID
            form_id = data.get('id')
            form = get_object_or_404(Form, id=form_id)
            form.name = data.get('name', form.name)
            form.save()

            # Process questions in the form
            for question_data in data.get('questionList', []):
                question_id = question_data.get('id')
                if question_id:
                    # Update existing question
                    question = get_object_or_404(Question, id=question_id, form=form)
                    question.title = question_data.get('title', question.title)
                    question.description = question_data.get('description', question.description)
                    question.multiple = question_data.get('multiple', question.multiple)
                    question.required = question_data.get('required', question.required)
                    question.image_file = question_data.get('imageFile', question.image_file)
                    question.placement = question_data.get('placement', question.placement)
                    question.save()

                    # Update choices for the question
                    for choice_data in question_data.get('choices', []):
                        choice_id = choice_data.get('id')
                        if choice_id:
                            choice = get_object_or_404(Choice, id=choice_id, question=question)
                            choice.answer = choice_data.get('answer', choice.answer)
                            choice.selected = choice_data.get('selected', choice.selected)
                            choice.save()
                        else:
                            # Create new choice
                            Choice.objects.create(
                                question=question,
                                answer=choice_data['answer'],
                                selected=choice_data['selected']
                            )
                else:
                    # Create new question
                    new_question = Question.objects.create(
                        form=form,
                        title=question_data['title'],
                        description=question_data['description'],
                        multiple=question_data['multiple'],
                        required=question_data['required'],
                        image_file=question_data.get('imageFile'),
                        placement=question_data['placement']
                    )
                    for choice_data in question_data.get('choices', []):
                        Choice.objects.create(
                            question=new_question,
                            answer=choice_data['answer'],
                            selected=choice_data['selected']
                        )

            return Response({'message': 'Quiz updated successfully.', 'proceed': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e), 'proceed': False}, status=status.HTTP_400_BAD_REQUEST)
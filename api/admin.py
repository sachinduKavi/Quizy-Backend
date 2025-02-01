from django.contrib import admin
from .models import User, Quiz, Question, Answers, SelectedValue, Submission

# Register your models here.
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Submission)
admin.site.register(SelectedValue)
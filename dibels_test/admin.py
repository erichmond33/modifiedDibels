from re import I
from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Sentence)
admin.site.register(mazeTest)
admin.site.register(mazeQuestionAttempt)
admin.site.register(imageTest)
admin.site.register(imageQuestionAttempt)
admin.site.register(queuedMazeQuestion)
admin.site.register(queuedImageQuestion)
admin.site.register(Font)
admin.site.register(Image)





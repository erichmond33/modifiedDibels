from re import I
from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(mazeTest, mazeTestAdmin)
admin.site.register(mazeQuestionAttempt, mazeQuestionAttemptAdmin)
admin.site.register(imageTest, imageTestAdmin)
admin.site.register(imageQuestionAttempt, imageQuestionAttemptAdmin)
admin.site.register(queuedMazeQuestion, queuedMazeQuestionAdmin)
admin.site.register(queuedImageQuestion, queuedImageQuestionAdmin)
admin.site.register(Font, FontAdmin)
admin.site.register(Image, ImageAdmin)



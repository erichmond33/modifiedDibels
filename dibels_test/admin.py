from re import I
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


class SentenceResource(resources.ModelResource):
    class Meta:
        model = Sentence

class SentenceAdmin(ImportExportModelAdmin):
    resource_class = SentenceResource


class mazeTestResource(resources.ModelResource):
    class Meta:
        model = mazeTest

class mazeTestAdmin(ImportExportModelAdmin):
    resource_class = mazeTestResource


class mazeQuestionAttemptResource(resources.ModelResource):
    class Meta:
        model = mazeQuestionAttempt

class mazeQuestionAttemptAdmin(ImportExportModelAdmin):
    resource_class = mazeQuestionAttemptResource


class imageTestResource(resources.ModelResource):
    class Meta:
        model = imageTest

class imageTestAdmin(ImportExportModelAdmin):
    resource_class = imageTestResource


class imageQuestionAttemptResource(resources.ModelResource):
    class Meta:
        model = imageQuestionAttempt

class imageQuestionAttemptAdmin(ImportExportModelAdmin):
    resource_class = imageQuestionAttemptResource


class queuedMazeQuestionResource(resources.ModelResource):
    class Meta:
        model = queuedMazeQuestion

class queuedMazeQuestionAdmin(ImportExportModelAdmin):
    resource_class = queuedMazeQuestionResource


class queuedImageQuestionResource(resources.ModelResource):
    class Meta:
        model = queuedImageQuestion
    
class queuedImageQuestionAdmin(ImportExportModelAdmin):
    resource_class = queuedImageQuestionResource


class FontResource(resources.ModelResource):
    class Meta:
        model = Font

class FontAdmin(ImportExportModelAdmin):
    resource_class = FontResource


class ImageResource(resources.ModelResource):
    class Meta:
        model = Image

class ImageAdmin(ImportExportModelAdmin):
    resource_class = ImageResource


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



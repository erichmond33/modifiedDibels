#from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Register your models here.

"""
Revaulate the examinee model

Hash the testAdmin... SHA

Set of attributes that were used to create the font
"""
class Font(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    style = models.CharField(max_length=75)
    size = models.CharField(max_length=20)
    angular = models.FloatField(blank=True)
    artistic = models.FloatField(blank=True)
    attention_grabbing = models.FloatField(blank=True)
    attractive = models.FloatField(blank=True)
    bad = models.FloatField(blank=True)
    boring = models.FloatField(blank=True)
    calm = models.FloatField(blank=True)
    capitals = models.FloatField(blank=True)
    charming = models.FloatField(blank=True)
    clumsy = models.FloatField(blank=True)
    complex = models.FloatField(blank=True)
    cursive = models.FloatField(blank=True)
    delicate = models.FloatField(blank=True)
    disorderly = models.FloatField(blank=True)
    display = models.FloatField(blank=True)
    dramatic = models.FloatField(blank=True)
    formal = models.FloatField(blank=True)
    fresh = models.FloatField(blank=True)
    friendly = models.FloatField(blank=True)
    gentle = models.FloatField(blank=True)
    graceful = models.FloatField(blank=True)
    happy = models.FloatField(blank=True)
    italic = models.FloatField(blank=True)
    legible = models.FloatField(blank=True)
    modern = models.FloatField(blank=True)
    monospace = models.FloatField(blank=True)
    playful = models.FloatField(blank=True)
    pretentious = models.FloatField(blank=True)
    serif = models.FloatField(blank=True)
    sharp = models.FloatField(blank=True)
    sloppy = models.FloatField(blank=True)
    soft = models.FloatField(blank=True)
    strong = models.FloatField(blank=True)
    technical = models.FloatField(blank=True)
    thin = models.FloatField(blank=True)
    warm = models.FloatField(blank=True)
    wide = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.id} : {self.name}"

class Sentence(models.Model):
    body = models.TextField(blank=True)
    gradeLevel = models.CharField(max_length=20, default="null")
    selectedWord = models.CharField(max_length=50)
    distractorWord1 = models.CharField(max_length=50)
    distractorWord2 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} : {self.body}"

class mazeQuestionAttempt(models.Model):
    question = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    font = models.ForeignKey(Font, on_delete=models.CASCADE, default=230)
    wordSelection = models.CharField(max_length=50)
    wordAttempt = models.CharField(max_length=50)
    correct = models.BooleanField(blank=True)

    def __str__(self):
        return f"{self.font}" #: {self.font}  : {self.wordSelection} : {self.wordAttempt} : {self.correct}"

class mazeTest(models.Model):
    #user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userMaze", default="null")
    testAdmin = models.CharField(max_length=50, default="null")
    #examinee = models.CharField(max_length=50, default="null")
    gradeLevel = models.CharField(max_length=20, default="null")
    timestamp = models.DateTimeField(auto_now_add=True)
    mazeQuestionAttempts = models.ManyToManyField(
       mazeQuestionAttempt , blank=False, related_name="mazeQuestionAttemps")

    def __str__(self):
        return f"{self.id} : {self.timestamp}"

class queuedMazeQuestion(models.Model):
    testId = models.ForeignKey(mazeTest, on_delete=models.CASCADE)
    queuedSentenceId = models.IntegerField(default="-1")
    queuedWordSelection = models.CharField(max_length=50, blank=True)
    queuedGeneratedWord1 = models.CharField(max_length=50, blank=True)
    queuedGeneratedWord2 = models.CharField(max_length=50, blank=True)
    font = models.ForeignKey(Font, on_delete=models.CASCADE, default=300)


class Image(models.Model):
    body = models.CharField(max_length=30)
    gradeLevel = models.CharField(max_length=50, default="null")

    def __str__(self):
        return f"{self.id} : {self.body} : {self.gradeLevel}"

class imageQuestionAttempt(models.Model):
    font = models.ForeignKey(Font, on_delete=models.CASCADE, default=230)
    wordSelection = models.CharField(max_length=50)
    wordAttempt = models.CharField(max_length=50)
    correct = models.BooleanField(blank=True)

    def __str__(self):
        return f"{self.font} : {self.wordSelection} : {self.wordAttempt} : {self.correct}"

class imageTest(models.Model):
    #user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userImage", default="null")
    testAdmin = models.CharField(max_length=50, default="null")
    #examinee = models.CharField(max_length=50, default="null")
    gradeLevel = models.CharField(max_length=20, default="null")
    timestamp = models.DateTimeField(auto_now_add=True)
    imageQuestionAttempts = models.ManyToManyField(
       imageQuestionAttempt , blank=False, related_name="imageQuestionAttemps")

    def __str__(self):
        return f"{self.id} : {self.timestamp}"

class queuedImageQuestion(models.Model):
    testId = models.ForeignKey(imageTest, on_delete=models.CASCADE)
    queuedImageSelection = models.CharField(max_length=50, default="null")
    queuedGeneratedWord1 = models.CharField(max_length=50, blank=True)
    queuedGeneratedWord2 = models.CharField(max_length=50, blank=True)
    font = models.ForeignKey(Font, on_delete=models.CASCADE, default=160)

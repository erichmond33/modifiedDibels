from operator import ge
#from tkinter.tix import MAX
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
from django.http.response import JsonResponse
import re
import hashlib
from datetime import datetime
import os
import copy
import spacy    
import json


from .models import *
from .helpers import *
# Create your views here.

MAX_MAZE_QUESTIONS = 25

def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "test/home.html", {"username" : request.user.username})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = hashlib.sha256(request.POST["username"].encode())
        username = username.hexdigest()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "test/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "test/login.html", status=200)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):

    if request.method == "POST":

        username = hashlib.sha256(request.POST["username"].encode())
        username = username.hexdigest()

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "test/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, "null", password)
            user.save()
        except IntegrityError:
            return render(request, "test/register.html", {
                "message": "Username already taken."
            })

        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "test/register.html")

@login_required
def home(request):

    return render(request, "test/home.html", {"username" : request.user.username})

@login_required
def mazeAdmin(request):

    if request.method == "POST":
        previousTests = mazeTest.objects.filter(testAdmin=request.user.username)
        if len(previousTests) == 4:
            return render(request, "test/mazeAdmin.html", {"message" : "You can only take 4 maze tests. Thank you for participating!"})
        else:
            for test in previousTests:
                if len(test.mazeQuestionAttempts.all()) != MAX_MAZE_QUESTIONS:
                    return render(request, "test/mazeAdmin.html", {"message" : "You have not completed all of your maze tests. Please complete all of your tests before taking another."})
            #Add date and admin to db
            newTest = mazeTest(
                testAdmin=request.user.username,
                #examinee=request.POST["testTaker"],
                gradeLevel=request.POST["gradeLevel"]
            )
            newTest.save()

            queuedMazeQuestionObject = queuedMazeQuestion(
                    testId = newTest,
                    queuedSentenceId = -1,
                    queuedWordSelection = "",
                    queuedGeneratedWord1 = "3",
                    queuedGeneratedWord2 = ""
                )
            queuedMazeQuestionObject.save()

            #return render(request, "test/test.html", {"id" : id})
            return redirect('mazeGeneration', newTest.id)
    else:
        return render(request, "test/mazeAdmin.html", {"username" : request.user.username})

@login_required
def imageAdmin(request):

    if request.method == "POST":
        
        #Add date and admin to db
        newTest = imageTest(
            #testAdmin=request.POST["testAdmin"],
            testAdmin=request.user.username,
            #examinee=request.POST["testTaker"],
            gradeLevel=request.POST["gradeLevel"]
        )
        newTest.save()

        queuedImageQuestionObject = queuedImageQuestion(
                testId = newTest,
                queuedImageSelection = "null",
                queuedGeneratedWord1 = "",
                queuedGeneratedWord2 = ""
            )
        queuedImageQuestionObject.save()

        return redirect('imageGeneration', newTest.id)

    else:
        return render(request, "test/imageAdmin.html", {"username" : request.user.username})

@login_required
def mazeSubmission(request):
    
    if request.method == "POST":

        #Getting the data from post
        id = request.POST["id"]
        sentenceId = request.POST["sentenceId"]
        correctAnswer = request.POST["selection"]
        studentAnswer = request.POST["options"]
        fontId = request.POST["fontId"]
        correct = True if correctAnswer == studentAnswer else False

        #Saving the data
        testObject = mazeTest.objects.get(id=id)
        senteceObject = Sentence.objects.get(id=sentenceId)
        fontObject = Font.objects.get(id=fontId)
        questionAttemptObject = mazeQuestionAttempt(
            question=senteceObject,
            wordSelection=correctAnswer,
            wordAttempt=studentAnswer,
            correct=correct,
            font = fontObject)
        #Making sure a sentence is only submitted once
        for attempt in testObject.mazeQuestionAttempts.all():
            if senteceObject == attempt.question:
                return redirect('mazeGeneration', id)
        questionAttemptObject.save()
        testObject.mazeQuestionAttempts.add(questionAttemptObject)
        testObject.save()

        queuedMazeQuestionObject = queuedMazeQuestion.objects.get(testId=testObject.id)
        queuedMazeQuestionObject.queuedSentenceId = -1
        queuedMazeQuestionObject.queuedWordSelection = "2"
        queuedMazeQuestionObject.queuedGeneratedWord1 = ""
        queuedMazeQuestionObject.queuedGeneratedWord2 = ""
        queuedMazeQuestionObject.save()

        return redirect('mazeGeneration', id)

@login_required
def mazeGeneration(request, metadata_id):

    if request.method == "GET":
        print(mazeTest.objects.filter(testAdmin=request.user.username))

        # ----- Checking to see if the user is correct -----
        testObject = mazeTest.objects.get(id=metadata_id)
        if (str(request.user) != (str(testObject.testAdmin))):
            return redirect("home")

        # ----- Checking to see if the test is over -----
        gradeLevel = mazeTest.objects.get(id=metadata_id).gradeLevel
        allQuestions = Sentence.objects.filter(gradeLevel=gradeLevel)
        thisTestPreviousQuestions = testObject.mazeQuestionAttempts.all()

        if len(thisTestPreviousQuestions) == MAX_MAZE_QUESTIONS:
            queuedMazeQuestion.objects.get(testId=testObject.id).delete()
            return redirect("done")
        for question in thisTestPreviousQuestions:
            print(question.question)
            
        # This is kinda cryptic... but a -1 queuedSentenceId represents a brand new test question
        if queuedMazeQuestion.objects.get(testId=testObject.id).queuedSentenceId == -1:

            # ----- Positive feedback -----
            try:
                testObject.mazeQuestionAttempts.last().correct
            except:
                POSITIVE_FEEBACK = generationHelpers.positiveFeedbackWithRandomnessAfterCorrectAnswer(False)
                print("ERROR mazeGeneration: testObject.mazeQuestionAttempts.last().correct returned NULL")
            else:
                POSITIVE_FEEBACK = generationHelpers.positiveFeedbackWithRandomnessAfterCorrectAnswer(testObject.mazeQuestionAttempts.last().correct)

            # ---- selecting the question -----
            #selectedQuestion = allQuestions[len(testObject.mazeQuestionAttempts.all())]
            selectedQuestion = random.choice(allQuestions)

            previousTests = mazeTest.objects.filter(testAdmin=request.user.username)
            allTestsPreviousQuestions = []
            for test in previousTests:
                for question in test.mazeQuestionAttempts.all():
                    allTestsPreviousQuestions.append(question.question)

            while selectedQuestion in allTestsPreviousQuestions:
                selectedQuestion = random.choice(allQuestions)

            # ----- Formatting the sentence -----*
            selectedQuestionId = selectedQuestion.id
            questionString = str(selectedQuestion.body)
            questionSelectedWord = selectedQuestion.selectedWord
            selectedDummyWord1 = selectedQuestion.distractorWord1
            selectedDummyWord2 = selectedQuestion.distractorWord2
            helpers = mazeGenerationHelpers()
            formattedSentenceForHtml = helpers.formatSentenceForHtml(
                questionString,
                questionSelectedWord
            )

            # ---- get a random font ----- 
            previousTestFonts = []
            for questionObject in testObject.mazeQuestionAttempts.all():
                previousTestFonts.append(questionObject.font)

            font = random.choice(Font.objects.all())
            while font in previousTestFonts:
                font = random.choice(Font.objects.all())
            style = font.style
            link = font.link
            size = font.size

            # ----- Saving the queued question -----
            queuedMazeQuestionObject = queuedMazeQuestion.objects.get(testId=testObject.id)
            queuedMazeQuestionObject.queuedSentenceId = selectedQuestion.id
            queuedMazeQuestionObject.queuedWordSelection = questionSelectedWord
            queuedMazeQuestionObject.queuedGeneratedWord1 = selectedDummyWord1
            queuedMazeQuestionObject.queuedGeneratedWord2 = selectedDummyWord2
            queuedMazeQuestionObject.font = font
            queuedMazeQuestionObject.save()
    

        else:

            # ----- Load in old question -----
            queuedMazeQuestionObject = queuedMazeQuestion.objects.get(testId=testObject.id)
            selectedQuestionId = queuedMazeQuestionObject.queuedSentenceId
            selectedWord = queuedMazeQuestionObject.queuedWordSelection
            selectedDummyWord1 = queuedMazeQuestionObject.queuedGeneratedWord1
            selectedDummyWord2 = queuedMazeQuestionObject.queuedGeneratedWord2
            font = queuedMazeQuestionObject.font
            link = queuedMazeQuestionObject.font.link
            style = queuedMazeQuestionObject.font.style
            size = queuedMazeQuestionObject.font.size

            # ----- Formatting -----
            selectedQuestion = Sentence.objects.get(id=selectedQuestionId)
            questionString = str(selectedQuestion.body)
            questionSelectedWord = selectedQuestion.selectedWord
            selectedDummyWord1 = selectedQuestion.distractorWord1
            selectedDummyWord2 = selectedQuestion.distractorWord2
            helpers = mazeGenerationHelpers()
            formattedSentenceForHtml = helpers.formatSentenceForHtml(
                questionString,
                questionSelectedWord
            )

            # ----- Positive feedback -----
            POSITIVE_FEEBACK = [False,False,False]

        # ----- Randomizing the results -----
        shuffledAnswerList = [questionSelectedWord, selectedDummyWord1, selectedDummyWord2]
        random.shuffle(shuffledAnswerList)


        return render(request, "test/mazeTest.html", {
        "username" : request.user.username,
        "sentenceId" : selectedQuestionId,
        "splitSentence" : formattedSentenceForHtml,
        "selection" : questionSelectedWord,
        "generatedWord1" : selectedDummyWord1,
        "randWord1" : shuffledAnswerList[0],
        "randWord2" : shuffledAnswerList[1],
        "randWord3": shuffledAnswerList[2],
        "generatedWord2" : selectedDummyWord2,
        "id" : metadata_id,
        "funkyChars" : ["\"", ",", "-"],
        "nofQuestions" : len(testObject.mazeQuestionAttempts.all())+1,
        "MAX_QUESTIONS" : MAX_MAZE_QUESTIONS,
        "percentProgress" : int((len(testObject.mazeQuestionAttempts.all())) / MAX_MAZE_QUESTIONS  * 100),
        "style" : style,
        "link" : link,
        "size" : size,
        "fontId" : font.id,
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_3" : POSITIVE_FEEBACK[0],
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_9" : POSITIVE_FEEBACK[1],
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_15" : POSITIVE_FEEBACK[2],
        })
        
@login_required
def imageSubmission(request):
    
    if request.method == "POST":

        #Getting the data from post
        id = request.POST["id"]
        correctAnswer = request.POST["selection"]
        studentAnswer = request.POST["options"]
        fontId = request.POST["fontId"]
        correct = True if correctAnswer == studentAnswer else False

        #Saving the data
        testObject = imageTest.objects.get(id=id)
        fontObject = Font.objects.get(id=fontId)
        questionAttemptObject = imageQuestionAttempt(
            wordSelection=correctAnswer,
            wordAttempt=studentAnswer,
            correct=correct,
            font = fontObject)
        #Making sure a sentence is only submitted once
        for attempt in testObject.imageQuestionAttempts.all():
            if correctAnswer == attempt.wordSelection:
                return redirect('imageGeneration', id)
        questionAttemptObject.save()
        testObject.imageQuestionAttempts.add(questionAttemptObject)
        testObject.save()

        queuedImageQuestionObject = queuedImageQuestion.objects.get(testId=testObject.id)
        queuedImageQuestionObject.queuedImageSelection = "null"
        queuedImageQuestionObject.queuedGeneratedWord1 = ""
        queuedImageQuestionObject.queuedGeneratedWord2 = ""
        queuedImageQuestionObject.save()

        return redirect('imageGeneration', id)

@login_required
def imageGeneration(request, metadata_id):

    if request.method == "GET":

        # ----- Checking to see if the user is correct -----
        testObject = imageTest.objects.get(id=metadata_id)
        if (str(request.user) != (str(testObject.testAdmin))):
            return redirect("home")
        '''
        previousTestQuestionsObjects = testObject.imageQuestionAttempts.all()
        previousTestQuestions = []
        for questionObject in previousTestQuestionsObjects:
            previousTestQuestions.append(questionObject.wordSelection)
        '''
        # ----- Checking to see if the test is over -----
        gradeLevel = imageTest.objects.get(id=metadata_id).gradeLevel
        allQuestions = Image.objects.filter(gradeLevel=gradeLevel)

        if len(testObject.imageQuestionAttempts.all()) == len(allQuestions):
            queuedImageQuestion.objects.get(testId=testObject.id).delete()
            return redirect("done")


        if queuedImageQuestion.objects.get(testId=testObject.id).queuedImageSelection == "null":

            # ----- Positive feedback -----
            try:
                testObject.imageQuestionAttempts.last().correct
            except:
                POSITIVE_FEEBACK = generationHelpers.positiveFeedbackWithRandomnessAfterCorrectAnswer(False)
                print("ERROR imageGeneration: testObject.imageQuestionAttempts.last().correct returned NULL")
            else:
                POSITIVE_FEEBACK = generationHelpers.positiveFeedbackWithRandomnessAfterCorrectAnswer(testObject.imageQuestionAttempts.last().correct)

            # ---- Randomly selecting the question/correct answer -----
            questionSelectedWord = allQuestions[len(testObject.imageQuestionAttempts.all())].body
            '''
            questionSelectedWord = random.choice(possibleTestQuestions)

            while questionSelectedWord in previousTestQuestions:
                questionSelectedWord = random.choice(possibleTestQuestions)
            '''
            
            # ----- Randomly selected the alternative answers -----
            alternativeAnswer1 = random.choice(allQuestions).body
            while (alternativeAnswer1 == questionSelectedWord):
                alternativeAnswer1 = random.choice(allQuestions).body

            alternativeAnswer2 = random.choice(allQuestions).body
            while (alternativeAnswer2 == alternativeAnswer1) or (alternativeAnswer2 == questionSelectedWord):
                alternativeAnswer2 = random.choice(allQuestions).body

            # ---- get a random font ----- 
            previousTestFonts = []
            for questionObject in testObject.imageQuestionAttempts.all():
                previousTestFonts.append(questionObject.font)

            font = random.choice(Font.objects.all())
            while font in previousTestFonts:
                font = random.choice(Font.objects.all())
            style = font.style
            link = font.link

            # ----- Saving the queued question -----
            queuedImageQuestionObject = queuedImageQuestion.objects.get(testId=testObject.id)
            queuedImageQuestionObject.queuedImageSelection = questionSelectedWord
            queuedImageQuestionObject.queuedGeneratedWord1 = alternativeAnswer1
            queuedImageQuestionObject.queuedGeneratedWord2 = alternativeAnswer2
            queuedImageQuestionObject.font = font
            queuedImageQuestionObject.save()

        else:
            # ----- Load in old question -----
            queuedImageQuestionObject = queuedImageQuestion.objects.get(testId=testObject.id)
            questionSelectedWord = queuedImageQuestionObject.queuedImageSelection
            alternativeAnswer1 = queuedImageQuestionObject.queuedGeneratedWord1
            alternativeAnswer2 = queuedImageQuestionObject.queuedGeneratedWord2
            font = queuedImageQuestionObject.font
            link = queuedImageQuestionObject.font.link
            style = queuedImageQuestionObject.font.style

            # ----- Positive feedback -----
            POSITIVE_FEEBACK = [False,False,False]

        # ----- Randmozing the results -----
        shuffledAnswerList = [questionSelectedWord,alternativeAnswer1,alternativeAnswer2]
        random.shuffle(shuffledAnswerList)

        # ----- Getting image path -----
        imagePath = f"/static/test/images/{questionSelectedWord.strip()}.png"
        doneYet = True
        print(doneYet)


        return render(request, "test/imageTest.html",
        {"username" : request.user.username,
        "selection" : questionSelectedWord, 
        "imagePath" : imagePath,
        "doneYet" : doneYet,
        "generatedWord1" : alternativeAnswer1, 
        "generatedWord2" : alternativeAnswer2,
        "randWord1" : shuffledAnswerList[0],
        "randWord2" : shuffledAnswerList[1],
        "randWord3" : shuffledAnswerList[2],
        "id" : metadata_id,
        "nofQuestions" : len(testObject.imageQuestionAttempts.all())+1,
        "MAX_QUESTIONS" : len(allQuestions),
        "percentProgress" : int((len(testObject.imageQuestionAttempts.all())) / len(allQuestions)  * 100),
        "style" : style,
        "link" : link,
        "fontId" : font.id,
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_3" : POSITIVE_FEEBACK[0],
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_9" : POSITIVE_FEEBACK[1],
        "POSITIVE_FEEBACK_PROBABILITY_1_OVER_15" : POSITIVE_FEEBACK[2],
        })

@login_required
def done(request):

    return render(request, "test/done.html", 
        {"username" : request.user.username})

@login_required
def continueTesting(request):

    if request.method == "GET":
        allTestsMaze = []
        mazeTests = mazeTest.objects.filter(testAdmin=request.user.username)
        for test in mazeTests:
            singleTestMaze = []
            if len(test.mazeQuestionAttempts.all()) < MAX_MAZE_QUESTIONS:
                singleTestMaze.append(test.id)
                singleTestMaze.append(test.gradeLevel)
                singleTestMaze.append(len(test.mazeQuestionAttempts.all())+1)
                singleTestMaze.append(MAX_MAZE_QUESTIONS)
                singleTestMaze.append(test.id)
                singleTestMaze.append(test.timestamp)

                allTestsMaze.append(singleTestMaze)


        allTestsImage = []
        imageTests = imageTest.objects.filter(testAdmin=request.user.username)
        for test in imageTests:
            singleTestImage = []
            allQuestions1stGrade = []
            with open(f'words/1st grade.txt','r') as file:
                    for line in file:
                        for word in line.split():
                            allQuestions1stGrade.append(word)
            if (len(test.imageQuestionAttempts.all()) < len(Image.objects.filter(gradeLevel=test.gradeLevel))):
                singleTestImage.append(test.id)
                singleTestImage.append(test.gradeLevel)
                singleTestImage.append(len(test.imageQuestionAttempts.all())+1)
                singleTestImage.append(len(Image.objects.filter(gradeLevel=test.gradeLevel)))
                singleTestImage.append(test.id)
                singleTestImage.append(test.timestamp)

                allTestsImage.append(singleTestImage)

        return render(request, "test/continueTesting.html",
        {"username" : request.user.username,
        "allTestsMaze" : allTestsMaze,
        "allTestsImage" : allTestsImage})

@login_required
def guidelines(request):
    if request.method == "GET":
        return render(request, "test/guidelines.html")


@login_required
def gallery(request):

    studentImages = ['wave', 'room', 'animal', 'clean', 'voice', 'travel', 'time', 'rose', 'game', 'race', 'doctor', 'eat', 'old', 'sky', 'sea', 'last', 'river', 'write', 'summer', 'table', 'earth', 'chain', 'bank', 'fight', 'season', 'foot', 'carry', 'land', 'friends', 'fly', 'people', 'ice', 'step', 'summer', 'path', 'mouth', 'island', 'party', 'sit', 'food', 'ride', 'heavy', 'art', 'heat', 'walk', 'think', 'story', 'drink', 'water', 'paper', 'school', 'play', 'switch', 'line', 'rock', 'king', 'snow', 'car', 'ran', 'open', 'arm', 'under', 'bear', 'face', 'picture', 'floor', 'news', 'sick', 'turn']

    imagePaths = []
    imageNames = []

    for word in studentImages:
        imagePaths.append(f"/static/test/images/{word}.png")
        imageNames.append(word)

    imagePathsAndNames = zip(imagePaths, imageNames)

    return render(request, "test/gallery.html",
        {"username" : request.user.username,
        "imagePathsAndNames" : imagePathsAndNames})

def addData(request):
    '''
    with open("words/6th grade.json", 'r') as f:
        data = json.load(f)
    f.close()
    print("-------")
    for sentence in data.values():
        for i in sentence:
            sentenceObject = Sentence (
                body = i['body'],
                gradeLevel = "6th grade",
                selectedWord = i['selectedWord'],
                distractorWord1 = i['distractorWord1'],
                distractorWord2 = i['distractorWord2']
            )
            sentenceObject.save()

    with open("words/5th grade.json", 'r') as f:
        data = json.load(f)
    f.close()
    print("-------")
    for sentence in data.values():
        for i in sentence:
            sentenceObject = Sentence (
                body = i['body'],
                gradeLevel = "5th grade",
                selectedWord = i['selectedWord'],
                distractorWord1 = i['distractorWord1'],
                distractorWord2 = i['distractorWord2']
            )
            sentenceObject.save()

    with open("words/4th grade.json", 'r') as f:
        data = json.load(f)
    f.close()
    print("-------")
    for sentence in data.values():
        for i in sentence:
            sentenceObject = Sentence (
                body = i['body'],
                gradeLevel = "4th grade",
                selectedWord = i['selectedWord'],
                distractorWord1 = i['distractorWord1'],
                distractorWord2 = i['distractorWord2']
            )
            sentenceObject.save()

    with open("words/3rd grade.json", 'r') as f:
        data = json.load(f)
    f.close()
    print("-------")
    for sentence in data.values():
        for i in sentence:
            sentenceObject = Sentence (
                body = i['body'],
                gradeLevel = "3rd grade",
                selectedWord = i['selectedWord'],
                distractorWord1 = i['distractorWord1'],
                distractorWord2 = i['distractorWord2']
            )
            sentenceObject.save()
    
    with open("words/2nd grade.json", 'r') as f:
        data = json.load(f)
    f.close()
    print("-------")
    for sentence in data.values():
        for i in sentence:
            sentenceObject = Sentence (
                body = i['body'],
                gradeLevel = "2nd grade",
                selectedWord = i['selectedWord'],
                distractorWord1 = i['distractorWord1'],
                distractorWord2 = i['distractorWord2']
            )
            sentenceObject.save()
    
    ------
    
    with open(f'words/1st grade.txt','r') as file:
        for line in file:
            imageObject = Image(
                body = line,
                gradeLevel = "1st grade"
            )
            imageObject.save()
    
    with open(f'words/Kindergarten.txt','r') as file:
        for line in file:
            imageObject = Image(
                body = line,
                gradeLevel = "Kindergarten"
            )
            imageObject.save()
    
    ------------
    with open(f'words/2nd grade.txt','r') as file:
        for line in file:
            sentenceObject = Sentence(
                body = line,
                gradeLevel = "2nd grade"
            )
            sentenceObject.save()

    with open(f'words/3rd grade.txt','r') as file:
        for line in file:
            sentenceObject = Sentence(
                body = line,
                gradeLevel = "3rd grade"
            )
            sentenceObject.save()

    with open(f'words/4th grade.txt','r') as file:
        for line in file:
            sentenceObject = Sentence(
                body = line,
                gradeLevel = "4th grade"
            )
            sentenceObject.save()

    with open(f'words/5th grade.txt','r') as file:
        for line in file:
            sentenceObject = Sentence(
                body = line,
                gradeLevel = "5th grade"
            )
            sentenceObject.save()

    with open(f'words/6th grade.txt','r') as file:
        for line in file:
            sentenceObject = Sentence(
                body = line,
                gradeLevel = "6th grade"
            )
            sentenceObject.save()
    
    with open("temp2 copy.json", 'r') as f:
        data = json.load(f)
    f.close()

    for font in data.values():
        fontObject = Font(
            name = font['name'],
            link = font['link'],
            style = font['style'],
            size = font['size'],
            angular = font['attributes']['angular'],
            artistic = font['attributes']['artistic'],
            attention_grabbing = font['attributes']['attention-grabbing'],
            attractive = font['attributes']['attractive'],
            bad = font['attributes']['bad'],
            boring = font['attributes']['boring'],
            calm = font['attributes']['calm'],
            capitals = font['attributes']['capitals'],
            charming = font['attributes']['charming'],
            clumsy = font['attributes']['clumsy'],
            complex = font['attributes']['complex'],
            cursive = font['attributes']['cursive'],
            delicate = font['attributes']['delicate'],
            disorderly = font['attributes']['disorderly'],
            display = font['attributes']['display'],
            dramatic = font['attributes']['dramatic'],
            formal = font['attributes']['formal'],
            fresh = font['attributes']['fresh'],
            friendly = font['attributes']['friendly'],
            gentle = font['attributes']['gentle'],
            graceful = font['attributes']['graceful'],
            happy = font['attributes']['happy'],
            italic = font['attributes']['italic'],
            legible = font['attributes']['legible'],
            modern = font['attributes']['modern'],
            monospace = font['attributes']['monospace'],
            playful = font['attributes']['playful'],
            pretentious = font['attributes']['pretentious'],
            serif = font['attributes']['serif'],
            sharp = font['attributes']['sharp'],
            sloppy = font['attributes']['sloppy'],
            soft = font['attributes']['soft'],
            strong = font['attributes']['strong'],
            technical = font['attributes']['technical'],
            thin = font['attributes']['thin'],
            warm = font['attributes']['warm'],
            wide = font['attributes']['wide'],
        )
        fontObject.save()
    '''





    

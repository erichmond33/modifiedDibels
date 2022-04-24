import random

class mazeGenerationHelpers():

    def __init__(self):
        pass

    # ----- Formatting our sentence and word -----

    def splitBySpacesAndRemoveNonAlphanumChars(self, sentenceString):
        sentenceStringListSplitBySpaces = sentenceString.split()
        
        sentenceStringListSplitBySpacesOnlyAlpha = []
        for string in sentenceStringListSplitBySpaces:
            for char in string:
                if char.isalnum() == False:
                    string = string.replace(char, "")
            sentenceStringListSplitBySpacesOnlyAlpha.append(string)
        return sentenceStringListSplitBySpacesOnlyAlpha

    def replaceAWithAOrAn(self, listOfStrings, index):
        if listOfStrings[index - 1] in ["a", "an"]:
            listOfStrings[index - 1] = "a/an"
        return listOfStrings
        
    def getWordIndex(self, sentenceSplitBySpaces, selectedWord):
        for word in sentenceSplitBySpaces:
            if word.lower() == selectedWord.lower():
                index = sentenceSplitBySpaces.index(word)
        return index

    def formatWordForHtml(self, sentenceSplitBySpacesWithoutSelectedWord, wordWithNonAlphanums, selectedWord, wordIndex):
        # Lol, jank friggin code right here
        appendedWord = False
        for char in wordWithNonAlphanums:
            if char.isalnum() == False:
                sentenceSplitBySpacesWithoutSelectedWord.insert(wordIndex, char)
                wordIndex += 1
            elif appendedWord == False:
                appendedWord = True
                sentenceSplitBySpacesWithoutSelectedWord.insert(wordIndex, selectedWord)
                wordIndex += 1
        return sentenceSplitBySpacesWithoutSelectedWord

    def formatSentenceForHtml(self, sentenceString, selectedWord):
        splitBySpaces = sentenceString.split()
        
        splitBySpacesNoPunctuation = self.splitBySpacesAndRemoveNonAlphanumChars(
            sentenceString)
        wordIndex = self.getWordIndex(
            splitBySpacesNoPunctuation,
            selectedWord)
        
        splitBySpaces = self.replaceAWithAOrAn(
            splitBySpaces,
            wordIndex)

        selectedWordWithMessyChars = splitBySpaces[wordIndex]
        del splitBySpaces[wordIndex]
        splitBySpaces = self.formatWordForHtml(
            splitBySpaces,
            selectedWordWithMessyChars,
            selectedWord,
            wordIndex)

        return splitBySpaces



class generationHelpers():

    # ----- Positive Feedback -----

    def positiveFeedbackWithRandomnessAfterCorrectAnswer (previousQuestionCorrectness):

        POSITIVE_FEEBACK_TEXTS = [
            "You are doing a fantastic job",
            "This is a really great effort",
            "Keep it up!",
            "First class work!",
            "Your determination is very impressive",
            "I knew you could do it :)",
            "Sensational!",
            "Your effort does not go unnocticed",
            "Keep going! :)))",
            "Truly great job"
        ]

        POSITIVE_FEEDBACK_EMOJIS= [
            "😆😆😆😆😆",
            "💪🏻💪🏻💪🏻💯💯💯💯",
            "🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩",
            "You are on fire 🔥🔥🔥",
            "🤟🤟🤟🤟",
            "5️⭐️⭐️⭐️⭐️⭐️",
            "Too 🥶"
        ]

        POSITIVE_FEEBACK_GIFS = [
            "/static/test/positive_feedback/nachoLibre.gif",
            "/static/test/positive_feedback/theOffice.gif",
            "/static/test/positive_feedback/rickyBobby.gif",
            "/static/test/positive_feedback/mccracken.gif",
            "/static/test/positive_feedback/anchorman.gif",

        ]
            
        POSITIVE_FEEBACK_PROBABILITY_1_OVER_3 = False
        POSITIVE_FEEBACK_PROBABILITY_1_OVER_9 = False
        POSITIVE_FEEBACK_PROBABILITY_1_OVER_15 = False

        if previousQuestionCorrectness:
            # 1/3
            if random.randrange(0,100) <= 33:
                POSITIVE_FEEBACK_PROBABILITY_1_OVER_3 = random.choice(POSITIVE_FEEBACK_TEXTS)
                POSITIVE_FEEBACK_TEXTS.remove(POSITIVE_FEEBACK_PROBABILITY_1_OVER_3)

                # 1/2
                if random.randrange(0,2) == 1:
                    # 1/9
                    if random.randrange(0,100) <= 66:
                        POSITIVE_FEEBACK_PROBABILITY_1_OVER_9 = random.choice(POSITIVE_FEEDBACK_EMOJIS)

                else:
                    # 1/15
                    if random.randrange(0,100) <= 40:
                        POSITIVE_FEEBACK_PROBABILITY_1_OVER_15 = random.choice(POSITIVE_FEEBACK_GIFS)
                    
        return [POSITIVE_FEEBACK_PROBABILITY_1_OVER_3, POSITIVE_FEEBACK_PROBABILITY_1_OVER_9, POSITIVE_FEEBACK_PROBABILITY_1_OVER_15]

from django.test import TestCase, Client
from .helpers import *

# Create your tests here.
class mazeGeneration(TestCase, mazeGenerationHelpers):

    def setUp(self):
        pass

    def test_splitBySpacesAndRemoveNonAlphanumChars(self):
        string = "Hello, World"
        output = mazeGenerationHelpers.splitBySpacesAndRemoveNonAlphanumChars(self, string)
        self.assertEqual(output, ["Hello", "World"])

    def test_splitBySpacesAndRemoveNonAlphanumChars_manyNonAlphas(self):
        string = "!Hello, --_World890"
        output = mazeGenerationHelpers.splitBySpacesAndRemoveNonAlphanumChars(self, string)
        self.assertEqual(output, ["Hello", "World890"])

    def test_replaceAWithAOrAn(self):
        listOfStrings = ["I", "ate", "an", "apple"]
        index = 3
        output = mazeGenerationHelpers.replaceAWithAOrAn(self,listOfStrings, index)
        self.assertEqual(output, ["I", "ate", "a/an", "apple"])

    def test_getWordIndex(self):
        sentenceString = ["I", "ate", "a/an", "apple", "for", "breakfast"]
        selectedWord = "apple"
        output = mazeGenerationHelpers.getWordIndex(self, sentenceString, selectedWord)
        self.assertEqual(output, 3)

    def test_getWordIndexWithCapitalSelection(self):
        sentenceString = ['As','Eric','ate','the','steaming','hot','pancakes,','his','mother','asked','him','if','he','was','excited','about','starting','at','the','new','school.']
        selectedWord = "Steaming"
        output = mazeGenerationHelpers.getWordIndex(self, sentenceString, selectedWord)
        self.assertEqual(output, 4)

    def test_formatWordForHtml_exhaustive(self):
        selectedMessyWord = "\"'apple\"$"
        selectedWord = "apple"
        index = 3
        sentenceSplitBySpaces = ["I", "ate", "an", "for", "breakfast"]
        output = mazeGenerationHelpers.formatWordForHtml(self, sentenceSplitBySpaces, selectedMessyWord ,selectedWord, index)
        self.assertEqual(output, ["I", "ate", "an", "\"", "'", "apple", "\"", "$", "for", "breakfast"])

    def test_formatSentenceForHtml(self):
        sentence = "I ate an \"apple\" for breakfast"
        selectedWord = "apple"
        output = mazeGenerationHelpers.formatSentenceForHtml(self, sentence, selectedWord)
        self.assertEqual(output, ['I', 'ate', 'a/an', '"', 'apple', '"', 'for', 'breakfast'])
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from random import shuffle,randrange

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.


# def testFunction():
#     # get the number of cards in the current collection, which is stored in
#     # the main window
#     cardCount = mw.col.cardCount()
#     # show a message box
#     showInfo("Card count: %d" % cardCount)

def getReviews():
    '''Gets all of the cards in the current deck that have been seen before. '''
    ids = mw.col.findCards("is:review deck:current")

    card = mw.col.getCard(ids[0])
    return ids


def quiz():
    '''Runs a multiple choice quiz'''

    cards = getReviews()
    
    mw.myWidget = widget = Quiz(6, cards)
    widget.show()
    
class QuizQuestion(QWidget):

    def __init__(self, cardid, othercards):
        super(QuizQuestion, self).__init__()

        self.cardid = cardid
        self.card = mw.col.getCard(cardid) #
        self.othercards = self.getothers(othercards) # These are the cards whose answers will also be shown

        self.doLayout()

    def getothers(self, otherids):
        others = []
        for cid in otherids:
            others.append(mw.col.getCard(cid)) # Get the cards coressponding to the ids

        return others

    def doLayout(self):
        
        layout = QHBoxLayout()
        realnote = self.card.note()
        
        
        # Prepare the answer section
        answerssection = QWidget()
        answers = QVBoxLayout()
        
        allnotes = [c.note() for c in self.othercards] # Get the notes to do with the other cards
        allnotes.append(realnote)
        shuffle(allnotes) # Shuffle them

        for note in allnotes:
            answers.addWidget(QRadioButton(note['Back']))

        answerssection.setLayout(answers)

        layout.addWidget(QLabel(realnote['Front']))
        layout.addWidget(answerssection)
        
        self.setLayout(layout)



class Quiz(QWidget):
    NUMBER_OF_ANSWERS = 4

    def __init__(self, noOfQuestions, cards):
        super(Quiz, self).__init__()
        self.questions = self.makeQuestions(noOfQuestions, cards)
        self.doLayout()

    def doLayout(self):
        layout = QVBoxLayout() # Vertical box layout
        
        for question in self.questions:
            layout.addWidget(question)

        self.setLayout(layout)

    def makeQuestions(self, noOfQuestions, cards):
        '''Gathers questions for a quiz'''
        questions = []
        cardidsused = [-1] # Keep track of the cards that we've already used so that we don't repeat them
        
        for _ in range(noOfQuestions):
            
            cardid = -1
            while cardid in cardidsused:
                cardid = randrange(0,len(cards))

            # We should now have a unqiue cardid
            questioncards = cards[cardid:cardid+Quiz.NUMBER_OF_ANSWERS]

            cardidsused.extend(range(cardid, cardid+Quiz.NUMBER_OF_ANSWERS)) # Add all the ids used to the list

            newQuestion = QuizQuestion(questioncards.pop(0), questioncards)

            questions.append(newQuestion)

        return questions


            


# create a new menu item, "test"
action = QAction("doQuiz", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(quiz)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


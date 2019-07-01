# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from random import shuffle

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
    
    mw.myWidget = widget = QuizQuestion(cards[0], cards[1:4])
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
        #answers.addWidget(QLabel(note['Back']))


        answerssection.setLayout(answers)

        layout.addWidget(QLabel(realnote['Front']))
        layout.addWidget(answerssection)
        
        self.setLayout(layout)
# create a new menu item, "test"
action = QAction("doQuiz", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(quiz)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


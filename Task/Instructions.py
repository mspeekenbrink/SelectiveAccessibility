#!/usr/bin/env python
from psychopy import visual, event, core

class Instructions():
    
    def __init__(self, win):
        
        instructionText = []
        txt = 'This experiment is a pre-test in order to find out the best wording and presentation format for general-knowledge questions. '
        txt += 'Specifically, we compare traditional methods that use general-knowledge questions and modern methods '
        txt += 'that analyze how quickly and accurately people recognize words.\n\n'
        txt += 'Some of the questions require a comparison with a given number. These numbers were chosen randomly, with a mechanism like a '
        txt += '"wheel of fortune." This is to minimise any influence they might have on your answers and so we can assess the impact of '
        txt += 'different question formats.\n\n'
        txt += 'Some questions require you to answer by pressing either the P or the Q key on the keyboard. The keys corresponding to the '
        txt += 'two possible answers will be displayed at the bottom of the screen. During these questions, please keep your forefingers on '
        txt += 'these two keys to enable you to answer quickly. Other questions will require you to type an answer using the number pad on '
        txt += 'the keyboard.\n\n'
        txt += 'Please answer all questions as accurately and quickly as possible.'
        instructionText.append(txt)
        
        txt = 'Part of the experiment is testing a new method for assessing general knowledge. It is designed to implicitly assess general '
        txt += 'knowledge by analysing how quickly people discriminate words from non-words. Collections of letters will be presented on '
        txt += 'the screen and, using the P and Q keys on the keyboard, you should, as quickly as you can, indicate whether the collection '
        txt += 'of letters has meaning for an English speaking person.\n\n'
        txt += 'For example:\n'
        txt += 'BRICK\t\tThis has meaning, because it is a small block used in building.\n'
        txt += 'COLGATE\t\tThis has meaning, because it is a brand of toothpaste.\n'
        txt += 'DOLPIP\t\tThis does not have meaning.\n'
        txt += 'EXCEED\t\tThis has meaning, because it means to surpass or go beyond.\n'
        txt += 'FACEBOOK\t\tThis has meaning, because it is a social networking website.\n'
        txt += 'GRESDOR\t\tThis does not have meaning.'
        instructionText.append(txt)
        
        txt = 'If you have any questions, please ask these to the experimenter now. Otherwise, you can continue with the experiment. \n\n'
        instructionText.append(txt)

        self.instructionText = instructionText
        self.continueText = 'Press any key to continue'
        
        self.win = win
        self.instructions = visual.TextStim(win, pos=[0,0],text='Press any key to start',wrapWidth=1.5)
        self.instructions.setHeight(.07)
        self.cont = visual.TextStim(win, pos=[.98,-.98], text = 'Press any key to continue', alignHoriz = 'right', alignVert = 'bottom')
        self.cont.setHeight(.07)
            
    def Run(self):
        self.instructions.draw()
        self.win.flip()#to show our newly drawn 'stimuli'
        #pause until there's a keypress
        event.waitKeys()
        # the following will loop through the instructionText array
        
        for i in range(len(self.instructionText)):
            self.instructions.setText(self.instructionText[i])
            self.instructions.draw()
            if(i < len(self.instructionText)):
                self.cont.draw()
            self.win.flip() #to show our newly drawn 'stimuli'
            event.waitKeys()

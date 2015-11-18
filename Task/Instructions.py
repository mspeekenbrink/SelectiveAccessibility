#!/usr/bin/env python
from psychopy import visual, event, core

class Instructions():
    
    def __init__(self, win, responses):
        
        instructionText = []
        
        txt = 'This experiment is designed to test different methods for the assessment of general knowledge. Specifically, '
        txt += 'variations on traditional methods that use general-knowledge questions will be compared with modern methods '
        txt += 'that analyse how quickly and accurately people respond to words.\n\n'

        txt += 'Some of the questions require a comparison with a given number. These numbers were chosen randomly, with a '
        txt += 'mechanism like a "wheel of fortune." This is to minimise any influence they might have on your answers and so '
        txt += 'we can assess the impact of different question formats. For these questions, you will respond using the keys '
        txt += 'marked blue or yellow on the keyboard. If a question requires you to provide a numerical answer, please use the '
        txt += 'number pad on the right of your keyboard.\n\n'
        
        txt += 'Please answer all questions as accurately and quickly as possible.'
        instructionText.append(txt)
        
        txt = 'A more modern method assessing general knowledge implicitly assesses general knowledge by analysing how '
        txt += 'quickly people discriminate words from non-words. Collections of letters will be presented on the screen and, using '
        txt += 'the blue and yellow keys on the keyboard, you should indicate whether the collection of letters has meaning for an '
        txt += 'English speaking person. The blue key corresponds to "' + responses[0] + '" and the yellow key to "' + responses[1] + '".\n\n'
        
        txt += 'For example, STEAVES does not have meaning, whilst AMAZING does (as it is a word). In addition, although they are '
        txt += 'proper nouns, LONDON, COLGATE, ALDI, IKEA and KIT-KAT also mean something to an English speaking person.\n\n'

        txt += 'Further examples are given below::\n'
        txt += 'BRICK\t\tThis has meaning (it is a word).\n'
        txt += 'DOLPIP\t\tThis does not have meaning.\n'
        txt += 'EXCEED\t\tThis has meaning (it is a word)\n'
        txt += 'FACEBOOK\t\tThis has meaning, because it is a social networking website.\n'
        txt += 'GRESDOR\t\tThis does not have meaning.'
        instructionText.append(txt)
        
        txt = 'In between sets of general knowledge tasks, you will be asked to memorize short sequences of consonants. '
        txt += 'You will see a sequence of consonants one by one on the screen. '
        txt += 'After each sequence, you will be asked to recall the sequence and type it in the correct order.'
        instructionText.append(txt)
        
        txt = 'If you have any questions, please ask the experimenter now. Otherwise, you can continue with the experiment. \n\n'
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

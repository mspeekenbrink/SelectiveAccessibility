#!/usr/bin/env python
from psychopy import visual, event, core

class Instructions():
    
    def __init__(self, win, responses):
        
        instructionText = []
        
        txt = 'This experiment is designed to test different methods for the assessment of general knowledge. Specifically, '
        txt += 'variations on traditional methods that use general-knowledge questions will be compared with modern methods '
        txt += 'that analyse how quickly and accurately people respond to words.'
        instructionText.append(txt)

        txt = 'Some of the questions require a comparison with a given number. These numbers were chosen randomly, with a '
        txt += 'mechanism like a "wheel of fortune." This is to minimise any influence they might have on your answers and so '
        txt += 'we can assess the impact of different question formats.\n\nFor these questions, you will respond using the keys '
        txt += 'marked blue or yellow on the keyboard.'
        instructionText.append(txt)
        
        txt = 'Some of the questions require you to provide a numerical answer. Please use the '
        txt += 'number pad on the right of your keyboard to answer these questions.\n\n'
        instructionText.append(txt)
        
        txt = 'A more modern method implicitly assesses general knowledge by analysing how '
        txt += 'quickly people discriminate words from non-words.\n\n'
        instructionText.append(txt)
        
        txt = 'Collections of letters will be presented on the screen and, using '
        txt += 'the blue and yellow keys on the keyboard, you should indicate whether the collection of letters has meaning for an '
        txt += 'English speaking person.\n\n'
        txt += 'Please answer these questions as quickly and accurately as possible.'
        instructionText.append(txt)
        
        txt = 'The question is "DOES IT HAVE MEANING?"\n\n'
        txt += 'The blue key corresponds to "' + responses[0] + '" and the yellow key to "' + responses[1] + '".\n\n'
        
        txt += 'For example, STEAVES does not have meaning, whilst AMAZING does (as it is a word). In addition, although they are '
        txt += 'proper nouns, LONDON, COLGATE, ALDI, IKEA and KIT-KAT also mean something to an English speaking person.\n\n'

        txt += 'Further example answers are given below:\n'
        txt += 'BRICK\t\tYES  (it is a word)\n'
        txt += 'DOLPIP\t\tNO\n'
        txt += 'EXCEED\t\tYES (it is a word)\n'
        txt += 'FACEBOOK\t\tYES (it is a social networking website)\n'
        txt += 'GRESDOR\t\tNO'
        instructionText.append(txt)
        
        txt = 'Between sets of general knowledge tasks, you will be asked to memorize short sequences of consonants. '
        instructionText.append(txt)
        
        txt = 'Whenever you see a cross in the middle of the screen please look at it and be ready to respond as quickly and accurately as possible.'
        instructionText.append(txt)
        
        txt = 'If you have any questions, please ask the experimenter now. Otherwise, you can continue with the experiment.'
        instructionText.append(txt)
        
        txt = 'Remember to answer all questions as quickly and accurately as possible.'
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

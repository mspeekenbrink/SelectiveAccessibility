import random, math, array, random, csv
import Button
from psychopy import core,visual,event

class Task:

    ITI = 1.0
   
    def __init__(self,win,filename,tasknr,questionText,unit,comparativeOptions,which):

        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'
        self.win = win
        self.tasknr = tasknr
        self.questionText = questionText
        self.comparativeOptions = comparativeOptions
        if which == 1:
            self.instructionText = 'Q = ' + comparativeOptions[0] + ', ' + 'P = ' + comparativeOptions[1]
        else:
            self.instructionText = 'Use the number pad to type in your answer and press enter'
        self.unit = unit
        self.which = which
        self.trial = 1
        
        # visuals
        self.Question = visual.TextStim(self.win,text=self.questionText,pos=(.0,.3),height=.08,alignVert='center',wrapWidth=1.5)
        self.Instructions = visual.TextStim(self.win,text=self.instructionText,pos=(.0,-.8),height=.07,alignVert='center',wrapWidth=1.5)
        self.Response = visual.TextStim(self.win,text="___" + unit,pos=(.0,.0),height=.08,alignVert='center',wrapWidth=1.5)
        self.trialClock = core.Clock()
        self.datafile.write('taskNr,question,response,RT\n')
        
    def Run(self):
        if self.which == 1:

            # display question
            self.Question.draw()
            self.Instructions.draw()
            self.win.flip()
            # start RT measurement
            self.trialClock.reset()
            # wait for response
            cont = False
            while (cont == False):
                for key in event.getKeys():
                    if key in ['p','q']:
                        RT = self.trialClock.getTime()
                        if key == 'p':
                            response = self.comparativeOptions[1]
                        else:
                            response = self.comparativeOptions[0]
                        cont = True
                    if key in ['escape']:
                        self.win.close()
                        core.quit()
            
        if self.which == 2:
            text=''
            # until return pressed, listen for letter keys & add to text string
            self.trialClock.reset()
            while event.getKeys(keyList=['return'])==[]:
                letterlist=event.getKeys(keyList=['1','2','3','4','5','6','7','8','9','0','backspace'])
                for l in letterlist:
                    #if key isn't backspace, add key pressed to the string
                    if l !='backspace':
                        text+=l
                    #otherwise, take the last letter off the string
                    elif len(text)>0:
                        text=text[:-1]
                #continually redraw text onscreen until return pressed
                self.Response.setText(text + self.unit)
                self.Question.draw()
                self.Response.draw()
                self.Instructions.draw()
                self.win.flip()
            
            # get RT
            RT = self.trialClock.getTime()
            # get response
            response = text
            # clear keypresses
            event.clearEvents()
        
        # write data
        self.datafile.write(
                str(self.tasknr) + ',' +
                str(''.join([x.encode('latin-1') for x in self.questionText])) + ',' +
                response + ',' +
                str(1000*RT) + '\n')
        
        # ITI
        self.win.flip()
        core.wait(self.ITI)
                    
        self.datafile.close()

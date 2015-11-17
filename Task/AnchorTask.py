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
        self.unit = unit
        self.which = which
        self.trial = 1
        
        # visuals
        self.Instructions = visual.TextStim(self.win,text=self.questionText,pos=(.0,.3),height=.08,alignVert='center',wrapWidth=1.5)
        self.Response = visual.TextStim(self.win,text="___" + unit,pos=(.0,.0),height=.08,alignVert='center',wrapWidth=1.5)
        self.Button1 = Button.Button(self.win,pos=[-0.3,-0.3],size=[.3,.2],label=comparativeOptions[0],name=comparativeOptions[0],
                                      textSize=0.6,fillColor=[.2,.2,.2],hoverFillColor=[.1,.1,.1],
                                      lineColor=[-.3,-.3,-.3],hoverLineColor=[-.4,-.4,-.4])
        self.Button2 = Button.Button(self.win,pos=[0.3,-0.3],size=[.3,.2],label=comparativeOptions[1],name=comparativeOptions[1],
                                      textSize=0.6,fillColor=[.2,.2,.2],hoverFillColor=[.1,.1,.1],
                                      lineColor=[-.3,-.3,-.3],hoverLineColor=[-.4,-.4,-.4])
        self.trialClock = core.Clock()
        self.datafile.write('taskNr,question,response,RT\n')
        
    def Run(self):
        if self.which == 1:

            # start RT measurement
            self.trialClock.reset()
            # wait for response
            while self.Button1.noResponse and self.Button2.noResponse:
                # allow to quit
                for key in event.getKeys():
                    if key in ['escape']:
                        done = True
                        core.quit()
                self.Instructions.draw()
                self.Button1.draw()
                self.Button2.draw()
                self.win.flip()
            # get RT measurement
            RT = self.trialClock.getTime() # could have done with button
            # get response
            if not self.Button1.noResponse:
                response = self.Button1.name
            else:
                response = self.Button2.name
            
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
                self.Instructions.draw()
                self.Response.draw()
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

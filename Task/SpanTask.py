import random, math, array, random, csv
from psychopy import core,visual,event

class Task:

    fixTime = 1.0 # fixation time in seconds
    displayTime = 0.8 # display time for consonants in seconds
    intervalTime = 0.2 # interval between consonants in seconds
    ITI = 1.0 # inter-trial interval in seconds
    
    def __init__(self,win,filename,tasknr):

        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'
        self.win = win
        self.tasknr = tasknr
        self.consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
        
        # visuals
        self.Instructions = visual.TextStim(self.win,text="Please type in the letters in the correct order and press enter to confirm",pos=(.0,.8),height=.08,alignVert='center',wrapWidth=1.5)
        self.Stimulus = visual.TextStim(self.win,text="",pos=(.0,.0),height=.15,alignVert='center',wrapWidth=1.5)
        self.Response = visual.TextStim(self.win,text="___",pos=(.0,.0),height=.15,alignVert='center',wrapWidth=1.5)
        self.fixation = visual.ShapeStim(win,
            units='pix',
            lineColor='white',
            lineWidth=2.0,
            vertices=((-25, 0), (25, 0), (0,0), (0,25), (0,-25)),
            closeShape=False,
            pos= [0,0])
        self.trialClock = core.Clock()
        # write header for data
        self.datafile.write('taskNr,trial,stimulus,response,RT\n')
        
            
    def Run(self):
        running = True
        trial = 1
        length = 4
        while running:
            
            # get a random sequence of consonants
            random.shuffle(self.consonants)
            # to write this to the data
            stimulus = ''
            for i in range(length):
                stimulus += self.consonants[i]
            
            # display fixation cross
            self.fixation.draw()
            self.win.flip()
            core.wait(self.fixTime)
            # display consonants
            for i in range(length):
                self.Stimulus.setText(self.consonants[i])
                self.Stimulus.draw()
                self.win.flip()
                core.wait(self.displayTime)
                self.win.flip()
                core.wait(self.intervalTime)
            
            text=''
            #until return pressed, listen for letter keys & add to text string
            self.trialClock.reset()
            while event.getKeys(keyList=['return'])==[]:
                letterlist=event.getKeys(keyList=self.consonants + ['backspace'])
                for l in letterlist:
                    #if key isn't backspace, add key pressed to the string
                    if l !='backspace':
                        text+=l
                    #otherwise, take the last letter off the string
                    elif len(text)>0:
                        text=text[:-1]
                #continually redraw text onscreen until return pressed
                self.Instructions.draw()
                self.Response.setText(text)
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
                str(trial) + ',' +
                str(stimulus) + ',' +
                str(response) + ',' +
                str(1000*RT) + '\n')
            
            # ITI    
            self.win.flip()
            core.wait(self.ITI)
            
            trial += 1
            length += 1
            
            if length > 7:
                running = False
                    
        self.datafile.close()

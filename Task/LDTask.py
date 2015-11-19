import random, math, array, random, csv
from psychopy import core,visual,event

class Task:

    fixTime = 0.8 # fixation time in seconds
    ITI = 1.0 # inter-trial interval in seconds
    
    def __init__(self,win,filename,tasknr,taskid,responses):

        # Adapted from http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
        reader = csv.DictReader(open('Files/LDT' + str(taskid) + '.csv'))
        result = []
        for row in reader:
            result.append(row)
        
        # determine whether there are practice items to go first
        practice_id = []
        word_id = []
        for i in range(len(result)):
            if result[i]['type'] == 'practice':
                practice_id.append(i)
            else:
                word_id.append(i)
        
        # randomize order
        random.shuffle(practice_id)
        random.shuffle(word_id)        
        stimuli = []
        for i in range(len(practice_id)):
            stimuli.append(result[practice_id[i]])
        for i in range(len(word_id)):
            stimuli.append(result[word_id[i]])
        
        self.instructionText = 'Q = ' + responses[0] + ', ' + 'P = ' + responses[1]
        self.stimuli = stimuli
        self.ntrials = len(stimuli)
        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'
        self.win = win
        self.tasknr = tasknr
        self.trial = 1
        self.responses = responses
        
        # visuals
        self.Instructions = visual.TextStim(self.win,text=self.instructionText,pos=(.0,-.8),height=.07,alignVert='center',wrapWidth=1.5)
        self.Stimulus = visual.TextStim(self.win,text="sadjhgsad",pos=(.0,.0),height=.1,alignVert='center',wrapWidth=1.5)
        self.fixation = visual.ShapeStim(win,
            units='pix',
            lineColor='white',
            lineWidth=3.0,
            vertices=((-25, 0), (25, 0), (0,0), (0,25), (0,-25)),
            closeShape=False,
            pos= [0,0])        
        
        self.trialClock = core.Clock()
        
        self.datafile.write('taskNr,trial,type,stimulus,response,RT\n')
        
            
    def Run(self):
        running = True
        trial = 1
        
        while running:
        
            # display fixation cross
            stimulus = self.stimuli[trial-1]['word']
            stype = self.stimuli[trial-1]['type']
            self.Stimulus.setText(stimulus)
            self.fixation.draw()
            self.win.flip()
            core.wait(self.fixTime)
            
            # display word
            cont = False
            event.clearEvents()
            self.Stimulus.draw()
            #self.Instructions.draw()
            self.win.flip()
            
            self.trialClock.reset()
            
            # wait for response
            while (cont == False):
                for key in event.getKeys():
                    if key in ['p','q']:
                        RT = self.trialClock.getTime()
                        if key == 'p':
                            response = self.responses[1]
                        else:
                            response = self.responses[0]
                        cont = True
                    if key in ['escape']:
                        self.win.close()
                        core.quit()
            
            # write data
            self.datafile.write(
                str(self.tasknr) + ',' +
                str(trial) + ',' +
                str(stype) + ',' +
                str(stimulus) + ',' +
                str(response) + ',' +
                str(1000*RT) + '\n')
            
            # ITI
            self.win.flip()
            core.wait(self.ITI)
            
            trial += 1
            
            if trial > self.ntrials:
                running = False
                        
        self.datafile.close()

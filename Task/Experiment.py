#!/usr/bin/env python
import random, csv
from psychopy import visual, event, core, data, gui, misc
import numpy as np
import Instructions, AnchorTask, LDTask, SpanTask
  
# some variables
interTaskTime = 3
resolution = (1600,900)
responses = ['word','nonword']
taskAnchors = [['15'],['600'],['10','18'],['8,000','20,000']]
comparativeQuestions = ['Is Big Ben taller or shorter than 15 meters high?',
                        'Is the M25 longer or shorter than 600 miles?',
                        u'Is the annual average temperature in the UK higher or lower than [anchor]\u00B0',
                        u'Is the average price of a new car in the UK higher or lower than \u00A3[anchor]?']
comparativeOptions = [['taller','shorter'],
                   ['longer','shorter'],
                   ['higher','lower'],
                   ['higher','lower']]
                   
absoluteQuestions = ['How tall is Big Ben?',
                     'How long is the M25?',
                     'What is the annual average temperature in the UK?',
                     'What is the average price of a new car in the UK?']
units = [' metres',
         ' miles',
         u'\u00B0C',
         u' \u00A3']
         
# Admin
expInfo = {'date':data.getDateStr(),'subject':'1'}

#present a dialogue to change params
ok = False
while(not ok):
    dlg = gui.DlgFromDict(expInfo, title='Accessibility', fixed=['date'],order=['date','subject'])
    if dlg.OK:
        misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
        ok = True
    else:
        core.quit()#the user hit cancel so exit


# setup data file
fileName = 'Data/' + str(expInfo['subject']) + expInfo['date'] + '.csv'

# Read in counterbalancing etc.
# Adapted from http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
reader = csv.DictReader(open('Files/ExpStructure.csv'))
result = []
for row in reader:
    if row['id'] == str(expInfo['subject']):
        result = row
if result['whichExpt.First'] == 1:
    taskOrder = random.sample([1,2],2) + [3,4]
    anchors = [taskAnchors[0],taskAnchors[1],taskAnchors[2][int(result['E1anchor']) - 1],taskAnchors[3][int(result['E2anchor']) - 1]]
else:
    taskOrder = random.sample([1,2],2) + [4,3]
    anchors = [taskAnchors[0],taskAnchors[1],taskAnchors[2][int(result['E1anchor']) - 1],taskAnchors[3][int(result['E2anchor']) - 1]]
for i in [2,3]:
    comparativeQuestions[i] = comparativeQuestions[i].replace('[anchor]',anchors[i])
random.shuffle(responses) # randomize

dataFile = open(fileName, 'w') #a simple text file with 'comma-separated-values'
dataFile.write('subject = ' + str(expInfo['subject']) + "; date = " + str(expInfo['date']) + '\n')
dataFile.write('taskOrder = ' + str(taskOrder) + "; responses (P,Q) = " + str(responses) + '\n')
dataFile.close()


#create a window to draw in
myWin =visual.Window(resolution, allowGUI=False,
    bitsMode=None, units='norm', color=(0,0,0))

instr = Instructions.Instructions(myWin)
instr.Run()


for tsk in range(4):
    task = AnchorTask.Task(myWin,fileName,tsk+1,comparativeQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],1)
    task.Run()
    core.wait(interTaskTime)
    task = LDTask.Task(myWin,fileName,tsk+1,taskOrder[tsk],responses)
    task.Run()
    core.wait(interTaskTime)
    task = AnchorTask.Task(myWin,fileName,tsk+1,absoluteQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],2)
    task.Run()
    if tsk < 3:
        core.wait(interTaskTime)
        task = SpanTask.Task(myWin,fileName,tsk+1)
        task.Run()


endText = "This is the end of the experiment. \n\n"
endText += "Thank your for your participation."
end = visual.TextStim(myWin, pos=[0,0],text=endText)
end.draw()
myWin.flip()

done = False
while not done:
    for key in event.getKeys():
        if key in ['escape']:
            done = True
            core.quit()

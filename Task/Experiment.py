#!/usr/bin/env python
import random, csv
from psychopy import visual, event, core, data, gui, misc
import numpy as np
import Instructions, AnchorTask, LDTask, SpanTask
  
# some variables
interTaskTime = 3
interTaskTime2 = 6
resolution = (1600,900)
responses = ['yes','no']
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
         u'\u00A3']
         
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
fileName = 'Data/' + 'Subject' + str(expInfo['subject']) + '_' + expInfo['date'] + '.csv'

# Read in counterbalancing etc.
# Adapted from http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
reader = csv.DictReader(open('Files/ExpStructure.csv'))
result = []
for row in reader:
    if row['id'] == str(expInfo['subject']):
        result = row
if result['whichExpt.First'] == '1':
    taskOrder = random.sample([1,2],2) + [3,4]
    anchors = [taskAnchors[0],taskAnchors[1],taskAnchors[2][int(result['E1anchor']) - 1],taskAnchors[3][int(result['E2anchor']) - 1]]
else:
    taskOrder = random.sample([1,2],2) + [4,3]
    anchors = [taskAnchors[0],taskAnchors[1],taskAnchors[2][int(result['E1anchor']) - 1],taskAnchors[3][int(result['E2anchor']) - 1]]
for i in [2,3]:
    comparativeQuestions[i] = comparativeQuestions[i].replace('[anchor]',anchors[i])
if result['wordKey'] == "P":
    responses = [responses[1],responses[0]]

dataFile = open(fileName, 'w') #a simple text file with 'comma-separated-values'
dataFile.write('subject = ' + str(expInfo['subject']) + "; date = " + str(expInfo['date']) + '\n')
dataFile.write('taskOrder = ' + str(taskOrder) + "; responses (Q/blue,P/yellow) = " + str(responses) + '\n')
dataFile.close()

#create a window to draw in
myWin =visual.Window(resolution, allowGUI=False, bitsMode=None, units='norm', color=(0,0,0))

instructions = visual.TextStim(myWin,pos=[0,0],text="",height=.08,alignHoriz='center',wrapWidth=1.2)
LDTtext = 'Place your index fingers on the blue and yellow keys now.\n\nDOES IT HAVE MEANING?\n\nblue = ' + responses[0] + '\nyellow = ' + responses[1] + '\n\nRespond as quickly and accurately as possible.'
LDTtext2 = 'Place your index fingers on the blue and yellow keys now.\n\nDOES IT HAVE MEANING?\n\nRespond as quickly and accurately as possible.'
SpanText = "You will now be shown letters one at a time. Please memorize them and recall them in order when asked."

BetweenText = []
txt = 'This is the end of the first round of tasks. There will be three more rounds just like this one. '
txt += 'In the "DOES IT HAVE MEANING?" task, please respond as quickly as possible. '
txt += '\n\nThe blue key will always correspond to "' + responses[0] 
txt += '" and the yellow key to "' + responses[1] + '". Make sure your index fingers rest on these keys.\n\nIf you have any questions, ask the experimenter now. '
txt += 'Take a short break if you want to. Press any key to continue to the next block of the experiment.'
BetweenText.append(txt)
txt = 'This is the end of the second round of tasks. There will be two more rounds just like this one. '
txt += 'In the "DOES IT HAVE MEANING?" task, please respond as quickly as possible. '
txt += '\n\nThe blue key will always correspond to "' + responses[0] 
txt += '" and the yellow key to "' + responses[1] + '". Make sure your index fingers rest on these keys.\n\n'
txt += 'Take a short break if you want to. Press any key to continue to the next block of the experiment.'
BetweenText.append(txt)
txt = 'This is the end of the third round of tasks. There will be one more round just like this one. '
txt += 'In the "DOES IT HAVE MEANING?" task, please respond as quickly as possible. '
txt += '\n\nThe blue key will always correspond to "' + responses[0] 
txt += '" and the yellow key to "' + responses[1] + '". Make sure your index fingers rest on these keys.\n\n'
txt += 'Take a short break if you want to. Press any key to continue to the next block of the experiment.'
BetweenText.append(txt)

instr = Instructions.Instructions(myWin,responses)
instr.Run()


for tsk in range(4):
    task = AnchorTask.Task(myWin,fileName,tsk+1,comparativeQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],1)
    task.Run()
    if tsk == 0:
        instructions.setText(LDTtext)
    else:
        instructions.setText(LDTtext2)
    instructions.draw()
    myWin.flip()
    if tsk == 0:
        core.wait(interTaskTime2-.5)
        myWin.flip()
        core.wait(0.5)
    else:
        core.wait(interTaskTime-.5)
        myWin.flip()
        core.wait(0.5)
    task = LDTask.Task(myWin,fileName,tsk+1,taskOrder[tsk],responses)
    task.Run()
    core.wait(interTaskTime-.5)
    myWin.flip()
    core.wait(0.5)
    task = AnchorTask.Task(myWin,fileName,tsk+1,absoluteQuestions[taskOrder[tsk]-1],units[taskOrder[tsk]-1],comparativeOptions[taskOrder[tsk]-1],2)
    task.Run()
    if tsk < 3:
        instructions.setText(SpanText)
        instructions.draw()
        myWin.flip()
        if tsk == 0:
            core.wait(interTaskTime2-.5)
            myWin.flip()
            core.wait(0.5)
        else:
            core.wait(interTaskTime-.5)
            myWin.flip()
            core.wait(0.5)
        task = SpanTask.Task(myWin,fileName,tsk+1)
        task.Run()
        instructions.setText(BetweenText[tsk])
        instructions.draw()
        myWin.flip()
        event.waitKeys()

endText = "This is the end of the experiment. \n\n"
endText += "Thank you for your participation."
instructions.setText(endText) 
instructions.draw()
myWin.flip()

done = False
while not done:
    for key in event.getKeys():
        if key in ['escape']:
            done = True
            core.quit()

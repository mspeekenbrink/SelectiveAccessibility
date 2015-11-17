import sys
from psychopy import core, visual, gui, data, misc, event, sound
import time, random, math

from psychopy.constants import *

class Button:
    """myButton = <create your text, image, movie, ...> 
       myButton = controls.Button(myWin) 
       while myButton.noResponse: 
           myButton.draw()   
           myWin.flip() 
           rating = myRatingScale.getRating() 
           decisionTime = myRatingScale.getRT()"""
    def __init__(self,
                win,
                pos,
                size,
                units="",
                label="",
                textColor='black',
                textSize=1,
                textFont='Helvetica Bold',
                fillColor=None,
                lineColor='black',
                lineWidth=1,
                hoverFillColor=None,
                hoverLineColor='white',
                minTime = 0.0,
                maxTime = 0.0,
                name=''):
        self.win = win
        
        # internally work in norm units, restore to orig units at the end of __init__:
        self.savedWinUnits = self.win.units
        self.win.units = 'norm'
        
        self.position = pos
        self.label = label
        self.size = size
        
        
        if(fillColor == None):
            self.fillColor = self.win.color
        else:
            self.fillColor = fillColor

        self.currentFillColor = self.fillColor
        
        if(hoverFillColor == None):
            self.hoverFillColor = self.win.color
        else:
            self.hoverFillColor = hoverFillColor
        
        self.textColor = textColor
        self.textSize = size[1]*textSize
        self.textFont = textFont
        
        self.currentLineColor = self.lineColor = lineColor
        self.hoverLineColor = hoverLineColor
         
        self.lineWidth = lineWidth
        
        #unit conversions 
        #if len(units): self.units = units 
        #else: self.units = self.win.units 
        #if self.units=='norm': self._winScale='norm' 
        #else: self._winScale='pix' #set the window to have pixels coords 
        #'rendered' coordinates represent the stimuli in the scaled coords of the window 
        #(i.e. norm for units==norm, but pix for all other units)
          
        #self.labelStim = visual.TextStim(win=self.win,pos=self.pos,text=self.label)

        #self.boxStim = visual.ShapeStim(win=self.win,lineWidth=3,fillColor=self.fillColor,lineColor=self.lineColor,pos=[self.pos[0]*self.win.size[0],self.pos[1]*self.win.size[1]],vertices=((-.5*size[0]*self.win.size[0], -.5*size[1]*self.win.size[1]), (-5*size[0]*self.win.size[0], .5*size[1]*self.win.size[1]), (.5*size[0]*self.win.size[0], .5*size[1]*self.win.size[1]), (5*size[0]*self.win.size[0],-.5*size[1]*self.win.size[1])),units='pix')
        self.active = True
        self.hover = False
        self.clicked = False
        
        self.name = name
        
        self.myClock = core.Clock() # for decision time
        try:
            self.minimumTime = float(minTime)
        except ValueError:
            self.minimumTime = 0.0
        self.minimumTime = max(self.minimumTime, 0.)
        try:
            self.maximumTime = float(maxTime)
        except ValueError:
            self.maximumTime = 0.0
        self.timedOut = False
        
        self.myMouse = event.Mouse(win=self.win, visible=True)
        self.decisionTime = 0.0
        self.firstDraw = True
        self.noResponse = True
        
        self._initBox()
        self._setText()
        
        self.win.units = self.savedWinUnits # restore

    def _initBox(self):
        self._calcVertices()
        self._setBox()
                            
    def _calcVertices(self):

        # define self.box:
        self.boxtop = boxtop = self.position[1] + .5*self.size[1]
        self.boxbot = boxbot = self.position[1] - .5*self.size[1]
        self.boxleft = boxleft = self.position[0] - .5*self.size[0]
        self.boxright = boxright = self.position[0] + .5*self.size[0]

        # define a rectangle with rounded corners; for square corners, set delta2 to 0
        delta = 0.025
        delta2 = delta / 7
        self.boxVertices = [
            [boxleft,boxtop-delta], [boxleft+delta2,boxtop-3*delta2],
            [boxleft+3*delta2,boxtop-delta2], [boxleft+delta,boxtop],
            [boxright-delta,boxtop], [boxright-3*delta2,boxtop-delta2],
            [boxright-delta2,boxtop-3*delta2], [boxright,boxtop-delta],
            [boxright,boxbot+delta],[boxright-delta2,boxbot+3*delta2],
            [boxright-3*delta2,boxbot+delta2], [boxright-delta,boxbot],
            [boxleft+delta,boxbot], [boxleft+3*delta2,boxbot+delta2],
            [boxleft+delta2,boxbot+3*delta2], [boxleft,boxbot+delta] ]
            
    def _setBox(self):
        if not sys.platform.startswith('linux'):
            self.boxStim = visual.ShapeStim(win=self.win, vertices=self.boxVertices,
                            fillColor=self.currentFillColor, lineColor=self.currentLineColor,
                            lineWidth=self.lineWidth,
                            name=self.name+'.box')
        else: # interpolation looks bad on linux, as of Aug 2010
            self.boxStim = visual.ShapeStim(win=self.win, vertices=self.boxVertices,
                            fillColor=self.currentFillColor, lineColor=self.currentLineColor,
                            lineWidth=self.lineWidth,
                            interpolate=False, name=self.name+'.box')
    
    def _setText(self):
        self.textStim = visual.TextStim(win=self.win, text=self.label, font=self.textFont,
                            pos=self.position,
                            height=self.textSize, color=self.textColor,
                            #colorSpace=self.textColorSpace, 
                            autoLog=False)
        self.textStim.setFont(self.textFont)

        #self.acceptTextColor = markerColor
        #if markerColor in ['White']:
        #    self.acceptTextColor = 'Black'
    
    def _setActive(self,active):
        if active:
            self.active = True
        else:
            self.active = False
        
    def _setHover(self,hover):
        if hover:
            self.hover = True
            self.currentLineColor = self.hoverLineColor
            self.currentFillColor = self.hoverFillColor
            self._setBox()
        else:
            self.hover = False
            self.currentLineColor = self.lineColor
            self.currentFillColor = self.fillColor
            self._setBox()
        
    def setLabel(self,label):
        self.label = str(label)
        self._setText()
        
    def setActive(self,active):
        if active:
            if not self.active: 
                self._setActive(True)
        else:
            if self.active: 
                self._setActive(False)
                
#    def setVertices(self,value=None):
#        """Set the xy values of the vertices (relative to the centre of the field). 
#           Values should be:
#             - an array/list of Nx2 coordinates.""" 
#        #make into an array
#        if type(value) in [int, float, list, tuple]:
#            value = numpy.array(value, dtype=float) 
#        #check shape
#        if not (value.shape==(2,) \
#            or (len(value.shape)==2 and value.shape[1]==2)
#            ):
#                raise ValueError("New value for setXYs should be 2x1 or Nx2")
#                
#        self.vertices=value 
#        self.needVertexUpdate=True
#        
#    def _calcVerticesRendered(self):
#        self.needVertexUpdate=False
#        if self.units in ['norm', 'pix']:
#            self._verticesRendered=self.vertices
#            self._posRendered=self.pos
#        elif self.units in ['deg', 'degs']: 
#            self._verticesRendered=psychopy.misc.deg2pix(self.vertices, self.win.monitor)
#            self._posRendered=psychopy.misc.deg2pix(self.pos, self.win.monitor)
#        elif self.units=='cm':
#            self._verticesRendered=psychopy.misc.cm2pix(self.vertices, self.win.monitor)
#            self._posRendered=psychopy.misc.cm2pix(self.pos, self.win.monitor)


    def draw(self,win=None):
        #if self.needVertexUpdate: self._calcVerticesRendered()
        #if win==None: win=self.win
        
        if self.firstDraw:
            self.firstDraw = False
            self.myClock.reset()
            self.status = STARTED
            self.history = [(None, 0.0)]
        
        mouseX, mouseY = self.myMouse.getPos() # done above
        # handle hover if active:
        if self.active:
            if self.boxStim.contains(mouseX, mouseY):
                if not self.hover:
                    self._setHover(True)
            else:
                if self.hover:
                    self._setHover(False)
                
        self.boxStim.draw()
        self.textStim.draw()
        
        if self.boxStim.contains(mouseX, mouseY):
            if self.myMouse.getPressed()[0]: # if mouse (left click) is pressed...
                # if in box and enough time has elapsed:
                self.clicked = True
                if self.active:
                    if (self.myClock.getTime() > self.minimumTime and
                        self.boxStim.contains(mouseX, mouseY)):
                        self.noResponse = False # accept the currently marked value
                        #self.history.append((self.getRating(), self.getRT())) # RT when accept pressed
                        #logging.data('RatingScale %s: (mouse response) rating=%s' %
                        #    (self.name, unicode(self.getRating())) )

                    # decision time = time from the first .draw() to when 'accept' was pressed:
                    if not self.noResponse and self.decisionTime == 0:
                        self.decisionTime = self.myClock.getTime()
                        #logging.data('Button %s: RT=%.3f' % (self.name, self.decisionTime))
                        # only set this once: at the time 'accept' is indicated by subject
                        # minimum time is enforced during key and mouse handling
                        self.status = FINISHED

        # build up response history:
        #tmpRating = self.getRating()
        #if self.history[-1][0] != tmpRating:
        #    self.history.append((tmpRating, self.getRT())) # tuple

        # restore user's units:
        self.win.units = self.savedWinUnits
        
    def reset(self):
        """Restores the rating-scale to its post-creation state.

The history is cleared, and the status is set to NOT_STARTED. Does not
restore the scale text description (such reset is needed between
items when rating multiple items)
"""
        # only resets things that are likely to have changed when the ratingScale instance is used by a subject
        self.noResponse = True
        
        self.clicked = False

        self.firstDraw = True # triggers self.myClock.reset() at start of draw()
        self.decisionTime = 0

        #self.frame = 0 # a counter used only to 'pulse' the 'accept' box
        self._setHover(False)
        self._setBox()
        self._setText()
        #logging.exp('Button %s: reset()' % self.name)
        self.status = NOT_STARTED
        self.history = None
        
    def getRT(self):
        """Returns the seconds taken to click the button (or to indicate skip).
Returns None if no rating available, or maxTime if the response timed out.
Returns the time elapsed so far if no rating has been accepted yet (e.g.,
for continuous usage).
"""
        if self.status != FINISHED:
            return self.myClock.getTime()
        if self.noResponse:
            if self.timedOut:
                return self.maximumTime
            return None
        return self.decisionTime

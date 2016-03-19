#! /usr/bin/env python

from Tkinter import *
from types import *
import math, random, time, sys, os, tempfile, copy
from optparse import OptionParser
import subprocess

#
# Basics of the program
#

WINDOW_WIDTH_IPHONE5  = 568
WINDOW_HEIGHT_IPHONE5 = 320


# 
# Safely delete an item from the canvas (if it exists)
# - assumes that deleted items are set to -1
# - generally used by setting the item to the return value here
# 
def SafeDelete(canvas, item):
    if item != -1:
        canvas.delete(item)
    return 

# called when something is horribly wrong
def Abort(str):
    print 'ABORTING [%s]' % str
    exit(1)


class Level:
    def __init__(self):
        self.number = -1
        self.text   = ''
        self.boxes  = {}
        self.maxID  = 0
        return

    def SetNumber(self, number):
        self.number = number
        return

    def SetText(self, text):
        self.text   = text
        return

    def AddBox(self, x1, y1, x2, y2, mode):
        if x1 > x2:
            tmp = x1
            x1  = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1  = y2
            y2 = tmp
        uid = self.maxID
        self.maxID += 1
        self.boxes[uid] = {'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2, 'mode':mode, 'uid':uid}
        return uid

    def Length(self):
        return len(self.boxes)

    def GetBox(self, tid):
        assert(tid in self.boxes)
        return self.boxes[tid]

    def DeleteBox(self, tid):
        assert(tid in self.boxes)
        self.boxes[tid] = {'x1': -1, 'y1': -1, 'x2': -1, 'y2': -1, 'mode': -1, 'uid': -1}

    def PrintBoxes(self):
        print 'Boxes:'
        for i in range(len(self.boxes)):
            print i, self.boxes[i]
        print ''

    def Load(self, outdir, level):
        fname = outdir + '/' + str(level)
        if os.path.isfile(fname):
            tmpBox = []
            fd = open(fname)
            for line in fd:
                tmp = line.split()
                if tmp[0] == 'box':
                    x1, y1, x2, y2, mode = int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])
                    tmpBox.append({'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2, 'mode':mode})
                    print 'append', tmpBox[len(tmpBox)-1]
                else:
                    print 'error: malformed line, skipping (bad line %s)' % line.strip()
            fd.close()

            # now, read it all in, so populate
            self.maxID = 0
            self.boxes = {}
            for i in range(len(tmpBox)):
                self.boxes[i] = {'x1':tmpBox[i]['x1'], 'y1':tmpBox[i]['y1'], 'x2':tmpBox[i]['x2'], 'y2':tmpBox[i]['y2'],
                                 'mode':tmpBox[i]['mode'], 'uid':self.maxID}
                self.maxID += 1
                
        else:
            print 'warning: cannot find file %s' % fname

    def Save(self, outdir, level):
        fname = outdir + '/' + str(level)
        fd = open(fname, 'w')
        for i in range(len(self.boxes)):
            b = self.boxes[i]
            print 'b is', b
            if b['uid'] != -1:
                outstr = 'box %3d %3d %3d %3d %3d\n' % (b['x1'], b['y1'], b['x2'], b['y2'], b['mode'])
                fd.write(outstr)
        fd.close()

# helper functions for buttons
def Update():
    global Ctrl
    Ctrl.DoUpdate()

def ModeZero():
    global Ctrl
    Ctrl.ModeZero()

def ModeOne():
    global Ctrl
    Ctrl.ModeOne()

def ModeTwo():
    global Ctrl
    Ctrl.ModeTwo()

#
# main work is done in this class
#
class Controller:
    def DoUpdate(self):
        self.UpdateLevelText(self.e1.get())
        self.el.set('')
    
    def __init__(self, infile):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH_IPHONE5, height=WINDOW_HEIGHT_IPHONE5)
        self.canvas.pack()

        self.f1 = Frame(height=1)
        self.f1.pack(fill=X)

        self.l1 = Label(self.root, text='Level text:')
        self.l1.pack(side=LEFT, in_=self.f1)

        self.e1 = Entry(self.root, width=55)
        self.e1.pack(side=LEFT, in_=self.f1)
        self.b1 = Button(self.root, text='Update', command=Update)
        self.b1.pack(side=LEFT, in_=self.f1)

        self.f2 = Frame(height=1)
        self.f2.pack(fill=X)

        self.l2 = Label(self.root, text='Modes     :')
        self.l2.pack(side=LEFT, in_=self.f2)
        self.m1 = Button(self.root, text='Normal (0)', command=ModeZero)
        self.m1.pack(side=LEFT, in_=self.f2)
        self.m2 = Button(self.root, text='Death  (1)', command=ModeOne)
        self.m2.pack(side=LEFT, in_=self.f2)
        self.m3 = Button(self.root, text='Bouncy (2)', command=ModeTwo)
        self.m3.pack(side=LEFT, in_=self.f2)

        self.infile   = infile

        # mouse buttons: they are complicated and hence ...
        self.canvas.bind('<ButtonPress-1>',         self.LeftButtonPress)
        self.canvas.bind('<ButtonRelease-1>',       self.LeftButtonRelease)

        # special: for mouse motion
        self.canvas.bind('<Motion>',              self.UpdateMouse)

        # other useful key bindings
        # self.root.bind('0',                       self.Key0)
        # self.root.bind('1',                       self.Key1)
        # self.root.bind('2',                       self.Key2)
        self.root.bind('<Escape>',                self.KeyEscape)
        self.root.bind('q',                       self.KeyQuit)
        self.root.bind('s',                       self.KeySaveLevel)
        self.root.bind('<BackSpace>',             self.KeyDeleteBox)
        self.root.bind('+',                       self.KeyPlus)
        self.root.bind('-',                       self.KeyMinus)
        self.root.bind('I',                       self.KeyInsertLevel)
        self.root.bind('D',                       self.KeyDeleteLevel)
        # self.root.bind('t',                       self.GetText)
        # self.root.bind('<Return>',                self.Return)

        # basic drawing stuff
        self.boxMode    = 0       # which type of box to draw: black, red, purple
        self.boxID      = -1      # used for the ID of the currently-drawn box
        self.boxNumToID = {}      # maps box numbers to canvas IDs
        self.hiliteBox  = -1      # if hovering over a box, this is its number (not canvas ID)
        
        # Fixed boxes
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH_IPHONE5, WINDOW_HEIGHT_IPHONE5, fill='gray',  outline='')
        self.canvas.create_rectangle(0, WINDOW_HEIGHT_IPHONE5 - 100, WINDOW_WIDTH_IPHONE5, WINDOW_HEIGHT_IPHONE5, fill='black', outline='')
        self.canvas.create_rectangle(0, 0, 20, WINDOW_HEIGHT_IPHONE5, fill='black', outline='')

        # assumes nothing to start with
        self.levelNumber = 0       
        self.DrawLevelNumber()

        self.levelName   = ''
        self.DrawLevelText()

        self.level       = Level()
        self.level.Load('Levels', self.levelNumber)
        print self.level.Length()

        # draw them if they exist
        self.DrawLevel()

        # where is the mouse?
        self.mouseX     = 0
        self.mouseY     = 0
        self.DrawMousePosition()

        self.MODE_NIL   = 1
        self.MODE_DEF   = 2
        self.mode       = self.MODE_NIL
        self.DrawMode()

        self.xmax = WINDOW_WIDTH_IPHONE5
        self.ymax = WINDOW_HEIGHT_IPHONE5

        # get it all going
        return

    def GetRoot(self):
        return self.root        

    def GetColorFromMode(self, mode):
        if mode == 0:
            return 'black'
        elif mode == 1:
            return 'red'
        elif mode == 2:
            return 'purple'
        return
    
    def DrawLevelNumber(self):
        self.levelTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 80, text='Level : %3d' % self.levelNumber,
                                                font=('courier', 14), fill='white', anchor='w')
        return

    def UpdateLevelNumber(self):
        SafeDelete(self.canvas, self.levelTxt)
        self.DrawLevelNumber()
        return

    def DrawLevelText(self):
        self.nameID = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 60,  text='Text  : %s' % self.levelName,
                                              font=('courier', 14), fill='white', anchor='w')
        return

    def UpdateLevelText(self, name=''):
        if name != '':
            self.levelName = name
        SafeDelete(self.canvas, self.nameID)
        self.DrawLevelText()
        return

    def DrawMode(self):
        self.modeTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 40,  text='Mode  : %3d' % self.boxMode,
                                               font=('courier', 14), fill='white', anchor='w')
        return
    
    def DrawMousePosition(self):
        self.mouseTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 20, text='Mouse : %3d,%3d' % (self.mouseX, self.mouseY),
                                                font=('courier', 14), fill='white', anchor='w')
        return

    def CurrentBox(self):
        boxColor = self.GetColorFromMode(self.boxMode)
        if self.mode == self.MODE_DEF:
            self.boxID = self.canvas.create_rectangle(self.startX, self.startY, self.mouseX, self.mouseY, fill=boxColor, outline='')
        
    def UpdateMouse(self, event):
        self.mouseX = event.x
        self.mouseY = event.y

        # show the current mouse position at all times
        SafeDelete(self.canvas, self.mouseTxt)
        self.DrawMousePosition()

        # also draw the current box if need be
        SafeDelete(self.canvas, self.boxID)
        self.CurrentBox()

        # if not defining a new box, check for hilight possibility
        if self.mode == self.MODE_NIL:
            self.hiliteBox = -1
            # clear all highlights
            for i in range(self.level.Length()):
                boxID = self.boxNumToID[i]
                self.canvas.itemconfig(boxID, outline='black', width=0)

            # find EXACTLY ONE to highlight
            max = self.level.Length()
            for i in range(max):
                j = max - i - 1
                box   = self.level.GetBox(j)
                if box['uid'] == -1:
                    continue
                boxID = self.boxNumToID[j]
                if self.mouseX < box['x2'] and self.mouseX > box['x1'] and self.mouseY < box['y2'] and self.mouseY > box['y1']:
                    self.canvas.itemconfig(boxID, outline='orange', width=2)
                    self.hiliteBox = j
                    break
                else:
                    self.canvas.itemconfig(boxID, outline='black', width=0)
        return

    # draws each box
    # also sets map of boxNums to canvasIDs
    def DrawLevel(self):
        self.boxNumToID = {}
        for i in range(self.level.Length()):
            b = self.level.GetBox(i)
            color = self.GetColorFromMode(b['mode'])
            tmpID = self.canvas.create_rectangle(b['x1'], b['y1'], b['x2'], b['y2'], fill=color, outline='', width=0)
            self.boxNumToID[i] = tmpID
        return

    # deletes each box
    # also unsets boxNum to canvasID map
    def UndrawLevel(self):
        for i in range(self.level.Length()):
            tmpID = self.boxNumToID[i]
            SafeDelete(self.canvas, tmpID)
        self.boxNumToID = {}
        return

    def LeftButtonPress(self, event):
        # check if in range
        print event.x, self.xmax, ' and ', event.y, self.ymax
        if event.y < 0 or event.y > self.ymax:
            return
        if event.x < 0 or event.x > self.xmax:
            return
        
        if self.mode == self.MODE_NIL:
            self.mode = self.MODE_DEF
            self.startX, self.startY = self.mouseX, self.mouseY
        elif self.mode == self.MODE_DEF:
            self.mode = self.MODE_NIL
            endX, endY = self.mouseX, self.mouseY

            boxColor = self.GetColorFromMode(self.boxMode)
            tmpID = self.canvas.create_rectangle(self.startX, self.startY, self.mouseX, self.mouseY, fill=boxColor, outline='')
            bnum  = self.level.AddBox(self.startX, self.startY, endX, endY, self.boxMode)
            self.boxNumToID[bnum] = tmpID

            self.level.PrintBoxes()
        else:
            Abort('problem: bad mode')
        return

    def LeftButtonRelease(self, event):
        return

    def KeyQuit(self, event):
        exit(1)
        return

    def KeySaveLevel(self, event):
        self.level.Save('Levels', 0)
        return

    def KeyInsertLevel(self, event):
        process = subprocess.Popen('./insert.csh %d' % self.levelNumber, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print 'insert done (%s)' % str(process.returncode)
        self.UndrawLevel()
        self.level = Level()
        return

    def KeyDeleteLevel(self, event):
        process = subprocess.Popen('./delete.csh %d' % self.levelNumber, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print 'delete done (%s)' % str(process.returncode)
        self.UndrawLevel()
        self.level = Level()
        self.level.Load('Levels', self.levelNumber)
        self.DrawLevel()
        return

    def KeyPlus(self, event):
        print 'move level up one', self.levelNumber + 1
        self.level.Save('Levels', self.levelNumber)
        self.UndrawLevel()
        self.levelNumber += 1
        self.UpdateLevelNumber()
        self.level = Level()   # warning: deletes old one 
        self.level.Load('Levels', self.levelNumber)
        self.DrawLevel()
        return

    def KeyMinus(self, event):
        if self.levelNumber == 0:
            return
        print 'move level down one', self.levelNumber - 1
        self.level.Save('Levels', self.levelNumber)
        self.UndrawLevel()
        self.levelNumber -= 1
        self.UpdateLevelNumber()
        self.level = Level()   # warning: deletes old one 
        self.level.Load('Levels', self.levelNumber)
        self.DrawLevel()
        return

    def KeyDeleteBox(self, event):
        if self.hiliteBox == -1:
            return
        print 'delete box ID', self.hiliteBox
        self.level.DeleteBox(self.hiliteBox)
        self.level.PrintBoxes()
        SafeDelete(self.canvas, self.boxNumToID[self.hiliteBox])
        return

    def ModeZero(self):
        self.boxMode = 0
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def ModeOne(self):
        self.boxMode = 1
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def ModeTwo(self):
        self.boxMode = 2
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def KeyEscape(self, event):
        self.mode = self.MODE_NIL
        return

#
# MAIN 
#
parser = OptionParser()
parser.add_option('-f', '--file', default='Levels', help='where to store levels', action='store', type='string', dest='infile')
(options, args) = parser.parse_args()

# canvas.bind("<1>", lambda event: canvas.focus_set())

# entryTxt = StringVar()
# e = Entry(root, textvariable=entryTxt, width=80)
# e.pack()

Ctrl = Controller(infile=options.infile)
root = Ctrl.GetRoot()
root.mainloop()



